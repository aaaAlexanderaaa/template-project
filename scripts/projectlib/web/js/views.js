// Role: Pure view renderers for Overview, Boundaries & Architecture, Roadmap & Lineage, and Long-Form Documents.
// Out of scope: Network IO, browser event listeners (app.js), and direct SVG layout algorithms (charts.js/diagrams.js).
// Anchors: spec=ui.perspective-web, docs/contracts/frontend-and-visual-discipline.md, SRC-005, SRC-007, SRC-008, SRC-013

import { escHtml, truncMiddle, fmtNum, fmtStatusCount, t, trStage, trTaskState, trHumanCheck, trCategory, trDecisionStatus, trDiffDomain, trSeverity, trFileStatus, trRuleId } from "./i18n.js";
import { renderMermaidSvg } from "./diagrams.js";
import { renderTimelineSvg, renderProvenanceSvg, renderDomainMapSvg, renderModuleMapSvg } from "./charts.js";
import { buildContextPackHtml, renderDocContentAndSidenotes, taskPackFromGraph, inboxPackFromGraph, renderArchitectureDigestHtml, extractArchitectureHighlights } from "./drawer.js";
import { renderRoadmapTraceHtml, renderRoadmapDiffHtml } from "./roadmap_panels.js";

function _colHintHtml(lang, midKey, narrowKey) {
  const midTxt = midKey ? `<span class="col-hidden-note col-hint-mid">${escHtml(t(lang, midKey))}</span>` : "";
  const narrowTxt = narrowKey ? `<span class="col-hidden-note col-hint-narrow">${escHtml(t(lang, narrowKey))}</span>` : "";
  return `${midTxt}${narrowTxt}`;
}

