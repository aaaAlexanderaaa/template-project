// Role: Four-part inline Context Pack card builders, doc prose + Tufte sidenotes extractor, and test-compatible reader shims.
// Out of scope: Page layout routing (app.js), topbar views (views.js), and SVG graph layout (charts.js/diagrams.js).
// Anchors: spec=ui.perspective-web, docs/contracts/frontend-and-visual-discipline.md, SRC-007, SRC-010, SRC-013

import { escHtml, truncMiddle, fmtNum, t, trStage, trTaskState, trHumanCheck, trCategory, trDecisionStatus } from "./i18n.js";
import { slugifyHeading, renderMarkdownToHtml, stripCommentsOutsideCode } from "./markdown.js";
import { renderMermaidSvg } from "./diagrams.js";

function normNonGoals(val) {
  if (Array.isArray(val)) return val.map((v) => String(v || "").trim()).filter(Boolean);
  return String(val || "").split(/[;\n；]+/).map((s) => s.trim()).filter(Boolean);
}

export function extractMarkdownHeadings(markdown) {
  const headings = [];
  let inCode = false, inComment = false, secIdx = 0;
  for (const raw of String(markdown ?? "").replace(/\r\n/g, "\n").split("\n")) {
    const trimmedRaw = raw.trim();
    if (/^(?:```|~~~)/.test(trimmedRaw)) { inCode = !inCode; continue; }
    if (inCode) continue;
    const stripped = stripCommentsOutsideCode(raw, inComment);
    inComment = stripped.inComment;
    const trimmed = stripped.text.trim();
    const m = trimmed.match(/^(#{1,4})\s+(.+)$/);
    if (m) {
      secIdx += 1;
      const clean = m[2].replace(/[`*[\]]/g, "");
      headings.push({ id: `sec-${secIdx}`, slug: slugifyHeading(m[2]), level: m[1].length, text: clean });
    }
  }
  return headings;
}

