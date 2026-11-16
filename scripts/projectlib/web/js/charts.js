// Role: Native SVG visualizers for timeline, provenance lineage, domain dependency map, and module internals.
// Out of scope: Mermaid text parsing (diagrams.js), DOM drawer rendering (drawer.js), and API calls.
// Anchors: spec=ui.perspective-web, docs/contracts/frontend-and-visual-discipline.md, SRC-016, SRC-019

import { escHtml, wrapTextLines, t, trStage, trTaskState, trDecisionStatus } from "./i18n.js";

export function esc(value) {
  return escHtml(value);
}

export function wrapLines(text, maxChars = 22) {
  return wrapTextLines(text, maxChars);
}

function markerDefs(prefix) {
  return `<defs>
    <marker id="${prefix}-dec" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">
      <path d="M 1 1 L 9 5 L 1 9 z" class="svg-text-muted" />
    </marker>
    <marker id="${prefix}-foc" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">
      <path d="M 1 1 L 9 5 L 1 9 z" class="svg-text-focus" />
    </marker>
    <marker id="${prefix}-vio" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">
      <path d="M 1 1 L 9 5 L 1 9 z" class="svg-text-signal" />
    </marker>
  </defs>`;
}

function curvedEdge(x1, y1, x2, y2, cls, markerId, label = "", opts = {}) {
  const dx = x2 - x1;
  const dy = y2 - y1;
  let d;
  if (opts.vertical) {
    const sy = dy >= 0 ? 1 : -1;
    const cy = Math.max(20, Math.min(72, Math.abs(dy) * 0.48));
    d = `M ${x1} ${y1} C ${x1} ${y1 + sy * cy}, ${x2} ${y2 - sy * cy}, ${x2} ${y2}`;
  } else {
    const s = dx >= 0 ? 1 : -1;
    const cx = Math.max(18, Math.min(84, Math.abs(dx) * 0.48));
    const arch = opts.arch ?? (Math.abs(dy) < 12 && dx < 0 ? -38 : 0);
    d = `M ${x1} ${y1} C ${x1 + s * cx} ${y1 + arch}, ${x2 - s * cx} ${y2 + arch}, ${x2} ${y2}`;
  }
  const mx = (x1 + x2) / 2;
  const my = (y1 + y2) / 2 + (opts.arch ? opts.arch * 0.75 - 5 : -5);
  const lbl = label
    ? `<text x="${mx.toFixed(1)}" y="${my.toFixed(1)}" text-anchor="middle" font-size="10.5" class="${cls.includes("violation") ? "svg-text-signal" : "svg-text-muted"}">${esc(label)}</text>`
    : "";
  return `<path d="${d}" class="${cls}" marker-end="url(#${markerId})" />${lbl}`;
}

function orthoBypassH(x1, y1, xOut, xIn, x2, y2, laneY) {
  const sx1 = Math.sign(xOut - x1) || 1, sy1 = Math.sign(laneY - y1) || 1;
  const sxm = Math.sign(xIn - xOut) || 1, sy2 = Math.sign(y2 - laneY) || 1, sx2 = Math.sign(x2 - xIn) || 1;
  const r1 = Math.min(8, Math.abs(xOut - x1) / 2, Math.abs(laneY - y1) / 2);
  const r2 = Math.min(8, Math.abs(xIn - xOut) / 4, Math.abs(laneY - y1) / 2, Math.abs(y2 - laneY) / 2);
  const r3 = Math.min(8, Math.abs(x2 - xIn) / 2, Math.abs(y2 - laneY) / 2);
  return [
    `M ${x1} ${y1}`,
    `L ${xOut - sx1 * r1} ${y1}`,
    r1 > 0.5 ? `Q ${xOut} ${y1} ${xOut} ${y1 + sy1 * r1}` : `L ${xOut} ${y1}`,
    `L ${xOut} ${laneY - sy1 * r2}`,
    r2 > 0.5 ? `Q ${xOut} ${laneY} ${xOut + sxm * r2} ${laneY}` : `L ${xOut} ${laneY}`,
    `L ${xIn - sxm * r2} ${laneY}`,
    r2 > 0.5 ? `Q ${xIn} ${laneY} ${xIn} ${laneY + sy2 * r2}` : `L ${xIn} ${laneY}`,
    `L ${xIn} ${y2 - sy2 * r3}`,
    r3 > 0.5 ? `Q ${xIn} ${y2} ${xIn + sx2 * r3} ${y2}` : `L ${xIn} ${y2}`,
    `L ${x2} ${y2}`,
  ].join(" ");
}