export function renderOverviewView(graph, uiState) {
  const lang = uiState.lang;
  const p = graph.project || {};
  const canMutate = !uiState.staticMode;
  const blocked = graph.blocked_inbox || [];
  const ready = graph.ready_inbox || [];
  const allActions = [
    ...blocked.map((b) => ({ kind: "blocked", key: `ov-act::${b.task_id}`, item: b })),
    ...ready.map((r) => ({ kind: "ready", key: `ov-act::${r.task_id}`, item: r })),
  ];

  const actionRows = allActions.map(({ kind, key, item }) => {
    const isExp = uiState.expandedKey === key;
    const dotCls = kind === "blocked" ? "dot-warn" : "dot-ok";
    const statusTxt = kind === "blocked" ? trTaskState(lang, "blocked") : trTaskState(lang, "ready_for_check");
    const pack = uiState.contextCache[item.task_id] || inboxPackFromGraph(graph, item, kind === "blocked");
    const expRow = isExp
      ? `<tr class="inline-expand-row"><td colspan="4">${buildContextPackHtml(pack, graph, lang, canMutate)}</td></tr>`
      : "";
    return `<tr class="data-row" data-expand-key="${escHtml(key)}" data-context-q="${escHtml(item.task_id)}" data-expanded="${isExp}">
      <td><strong>${escHtml(item.task_id)}</strong> · ${escHtml(item.domain_name)}<div class="row-sub">${escHtml(kind === "blocked" ? item.blocker_question : item.title)}</div></td>
      <td><span class="status-label"><span class="status-dot ${dotCls}"></span>${escHtml(statusTxt)}</span></td>
      <td class="col-pri-2">${escHtml(item.source_id || "-")}</td>
      <td class="col-pri-3 num">${escHtml(item.module_id || "-")}</td>
    </tr>${expRow}`;
  }).join("");

  const actionSection = allActions.length
    ? `<div class="platter-section">
        <div class="section-head"><h2 class="section-title">${escHtml(t(lang, "actionNeededHead"))} (${allActions.length})</h2></div>
        <table class="data-table">
          <thead><tr>
            <th>${escHtml(t(lang, "colTaskItem"))}${_colHintHtml(lang, "colHiddenMid1", "colHiddenNarrow2")}</th>
            <th>${escHtml(t(lang, "colTaskState"))}</th>
            <th class="col-pri-2">${escHtml(t(lang, "colTaskSources"))}</th>
            <th class="col-pri-3">${escHtml(t(lang, "colModName"))}</th>
          </tr></thead>
          <tbody>${actionRows}</tbody>
        </table>
      </div><div class="platter-divider"></div>`
    : `<div class="platter-section"><span class="status-label"><span class="status-dot dot-ok"></span><span class="muted">${escHtml(t(lang, "actionCalmNote"))}</span></span></div><div class="platter-divider"></div>`;

  const mermaids = graph.system_mermaids || [];
  const dIdx = Math.min(uiState.overviewDiagramIdx || 0, Math.max(0, mermaids.length - 1));
  const diagramSwitcher = mermaids.length > 1
    ? `<div class="filter-group">${mermaids.map((m, idx) =>
        `<button type="button" class="filter-btn${idx === dIdx ? " is-active" : ""}" data-diagram-idx="${idx}">${escHtml(m.title || `#${idx + 1}`)}</button>`
      ).join("")}</div>`
    : "";
  const activeDiagram = mermaids[dIdx] ? `<div class="diagram-box">${renderMermaidSvg(mermaids[dIdx].code, lang)}</div>` : "";

  const starterPaths = lang === "en"
    ? ["README.md", "ARCHITECTURE.md", "AGENTS.md", "README_CN.md", "docs/design/perspective-web.md"]
    : ["README_CN.md", "README.md", "ARCHITECTURE.md", "AGENTS.md", "docs/design/perspective-web.md"];
  const starterDocs = [];
  for (const sp of starterPaths) {
    const found = (graph.repo_docs || []).find((d) => d.path === sp);
    if (found && starterDocs.length < 4) starterDocs.push(found);
  }
  if (starterDocs.length < 3) {
    for (const d of graph.repo_docs || []) {
      if (!starterDocs.includes(d) && starterDocs.length < 3) starterDocs.push(d);
    }
  }
  const starterHtml = starterDocs.map((d) =>
    `<button type="button" class="starter-link" data-jump-doc="${escHtml(d.path)}">
      <strong>${escHtml(d.title)}</strong>
      <div class="row-sub mono">${escHtml(truncMiddle(d.path, 14, 16))} · ${escHtml(trCategory(lang, d.category))}</div>
    </button>`
  ).join("");

  const archItems = extractArchitectureHighlights(p.architecture_markdown || "");
  const archSummaryHtml = archItems.length
    ? `<div class="arch-summary">
        <div class="section-sub"><strong>${escHtml(t(lang, "archSummaryTitle"))}</strong></div>
        <ul class="arch-list">${archItems.map((it) => `<li><strong>${escHtml(it.heading)}</strong>${it.summary ? ` — ${escHtml(it.summary)}` : ""}</li>`).join("")}</ul>
        ${(graph.repo_docs || []).some((d) => d.path === "ARCHITECTURE.md") ? `<div class="link-row"><button type="button" class="btn-quiet" data-jump-doc="ARCHITECTURE.md">${escHtml(t(lang, "readArchBtn"))}</button></div>` : ""}
      </div>`
    : "";

  const dirs = graph.directory_map || [];
  const docsByPath = new Map((graph.repo_docs || []).map((d) => [d.path, d]));
  const dirRows = dirs.map((de) => {
    const key = `ov-dir::${de.path}`;
    const isExp = uiState.expandedKey === key;
    const label = lang === "zh" ? (de.label_zh || de.path) : (de.label_en || de.path);
    const summary = lang === "zh" ? (de.summary_zh || de.summary_en || "") : (de.summary_en || de.summary_zh || "");
    const expRow = isExp
      ? `<tr class="inline-expand-row"><td colspan="5"><div class="inline-expand-card">
          <div><strong>${escHtml(de.path)}</strong> · ${escHtml(label)}</div>
          <div class="muted">${escHtml(summary)}</div>
          <div class="link-row">${(de.doc_paths || []).map((dp) => {
            const doc = docsByPath.get(dp);
            return `<button type="button" class="btn-quiet" data-jump-doc="${escHtml(dp)}">${escHtml(doc ? doc.title : truncMiddle(dp, 12, 14))}</button>`;
          }).join("") || `<span class="small-note">${escHtml(t(lang, "noneText"))}</span>`}</div>
        </div></td></tr>`
      : "";
    return `<tr class="data-row" data-expand-key="${escHtml(key)}" data-expanded="${isExp}">
      <td class="mono">${escHtml(de.path)}</td>
      <td><strong>${escHtml(label)}</strong><div class="row-sub">${escHtml(summary)}</div></td>
      <td class="col-pri-3">${escHtml(de.domain || "-")}</td>
      <td class="col-pri-2 num">${escHtml(`${fmtNum(de.file_count)} / ${fmtNum(de.doc_count)}`)}</td>
      <td class="col-pri-2 num">${escHtml(fmtNum(de.total_lines))}</td>
    </tr>${expRow}`;
  }).join("");

  const topNote = p.identity === "template" ? t(lang, "templateGuideNote") : (p.is_day_zero ? t(lang, "dayZeroNote") : "");
  const docLoc = p.doc_loc != null ? ` · ${t(lang, "docLocLabel")} ${fmtNum(p.doc_loc)}` : "";
  const canvasSummary = `${p.name || t(lang, "brandFallback")} · ${trStage(lang, p.stage)} · ${fmtNum(p.domain_count)} ${t(lang, "domainsUnit")} · ${fmtNum(p.doc_count)} ${t(lang, "docsUnit")} · ${t(lang, "codeLocLabel")} ${fmtNum(p.total_loc)}${docLoc}`;

  return {
    html: `<div class="orient-shell">
      <div class="canvas-bar">
        <span class="small-note">${escHtml(canvasSummary)}</span>
        ${topNote ? `<span class="small-note">${escHtml(topNote)}</span>` : ""}
      </div>
      <div class="platter">
        ${actionSection}
        <div class="platter-section">
          <div class="section-head"><h2 class="section-title">${escHtml(t(lang, "overviewIntroTitle"))}</h2>${diagramSwitcher}</div>
          <p class="section-sub">${escHtml(p.one_liner || "")}</p>
          ${activeDiagram}
          ${archSummaryHtml}
        </div>
        <div class="platter-divider"></div>
        <div class="platter-section">
          <div class="section-head"><h2 class="section-title">${escHtml(t(lang, "starterDocsTitle"))}</h2></div>
          <div class="starter-grid">${starterHtml}</div>
        </div>
        <div class="platter-divider"></div>
        ${renderArchitectureDigestHtml(graph, lang)}
        <div class="platter-section">
          <div class="section-head"><h2 class="section-title">${escHtml(t(lang, "dirTableTitle"))}</h2></div>
          <table class="data-table">
            <thead><tr>
              <th>${escHtml(t(lang, "colDirPath"))}</th>
              <th>${escHtml(t(lang, "colDirRole"))}${_colHintHtml(lang, "colHiddenMid1", "colHiddenNarrow3")}</th>
              <th class="col-pri-3">${escHtml(t(lang, "colDirDomain"))}</th>
              <th class="col-pri-2">${escHtml(t(lang, "colDirFiles"))}</th>
              <th class="col-pri-2">${escHtml(t(lang, "colDirLoc"))}</th>
            </tr></thead>
            <tbody>${dirRows}</tbody>
          </table>
        </div>
      </div>
    </div>`,
    statusLeft: "",
    statusRight: "",
  };
}