export function buildContextPackHtml(pack, data, lang, canMutate) {
  if (!pack) return `<div class="muted">${escHtml(t(lang, "noneText"))}</div>`;
  const mod = pack.module || {};
  const task = pack.task || null;
  const domName = typeof pack.domain === "object" ? (pack.domain?.name || pack.domain?.id || "") : (pack.domain || "");
  const tel = pack.telemetry || {};
  const quotes = pack.verbatim_sources || pack.sources || [];
  const adrs = pack.decisions || [];
  const docPath = mod.doc_path || pack.document?.path || "";
  const roTitle = canMutate ? "" : ` title="${escHtml(t(lang, "staticReadonlyTip"))}"`;
  const disabledAttr = canMutate ? "" : " disabled";

  const copyLine = (label, rawVal) => {
    const full = String(rawVal || "");
    if (!full) return "";
    return `<div class="copy-row">
      <span class="muted">${escHtml(label)}: <span class="mono" title="${escHtml(full)}">${escHtml(full)}</span></span>
      <button type="button" class="btn-quiet" data-copy-text="${escHtml(full)}">${escHtml(t(lang, "copyBtn"))}</button>
    </div>`;
  };

  const part1 = `<div class="ctx-section">
    <div class="ctx-heading">${escHtml(t(lang, "ctxPart1"))} · ${escHtml(t(lang, "provAi"))}</div>
    <div><strong>${escHtml(domName ? `${domName} / ` : "")}${escHtml(mod.id || pack.target || pack.document?.path || pack.query || domName || "")}</strong>
      ${mod.stage ? ` · <span class="muted">${escHtml(trStage(lang, mod.stage))}</span>` : ""}</div>
    ${mod.promise || mod.summary ? `<div>${escHtml(mod.promise || mod.summary)}</div>` : ""}
    ${task ? `<div class="row-sub"><strong>${escHtml(task.id)}</strong> · ${escHtml(task.title)} (${escHtml(trTaskState(lang, task.state))} / ${escHtml(trHumanCheck(lang, task.human_check))})</div>` : ""}
    ${pack.finding_msg ? `<div class="row-sub">${escHtml(pack.finding_msg)}</div>${copyLine(t(lang, "findingColLoc"), pack.finding_loc)}` : ""}
    ${task?.blocker_question ? `<div class="row-sub"><strong>?</strong> ${escHtml(task.blocker_question)}</div>` : ""}
    ${task?.selected_option ? `<div class="row-sub"><strong>✓</strong> ${escHtml(task.selected_option)}</div>` : ""}
  </div>`;

  const quoteCard = (q) =>
    `<div class="quote-box"><strong class="mono">${escHtml(q.id)}</strong>${q.date ? ` (${escHtml(q.date)})` : ""}: ${escHtml(q.quote || q.context || "")}</div>`;
  const quoteCards = `${quotes.slice(0, 4).map(quoteCard).join("")}${quotes.length > 4 ? `<details class="diagram-src-toggle"><summary>+${quotes.length - 4} ${escHtml(t(lang, "drawerSources"))}</summary>${quotes.slice(4).map(quoteCard).join("")}</details>` : ""}`;
  const adrChips = adrs.map((d) =>
    `<button type="button" class="btn-quiet" data-jump-trace="${escHtml(d.id)}">${escHtml(d.id)}${d.title && d.title !== d.id ? ` · ${escHtml(truncMiddle(d.title, 20, 12))}` : ""} · ${escHtml(trDecisionStatus(lang, d.status || "current"))}</button>`
  ).join("");
  const part2 = `<div class="ctx-section">
    <div class="ctx-heading">${escHtml(t(lang, "ctxPart2"))} · ${escHtml(t(lang, "provHuman"))}</div>
    ${quoteCards || `<div class="small-note">${escHtml(t(lang, "noneText"))}</div>`}
    ${adrChips ? `<div class="link-row">${adrChips}</div>` : ""}
  </div>`;

  const violHtml = (tel.import_violations || []).slice(0, 6).map((v) =>
    copyLine(`${v.line ? `L${v.line} ` : ""}${v.target_module || v.ref || "violation"}`, `${v.file || ""}:${v.line || ""}`)
  ).join("");
  const fileHtml = (tel.files || []).slice(0, 6).map((f) =>
    copyLine(`${fmtNum(f.lines ?? f.loc ?? 0)} ${t(lang, "linesUnit")}`, f.path)
  ).join("");
  const commitList = Array.isArray(tel.recent_commits) ? tel.recent_commits : [];
  const commitCount = typeof tel.recent_commits === "number" ? tel.recent_commits : commitList.length;
  const shaHtml = commitList.slice(0, 3).map((c) =>
    copyLine(`${truncMiddle(c.sha, 7, 5)} · ${c.subject || ""}`, c.sha)
  ).join("");
  const part3 = `<div class="ctx-section">
    <div class="ctx-heading">${escHtml(t(lang, "ctxPart3"))} · ${escHtml(t(lang, "provFact"))}</div>
    <div class="small-note">${escHtml(fmtNum(tel.file_count || 0))} ${escHtml(t(lang, "filesUnit"))} · ${escHtml(fmtNum(tel.total_loc || 0))} ${escHtml(t(lang, "linesUnit"))} · ${escHtml(t(lang, "drawerCommits"))}: ${escHtml(fmtNum(commitCount))} · ${escHtml(fmtNum(tel.git_doc_lag_commits || 0))} ${escHtml(t(lang, "docLagUnit"))}</div>
    ${violHtml}${fileHtml}${shaHtml}
  </div>`;

  let actionBlock = `<div class="small-note">${escHtml(t(lang, "ctxNoActionNeeded"))}</div>`;
  if (task && task.state === "blocked") {
    const opts = (task.blocker_options || []).map((opt) =>
      `<label class="radio-item"><input type="radio" name="inline-blocker-${escHtml(task.id)}" value="${escHtml(opt)}"${task.selected_option === opt ? " checked" : ""} /><span>${escHtml(opt)}</span></label>`
    ).join("");
    actionBlock = `<div class="radio-list">${opts}</div>
      <label class="small-note">${escHtml(t(lang, "blockerCustomLabel"))}
        <textarea class="input-ctl textarea-ctl" id="inline-custom-${escHtml(task.id)}"></textarea>
      </label>
      <div class="link-row">
        <button type="button" class="btn-primary" data-submit-blocker="${escHtml(task.id)}"${disabledAttr}${roTitle}>${escHtml(t(lang, "btnSubmitBlocker"))}</button>
      </div>
      <div id="inline-err-${escHtml(task.id)}" class="inline-error-msg" hidden></div>`;
  } else if (task && task.state === "ready_for_check" && task.human_check === "pending") {
    actionBlock = `<div class="link-row">
      <button type="button" class="btn-primary" data-approve-task="${escHtml(task.id)}"${disabledAttr}${roTitle}>${escHtml(t(lang, "btnApproveInline"))}</button>
    </div>
    <div id="inline-err-${escHtml(task.id)}" class="inline-error-msg" hidden></div>`;
  }

  const navBtns = [
    docPath ? `<button type="button" class="btn-quiet" data-jump-doc="${escHtml(docPath)}">${escHtml(t(lang, "readDocBtn"))} (${escHtml(truncMiddle(docPath, 14, 16))})</button>` : "",
    ...(task?.design_docs || []).map((dd) => `<button type="button" class="btn-quiet" data-jump-doc="${escHtml(dd)}">${escHtml(truncMiddle(dd, 14, 16))}</button>`),
  ].filter(Boolean).join("");

  const part4 = `<div class="ctx-section">
    <div class="ctx-heading">${escHtml(t(lang, "ctxPart4"))}</div>
    ${actionBlock}
    ${navBtns ? `<div class="link-row">${navBtns}</div>` : ""}
  </div>`;

  return `<div class="inline-expand-card">${part1}${part2}${part3}${part4}</div>`;
}

