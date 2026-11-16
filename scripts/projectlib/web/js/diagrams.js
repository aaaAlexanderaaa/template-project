// Role: Offline native SVG renderer for Mermaid flowcharts (LR/TD/TB) and sequence diagrams without CDN scripts.
// Out of scope: Domain/module graph layout (charts.js), network calls, and Markdown block parsing (i18n.js).
// Anchors: spec=ui.perspective-web, ADR-002, SRC-016, SRC-019

import { escHtml, wrapTextLines, t } from "./i18n.js";

function diagramHash(text) {
  let h = 2166136261;
  for (let i = 0; i < text.length; i += 1) {
    h ^= text.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return (h >>> 0).toString(36);
}

function parseNodeToken(token, labels) {
  const clean = token.trim();
  const patterns = [
    /^([A-Za-z0-9_.-]+)\s*\[\((.+)\)\]$/,
    /^([A-Za-z0-9_.-]+)\s*\(\[(.+)\]\)$/,
    /^([A-Za-z0-9_.-]+)\s*\[(.+)\]$/,
    /^([A-Za-z0-9_.-]+)\s*\((.+)\)$/,
    /^([A-Za-z0-9_.-]+)\s*\{(.+)\}$/,
  ];
  for (const re of patterns) {
    const m = clean.match(re);
    if (m) {
      const id = m[1];
      const lbl = m[2].replace(/^["']|["']$/g, "").replace(/\\n/g, " ").trim();
      if (!labels.has(id) || lbl.length >= labels.get(id).length) labels.set(id, lbl);
      return id;
    }
  }
  const bare = clean.match(/^([A-Za-z0-9_.-]+)$/);
  if (bare) {
    const id = bare[1];
    if (!labels.has(id)) labels.set(id, id);
    return id;
  }
  return null;
}

function parseFlowchart(lines) {
  const head = lines[0].trim();
  const horizontal = /\b(LR|RL)\b/i.test(head);
  const labels = new Map();
  const order = [];
  const edges = [];
  const ensureNode = (tok) => {
    const id = parseNodeToken(tok, labels);
    if (id && !order.includes(id)) order.push(id);
    return id;
  };
  for (let i = 1; i < lines.length; i += 1) {
    const raw = lines[i].trim();
    if (!raw || raw.startsWith("%%") || raw === "end" || raw.startsWith("subgraph ")
      || raw.startsWith("direction ") || raw.startsWith("classDef ") || raw.startsWith("class ") || raw.startsWith("style ")) continue;
    const edgeRe = /^(.+?)\s+(-->|-.->|==>|---)\s*(?:\|([^|]+)\|\s*)?(.+)$/;
    const namedRe = /^(.+?)\s+--\s+([^-][^>]*?)\s+-->\s+(.+)$/;
    let m = raw.match(namedRe);
    if (m) {
      const from = ensureNode(m[1]), to = ensureNode(m[3]);
      if (from && to) edges.push({ from, to, label: m[2].trim(), dashed: false, isBack: false });
      continue;
    }
    m = raw.match(edgeRe);
    if (m) {
      const parts = raw.split(/\s+(-->|-.->|==>|---)\s*/);
      if (parts.length >= 3 && !raw.includes("|")) {
        for (let j = 0; j + 2 < parts.length; j += 2) {
          const from = ensureNode(parts[j]), to = ensureNode(parts[j + 2]);
          if (from && to) edges.push({ from, to, label: "", dashed: parts[j + 1] === "-.->", isBack: false });
        }
        continue;
      }
      const from = ensureNode(m[1]), to = ensureNode(m[4]);
      if (from && to) edges.push({ from, to, label: (m[3] || "").trim(), dashed: m[2] === "-.->", isBack: false });
      continue;
    }
    ensureNode(raw);
  }
  return { horizontal, order, labels, edges };
}

function canReach(adj, start, target) {
  if (start === target) return true;
  const seen = new Set([start]);
  const stack = [start];
  while (stack.length) {
    const cur = stack.pop();
    for (const nxt of (adj.get(cur) || [])) {
      if (nxt === target) return true;
      if (!seen.has(nxt)) { seen.add(nxt); stack.push(nxt); }
    }
  }
  return false;
}

function assignLayers(order, edges) {
  const dagAdj = new Map(order.map((id) => [id, []]));
  const dagEdges = [];
  for (const e of edges) {
    if (canReach(dagAdj, e.to, e.from)) {
      e.isBack = true;
    } else {
      e.isBack = false;
      dagAdj.get(e.from)?.push(e.to);
      dagEdges.push(e);
    }
  }
  const rank = new Map(order.map((id) => [id, 0]));
  for (let pass = 0; pass < order.length; pass += 1) {
    let changed = false;
    for (const e of dagEdges) {
      const a = rank.get(e.from) ?? 0;
      const b = rank.get(e.to) ?? 0;
      if (b <= a) { rank.set(e.to, a + 1); changed = true; }
    }
    if (!changed) break;
  }
  const cols = new Map();
  for (const id of order) {
    const r = rank.get(id) ?? 0;
    if (!cols.has(r)) cols.set(r, []);
    cols.get(r).push(id);
  }
  return { layers: Array.from(cols.entries()).sort((a, b) => a[0] - b[0]).map(([, ids]) => ids), rank };
}

function renderFlowchartSvg(code, uid) {
  const lines = code.replace(/\r\n/g, "\n").split("\n").filter((l) => l.trim());
  const { horizontal, order, labels, edges } = parseFlowchart(lines);
  if (!order.length) return "";
  const { layers, rank } = assignLayers(order, edges);
  const boxW = 220, gapX = 64, gapY = 26, pad = 42;
  const wrapped = new Map(order.map((id) => [id, wrapTextLines(labels.get(id) || id, 24)]));
  const boxH = new Map(order.map((id) => [id, Math.max(46, 20 + wrapped.get(id).length * 16)]));
  const pos = new Map();
  let width = 320, height = 160;

  if (horizontal) {
    const maxColH = Math.max(...layers.map((ids) => ids.reduce((s, id) => s + boxH.get(id) + gapY, -gapY)));
    let curX = pad;
    layers.forEach((ids, li) => {
      const colH = ids.reduce((s, id) => s + boxH.get(id) + gapY, -gapY);
      let curY = pad + Math.max(0, (maxColH - colH) / 2);
      for (const id of ids) {
        const h = boxH.get(id);
        pos.set(id, { x: curX, y: curY, w: boxW, h, li });
        curY += h + gapY;
      }
      curX += boxW + gapX;
    });
    width = Math.max(500, curX - gapX + pad);
    height = Math.max(150, maxColH + pad * 2);
  } else {
    const maxRowW = Math.max(...layers.map((ids) => ids.length * (boxW + gapX) - gapX));
    let curY = pad;
    layers.forEach((ids, li) => {
      const rowW = ids.length * (boxW + gapX) - gapX;
      let curX = pad + Math.max(0, (maxRowW - rowW) / 2);
      const rowH = Math.max(...ids.map((id) => boxH.get(id)));
      for (const id of ids) {
        pos.set(id, { x: curX, y: curY, w: boxW, h: boxH.get(id), li });
        curX += boxW + gapX;
      }
      curY += rowH + gapY + 14;
    });
    width = Math.max(500, maxRowW + pad * 2);
    height = Math.max(150, curY - gapY + pad);
  }

  let backCount = 0, skipLrTop = false, skipLrBot = 0, skipTdIdx = 0;
  let maxBackY = height, maxBackX = width;
  const allPos = Array.from(pos.values());
  const edgeSvg = edges.map((e) => {
    const a = pos.get(e.from), b = pos.get(e.to);
    if (!a || !b) return "";
    let d, lx, ly;
    if (e.isBack) {
      const laneIdx = backCount;
      backCount += 1;
      const r = 8;
      if (horizontal) {
        const laneY = height + 10 + laneIdx * 28;
        maxBackY = Math.max(maxBackY, laneY + 24);
        const x1 = a.x + a.w, y1 = a.y + a.h / 2;
        const xOut = a.x + a.w + 18 + (laneIdx % 2) * 8;
        maxBackX = Math.max(maxBackX, xOut + 18);
        const xIn = Math.max(8, b.x - 16 - (laneIdx % 3) * 6), x2 = b.x, y2 = b.y + b.h / 2;
        d = `M ${x1} ${y1} L ${xOut - r} ${y1} Q ${xOut} ${y1} ${xOut} ${y1 + r} L ${xOut} ${laneY - r} Q ${xOut} ${laneY} ${xOut - r} ${laneY} L ${xIn + r} ${laneY} Q ${xIn} ${laneY} ${xIn} ${laneY - r} L ${xIn} ${y2 + r} Q ${xIn} ${y2} ${xIn + r} ${y2} L ${x2} ${y2}`;
        lx = (xOut + xIn) / 2;
        ly = laneY - 6;
      } else {
        const laneX = Math.max(width, maxBackX) + 14 + laneIdx * 32;
        maxBackX = Math.max(maxBackX, laneX + 30);
        const x1 = a.x + a.w / 2, y1 = a.y + a.h, yOut = a.y + a.h + 12;
        const x2 = b.x + b.w / 2, y2 = b.y, yIn = Math.max(8, b.y - 14);
        d = `M ${x1} ${y1} L ${x1} ${yOut - r} Q ${x1} ${yOut} ${x1 + r} ${yOut} L ${laneX - r} ${yOut} Q ${laneX} ${yOut} ${laneX} ${yOut - r} L ${laneX} ${yIn + r} Q ${laneX} ${yIn} ${laneX - r} ${yIn} L ${x2 + r} ${yIn} Q ${x2} ${yIn} ${x2} ${yIn + r} L ${x2} ${y2}`;
        lx = laneX - 6;
        ly = (yOut + yIn) / 2;
      }
    } else if (horizontal) {
      const x1 = a.x + a.w, y1 = a.y + a.h / 2, x2 = b.x, y2 = b.y + b.h / 2;
      const minLi = Math.min(a.li, b.li), maxLi = Math.max(a.li, b.li);
      const midNodes = maxLi - minLi > 1 ? allPos.filter((n) => n.li > minLi && n.li < maxLi) : [];
      const blocked = midNodes.some((n) => n.y <= Math.max(y1, y2) + 10 && n.y + n.h >= Math.min(y1, y2) - 10);
      if (blocked) {
        const r = 8;
        const midTop = Math.min(...midNodes.map((n) => n.y));
        const midBot = Math.max(...midNodes.map((n) => n.y + n.h));
        let laneY;
        if (!skipLrTop && midTop - 18 >= 10 && (y1 + y2) / 2 <= (midTop + midBot) / 2) {
          skipLrTop = true;
          laneY = midTop - 18;
        } else {
          laneY = midBot + 18 + skipLrBot * 20;
          skipLrBot += 1;
          maxBackY = Math.max(maxBackY, laneY + 22);
        }
        const xOut = x1 + 18, xIn = x2 - 18;
        const sy1 = Math.sign(laneY - y1) || 1, sy2 = Math.sign(y2 - laneY) || 1;
        const r1 = Math.min(r, Math.abs(laneY - y1) / 2), r2 = Math.min(r, Math.abs(y2 - laneY) / 2);
        d = `M ${x1} ${y1} L ${xOut - r} ${y1} Q ${xOut} ${y1} ${xOut} ${y1 + sy1 * r1} L ${xOut} ${laneY - sy1 * r1} Q ${xOut} ${laneY} ${xOut + r} ${laneY} L ${xIn - r} ${laneY} Q ${xIn} ${laneY} ${xIn} ${laneY + sy2 * r2} L ${xIn} ${y2 - sy2 * r2} Q ${xIn} ${y2} ${xIn + r} ${y2} L ${x2} ${y2}`;
        lx = (xOut + xIn) / 2;
        ly = laneY - 6;
      } else {
        const dx = Math.max(26, Math.abs(x2 - x1) * 0.45);
        d = `M ${x1} ${y1} C ${x1 + dx} ${y1}, ${x2 - dx} ${y2}, ${x2} ${y2}`;
        lx = (x1 + x2) / 2;
        ly = (y1 + y2) / 2 - 6;
      }
    } else {
      const minLi = Math.min(a.li, b.li), maxLi = Math.max(a.li, b.li);
      const midNodes = maxLi - minLi > 1 ? allPos.filter((n) => n.li > minLi && n.li < maxLi) : [];
      const xMidA = a.x + a.w / 2, xMidB = b.x + b.w / 2;
      const blocked = midNodes.some((n) => n.x <= Math.max(xMidA, xMidB) + 10 && n.x + n.w >= Math.min(xMidA, xMidB) - 10);
      if (blocked) {
        const r = 8;
        const midRight = Math.max(a.x + a.w, b.x + b.w, ...midNodes.map((n) => n.x + n.w));
        const laneX = midRight + 22 + skipTdIdx * 24;
        skipTdIdx += 1;
        maxBackX = Math.max(maxBackX, laneX + 28);
        const x1 = a.x + a.w, y1 = a.y + a.h / 2, x2 = b.x + b.w, y2 = b.y + b.h / 2;
        const sy = Math.sign(y2 - y1) || 1;
        d = `M ${x1} ${y1} L ${laneX - r} ${y1} Q ${laneX} ${y1} ${laneX} ${y1 + sy * r} L ${laneX} ${y2 - sy * r} Q ${laneX} ${y2} ${laneX - r} ${y2} L ${x2} ${y2}`;
        lx = laneX + 6;
        ly = (y1 + y2) / 2;
      } else {
        const x1 = xMidA, y1 = a.y + a.h, x2 = xMidB, y2 = b.y;
        const dy = Math.max(22, Math.abs(y2 - y1) * 0.45);
        d = `M ${x1} ${y1} C ${x1} ${y1 + dy}, ${x2} ${y2 - dy}, ${x2} ${y2}`;
        lx = (x1 + x2) / 2;
        ly = (y1 + y2) / 2 - 4;
      }
    }
    const cls = e.dashed || e.isBack ? "svg-edge-dashed" : "svg-edge-declared";
    const lbl = e.label ? `<text x="${lx.toFixed(1)}" y="${ly.toFixed(1)}" text-anchor="middle" font-size="10.5" class="svg-text-muted">${escHtml(e.label)}</text>` : "";
    return `<path d="${d}" class="${cls}" marker-end="url(#${uid}-arr)" />${lbl}`;
  }).join("");

  const finalW = Math.max(width, maxBackX);
  const finalH = Math.max(height, maxBackY);
  const nodeSvg = order.map((id) => {
    const p = pos.get(id), rows = wrapped.get(id), fullTitle = labels.get(id) || id;
    const startY = p.y + (p.h - rows.length * 16) / 2 + 12;
    const tspans = rows.map((line, idx) => `<text x="${p.x + p.w / 2}" y="${startY + idx * 16}" text-anchor="middle" font-size="11.5" font-weight="500" class="svg-text-ink">${escHtml(line)}</text>`).join("");
    return `<g><title>${escHtml(fullTitle)}</title><rect x="${p.x}" y="${p.y}" width="${p.w}" height="${p.h}" rx="8" class="svg-box-clean" />${tspans}</g>`;
  }).join("");

  return `<svg viewBox="0 0 ${finalW} ${finalH}" class="svg-canvas${finalW > 740 ? " svg-wide" : ""}" role="img" aria-label="Flowchart">
    <defs><marker id="${uid}-arr" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 1 1 L 9 5 L 1 9 z" class="svg-text-muted" /></marker></defs>
    ${edgeSvg}${nodeSvg}</svg>`;
}

function renderSequenceSvg(code, uid) {
  const lines = code.replace(/\r\n/g, "\n").split("\n").map((l) => l.trim()).filter(Boolean);
  const actors = [], actorLabels = new Map(), steps = [];
  const addActor = (id, label) => {
    if (!actors.includes(id)) actors.push(id);
    if (label) actorLabels.set(id, label);
    else if (!actorLabels.has(id)) actorLabels.set(id, id);
  };
  for (let i = 1; i < lines.length; i += 1) {
    const p = lines[i].match(/^(?:participant|actor)\s+([A-Za-z0-9_.-]+)(?:\s+as\s+(.+))?$/);
    if (p) { addActor(p[1], (p[2] || p[1]).trim()); continue; }
    const msg = lines[i].match(/^([^\s:]+?)\s*(-->>|-->|->>|->)\s*[+-]?([^\s:]+)\s*:\s*(.*)$/);
    if (msg) {
      addActor(msg[1]);
      addActor(msg[3]);
      steps.push({ from: msg[1], to: msg[3], dashed: msg[2].startsWith("--"), text: msg[4].trim() });
    }
  }
  if (!actors.length) return "";
  const colW = 220, boxW = 192, padX = 24, topY = 18;
  const wrappedActors = actors.map((id) => wrapTextLines(actorLabels.get(id), 24));
  const boxH = Math.max(40, ...wrappedActors.map((r) => 16 + r.length * 15));
  const stepWrapped = steps.map((s) => wrapTextLines(s.text, 30));
  const stepYs = [];
  let curY = topY + boxH + 34;
  for (const r of stepWrapped) {
    stepYs.push(curY);
    curY += Math.max(44, 24 + r.length * 14);
  }
  const width = Math.max(520, padX * 2 + actors.length * colW - (colW - boxW));
  const height = Math.max(topY + boxH + 60, curY + 18);
  const xOf = new Map(actors.map((id, idx) => [id, padX + idx * colW + boxW / 2]));

  const lifelines = actors.map((id, idx) => {
    const cx = xOf.get(id), rows = wrappedActors[idx];
    const startY = topY + (boxH - rows.length * 15) / 2 + 12;
    const tspans = rows.map((ln, ri) => `<text x="${cx}" y="${startY + ri * 15}" text-anchor="middle" font-size="11.5" font-weight="600" class="svg-text-ink">${escHtml(ln)}</text>`).join("");
    return `<line x1="${cx}" y1="${topY + boxH}" x2="${cx}" y2="${height - 14}" class="svg-axis-line" />
      <g><title>${escHtml(actorLabels.get(id))}</title><rect x="${cx - boxW / 2}" y="${topY}" width="${boxW}" height="${boxH}" rx="7" class="svg-box-clean" />${tspans}</g>`;
  }).join("");

  const arrows = steps.map((s, idx) => {
    const x1 = xOf.get(s.from), x2 = xOf.get(s.to), y = stepYs[idx], rows = stepWrapped[idx];
    const cls = s.dashed ? "svg-edge-dashed" : "svg-edge-focus";
    const textX = s.from === s.to ? x1 + 12 : (x1 + x2) / 2;
    const anchor = s.from === s.to ? "start" : "middle";
    const capY = y - 6 - (rows.length - 1) * 14;
    const captions = rows.map((ln, ri) => `<text x="${textX}" y="${capY + ri * 14}" text-anchor="${anchor}" font-size="10.5" class="svg-text-sec">${escHtml(ln)}</text>`).join("");
    if (x1 === x2) {
      return `<path d="M ${x1} ${y - 6} C ${x1 + 44} ${y - 6}, ${x1 + 44} ${y + 14}, ${x1} ${y + 14}" class="${cls}" marker-end="url(#${uid}-arr)" />${captions}`;
    }
    return `<path d="M ${x1} ${y} L ${x2} ${y}" class="${cls}" marker-end="url(#${uid}-arr)" />${captions}`;
  }).join("");

  return `<svg viewBox="0 0 ${width} ${height}" class="svg-canvas${width > 740 ? " svg-wide" : ""}" role="img" aria-label="Sequence Diagram">
    <defs><marker id="${uid}-arr" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 1 1 L 9 5 L 1 9 z" class="svg-text-focus" /></marker></defs>
    ${lifelines}${arrows}</svg>`;
}

export function renderMermaidSvg(code, lang = "zh") {
  const src = String(code ?? "").trim();
  const first = (src.split(/\r?\n/)[0] || "").trim().toLowerCase();
  const uid = `m-${diagramHash(src)}`;
  let svg = "";
  if (first.startsWith("flowchart") || first.startsWith("graph")) svg = renderFlowchartSvg(src, uid);
  else if (first.startsWith("sequencediagram")) svg = renderSequenceSvg(src, uid);
  const fallback = svg || `<pre><code>${escHtml(src)}</code></pre>`;
  return `${fallback}<details class="diagram-src-toggle"><summary>${escHtml(t(lang, "drawerMermaidRaw"))}</summary><pre><code>${escHtml(src)}</code></pre></details>`;
}