export function renderTimelineSvg(data, lang = "zh") {
  const archived = data?.timeline?.archived_milestones || [];
  const pivots = data?.timeline?.pivots || [];
  const review = data?.review || {};
  const eras = [];
  const eraMap = new Map();
  for (const m of archived) {
    const k = m.era || "archive";
    if (!eraMap.has(k)) {
      const entry = { kind: "era", id: k, title: `${m.id}: ${m.name}`, sub: k, allNames: [m.id] };
      eraMap.set(k, entry);
      eras.push(entry);
    } else {
      eraMap.get(k).allNames.push(m.id);
      eraMap.get(k).title = eraMap.get(k).allNames.join(" · ");
    }
  }
  const commits = review.commits_since_review || 0;
  const dirtyMods = (review.modules_since_review || []).length;
  const headSub = review.grill_suggested
    ? (commits > 0
      ? (lang === "zh" ? `距上次评审 +${commits} 次提交` : `+${commits} since review`)
      : (lang === "zh" ? `含未提交改动（${dirtyMods} 个模块）` : `${dirtyMods} dirty module(s)`))
    : (lang === "zh" ? "评审基线已对齐" : "Aligned with review");
  const nodes = [
    ...eras,
    ...pivots.map((p) => {
      const stText = trDecisionStatus(lang, p.status);
      return {
        kind: "pivot",
        id: p.id,
        title: `${p.id}: ${p.title}`,
        sub: p.superseded_by ? `${stText} -> ${p.superseded_by}` : stText,
        active: p.status === "current" || p.status === "accepted",
      };
    }),
    {
      kind: "head",
      id: "HEAD",
      title: lang === "zh" ? `当前代码 HEAD (${data?.project?.head_sha || "-"})` : `Current HEAD (${data?.project?.head_sha || "-"})`,
      sub: headSub,
      warn: Boolean(review.grill_suggested),
    },
  ];

  const colW = 186, padX = 28, axisY = 62, cardY = 84;
  const width = Math.max(680, padX * 2 + nodes.length * colW);
  const wrappedTitles = nodes.map((n) => wrapLines(n.title, 20));
  const wrappedSubs = nodes.map((n) => wrapLines(n.sub, 20));
  const maxLines = Math.max(2, ...wrappedTitles.map((r) => r.length));
  const maxSubLines = Math.max(1, ...wrappedSubs.map((r) => r.length));
  const boxH = 28 + maxLines * 15 + maxSubLines * 14;
  const height = cardY + boxH + 22;

  const line = `<line x1="${padX + 40}" y1="${axisY}" x2="${width - padX - 40}" y2="${axisY}" class="svg-axis-line" />`;
  const items = nodes.map((n, idx) => {
    const cx = padX + idx * colW + 88;
    const dotCls = n.kind === "head" ? (n.warn ? "svg-dot-signal" : "svg-dot-sage") : (n.kind === "pivot" ? "svg-dot-focus" : "svg-dot-sage");
    const boxCls = n.kind === "head" && n.warn ? "svg-box-warn" : (n.active ? "svg-box-focus" : "svg-box-clean");
    const attr = n.kind === "pivot" ? ` data-open-trace="${esc(n.id)}"` : "";
    const tag = n.kind === "era" ? (lang === "zh" ? "归档基线" : "Archived") : (n.kind === "pivot" ? "ADR" : "HEAD");
    const rows = wrappedTitles[idx];
    const subRows = wrappedSubs[idx];
    const tspans = rows.map((r, ri) => `<text x="${cx}" y="${cardY + 24 + ri * 15}" text-anchor="middle" font-size="11.5" font-weight="500" class="svg-text-ink">${esc(r)}</text>`).join("");
    const subStart = cardY + boxH - 10 - (subRows.length - 1) * 13;
    const subTspans = subRows.map((sr, si) => `<text x="${cx}" y="${subStart + si * 13}" text-anchor="middle" font-size="10.5" class="${n.warn ? "svg-text-signal" : "svg-text-muted"}">${esc(sr)}</text>`).join("");
    return `<g class="svg-node"${attr}>
      <title>${esc(n.title)}${n.sub ? ` (${esc(n.sub)})` : ""}</title>
      <circle cx="${cx}" cy="${axisY}" r="6" class="${dotCls}" />
      <text x="${cx}" y="${axisY - 14}" text-anchor="middle" font-size="10.5" font-weight="600" class="svg-text-muted">${esc(tag)}</text>
      <rect x="${cx - 82}" y="${cardY}" width="164" height="${boxH}" rx="8" class="${boxCls}" />
      ${tspans}${subTspans}
    </g>`;
  }).join("");

  return `<svg viewBox="0 0 ${width} ${height}" class="svg-canvas${width > 1100 ? " svg-wide" : ""}" role="img" aria-label="Timeline">${line}${items}</svg>`;
}

