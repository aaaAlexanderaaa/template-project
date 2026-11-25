// Role: Pure HTML renderers for Roadmap Provenance Lineage & Git Diff + Test Verification sub-tabs.
// Out of scope: Overview/Boundaries/Docs views (views.js), network calls (app.js), and raw SVG math (charts.js).
// Anchors: spec=ui.perspective-web, docs/contracts/frontend-and-visual-discipline.md, SRC-016, SRC-017, SRC-022

import { escHtml, truncMiddle, fmtNum, fmtStatusCount, t, trDecisionStatus, trDiffDomain, trFileStatus } from "./i18n.js";
import { renderProvenanceSvg } from "./charts.js";

export function renderRoadmapTraceHtml(provNodes, uiState, colHintFn) {
  const lang = uiState.lang;
  const rows = provNodes.map((pn) => {
    const tr = pn.trace || {};
    const key = `rm-tr::${pn.id}`;
    const isExp = uiState.expandedKey === key;
    const isSrc = (tr.anchor_type || pn.kind) === "source";
    const dotCls = isSrc ? "dot-ok" : (tr.status === "superseded" ? "dot-idle" : "dot-warn");
    const statusTxt = isSrc ? t(lang, "provHuman") : trDecisionStatus(lang, tr.status || "current");
    const modButtons = (tr.modules || []).map((m) => {
      const mid = m.id || m;
      return `<button type="button" class="btn-quiet" data-open-module="${escHtml(mid)}">${escHtml(mid)}</button>`;
    }).join("");
    const expRow = isExp
      ? `<tr class="inline-expand-row"><td colspan="4"><div class="inline-expand-card">
          <div><strong>${escHtml(pn.id)}</strong>${tr.date ? ` · <span class="small-note">${escHtml(tr.date)}</span>` : ""}</div>
          ${tr.quote ? `<div class="quote-box">${escHtml(tr.quote)}</div>` : ""}
          <div class="diagram-box">${renderProvenanceSvg(pn, lang)}</div>
          <div class="link-row">
            ${tr.doc_path ? `<button type="button" class="btn-quiet" data-jump-doc="${escHtml(tr.doc_path)}">${escHtml(t(lang, "readDocBtn"))}</button>` : ""}
            ${modButtons}
          </div>
        </div></td></tr>`
      : "";
    const rawLinks = isSrc
      ? [...(tr.decisions || []).map((d) => d.id || d), ...(tr.open_or_pending_tasks || []).map((x) => x.id || x)].join(", ")
      : [
          ...(tr.sources || []).map((s) => s.id || s),
          ...(tr.modules || []).map((m) => m.id || m),
          ...(tr.open_or_pending_tasks || []).map((x) => x.id || x),
        ].join(", ");
    const taskTotal = (tr.verified_done_count || 0) + (tr.open_or_pending_tasks?.length || 0);
    const impactTxt = `${fmtNum((tr.modules || []).length)} ${t(lang, "modulesUnit")} · ${fmtNum(taskTotal)} ${t(lang, "tasksUnit")}`;
    return `<tr class="data-row" tabindex="0" aria-expanded="${isExp}" data-expand-key="${escHtml(key)}" data-expanded="${isExp}">
      <td title="${escHtml(pn.label)}"><strong>${escHtml(truncMiddle(pn.label, 38, 24))}</strong></td>
      <td><span class="status-label"><span class="status-dot ${dotCls}"></span>${escHtml(statusTxt)}</span></td>
      <td class="col-pri-2 num">${escHtml(impactTxt)}</td>
      <td class="col-pri-3 mono" title="${escHtml(rawLinks || "-")}">${escHtml(truncMiddle(rawLinks || "-", 36, 22))}</td>
    </tr>${expRow}`;
  }).join("");

  return {
    statusLeft: fmtStatusCount(lang, provNodes.length, provNodes.length, "lineageUnit"),
    bodyHtml: `<table class="data-table">
      <thead><tr>
        <th>${escHtml(t(lang, "srcTraceHead"))}${colHintFn(lang, "colHiddenMid1", "colHiddenNarrow2")}</th>
        <th>${escHtml(t(lang, "colTaskState"))}</th>
        <th class="col-pri-2">${escHtml(t(lang, "colTraceImpact"))}</th>
        <th class="col-pri-3">${escHtml(t(lang, "colTraceLinks"))}</th>
      </tr></thead>
      <tbody>${rows}</tbody>
    </table>`,
  };
}