export function renderDocContentAndSidenotes(doc, data, lang) {
  if (!doc) return { proseHtml: "", sidenotes: [], headings: [] };
  const isMd = String(doc.path || "").toLowerCase().endsWith(".md");
  const mod = doc.owner_module ? data?.capsules?.[doc.owner_module]?.module : null;
  const pack = doc.owner_module ? data?.capsules?.[doc.owner_module] : null;
  const headings = isMd ? extractMarkdownHeadings(doc.body_markdown || "") : [];
  const findSec = (re) => (headings.find((h) => re.test(h.text)) || headings[1] || headings[0])?.id || "";
  const sidenotes = [];
  if (doc.summary) {
    sidenotes.push({ id: "note-summary", tag: t(lang, "provAi"), title: trCategory(lang, doc.category), body: doc.summary, anchorSec: findSec(/purpose|position|overview|背景|概述|目标/i) });
  }
  if (mod?.promise) {
    sidenotes.push({ id: "note-promise", tag: t(lang, "provAi"), title: mod.id, body: mod.promise, anchorSec: findSec(/boundary|interface|coupling|边界|职责/i) });
  }
  const domMatch = (data?.domains || []).find((d) => doc.path.endsWith(`specs/${d.id}/README.md`) || doc.owner_module === d.id);
  if (domMatch) {
    const ng = normNonGoals(domMatch.non_goals).slice(0, 2).join("; ");
    const modNames = (domMatch.modules || []).map((m) => m.id).join(", ");
    sidenotes.push({
      id: `note-dom-${domMatch.id}`,
      tag: t(lang, "provAi"),
      title: `${domMatch.name || domMatch.id} (${trStage(lang, domMatch.stage)})`,
      body: [domMatch.promise || "", ng ? `${t(lang, "drawerNonGoals")}: ${ng}` : "", modNames ? `${t(lang, "drawerModules")}: ${modNames}` : ""].filter(Boolean).join(" · "),
      anchorSec: findSec(/non-goal|scope|module|boundary|边界|不做什么/i),
    });
    if ((domMatch.decisions || []).length) {
      sidenotes.push({
        id: `note-dom-adrs-${domMatch.id}`,
        tag: t(lang, "provAi"),
        title: t(lang, "drawerDecisions"),
        body: domMatch.decisions.slice(0, 4).map((x) => x.id || x).join(", "),
        anchorSec: findSec(/decision|adr|决策|边界/i),
      });
    }
    if ((domMatch.sources || []).length) {
      sidenotes.push({
        id: `note-dom-srcs-${domMatch.id}`,
        tag: t(lang, "provHuman"),
        title: t(lang, "drawerSources"),
        body: domMatch.sources.slice(0, 4).map((x) => x.id || x).join(", "),
        anchorSec: findSec(/source|scope|定位|原则/i),
      });
    }
  }
  const adrMatch = doc.category === "decision"
    ? (data?.provenance_nodes || []).find((n) => (n.kind === "decision" || n.trace?.anchor_type === "decision") && doc.path.includes(n.id))
    : null;
  if (adrMatch?.trace) {
    const tr = adrMatch.trace;
    for (const s of (tr.sources || []).slice(0, 6)) {
      const sid = typeof s === "string" ? s : s.id;
      const sq = typeof s === "string" ? s : (s.quote || s.context || s.id);
      sidenotes.push({ id: `note-adr-src-${sid}`, tag: t(lang, "provHuman"), title: sid, body: truncMiddle(sq, 64, 24), traceId: sid, anchorSec: findSec(/context|source|decision|依据|背景|决定/i) });
    }
    if ((tr.modules || []).length) {
      sidenotes.push({ id: `note-adr-mods`, tag: t(lang, "provAi"), title: t(lang, "drawerAffectedModules"), body: tr.modules.map((m) => m.id || m).join(", "), traceId: tr.id, anchorSec: findSec(/consequence|effect|module|影响/i) });
    }
  }
  for (const s of (pack?.verbatim_sources || []).slice(0, 3)) {
    sidenotes.push({ id: `note-${s.id}`, tag: t(lang, "provHuman"), title: `${s.id} (${s.date || ""})`, body: truncMiddle(s.quote || s.context || "", 72, 24), traceId: s.id, anchorSec: findSec(/context|decision|source|背景|决策|约束/i) });
  }
  for (const d of (pack?.decisions || []).slice(0, 3)) {
    sidenotes.push({ id: `note-${d.id}`, tag: t(lang, "provAi"), title: d.id, body: d.title || d.id, traceId: d.id, anchorSec: findSec(/decision|invariant|约束|决策/i) });
  }
  if (pack?.telemetry) {
    const tel = pack.telemetry;
    sidenotes.push({
      id: "note-fact",
      tag: t(lang, "provFact"),
      title: truncMiddle(doc.path, 14, 16),
      body: `${fmtNum(doc.line_count)} ${t(lang, "linesUnit")} · ${fmtNum(tel.file_count || 0)} ${t(lang, "filesUnit")} / ${fmtNum(tel.total_loc || 0)} ${t(lang, "linesUnit")}`,
      copyPath: doc.path,
    });
  } else {
    sidenotes.push({
      id: "note-fact",
      tag: t(lang, "provFact"),
      title: truncMiddle(doc.path, 14, 16),
      body: `${fmtNum(doc.line_count)} ${t(lang, "linesUnit")}`,
      copyPath: doc.path,
    });
  }

  const inlineNotesHtml = sidenotes.length
    ? `<details class="sidenote-inline-wrap"><summary class="small-note">${escHtml(t(lang, "sidenoteToggle"))} (${sidenotes.length})</summary>
        ${sidenotes.map((n) => `<div class="row-sub"><strong>${escHtml(n.title)}</strong> <span class="tertiary">[${escHtml(n.tag)}]</span>: ${escHtml(n.body)}${n.traceId ? ` <button type="button" class="btn-quiet" data-jump-trace="${escHtml(n.traceId)}">${escHtml(n.traceId)}</button>` : ""}${n.copyPath ? ` <button type="button" class="btn-quiet" data-copy-text="${escHtml(n.copyPath)}">${escHtml(t(lang, "copyBtn"))}</button>` : ""}</div>`).join("")}
      </details>`
    : "";

  const proseHtml = isMd
    ? `${inlineNotesHtml}<article class="md-prose">${renderMarkdownToHtml(doc.body_markdown || "", (c) => renderMermaidSvg(c, lang), doc.path)}</article>`
    : `${inlineNotesHtml}<pre class="log-pre"><code>${escHtml(doc.body_markdown || "")}</code></pre>`;

  return { proseHtml, sidenotes, headings };
}