export function renderProvenanceSvg(nodeEntry, lang = "zh") {
  const tr = nodeEntry?.trace || {};
  if (!tr.found) {
    return `<p class="muted">${esc(lang === "zh" ? "暂无溯源记录。" : "No lineage record.")}</p>`;
  }
  const clipTxt = (v, lim = 96) => {
    const raw = String(v ?? "").replace(/\s+/g, " ").trim();
    return raw.length > lim ? `${raw.slice(0, lim - 1)}…` : raw;
  };
  const originSub = tr.date || (tr.status ? trDecisionStatus(lang, tr.status) : "");
  const col1 = [{ id: tr.id, title: clipTxt(tr.title || tr.quote || tr.id), sub: originSub, cls: "svg-box-focus", attr: `data-open-trace="${esc(tr.id)}"` }];
  const midItems = tr.anchor_type === "source"
    ? (tr.decisions || []).map((d) => ({ id: d.id, title: clipTxt(d.title || d.id), sub: trDecisionStatus(lang, d.status || "") }))
    : (tr.sources || []).map((s) => (typeof s === "string"
        ? { id: s, title: s, sub: lang === "zh" ? "用户原话" : "User quote" }
        : { id: s.id, title: clipTxt(s.quote || s.context || s.id), sub: s.date || (lang === "zh" ? "用户原话" : "User quote") }));
  const col2 = midItems.length
    ? midItems.map((d) => ({ id: d.id, title: `${d.id}: ${d.title || d.id}`, sub: d.sub || "", cls: "svg-box-clean", attr: `data-open-trace="${esc(d.id)}"` }))
    : [{ id: "-", title: lang === "zh" ? "直接落地到模块" : "Direct to modules", sub: "", cls: "svg-box-subtle", attr: "" }];
  const mods = tr.modules || [];
  const col3 = mods.length
    ? mods.map((m) => ({ id: m.id, title: `${m.title || m.id}`, sub: `${m.id} · ${trStage(lang, m.stage)}`, cls: "svg-box-clean", attr: `data-open-module="${esc(m.id)}"` }))
    : [{ id: "-", title: lang === "zh" ? "尚无关联模块" : "No owning module yet", sub: "", cls: "svg-box-subtle", attr: "" }];
  const col4 = [];
  if ((tr.verified_done_count || 0) > 0) {
    col4.push({
      id: "done-sum",
      title: lang === "zh" ? `已完成 ${tr.verified_done_count} 项任务` : `${tr.verified_done_count} done tasks`,
      sub: lang === "zh" ? "点击查看已完成任务" : "Open done tasks",
      cls: "svg-box-sage",
      attr: `data-jump-done-tasks="1"`,
    });
  }
  for (const tk of (tr.open_or_pending_tasks || [])) {
    col4.push({
      id: tk.id,
      title: `${tk.id}: ${tk.title}`,
      sub: trTaskState(lang, tk.state),
      cls: tk.state === "blocked" ? "svg-box-warn" : "svg-box-clean",
      attr: `data-open-trace="${esc(tr.id)}"`,
    });
  }
  if (!col4.length) {
    col4.push({ id: "no-task", title: lang === "zh" ? "当前无待办任务" : "No tasks recorded", sub: "", cls: "svg-box-subtle", attr: "" });
  }

  const cols = [col1, col2, col3, col4];
  const titles = lang === "zh" ? ["1. 源头诉求/决策", "2. 决策与依据", "3. 归属模块", "4. 对应任务产出"] : ["1. Origin", "2. ADR / Sources", "3. Modules", "4. Tasks"];
  const colX = [16, 256, 496, 736];
  const boxW = 208, gapY = 12, startY = 38;

  const layoutCol = (items, x) => {
    let y = startY;
    return items.map((it) => {
      const lines = wrapLines(it.title, 24);
      const subLines = it.sub ? wrapLines(it.sub, 26) : [];
      const h = Math.max(54, 24 + lines.length * 15 + subLines.length * 13);
      const box = { ...it, x, y, w: boxW, h, lines, subLines };
      y += h + gapY;
      return box;
    });
  };
  const boxes = cols.map((items, idx) => layoutCol(items, colX[idx]));
  const maxY = Math.max(...boxes.map((b) => (b.length ? b[b.length - 1].y + b[b.length - 1].h : startY))) + 18;
  const width = 960;
  const uid = `prov-${String(tr.id || "node").replace(/[^A-Za-z0-9_-]/g, "")}`;

  const connect = (fromList, toList, cls, marker) => fromList.flatMap((a) => toList.map((b) =>
    curvedEdge(a.x + a.w, a.y + a.h / 2, b.x, b.y + b.h / 2, cls, marker))).join("");
  const edges = [
    connect(boxes[0], boxes[1], "svg-edge-focus", `${uid}-foc`),
    connect(boxes[1], boxes[2], "svg-edge-declared", `${uid}-dec`),
    connect(boxes[2], boxes[3], "svg-edge-declared", `${uid}-dec`),
  ].join("");

  const headers = titles.map((lbl, idx) => `<text x="${colX[idx]}" y="20" font-size="11.5" font-weight="600" class="svg-text-muted">${esc(lbl)}</text>`).join("");
  const nodesSvg = boxes.flat().map((b) => {
    const tspans = b.lines.map((ln, ri) => `<text x="${b.x + 11}" y="${b.y + 20 + ri * 15}" font-size="11.5" font-weight="500" class="svg-text-ink">${esc(ln)}</text>`).join("");
    const subStart = b.y + b.h - 9 - Math.max(0, b.subLines.length - 1) * 13;
    const subSvg = b.subLines.map((sr, si) => `<text x="${b.x + 11}" y="${subStart + si * 13}" font-size="10.5" class="svg-text-muted">${esc(sr)}</text>`).join("");
    return `<g class="svg-node" ${b.attr}><title>${esc(b.title)}${b.sub ? ` (${esc(b.sub)})` : ""}</title><rect x="${b.x}" y="${b.y}" width="${b.w}" height="${b.h}" rx="8" class="${b.cls}" />${tspans}${subSvg}</g>`;
  }).join("");

  return `<svg viewBox="0 0 ${width} ${maxY}" class="svg-canvas svg-wide" role="img" aria-label="Provenance Lineage">${markerDefs(uid)}${headers}${edges}${nodesSvg}</svg>`;
}