export function renderBoundariesView(graph, uiState) {
  const lang = uiState.lang;
  const canMutate = !uiState.staticMode;
  const domains = graph.domains || [];
  const findings = graph.findings || [];
  const subMode = uiState.boundarySubMode || "matrix";

  const allModules = [];
  for (const d of domains) {
    for (const m of d.modules || []) {
      const hasIssue = (m.violation_count || 0) > 0 || (m.oversized_count || 0) > 0 || (m.git_lag || 0) > 0;
      allModules.push({ dom: d, mod: m, hasIssue });
    }
  }
  const issueTotal = allModules.filter((x) => x.hasIssue).length;
  const filteredMods = allModules.filter((x) => {
    if (uiState.boundaryDomain && x.dom.id !== uiState.boundaryDomain) return false;
    if (uiState.boundaryOnlyIssues && !x.hasIssue) return false;
    return true;
  });

  const filterHtml = `<div class="canvas-bar">
    <div class="canvas-row">
      <div class="filter-group">
        <button type="button" class="filter-btn${subMode === "matrix" ? " is-active" : ""}" data-bmode="matrix">${escHtml(t(lang, "subModeBoundariesMatrix"))} (${allModules.length})</button>
        <button type="button" class="filter-btn${subMode === "map" ? " is-active" : ""}" data-bmode="map">${escHtml(t(lang, "subModeBoundariesMap"))}</button>
        <button type="button" class="filter-btn${subMode === "findings" ? " is-active" : ""}" data-bmode="findings">${escHtml(t(lang, "subModeBoundariesFindings"))} (${findings.length})</button>
      </div>
      <select class="input-ctl compact-select" id="boundary-domain-select" aria-label="Domain filter">
        <option value="">${escHtml(t(lang, "filterAllDomains"))}</option>
        ${domains.map((d) => `<option value="${escHtml(d.id)}"${d.id === uiState.boundaryDomain ? " selected" : ""}>${escHtml(d.name)}</option>`).join("")}
      </select>
      ${subMode !== "findings" ? `<button type="button" class="filter-btn${uiState.boundaryOnlyIssues ? " is-active" : ""}" data-action="toggle-only-issues">${escHtml(t(lang, "filterOnlyIssues"))} (${issueTotal})</button>` : ""}
    </div>
  </div>`;

  let bodyHtml = "";
  let statusLeft = "";
  if (subMode === "matrix") {
    statusLeft = fmtStatusCount(lang, filteredMods.length, allModules.length, "modulesUnit");
    const rows = filteredMods.map(({ dom, mod, hasIssue }) => {
      const key = `bnd-mod::${mod.id}`;
      const isExp = uiState.expandedKey === key;
      const dotCls = (mod.violation_count || 0) > 0 ? "dot-err" : (hasIssue ? "dot-warn" : "dot-ok");
      const pack = uiState.contextCache[mod.id] || graph.capsules?.[mod.id];
      const maxPath = mod.max_file_path ? `${truncMiddle(mod.max_file_path, 12, 12)} (${mod.max_file_loc})` : "-";
      const expRow = isExp
        ? `<tr class="inline-expand-row"><td colspan="5">${buildContextPackHtml(pack, graph, lang, canMutate)}</td></tr>`
        : "";
      return `<tr class="data-row" data-expand-key="${escHtml(key)}" data-context-q="${escHtml(mod.id)}" data-expanded="${isExp}">
        <td><strong>${escHtml(mod.title || mod.id)}</strong><div class="row-sub mono">${escHtml(mod.id)}</div><div class="row-sub">${escHtml(mod.promise || mod.summary || "")}</div></td>
        <td><span class="status-label"><span class="status-dot ${dotCls}"></span>${escHtml(trStage(lang, mod.stage))}</span></td>
        <td class="col-pri-3">${escHtml(dom.name)}</td>
        <td class="col-pri-2 num">${escHtml(`${fmtNum(mod.loc)} (${fmtNum(mod.max_file_loc || 0)}/${fmtNum(mod.max_loc || 500)})`)}<div class="row-sub mono-trunc" title="${escHtml(mod.max_file_path || "")}">${escHtml(maxPath)}</div></td>
        <td class="col-pri-2 num">${escHtml(`${mod.violation_count || 0} ${t(lang, "violationsUnit")} · ${mod.git_lag || 0} ${t(lang, "docLagUnit")}`)}</td>
      </tr>${expRow}`;
    }).join("");
    bodyHtml = filteredMods.length
      ? `<table class="data-table">
          <thead><tr>
            <th>${escHtml(t(lang, "colModName"))}${_colHintHtml(lang, "colHiddenMid1", "colHiddenNarrow3")}</th>
            <th>${escHtml(t(lang, "colModStage"))}</th>
            <th class="col-pri-3">${escHtml(t(lang, "colModDomain"))}</th>
            <th class="col-pri-2">${escHtml(t(lang, "colModLoc"))}</th>
            <th class="col-pri-2">${escHtml(t(lang, "colModDeps"))}</th>
          </tr></thead>
          <tbody>${rows}</tbody>
        </table>`
      : `<div class="empty-state"><div>${escHtml(t(lang, "emptyFiltered"))}</div><button type="button" class="btn-quiet" data-clear-filters="boundaries">${escHtml(t(lang, "clearFilters"))}</button></div>`;
  } else if (subMode === "map") {
    const focusDom = domains.find((d) => d.id === uiState.boundaryDomain);
    const hasDomIssue = (d) => (d.violations || []).length > 0 || (d.oversized_count || 0) > 0 || (d.max_git_lag || 0) > 0;
    const hasModIssue = (m) => (m.violation_count || 0) > 0 || (m.oversized_count || 0) > 0 || (m.git_lag || 0) > 0;
    let mapBody = "";
    if (focusDom) {
      const allDomMods = focusDom.modules || [];
      const shownMods = uiState.boundaryOnlyIssues ? allDomMods.filter(hasModIssue) : allDomMods;
      statusLeft = fmtStatusCount(lang, shownMods.length, allDomMods.length, "modulesUnit");
      mapBody = shownMods.length
        ? `<div class="diagram-box">${renderModuleMapSvg({ ...focusDom, modules: shownMods }, lang)}</div>`
        : `<div class="empty-state"><div>${escHtml(t(lang, "emptyFiltered"))}</div><button type="button" class="btn-quiet" data-clear-filters="boundaries">${escHtml(t(lang, "clearFilters"))}</button></div>`;
    } else {
      const shownDoms = uiState.boundaryOnlyIssues ? domains.filter(hasDomIssue) : domains;
      statusLeft = fmtStatusCount(lang, shownDoms.length, domains.length, "domainsUnit");
      mapBody = shownDoms.length
        ? `<div class="diagram-box">${renderDomainMapSvg(shownDoms, graph.domain_edges || [], lang)}</div>`
        : `<div class="empty-state"><div>${escHtml(t(lang, "emptyFiltered"))}</div><button type="button" class="btn-quiet" data-clear-filters="boundaries">${escHtml(t(lang, "clearFilters"))}</button></div>`;
    }
    const backBtn = focusDom ? `<button type="button" class="btn-quiet" data-zoom-domain="">${escHtml(t(lang, "backAllDomains"))}</button>` : "";
    bodyHtml = `<div class="platter-section">
      <div class="section-head"><h2 class="section-title">${escHtml(focusDom ? focusDom.name : t(lang, "subModeBoundariesMap"))}</h2>${backBtn}</div>
      ${mapBody}
    </div>`;
  } else {
    const filteredFindings = findings.filter((f) => !uiState.boundaryDomain || f.domain === uiState.boundaryDomain || (!f.domain && String(f.path || "").includes(uiState.boundaryDomain)));
    statusLeft = fmtStatusCount(lang, filteredFindings.length, findings.length, "findingsUnit");
    const rows = filteredFindings.map((f, idx) => {
      const key = `bnd-fnd::${idx}`;
      const isExp = uiState.expandedKey === key;
      const dotCls = f.severity === "error" ? "dot-err" : "dot-warn";
      const rawPack = uiState.contextCache[f.path] || (f.module ? graph.capsules?.[f.module] : null);
      const hasModPack = Boolean(rawPack?.module?.id || rawPack?.task?.id);
      const locStr = f.line ? `${f.path}:${f.line}` : String(f.path || "");
      const shortLoc = `${truncMiddle(f.path, 14, 16)}${f.line ? `:${f.line}` : ""}`;
      const docNote = !hasModPack && rawPack?.document?.summary ? `<div class="row-sub muted">${escHtml(rawPack.document.summary)}</div>` : "";
      const fndCard = `<div class="inline-expand-card"><div class="copy-row"><span class="mono">${escHtml(locStr)}</span><button type="button" class="btn-quiet" data-copy-text="${escHtml(locStr)}">${escHtml(t(lang, "copyBtn"))}</button></div><div>${escHtml(f.message)}</div>${docNote}</div>`;
      const expRow = isExp
        ? `<tr class="inline-expand-row"><td colspan="3">${hasModPack ? buildContextPackHtml({ ...rawPack, finding_msg: f.message, finding_loc: locStr }, graph, lang, canMutate) : fndCard}</td></tr>`
        : "";
      return `<tr class="data-row" data-expand-key="${escHtml(key)}" data-context-q="${escHtml(f.path)}" data-expanded="${isExp}">
        <td><strong>${escHtml(trRuleId(lang, f.rule_id))}</strong><div class="row-sub">${escHtml(f.message)}</div></td>
        <td><span class="status-label"><span class="status-dot ${dotCls}"></span>${escHtml(trSeverity(lang, f.severity))}</span></td>
        <td class="col-pri-2 mono-trunc" title="${escHtml(locStr)}">${escHtml(shortLoc)}</td>
      </tr>${expRow}`;
    }).join("");
    bodyHtml = filteredFindings.length
      ? `<table class="data-table">
          <thead><tr>
            <th>${escHtml(t(lang, "findingColRule"))}${_colHintHtml(lang, "", "colHiddenMid1")}</th>
            <th>${escHtml(t(lang, "findingColSev"))}</th>
            <th class="col-pri-2">${escHtml(t(lang, "findingColLoc"))}</th>
          </tr></thead>
          <tbody>${rows}</tbody>
        </table>`
      : `<div class="empty-state"><div>${escHtml(findings.length === 0 ? t(lang, "findingsClean") : t(lang, "emptyFiltered"))}</div>${findings.length ? `<button type="button" class="btn-quiet" data-clear-filters="boundaries">${escHtml(t(lang, "clearFilters"))}</button>` : ""}</div>`;
  }

  return {
    html: `<div class="mgmt-shell">${filterHtml}<div class="platter mgmt-platter"><div class="platter-scroll" id="boundaries-scroll">${bodyHtml}</div></div></div>`,
    statusLeft,
    statusRight: `${t(lang, "provFact")} · ${fmtNum(graph.project?.total_loc || 0)} ${t(lang, "linesUnit")}`,
  };
}