/* Compatibility panel writers preserved for standalone helper harnesses */
export function openDrawer(kicker, title, htmlBody) {
  const kEl = document.getElementById("drawer-kicker");
  const tEl = document.getElementById("drawer-title");
  const bEl = document.getElementById("drawer-body");
  if (kEl) kEl.textContent = kicker || "";
  if (tEl) tEl.textContent = title || "";
  if (bEl) bEl.innerHTML = htmlBody || "";
}

export function closeDrawer() {
  document.getElementById("drawer-root")?.classList.add("hidden");
}

export function renderDocReader(doc, lang) {
  if (!doc) return;
  const { proseHtml } = renderDocContentAndSidenotes(doc, null, lang);
  openDrawer(trCategory(lang, doc.category), doc.title || doc.path, `<div>${escHtml(doc.path)}</div>${proseHtml}`);
}

export function renderDirectoryDrawer(dir, docsMap, lang) {
  if (!dir) return;
  const label = lang === "zh" ? (dir.label_zh || dir.path) : (dir.label_en || dir.path);
  const items = (dir.doc_paths || []).map((p) => {
    const doc = docsMap?.get(p);
    return `<button type="button" class="btn-quiet" data-jump-doc="${escHtml(p)}">${escHtml(doc ? doc.title : p)}</button>`;
  }).join("");
  openDrawer(dir.path, label, `<div>${escHtml(lang === "zh" ? dir.summary_zh : dir.summary_en)}</div><div>${items}</div>`);
}