export function renderDomainMapSvg(domains, domainEdges, lang = "zh") {
  const list = domains || [];
  if (!list.length) return `<p class="muted">${esc(t(lang, "noneText"))}</p>`;
  const edges = domainEdges || [];
  const cards = new Map();
  let maxNameLines = 1, maxMetaLines = 1, maxSubLines = 1;
  for (const d of list) {
    const vioN = (d.violations || []).length;
    const overN = d.oversized_count || 0;
    const hasWarn = vioN > 0 || overN > 0;
    const cls = hasWarn ? "svg-box-warn" : (d.is_exemplar ? "svg-box-sage" : "svg-box-clean");
    const nameLines = wrapLines(d.name || d.id, 28);
    const meta = `${trStage(lang, d.stage)} · ${d.module_count || 0} ${t(lang, "modulesUnit")} · ${d.loc || 0} ${t(lang, "linesUnit")}`;
    const warnParts = [];
    if (vioN > 0) warnParts.push(lang === "zh" ? `${vioN} 条越界` : `${vioN} violation(s)`);
    if (overN > 0) warnParts.push(lang === "zh" ? `${overN} 个文件偏大` : `${overN} oversized`);
    const sub = hasWarn ? (lang === "zh" ? `需留意：${warnParts.join("，")}` : warnParts.join(", ")) : d.id;
    const metaLines = wrapLines(meta, 40);
    const subLines = wrapLines(sub, 40);
    maxNameLines = Math.max(maxNameLines, nameLines.length);
    maxMetaLines = Math.max(maxMetaLines, metaLines.length);
    maxSubLines = Math.max(maxSubLines, subLines.length);
    cards.set(d.id, { d, hasWarn, cls, nameLines, metaLines, subLines });
  }
  const boxW = 308, boxH = Math.max(100, 28 + maxNameLines * 17 + maxMetaLines * 14 + maxSubLines * 14), gapX = 96, gapY = 48, padX = 28, padY = 24;
  const cols = list.length <= 2 ? list.length : 2;
  const pos = new Map();
  list.forEach((d, idx) => {
    const col = idx % cols;
    const row = Math.floor(idx / cols);
    pos.set(d.id, { x: padX + col * (boxW + gapX), y: padY + row * (boxH + gapY), w: boxW, h: boxH });
  });
  const rows = Math.ceil(list.length / cols);
  const width = Math.max(580, padX * 2 + cols * boxW + (cols - 1) * gapX);
  const height = Math.max(200, padY * 2 + rows * boxH + (rows - 1) * gapY);
  const uid = "dommap";

  const edgeSvg = edges.map((e) => {
    const a = pos.get(e.from), b = pos.get(e.to);
    if (!a || !b) return "";
    const isVio = e.kind === "violation";
    const sameRow = Math.abs(a.y - b.y) < 10;
    let x1 = a.x + a.w / 2, y1 = a.y + a.h / 2, x2 = b.x + b.w / 2, y2 = b.y + b.h / 2;
    if (sameRow) {
      x1 = a.x < b.x ? a.x + a.w : a.x;
      x2 = a.x < b.x ? b.x : b.x + b.w;
    } else if (a.y < b.y) {
      y1 = a.y + a.h; y2 = b.y;
    } else {
      y1 = a.y; y2 = b.y + b.h;
    }
    const lbl = isVio ? `! ×${e.count || 1}` : (e.count > 1 ? `×${e.count}` : "");
    const edgeCls = isVio ? "svg-edge-violation" : "svg-edge-declared";
    const markerId = isVio ? `${uid}-vio` : `${uid}-dec`;
    if (!sameRow && Math.abs(b.y - a.y) > Math.max(a.h, b.h) + 48) {
      const boxes = Array.from(pos.values());
      const hit = boxes.some((n) => n !== a && n !== b && n.y >= Math.min(a.y, b.y) + a.h - 4
        && n.y + n.h <= Math.max(a.y, b.y) + 4 && n.x <= Math.max(x1, x2) + 10 && n.x + n.w >= Math.min(x1, x2) - 10);
      if (hit) {
        const minL = Math.min(...boxes.map((n) => n.x)), maxR = Math.max(...boxes.map((n) => n.x + n.w));
        const useLeft = (a.x + b.x) / 2 <= (minL + maxR) / 2;
        const gx = useLeft ? Math.max(6, minL - 14) : maxR + 14;
        const r = 8, sy = b.y > a.y ? 1 : -1;
        const sx = useLeft ? a.x : a.x + a.w, ex = useLeft ? b.x : b.x + b.w;
        const ya = a.y + a.h / 2, yb = b.y + b.h / 2;
        const d = useLeft
          ? `M ${sx} ${ya} L ${gx + r} ${ya} Q ${gx} ${ya} ${gx} ${ya + sy * r} L ${gx} ${yb - sy * r} Q ${gx} ${yb} ${gx + r} ${yb} L ${ex} ${yb}`
          : `M ${sx} ${ya} L ${gx - r} ${ya} Q ${gx} ${ya} ${gx} ${ya + sy * r} L ${gx} ${yb - sy * r} Q ${gx} ${yb} ${gx - r} ${yb} L ${ex} ${yb}`;
        const lTag = lbl ? `<text x="${gx}" y="${((ya + yb) / 2).toFixed(1)}" text-anchor="middle" font-size="10.5" class="${isVio ? "svg-text-signal" : "svg-text-muted"}">${esc(lbl)}</text>` : "";
        return `<path d="${d}" class="${edgeCls}" marker-end="url(#${markerId})" />${lTag}`;
      }
    }
    return curvedEdge(x1, y1, x2, y2, edgeCls, markerId, lbl, { vertical: !sameRow });
  }).join("");

  const nodesSvg = list.map((d) => {
    const p = pos.get(d.id);
    const card = cards.get(d.id);
    const titleSvg = card.nameLines.map((ln, ri) => `<text x="${p.x + 14}" y="${p.y + 22 + ri * 17}" font-size="13" font-weight="600" class="svg-text-ink">${esc(ln)}</text>`).join("");
    const subStart = p.y + p.h - 10 - (card.subLines.length - 1) * 14;
    const metaStart = subStart - 16 - (card.metaLines.length - 1) * 14;
    const metaSvg = card.metaLines.map((ln, ri) => `<text x="${p.x + 14}" y="${metaStart + ri * 14}" font-size="11" class="svg-text-sec">${esc(ln)}</text>`).join("");
    const subSvg = card.subLines.map((ln, ri) => `<text x="${p.x + 14}" y="${subStart + ri * 14}" font-size="10.5" class="${card.hasWarn ? "svg-text-signal" : "svg-text-muted"}">${esc(ln)}</text>`).join("");
    return `<g class="svg-node" data-zoom-domain="${esc(d.id)}">
      <title>${esc(d.name || d.id)} (${esc(d.id)})</title>
      <rect x="${p.x}" y="${p.y}" width="${p.w}" height="${p.h}" rx="10" class="${card.cls}" />
      ${titleSvg}${metaSvg}${subSvg}
    </g>`;
  }).join("");

  return `<svg viewBox="0 0 ${width} ${height}" class="svg-canvas" role="img" aria-label="Domain Dependency Map">${markerDefs(uid)}${edgeSvg}${nodesSvg}</svg>`;
}