export function renderRoadmapView(graph, uiState) {
  const lang = uiState.lang;
  const canMutate = !uiState.staticMode;
  const subMode = uiState.roadmapSubMode || "tasks";
  const domains = graph.domains || [];
  const provNodes = graph.provenance_nodes || [];

  const counts = { all: 0, blocked: 0, ready_for_check: 0, active: 0, todo: 0, done: 0 };
  const bucketOf = (st) => {
    if (st === "blocked") return "blocked";
    if (st === "ready_for_check") return "ready_for_check";
    if (st === "active" || st === "doing" || st === "in_progress") return "active";
    if (st === "done") return "done";
    return "todo";
  };
  const allRows = [];
  for (const dom of domains) {
    const msGroups = [
      ...(dom.now_milestones || []),
      ...(dom.next_milestones || []),
      ...(dom.later_milestones || []),
      ...((dom.done_milestones || []).filter((m) => uiState.roadmapArchived || !m.archived)),
    ];
    for (const ms of msGroups) {
      for (const tk of ms.tasks || []) {
        counts.all += 1;
        counts[bucketOf(tk.state)] += 1;
        allRows.push({ dom, ms, tk });
      }
    }
  }

  const filterHtml = `<div class="canvas-bar">
    <div class="canvas-row">
      <div class="filter-group">
        <button type="button" class="filter-btn${subMode === "tasks" ? " is-active" : ""}" data-rmode="tasks">${escHtml(t(lang, "subModeRoadmapTasks"))}</button>
        <button type="button" class="filter-btn${subMode === "trace" ? " is-active" : ""}" data-rmode="trace">${escHtml(t(lang, "subModeRoadmapTrace"))} (${provNodes.length})</button>
        <button type="button" class="filter-btn${subMode === "diff" ? " is-active" : ""}" data-rmode="diff">${escHtml(t(lang, "subModeRoadmapDiff"))}</button>
      </div>
      ${subMode === "tasks" ? `<div class="filter-group">
        <button type="button" class="filter-btn${!uiState.roadmapState ? " is-active" : ""}" data-rstate="">${escHtml(t(lang, "filterAllStates"))} ${counts.all}</button>
        <button type="button" class="filter-btn${uiState.roadmapState === "blocked" ? " is-active" : ""}" data-rstate="blocked">${escHtml(trTaskState(lang, "blocked"))} ${counts.blocked}</button>
        <button type="button" class="filter-btn${uiState.roadmapState === "ready_for_check" ? " is-active" : ""}" data-rstate="ready_for_check">${escHtml(trTaskState(lang, "ready_for_check"))} ${counts.ready_for_check}</button>
        <button type="button" class="filter-btn${uiState.roadmapState === "active" ? " is-active" : ""}" data-rstate="active">${escHtml(trTaskState(lang, "active"))} ${counts.active}</button>
        <button type="button" class="filter-btn${uiState.roadmapState === "todo" ? " is-active" : ""}" data-rstate="todo">${escHtml(t(lang, "filterTodoStates"))} ${counts.todo}</button>
        <button type="button" class="filter-btn${uiState.roadmapState === "done" ? " is-active" : ""}" data-rstate="done">${escHtml(trTaskState(lang, "done"))} ${counts.done}</button>
      </div>` : ""}
    </div>
    ${subMode === "tasks" ? `<div class="canvas-row">
      <button type="button" class="filter-btn${uiState.roadmapSwimlane ? " is-active" : ""}" data-action="toggle-swimlane">${escHtml(t(lang, "showSwimlane"))}</button>
      <label class="small-note"><input type="checkbox" id="chk-archived"${uiState.roadmapArchived ? " checked" : ""} /> ${escHtml(t(lang, "showCompletedArchived"))}</label>
    </div>` : ""}
  </div>`;

  let bodyHtml = "";
  let statusLeft = "";
  if (subMode === "tasks") {
    const visible = allRows.filter((r) => !uiState.roadmapState || bucketOf(r.tk.state) === uiState.roadmapState);
    statusLeft = fmtStatusCount(lang, visible.length, allRows.length, "tasksUnit");
    let firstParent = "";
    let lastDomId = "", lastMsId = "";
    const trs = [];
    for (const { dom, ms, tk } of visible) {
      const domCol = uiState.collapsedGroups?.has(`dom:${dom.id}`);
      if (dom.id !== lastDomId) {
        lastDomId = dom.id;
        lastMsId = "";
        if (!firstParent) firstParent = dom.name;
        trs.push(`<tr class="data-row" data-parent-path="${escHtml(dom.name)}" data-toggle-group="dom:${escHtml(dom.id)}"><td colspan="4"><button type="button" class="tree-group-toggle" aria-expanded="${!domCol}">${domCol ? "▸" : "▾"} <strong>${escHtml(dom.name)}</strong></button> <span class="small-note">${escHtml(trStage(lang, dom.stage))}</span></td></tr>`);
      }
      if (domCol) continue;
      const msCol = uiState.collapsedGroups?.has(`ms:${ms.id}`);
      const pPath = `${dom.name} > ${ms.name}`;
      if (ms.id !== lastMsId) {
        lastMsId = ms.id;
        if (!firstParent || firstParent === dom.name) firstParent = pPath;
        trs.push(`<tr class="data-row" data-parent-path="${escHtml(pPath)}" data-toggle-group="ms:${escHtml(ms.id)}"><td colspan="4" class="tree-cell-d1"><button type="button" class="tree-group-toggle" aria-expanded="${!msCol}">${msCol ? "▸" : "▾"} <strong>${escHtml(ms.id)}</strong> · ${escHtml(ms.name)}</button> <span class="small-note num">${ms.done_tasks}/${ms.total_tasks}</span></td></tr>`);
      }
      if (msCol) continue;
      if (firstParent === dom.name) firstParent = pPath;
      const key = `rm-tk::${tk.id}`;
      const isExp = uiState.expandedKey === key;
      const dotCls = tk.state === "blocked" ? "dot-err" : (tk.state === "ready_for_check" ? "dot-warn" : (tk.state === "done" ? "dot-ok" : "dot-idle"));
      const pack = uiState.contextCache[tk.id] || taskPackFromGraph(graph, dom, ms, tk);
      const depthNum = Math.min(4, Math.max(2, Number(tk.depth) || 2));
      const cellCls = `tree-cell-d${depthNum}`;
      const srcDec = [...(tk.sources || []), ...(tk.decisions || [])].join(", ") || (tk.specs || []).join(", ") || "-";
      trs.push(`<tr class="data-row" data-parent-path="${escHtml(pPath)}" data-expand-key="${escHtml(key)}" data-context-q="${escHtml(tk.id)}" data-expanded="${isExp}">
        <td class="${cellCls}"><strong>${escHtml(tk.id)}</strong> · ${escHtml(tk.title)}</td>
        <td><span class="status-label"><span class="status-dot ${dotCls}"></span>${escHtml(trTaskState(lang, tk.state))}</span></td>
        <td class="col-pri-2">${escHtml(trHumanCheck(lang, tk.human_check))}</td>
        <td class="col-pri-3 mono">${escHtml(srcDec)}</td>
      </tr>`);
      if (isExp) {
        trs.push(`<tr class="inline-expand-row"><td colspan="4">${buildContextPackHtml(pack, graph, lang, canMutate)}</td></tr>`);
      }
    }
    const swimHtml = uiState.roadmapSwimlane ? `<div class="platter-section"><div class="diagram-box">${renderTimelineSvg(graph, lang)}</div></div>` : "";
    bodyHtml = visible.length
      ? `${swimHtml}<div class="sticky-parent-bar" id="roadmap-sticky-parent">${escHtml(t(lang, "parentPathPrefix"))}${escHtml(firstParent)}</div>
        <table class="data-table tree-table">
          <thead><tr>
            <th>${escHtml(t(lang, "colTaskItem"))}${_colHintHtml(lang, "colHiddenMid1", "colHiddenNarrow2")}</th>
            <th>${escHtml(t(lang, "colTaskState"))}</th>
            <th class="col-pri-2">${escHtml(t(lang, "colTaskSignoff"))}</th>
            <th class="col-pri-3">${escHtml(t(lang, "colTaskSources"))}</th>
          </tr></thead>
          <tbody>${trs.join("")}</tbody>
        </table>`
      : `<div class="empty-state"><div>${escHtml(t(lang, "emptyFiltered"))}</div><button type="button" class="btn-quiet" data-clear-filters="roadmap">${escHtml(t(lang, "clearFilters"))}</button></div>`;
  } else if (subMode === "trace") {
    ({ statusLeft, bodyHtml } = renderRoadmapTraceHtml(provNodes, uiState, _colHintHtml));
  } else {
    ({ statusLeft, bodyHtml } = renderRoadmapDiffHtml(graph, uiState, _colHintHtml));
  }

  return {
    html: `<div class="mgmt-shell">${filterHtml}<div class="platter mgmt-platter"><div class="platter-scroll" id="roadmap-scroll">${bodyHtml}</div></div></div>`,
    statusLeft,
    statusRight: `${t(lang, "provFact")} · HEAD ${truncMiddle(graph.project?.head_sha || "-", 7, 5)}`,
  };
}