export function renderModuleDetail(modId, graph, lang) {
  const cap = graph?.capsules?.[modId];
  if (!cap || !cap.found) return;
  openDrawer(`${cap.domain?.name || ""} / ${modId}`, cap.module?.title || modId, buildContextPackHtml(cap, graph, lang, false));
}

export function renderMilestoneDetail(ms, domainName, lang) {
  if (!ms) return;
  const rows = (ms.tasks || []).map((tk) => `<div><strong>${escHtml(tk.id)}</strong> · ${escHtml(tk.title)} (${escHtml(trTaskState(lang, tk.state))})</div>`).join("");
  openDrawer(domainName || "", `${ms.id} · ${ms.name || ""}`, rows);
}

export function renderTraceDetail(traceId, graph, lang) {
  const entry = (graph?.provenance_nodes || []).find((n) => n.id === traceId);
  const tr = entry?.trace;
  if (!tr || !tr.found) return;
  const modList = (tr.modules || []).map((m) => `<span>${escHtml(m.id)}</span>`).join(" ");
  openDrawer(tr.anchor_type === "source" ? "SRC" : "ADR", `${tr.id}${tr.title ? ` · ${tr.title}` : ""}`, `
    ${tr.quote ? `<div class="quote-box">${escHtml(tr.quote)}</div>` : ""}
    <div>${modList}</div>
  `);
}

export function taskPackFromGraph(graph, dom, ms, tk) {
  const specs = tk.specs || [];
  const firstModId = specs.find((s) => s.startsWith("ui.") && graph.capsules?.[s]) || specs.find((s) => graph.capsules?.[s]) || "";
  const base = firstModId ? graph.capsules[firstModId] : null;
  const provMap = new Map((graph.provenance_nodes || []).map((n) => [n.id, n.trace]));
  const pivotMap = new Map((graph.timeline?.pivots || []).map((p) => [p.id, p]));
  const srcIds = (tk.sources || []).filter(Boolean);
  const srcList = srcIds.map((sid) => {
    const tr = provMap.get(sid);
    return tr ? { id: sid, date: tr.date || "", quote: tr.quote || tr.context || "" } : { id: sid, quote: sid };
  });
  const decIds = (tk.decisions || []).filter(Boolean);
  const decList = decIds.map((did) => {
    const tr = provMap.get(did);
    const pv = pivotMap.get(did);
    return { id: did, title: tr?.title || pv?.title || did, status: tr?.status || pv?.status || "current" };
  });
  const baseSrcs = base?.verbatim_sources || [];
  const mergedSrcs = [...srcList, ...baseSrcs.filter((b) => !srcIds.includes(b.id))];
  const baseDecs = base?.decisions || [];
  const mergedDecs = [...decList, ...baseDecs.filter((b) => !decIds.includes(b.id))];
  return {
    target: tk.id,
    domain: { id: dom.id, name: dom.name },
    module: base?.module || { id: firstModId || dom.id, stage: dom.stage, promise: dom.promise },
    task: { ...tk, milestone: ms.id },
    verbatim_sources: mergedSrcs,
    decisions: mergedDecs,
    telemetry: base?.telemetry || { file_count: 0, total_loc: 0, git_doc_lag_commits: 0 },
  };
}