export function renderModuleMapSvg(domain, lang = "zh") {
  const mods = domain?.modules || [];
  if (!mods.length) return `<p class="muted">${esc(t(lang, "noneText"))}</p>`;
  const rawEdges = domain?.module_edges || [];
  const modIds = new Set(mods.map((m) => m.id));
  const extIds = [];
  for (const e of rawEdges) {
    if (e.external && !modIds.has(e.to) && !extIds.includes(e.to)) extIds.push(e.to);
  }
  const rank = new Map(mods.map((m) => [m.id, 0]));
  for (let p = 0; p < mods.length; p += 1) {
    for (const e of rawEdges) {
      if (!e.external && rank.has(e.from) && rank.has(e.to)) {
        const ra = rank.get(e.from), rb = rank.get(e.to);
        if (rb <= ra && ra + 1 <= mods.length) rank.set(e.to, ra + 1);
      }
    }
  }
  const cols = new Map();
  for (const m of mods) {
    const r = rank.get(m.id) || 0;
    if (!cols.has(r)) cols.set(r, []);
    cols.get(r).push(m);
  }
  const layers = Array.from(cols.entries()).sort((a, b) => a[0] - b[0]).map(([, ms]) => ms);
  if (extIds.length) layers.push(extIds.map((id) => ({ id, title: id, isExternal: true })));

  const extSubLabel = lang === "zh" ? "跨域依赖（点击查看）" : "External (click)";
  const cards = new Map();
  let maxTitleRows = 1, maxMetaRows = 1;
  for (const l of layers) {
    for (const m of l) {
      if (m.isExternal) {
        const lines = wrapLines(m.id, 28);
        const metaLines = wrapLines(extSubLabel, 28);
        maxTitleRows = Math.max(maxTitleRows, lines.length);
        maxMetaRows = Math.max(maxMetaRows, metaLines.length);
        cards.set(m.id, { lines, metaLines, isExternal: true, titleText: m.id, metaText: extSubLabel });
      } else {
        const warn = (m.violation_count || 0) > 0 || (m.oversized_count || 0) > 0;
        const cls = warn ? "svg-box-warn" : (domain.is_exemplar ? "svg-box-sage" : "svg-box-clean");
        const titleText = m.title || m.id;
        const metaText = `${m.id} · ${m.loc || 0} ${t(lang, "linesUnit")}`;
        const lines = wrapLines(titleText, 24);
        const metaLines = wrapLines(metaText, 30);
        maxTitleRows = Math.max(maxTitleRows, lines.length);
        maxMetaRows = Math.max(maxMetaRows, metaLines.length);
        cards.set(m.id, { lines, metaLines, warn, cls, titleText, metaText });
      }
    }
  }
  const boxW = 240, boxH = Math.max(78, 28 + maxTitleRows * 15 + maxMetaRows * 13), gapX = 72, gapY = 24, padX = 22, padY = 44;
  const maxRows = Math.max(1, ...layers.map((l) => l.length));
  const pos = new Map();
  layers.forEach((layer, ci) => {
    const x = padX + ci * (boxW + gapX);
    const totalH = layer.length * boxH + (layer.length - 1) * gapY;
    const areaH = maxRows * boxH + (maxRows - 1) * gapY;
    let y = padY + (areaH - totalH) / 2;
    layer.forEach((m) => {
      pos.set(m.id, { x, y, w: boxW, h: boxH, mod: m, ci });
      y += boxH + gapY;
    });
  });

  const width = Math.max(540, padX * 2 + layers.length * boxW + (layers.length - 1) * gapX);
  const height = Math.max(160, padY * 2 + maxRows * boxH + (maxRows - 1) * gapY);
  const uid = `modmap-${String(domain.id || "dom").replace(/[^A-Za-z0-9_-]/g, "")}`;
  const allPos = Array.from(pos.values());
  let skipTopUsed = false, skipBotIdx = 0, maxEdgeY = height;

  const edgesSvg = rawEdges.map((e) => {
    const a = pos.get(e.from), b = pos.get(e.to);
    if (!a || !b) return "";
    const isVio = e.kind === "violation";
    const forward = a.x <= b.x;
    const x1 = forward ? a.x + a.w : a.x, y1 = a.y + a.h / 2;
    const x2 = forward ? b.x : b.x + b.w, y2 = b.y + b.h / 2;
    const edgeCls = isVio ? "svg-edge-violation" : (e.external ? "svg-edge-declared" : "svg-edge-focus");
    const markerId = isVio ? `${uid}-vio` : `${uid}-foc`;
    const lbl = isVio && e.file ? `${e.file.split("/").pop()}:${e.line || ""}` : "";
    const minCi = Math.min(a.ci, b.ci), maxCi = Math.max(a.ci, b.ci);
    if (maxCi - minCi > 1) {
      const midNodes = allPos.filter((n) => n.ci > minCi && n.ci < maxCi);
      const bandMin = Math.min(y1, y2) - 10, bandMax = Math.max(y1, y2) + 10;
      if (midNodes.some((n) => n.y <= bandMax && n.y + n.h >= bandMin)) {
        const midTop = Math.min(...midNodes.map((n) => n.y));
        const midBot = Math.max(...midNodes.map((n) => n.y + n.h));
        let laneY;
        if (!skipTopUsed && midTop - 18 >= 12 && (y1 + y2) / 2 <= (midTop + midBot) / 2) {
          skipTopUsed = true;
          laneY = midTop - 18;
        } else {
          laneY = midBot + 18 + skipBotIdx * 16;
          skipBotIdx += 1;
          maxEdgeY = Math.max(maxEdgeY, laneY + 20);
        }
        const stepOff = 18 + ((skipBotIdx + (skipTopUsed ? 1 : 0)) % 3) * 6;
        const xOut = forward ? x1 + stepOff : x1 - stepOff;
        const xIn = forward ? x2 - stepOff : x2 + stepOff;
        const d = orthoBypassH(x1, y1, xOut, xIn, x2, y2, laneY);
        const lblSvg = lbl
          ? `<text x="${((xOut + xIn) / 2).toFixed(1)}" y="${(laneY - 5).toFixed(1)}" text-anchor="middle" font-size="10.5" class="${isVio ? "svg-text-signal" : "svg-text-muted"}">${esc(lbl)}</text>`
          : "";
        return `<path d="${d}" class="${edgeCls}" marker-end="url(#${markerId})" />${lblSvg}`;
      }
    }
    return curvedEdge(x1, y1, x2, y2, edgeCls, markerId, lbl);
  }).join("");

  const nodesSvg = Array.from(pos.values()).map(({ x, y, w, h, mod }) => {
    const c = cards.get(mod.id);
    const metaStart = y + h - 10 - (c.metaLines.length - 1) * 13;
    if (c.isExternal) {
      const extSvg = c.lines.map((ln, ri) => `<text x="${x + 12}" y="${y + 20 + ri * 15}" font-size="11" font-weight="500" class="svg-text-sec">${esc(ln)}</text>`).join("");
      const subSvg = c.metaLines.map((ln, ri) => `<text x="${x + 12}" y="${metaStart + ri * 13}" font-size="10" class="svg-text-muted">${esc(ln)}</text>`).join("");
      return `<g class="svg-node" data-open-module="${esc(mod.id)}"><title>${esc(mod.id)}</title><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="8" class="svg-box-external" />${extSvg}${subSvg}</g>`;
    }
    const titleSvg = c.lines.map((ln, ri) => `<text x="${x + 12}" y="${y + 20 + ri * 15}" font-size="12" font-weight="600" class="svg-text-ink">${esc(ln)}</text>`).join("");
    const metaSvg = c.metaLines.map((ln, ri) => `<text x="${x + 12}" y="${metaStart + ri * 13}" font-size="10.5" class="${c.warn ? "svg-text-signal" : "svg-text-muted"}">${esc(ln)}</text>`).join("");
    return `<g class="svg-node" data-open-module="${esc(mod.id)}">
      <title>${esc(c.titleText)} (${esc(c.metaText)})</title>
      <rect x="${x}" y="${y}" width="${w}" height="${h}" rx="8" class="${c.cls}" />
      ${titleSvg}${metaSvg}
    </g>`;
  }).join("");

  const finalH = Math.max(height, maxEdgeY);
  return `<svg viewBox="0 0 ${width} ${finalH}" class="svg-canvas${width > 740 ? " svg-wide" : ""}" role="img" aria-label="Module Dependency Map">${markerDefs(uid)}${edgesSvg}${nodesSvg}</svg>`;
}