export function renderDocsView(graph, uiState) {
  const lang = uiState.lang;
  const docs = graph.repo_docs || [];
  const doc = docs.find((d) => d.path === uiState.selectedDocPath) || docs[0];
  const { proseHtml, sidenotes } = renderDocContentAndSidenotes(doc, graph, lang);
  const sidenoteHtml = sidenotes.map((n) =>
    `<div class="sidenote-item" data-note-id="${escHtml(n.id)}"${n.anchorSec ? ` data-anchor-sec="${escHtml(n.anchorSec)}"` : ""}>
      <div><strong>${escHtml(n.title)}</strong> <span class="tertiary">[${escHtml(n.tag)}]</span></div>
      <div>${escHtml(n.body)}</div>
      ${n.traceId ? `<button type="button" class="btn-quiet" data-jump-trace="${escHtml(n.traceId)}">${escHtml(n.traceId)}</button>` : ""}
      ${n.copyPath ? `<button type="button" class="btn-quiet" data-copy-text="${escHtml(n.copyPath)}">${escHtml(t(lang, "copyBtn"))}</button>` : ""}
    </div>`
  ).join("");

  return {
    html: `<div class="reading-shell">
      <div class="reading-sticky-path">
        <span>${escHtml(doc ? `${trCategory(lang, doc.category)} / ${doc.title}` : "-")}</span>
        <span class="mono-trunc num" title="${escHtml(doc?.path || "")}">${escHtml(doc ? `${truncMiddle(doc.path, 14, 16)} · ${fmtNum(doc.line_count)} ${t(lang, "linesUnit")}` : "")}</span>
      </div>
      <div class="reading-grid">
        <div class="platter reading-platter">${proseHtml || `<div class="empty-state">${escHtml(t(lang, "emptyFiltered"))}</div>`}</div>
        <aside class="sidenote-rail" aria-label="${escHtml(t(lang, "sidenoteTitle"))}">${sidenoteHtml}</aside>
      </div>
    </div>`,
    sidenotes,
    statusLeft: "",
    statusRight: "",
  };
}