export function extractArchitectureHighlights(archMd) {
  const items = [];
  let inCode = false, codeLang = "", mermaidLbls = [], sawTableSep = false;
  const clip = (txt) => (txt.length > 140 ? `${txt.slice(0, 137)}…` : txt);
  const stripMd = (s) => s.replace(/\[([^\]]+)\]\([^)]+\)/g, "$1").replace(/[`*]/g, "").trim();
  for (const raw of String(archMd ?? "").replace(/\r\n/g, "\n").split("\n")) {
    const line = raw.trim();
    const fence = line.match(/^(?:```|~~~)\s*([a-zA-Z0-9_-]*)\s*$/);
    if (fence) {
      inCode = !inCode;
      if (inCode) { codeLang = fence[1].toLowerCase(); mermaidLbls = []; }
      else if (codeLang === "mermaid" && items.length && !items[items.length - 1].summary && mermaidLbls.length) {
        items[items.length - 1].summary = clip(mermaidLbls.slice(0, 4).join(" → "));
      }
      continue;
    }
    if (inCode) {
      if (codeLang === "mermaid") {
        for (const m of line.matchAll(/\["([^"]+)"\]/g)) mermaidLbls.push(stripMd(m[1]));
      }
      continue;
    }
    if (!line || line.startsWith("<!--")) continue;
    const hm = line.match(/^##\s+(.+)$/);
    if (hm) { items.push({ heading: hm[1].replace(/[`*[\]]/g, "").trim(), summary: "" }); sawTableSep = false; continue; }
    const cur = items[items.length - 1];
    if (!cur || cur.summary) continue;
    if (/^\|[\s:-]+\|/.test(line)) { sawTableSep = true; continue; }
    if (line.startsWith("|")) {
      if (!sawTableSep) continue;
      const cells = line.slice(1, -1).split("|").map((c) => stripMd(c)).filter(Boolean);
      if (cells.length) cur.summary = clip(cells.slice(0, 2).join(" — "));
      continue;
    }
    sawTableSep = false;
    if (line.startsWith("#")) continue;
    const clean = stripMd(line.replace(/^[-*>]\s+/, "").replace(/^\[![A-Z]+\]\s*/i, ""));
    if (clean) cur.summary = clip(clean);
  }
  return items.slice(0, 6);
}

export function renderArchitectureDigestHtml(graph, lang) {
  const domains = graph?.domains || [];
  if (!domains.length) return "";
  const docsSet = new Set((graph?.repo_docs || []).map((d) => d.path));
  const dirLocMap = new Map();
  for (const de of graph?.directory_map || []) {
    if (!de.domain) continue;
    const prev = dirLocMap.get(de.domain) || 0;
    dirLocMap.set(de.domain, prev + (de.total_lines || 0));
  }
  const rows = domains.map((d) => {
    const specPath = `docs/specs/${d.id}/README.md`;
    const jumpAttr = docsSet.has(specPath) ? `data-jump-doc="${escHtml(specPath)}"` : `data-open-domain="${escHtml(d.id)}"`;
    const nonGoals = normNonGoals(d.non_goals).slice(0, 2).join("；");
    const modCount = (d.modules || []).length;
    const adrCount = (d.decisions || []).length;
    const srcCount = (d.sources || []).length;
    const locVal = d.loc != null ? d.loc : (dirLocMap.get(d.id) || 0);
    const meta = [
      `${fmtNum(modCount)} ${t(lang, "modulesUnit")}`,
      adrCount ? `${fmtNum(adrCount)} ${t(lang, "decisionsUnit")}` : "",
      srcCount ? `${fmtNum(srcCount)} ${t(lang, "sourcesUnit")}` : "",
      locVal ? `${fmtNum(locVal)} ${t(lang, "linesUnit")}` : "",
    ].filter(Boolean).join(" · ");
    return `<tr class="data-row" ${jumpAttr}>
      <td><strong>${escHtml(d.name || d.id)}</strong><div class="row-sub mono">${escHtml(d.id)} · ${escHtml(trStage(lang, d.stage))}</div></td>
      <td><div>${escHtml(d.promise || "-")}</div>${nonGoals ? `<div class="row-sub muted">${escHtml(`${t(lang, "drawerNonGoals")}: ${nonGoals}`)}</div>` : ""}</td>
      <td class="col-pri-2 num">${escHtml(meta)}</td>
    </tr>`;
  }).join("");
  return `<div class="platter-section">
    <div class="section-head"><h2 class="section-title">${escHtml(t(lang, "subsystemsTitle"))}</h2></div>
    <table class="data-table"><thead><tr><th>${escHtml(t(lang, "colModDomain"))}<span class="col-hidden-note col-hint-narrow">${escHtml(t(lang, "colHiddenMid1"))}</span></th><th>${escHtml(t(lang, "colDirRole"))}</th><th class="col-pri-2">${escHtml(t(lang, "colTraceImpact"))}</th></tr></thead><tbody>${rows}</tbody></table>
  </div><div class="platter-divider"></div>`;
}

export function buildDocDrawerShellHtml() {
  return `<div class="section-head">
      <div class="filter-group">
        <button type="button" class="filter-btn" data-dtab="tree"></button>
        <button type="button" class="filter-btn" data-dtab="search"></button>
        <button type="button" class="filter-btn" data-dtab="notes"></button>
      </div>
      <button type="button" class="top-btn" data-action="close-doc-drawer"></button>
    </div>
    <div id="drawer-filter-wrap" class="drawer-filters">
      <input type="search" id="drawer-doc-search" class="input-ctl" />
      <select id="drawer-cat-select" class="input-ctl compact-select"></select>
    </div>
    <div class="drawer-scroll" id="drawer-doc-results"></div>`;
}

const DRAWER_CAT_ORDER = ["entry", "contract", "guide", "skill", "spec", "design", "decision", "template", "config"];

function _docSearchSnippet(body, q) {
  const text = String(body || "").replace(/\s+/g, " ").trim();
  const idx = text.toLowerCase().indexOf(q);
  if (idx < 0) return "";
  const start = Math.max(0, idx - 24);
  const slice = text.slice(start, start + 84).trim();
  return `${start > 0 ? "…" : ""}${slice}${start + 84 < text.length ? "…" : ""}`;
}

export function buildDocDrawerResultsHtml(graph, uiState) {
  const lang = uiState.lang;
  const docs = graph?.repo_docs || [];
  const activeDoc = docs.find((d) => d.path === uiState.selectedDocPath) || docs[0];
  const { sidenotes, headings } = renderDocContentAndSidenotes(activeDoc, graph, lang);
  if (uiState.docDrawerTab === "notes") {
    const html = sidenotes.map((n) => `<div class="sidenote-item">
      <button type="button" class="doc-tree-btn"${n.anchorSec ? ` data-jump-sec="${escHtml(n.anchorSec)}"` : ""}><strong>${escHtml(n.title)}</strong> <span class="tertiary">[${escHtml(n.tag)}]</span><div class="small-note">${escHtml(n.body)}</div></button>
      <div class="link-row">${n.traceId ? `<button type="button" class="btn-quiet" data-jump-trace="${escHtml(n.traceId)}">${escHtml(n.traceId)}</button>` : ""}${n.copyPath ? `<button type="button" class="btn-quiet" data-copy-text="${escHtml(n.copyPath)}">${escHtml(t(lang, "copyBtn"))}</button>` : ""}</div>
    </div>`).join("") || `<div class="small-note">${escHtml(t(lang, "noneText"))}</div>`;
    return { html, notesCount: sidenotes.length };
  }
  const q = uiState.docQuery.trim().toLowerCase();
  const filtered = docs.filter((d) => (uiState.docCategory === "all" || d.category === uiState.docCategory)
    && (!q || `${d.title} ${d.path} ${d.summary || ""} ${d.body_markdown || ""}`.toLowerCase().includes(q)));
  const renderDocBtn = (d) => {
    const snip = q && !`${d.title} ${d.path}`.toLowerCase().includes(q) ? _docSearchSnippet(d.body_markdown, q) : "";
    return `<button type="button" class="doc-tree-btn${d.path === activeDoc?.path ? " is-active" : ""}" data-select-doc="${escHtml(d.path)}">
      <div>${escHtml(d.title)}</div><div class="small-note mono">${escHtml(truncMiddle(d.path, 14, 14))}</div>
      ${snip ? `<div class="small-note">${escHtml(snip)}</div>` : ""}
    </button>`;
  };
  let listHtml = "";
  if (uiState.docDrawerTab === "tree" && !q && uiState.docCategory === "all") {
    const groups = new Map();
    for (const d of filtered) {
      const cat = d.category || "other";
      if (!groups.has(cat)) groups.set(cat, []);
      groups.get(cat).push(d);
    }
    const cats = [...DRAWER_CAT_ORDER.filter((c) => groups.has(c)), ...[...groups.keys()].filter((c) => !DRAWER_CAT_ORDER.includes(c))];
    listHtml = cats.map((cat) => {
      const items = groups.get(cat) || [];
      const isOpen = items.some((d) => d.path === activeDoc?.path) ? " open" : "";
      return `<details class="drawer-cat-group"${isOpen}><summary>${escHtml(trCategory(lang, cat))} (${items.length})</summary>${items.map(renderDocBtn).join("")}</details>`;
    }).join("");
  } else {
    listHtml = filtered.map(renderDocBtn).join("");
  }
  const tocHtml = uiState.docDrawerTab === "tree" && !q && uiState.docCategory === "all" && headings.length > 0
    ? `<div class="ctx-section"><div class="ctx-heading">${escHtml(t(lang, "docOutlineHead"))} · ${escHtml(activeDoc?.title || "")}</div>${headings.map((h) => {
        const indCls = h.level >= 3 ? " doc-toc-indent-3" : (h.level === 2 ? " doc-toc-indent-2" : "");
        return `<button type="button" class="doc-tree-btn${indCls}" data-jump-sec="${escHtml(h.id)}">${escHtml(h.text)}</button>`;
      }).join("")}</div>`
    : "";
  const bodyHtml = `${tocHtml}${listHtml || `<div class="small-note">${escHtml(t(lang, "emptyFiltered"))}</div>`}`;
  return { html: bodyHtml, notesCount: sidenotes.length };
}

export function inboxPackFromGraph(graph, item, blocked) {
  const base = item.module_id ? graph.capsules?.[item.module_id] : null;
  return {
    target: item.task_id,
    domain: { id: item.domain_id, name: item.domain_name },
    module: base?.module || { id: item.module_id || item.domain_id, promise: item.promise },
    task: {
      id: item.task_id,
      title: item.title,
      milestone: item.milestone_id,
      state: blocked ? "blocked" : "ready_for_check",
      human_check: "pending",
      blocker_question: item.blocker_question || "",
      blocker_options: item.blocker_options || [],
      design_docs: item.design_docs || [],
    },
    verbatim_sources: item.source_id ? [{ id: item.source_id, date: item.source_date, quote: item.source_quote }] : (base?.verbatim_sources || []),
    decisions: base?.decisions || [],
    telemetry: base?.telemetry || { file_count: 0, total_loc: 0, git_doc_lag_commits: 0 },
  };
}

export function renderBlockedModal(item, lang) {
  if (!item) return;
  openDrawer(item.task_id, item.blocker_question || item.title, `<div class="quote-box">${escHtml(item.source_quote || "")}</div>`);
}