export function renderRoadmapDiffHtml(graph, uiState, colHintFn) {
  const lang = uiState.lang;
  const refs = graph.project?.recent_refs || [];
  const commitSubj = Object.fromEntries((graph.project?.recent_commits || []).map((c) => [c.sha, c.subject || ""]));
  const diff = uiState.diff || graph.initial_diff || null;
  const files = [];
  for (const domGroup of diff?.domains || []) {
    const items = Array.isArray(domGroup.changed_files) ? domGroup.changed_files : (Array.isArray(domGroup.files) ? domGroup.files : []);
    for (const f of items) {
      const delta = f && typeof f === "object" && (f.added != null || f.deleted != null) ? `+${f.added || 0} / -${f.deleted || 0}` : "";
      files.push({ domain: trDiffDomain(lang, domGroup.domain), path: typeof f === "string" ? f : (f.path || ""), status: f.status || "modified", delta });
    }
  }

  const tr = graph.test_run;
  const testCard = tr && tr.command
    ? `<div class="platter-section">
        <div class="section-head">
          <h2 class="section-title">${escHtml(t(lang, "testRunTitle"))}</h2>
          <span class="status-label"><span class="status-dot ${Number(tr.exit_code) === 0 ? "dot-ok" : "dot-err"}"></span>${escHtml(`${t(lang, "testRunExit")}: ${tr.exit_code}`)}</span>
        </div>
        <div class="row-sub mono">${escHtml(tr.command)}${tr.head_sha ? ` · HEAD ${escHtml(truncMiddle(tr.head_sha, 7, 5))}` : ""}</div>
        ${tr.output_tail ? `<details class="diagram-src-toggle"><summary>${escHtml(t(lang, Number(tr.exit_code) === 0 ? "testPassed" : "testFailed"))}</summary><pre class="log-pre">${escHtml(tr.output_tail)}</pre></details>` : ""}
      </div><div class="platter-divider"></div>`
    : `<div class="platter-section"><div class="small-note">${escHtml(t(lang, "testRunEmpty"))}</div></div><div class="platter-divider"></div>`;

  const disAttr = uiState.staticMode ? ` disabled title="${escHtml(t(lang, "staticReadonlyTip"))}"` : "";
  const refSel = `<div class="platter-section">
    <div class="section-head">
      <label class="small-note">${escHtml(t(lang, "diffBaseLabel"))}
        <select class="input-ctl compact-select" id="diff-base-select"${disAttr}>
          <option value="">${escHtml(t(lang, "diffNoBase"))}</option>
          ${refs.map((r) => {
            const refVal = typeof r === "string" ? r : (r?.sha || "");
            const subj = (typeof r === "object" && r?.subject) || commitSubj[refVal] || "";
            const label = subj ? `${truncMiddle(refVal, 7, 5)} · ${subj}` : truncMiddle(refVal, 10, 6);
            return `<option value="${escHtml(refVal)}"${refVal === uiState.diffBase ? " selected" : ""}>${escHtml(label)}</option>`;
          }).join("")}
        </select>
      </label>
      <span class="small-note num">${escHtml(`${t(lang, "drawerCommits")}: ${graph.review?.commits_since_review || 0}`)}</span>
    </div>
    ${uiState.staticMode && !graph.initial_diff ? `<div class="small-note">${escHtml(t(lang, "diffStaticNotice"))}</div>` : ""}
  </div><div class="platter-divider"></div>`;

  const rows = files.map((f, i) => {
    const key = `rm-df::${i}`;
    const isExp = uiState.expandedKey === key;
    const stTxt = f.delta ? `${trFileStatus(lang, f.status)} · ${f.delta}` : trFileStatus(lang, f.status);
    const expRow = isExp
      ? `<tr class="inline-expand-row"><td colspan="3"><div class="inline-expand-card"><div class="copy-row"><span class="mono">${escHtml(f.path)}</span><button type="button" class="btn-quiet" data-copy-text="${escHtml(f.path)}">${escHtml(t(lang, "copyBtn"))}</button></div><div class="row-sub">${escHtml(f.domain)} · ${escHtml(stTxt)}</div></div></td></tr>`
      : "";
    return `<tr class="data-row" tabindex="0" aria-expanded="${isExp}" data-expand-key="${escHtml(key)}" data-expanded="${isExp}">
      <td class="mono-trunc" title="${escHtml(f.path)}">${escHtml(truncMiddle(f.path, 16, 18))}</td>
      <td>${escHtml(f.domain)}</td>
      <td class="col-pri-3">${escHtml(stTxt)}</td>
    </tr>${expRow}`;
  }).join("");

  const emptyMsg = uiState.staticMode && !diff ? t(lang, "diffStaticNotice") : t(lang, "diffClean");
  const diffBody = files.length
    ? `<table class="data-table"><thead><tr><th>${escHtml(t(lang, "diffHeadFile"))}${colHintFn(lang, "colHiddenMid1", "colHiddenMid1")}</th><th>${escHtml(t(lang, "diffHeadDomain"))}</th><th class="col-pri-3">${escHtml(t(lang, "diffHeadDelta"))}</th></tr></thead><tbody>${rows}</tbody></table>`
    : `<div class="empty-state"><div>${escHtml(emptyMsg)}</div></div>`;

  return {
    statusLeft: fmtStatusCount(lang, files.length, files.length, "changedFilesUnit"),
    bodyHtml: `${testCard}${refSel}${diffBody}`,
  };
}
