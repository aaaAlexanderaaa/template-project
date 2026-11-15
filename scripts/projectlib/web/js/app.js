// Role: Central client-side state manager, 4-view router, Stale-While-Revalidate fetch, drawer, and CSRF actions.
// Out of scope: Raw SVG geometry math (diagrams.js/charts.js) and HTML view string assembly (views.js).
// Anchors: spec=ui.perspective-web, ADR-002, ADR-005, SRC-005, SRC-010, SRC-013

import { escHtml, truncMiddle, t, trStage, trCategory } from "./i18n.js";
import { scrollDocToFragment, alignDocSidenotes } from "./markdown.js";
import { buildDocDrawerShellHtml, buildDocDrawerResultsHtml } from "./drawer.js";
import { renderOverviewView, renderBoundariesView, renderRoadmapView, renderDocsView } from "./views.js";

const CAT_ORDER = ["entry", "contract", "guide", "skill", "spec", "design", "decision", "template", "config"];

const uiState = {
  graph: null,
  diff: null,
  staticMode: false,
  lang: "zh",
  view: "overview",
  overviewDiagramIdx: 0,
  boundarySubMode: "matrix",
  boundaryDomain: "",
  boundaryOnlyIssues: false,
  roadmapSubMode: "tasks",
  roadmapState: "",
  roadmapArchived: false,
  roadmapSwimlane: false,
  selectedDocPath: "",
  docDrawerOpen: false,
  docDrawerTab: "tree",
  docQuery: "",
  docCategory: "all",
  expandedKey: "",
  collapsedGroups: new Set(),
  contextCache: {},
  diffBase: "",
  jumpHistory: [],
  noticeMsg: "",
  _statusRight: "",
  isRefreshing: false,
};

function resolveDocLinkPath(baseDoc, href) {
  const target = String(href || "").split("#")[0].split("?")[0].trim();
  if (!target) return "";
  if (target.startsWith("/")) return target.replace(/^\/+/, "");
  const parts = String(baseDoc || "").split("/");
  parts.pop();
  for (const seg of target.split("/")) {
    if (!seg || seg === ".") continue;
    if (seg === "..") { if (parts.length) parts.pop(); }
    else parts.push(seg);
  }
  return parts.join("/");
}

function getCsrfToken() {
  return uiState.graph?.csrf_token || document.querySelector('meta[name="project-csrf"]')?.content || "";
}

function syncTopbarAndChrome(statusLeft, statusRight) {
  const lang = uiState.lang;
  const g = uiState.graph;
  const p = g?.project || {};
  const archetype = uiState.view === "docs" ? "reading" : (uiState.view === "overview" ? "orientation" : "management");
  document.body.dataset.archetype = archetype;

  document.getElementById("brand-title").textContent = p.name || t(lang, "brandFallback");
  document.getElementById("brand-meta").textContent = `${trStage(lang, p.stage)} · ${uiState.staticMode ? t(lang, "statusStatic") : t(lang, "statusLive")}`;

  const tabSpecs = [
    ["overview", "tab-overview", "tabOverview"],
    ["boundaries", "tab-boundaries", "tabBoundaries"],
    ["roadmap", "tab-roadmap", "tabRoadmap"],
    ["docs", "tab-docs", "tabDocs"],
  ];
  const viewSelect = document.getElementById("view-select");
  tabSpecs.forEach(([vId, elId, key], idx) => {
    const label = t(lang, key);
    const btn = document.getElementById(elId);
    if (btn) {
      btn.textContent = label;
      btn.dataset.label = label;
      btn.classList.toggle("is-active", uiState.view === vId);
      btn.setAttribute("aria-selected", String(uiState.view === vId));
    }
    if (viewSelect?.options[idx]) {
      viewSelect.options[idx].textContent = label;
      viewSelect.options[idx].selected = uiState.view === vId;
    }
  });

  const drawerBtn = document.getElementById("btn-doc-drawer");
  const isDocs = uiState.view === "docs";
  drawerBtn.textContent = uiState.docDrawerOpen && isDocs ? t(lang, "btnCloseDrawer") : t(lang, "btnDocDrawer");
  drawerBtn.disabled = false;
  drawerBtn.title = isDocs ? "" : t(lang, "docDrawerOnlyDocsTip");

  const runBtn = document.getElementById("btn-run-tests");
  const markBtn = document.getElementById("btn-mark-reviewed");
  const langBtn = document.getElementById("btn-lang");
  runBtn.textContent = t(lang, "btnRunTests");
  markBtn.textContent = t(lang, "btnMarkReviewed");
  for (const btn of [runBtn, markBtn]) {
    btn.disabled = uiState.staticMode || uiState.isRefreshing;
    btn.title = uiState.staticMode ? t(lang, "staticReadonlyTip") : "";
  }
  langBtn.textContent = lang === "zh" ? "EN" : "中文";

  const statusbar = document.getElementById("statusbar");
  statusbar.hidden = archetype !== "management";
  uiState._statusRight = statusRight || "";
  if (archetype === "management") {
    document.getElementById("status-counts").textContent = statusLeft || "";
    document.getElementById("status-telemetry").textContent = uiState.noticeMsg || statusRight || "";
  }

  document.getElementById("topbar").dataset.loading = String(Boolean(uiState.isRefreshing));
  const jumpBtn = document.getElementById("jump-back-btn");
  if (uiState.jumpHistory.length > 0 && uiState.view === "docs") {
    const prev = uiState.jumpHistory[uiState.jumpHistory.length - 1];
    jumpBtn.textContent = `${t(lang, "btnJumpBack")} ${truncMiddle(prev.title, 10, 8)}`;
    jumpBtn.hidden = false;
  } else {
    jumpBtn.hidden = true;
  }
}

function renderMorePopover() {
  const lang = uiState.lang;
  const menu = document.getElementById("more-menu");
  const roAttr = uiState.staticMode || uiState.isRefreshing ? " disabled" : "";
  menu.innerHTML = `
    <button type="button" class="top-btn popover-item" data-action="run-tests"${roAttr}>${escHtml(t(lang, "btnRunTests"))}</button>
    <button type="button" class="top-btn popover-item" data-action="mark-reviewed"${roAttr}>${escHtml(t(lang, "btnMarkReviewed"))}</button>
    <button type="button" class="top-btn popover-item" data-action="toggle-lang">${escHtml(lang === "zh" ? "Switch to EN" : "切换中文")}</button>
  `;
}

function renderDocDrawerResults() {
  const resEl = document.getElementById("drawer-doc-results");
  if (!resEl || !uiState.graph) return;
  const prevTop = resEl.scrollTop;
  const { html, notesCount } = buildDocDrawerResultsHtml(uiState.graph, uiState);
  resEl.innerHTML = html;
  resEl.scrollTop = prevTop;
  const notesBtn = document.querySelector('#doc-drawer [data-dtab="notes"]');
  if (notesBtn) notesBtn.textContent = `${t(uiState.lang, "docDrawerNotes")} (${notesCount})`;
  const filterWrap = document.getElementById("drawer-filter-wrap");
  if (filterWrap) filterWrap.hidden = uiState.docDrawerTab === "notes";
}

function renderDocDrawerHtml() {
  const drawer = document.getElementById("doc-drawer");
  const showDrawer = uiState.view === "docs" && uiState.docDrawerOpen;
  drawer.hidden = !showDrawer;
  if (!showDrawer || !uiState.graph) return;
  const lang = uiState.lang;
  const docs = uiState.graph.repo_docs || [];
  if (!drawer.dataset.shellReady) {
    drawer.innerHTML = buildDocDrawerShellHtml();
    drawer.dataset.shellReady = "1";
  }
  const qMap = { tree: "docDrawerTree", search: "docDrawerSearch" };
  drawer.querySelectorAll("[data-dtab]").forEach((btn) => {
    const k = btn.dataset.dtab;
    if (qMap[k]) btn.textContent = t(lang, qMap[k]);
    btn.classList.toggle("is-active", uiState.docDrawerTab === k);
  });
  const closeBtn = drawer.querySelector('[data-action="close-doc-drawer"]');
  if (closeBtn) closeBtn.textContent = t(lang, "drawerClose");

  const searchEl = document.getElementById("drawer-doc-search");
  if (searchEl) {
    searchEl.placeholder = t(lang, "docSearchPlaceholder");
    if (document.activeElement !== searchEl && searchEl.value !== uiState.docQuery) searchEl.value = uiState.docQuery;
  }
  const catSel = document.getElementById("drawer-cat-select");
  const sig = `${lang}:${docs.length}`;
  if (catSel && catSel.dataset.sig !== sig) {
    catSel.dataset.sig = sig;
    catSel.innerHTML = `<option value="all">${escHtml(t(lang, "allCategories"))} (${docs.length})</option>` + CAT_ORDER.map((c) => {
      const n = docs.filter((d) => d.category === c).length;
      return n ? `<option value="${c}">${escHtml(trCategory(lang, c))} (${n})</option>` : "";
    }).join("");
  }
  if (catSel && catSel.value !== uiState.docCategory) catSel.value = uiState.docCategory;
  renderDocDrawerResults();
}

function renderActiveView() {
  if (!uiState.graph) return;
  const g = uiState.graph;
  if (!uiState.selectedDocPath && g.repo_docs?.length) uiState.selectedDocPath = g.repo_docs[0].path;

  const subKey = `${uiState.view}:${uiState.view === "boundaries" ? uiState.boundarySubMode : (uiState.view === "roadmap" ? uiState.roadmapSubMode : "")}`;
  const sameSurface = uiState._lastSurface === subKey;
  uiState._lastSurface = subKey;
  const prevWinY = window.scrollY || 0, prevBndTop = document.getElementById("boundaries-scroll")?.scrollTop || 0, prevRmTop = document.getElementById("roadmap-scroll")?.scrollTop || 0;

  for (const k of ["overview", "boundaries", "roadmap", "docs"]) {
    document.getElementById(`view-${k}`).hidden = k !== uiState.view;
  }

  let out = { html: "", statusLeft: "", statusRight: "" };
  if (uiState.view === "overview") out = renderOverviewView(g, uiState);
  else if (uiState.view === "boundaries") out = renderBoundariesView(g, uiState);
  else if (uiState.view === "roadmap") out = renderRoadmapView(g, uiState);
  else out = renderDocsView(g, uiState);

  document.getElementById(`view-${uiState.view}`).innerHTML = out.html;
  syncTopbarAndChrome(out.statusLeft, out.statusRight);
  renderMorePopover();
  renderDocDrawerHtml();
  bindScrollBreadcrumb();
  if (sameSurface) {
    const bnd = document.getElementById("boundaries-scroll"), rm = document.getElementById("roadmap-scroll");
    if (bnd) bnd.scrollTop = prevBndTop;
    if (rm) rm.scrollTop = prevRmTop;
    if ((uiState.view === "docs" || uiState.view === "overview") && prevWinY) window.scrollTo(0, prevWinY);
  }
  alignDocSidenotes(uiState.view === "docs");
}

function bindScrollBreadcrumb() {
  const scroller = document.getElementById("roadmap-scroll");
  const stickyEl = document.getElementById("roadmap-sticky-parent");
  if (!scroller || !stickyEl) return;
  scroller.addEventListener("scroll", () => {
    const rows = scroller.querySelectorAll("tr[data-parent-path]");
    const theadH = scroller.querySelector(".data-table thead")?.getBoundingClientRect().height || 0;
    const barBottom = stickyEl.getBoundingClientRect().bottom + theadH + 4;
    let current = "";
    for (const r of rows) {
      if (r.getBoundingClientRect().top <= barBottom) current = r.dataset.parentPath || "";
      else break;
    }
    if (current) stickyEl.textContent = `${t(uiState.lang, "parentPathPrefix")}${current}`;
  }, { passive: true });
}

async function fetchContextLazy(query) {
  if (!query || uiState.contextCache[query] || uiState.staticMode) return;
  uiState.isRefreshing = true;
  document.getElementById("topbar").dataset.loading = "true";
  try {
    const res = await fetch(`/api/context?q=${encodeURIComponent(query)}`);
    if (res.ok) uiState.contextCache[query] = await res.json();
  } catch { /* fallback to graph snapshot */ }
  uiState.isRefreshing = false;
  renderActiveView();
}

async function fetchDiff() {
  if (uiState.staticMode) return;
  const qs = uiState.diffBase ? `?base=${encodeURIComponent(uiState.diffBase)}&target=HEAD` : "";
  try {
    const res = await fetch(`/api/diff${qs}`);
    if (res.ok) uiState.diff = await res.json();
  } catch { /* optional */ }
}

let toastTimer = null;
function showNotice(msg, isOk = false, inlineId = "") {
  uiState.noticeMsg = msg || "";
  if (inlineId) {
    const el = document.getElementById(inlineId);
    if (el) { el.textContent = msg || ""; el.hidden = !msg; }
  }
  const tel = document.getElementById("status-telemetry");
  if (tel && msg) tel.textContent = msg;
  const toast = document.getElementById("action-toast");
  if (!toast) return;
  if (!msg) { toast.hidden = true; return; }
  toast.textContent = msg;
  toast.classList.toggle("is-ok", Boolean(isOk));
  toast.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    toast.hidden = true;
    uiState.noticeMsg = "";
    const curTel = document.getElementById("status-telemetry");
    if (curTel) curTel.textContent = uiState._statusRight || "";
  }, isOk ? 2800 : 5000);
}

async function postAction(url, body, onSuccess, inlineErrId = "") {
  if (uiState.staticMode) return;
  uiState.isRefreshing = true;
  renderActiveView();
  let failMsg = "";
  try {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-Project-Token": getCsrfToken() },
      body: JSON.stringify(body || {}),
    });
    const out = await res.json();
    if (!res.ok || (out?.ok === false && !out?.result)) throw new Error(out?.error || `HTTP ${res.status}`);
    if (onSuccess) onSuccess(out);
    const gr = await fetch("/api/graph");
    if (gr.ok) uiState.graph = await gr.json();
    await fetchDiff();
  } catch (err) {
    failMsg = err?.message || String(err);
  } finally {
    uiState.isRefreshing = false;
    renderActiveView();
    if (failMsg) showNotice(failMsg, false, inlineErrId);
  }
}

function jumpToDoc(targetPath, fragment = "") {
  const docs = uiState.graph?.repo_docs || [];
  const hit = docs.find((d) => d.path === targetPath);
  if (!hit) return;
  if (uiState.view === "docs" && uiState.selectedDocPath && uiState.selectedDocPath !== hit.path) {
    const cur = docs.find((d) => d.path === uiState.selectedDocPath);
    uiState.jumpHistory.push({ path: uiState.selectedDocPath, title: cur?.title || uiState.selectedDocPath, scrollY: window.scrollY });
  }
  uiState.selectedDocPath = hit.path;
  uiState.view = "docs";
  renderActiveView();
  if (fragment) scrollDocToFragment(fragment);
  else window.scrollTo({ top: 0 });
}

function bindEvents() {
  document.getElementById("view-select").addEventListener("change", (e) => { uiState.noticeMsg = ""; uiState.view = e.target.value; renderActiveView(); });
  document.addEventListener("change", async (e) => {
    if (e.target.id === "boundary-domain-select") { uiState.boundaryDomain = e.target.value; renderActiveView(); }
    else if (e.target.id === "drawer-cat-select") { uiState.docCategory = e.target.value; renderDocDrawerResults(); }
    else if (e.target.id === "chk-archived") { uiState.roadmapArchived = e.target.checked; renderActiveView(); }
    else if (e.target.id === "diff-base-select") { uiState.diffBase = e.target.value; await fetchDiff(); renderActiveView(); }
  });
  document.addEventListener("input", (e) => {
    if (e.target.id === "drawer-doc-search") { uiState.docQuery = e.target.value; renderDocDrawerResults(); }
  });
  document.addEventListener("click", async (e) => {
    const moreMenu = document.getElementById("more-menu");
    if (!e.target.closest(".more-wrap") && moreMenu && !moreMenu.hidden) {
      moreMenu.hidden = true;
      document.getElementById("btn-more")?.setAttribute("aria-expanded", "false");
    }
    const copyEl = e.target.closest("[data-copy-text]");
    if (copyEl) {
      navigator.clipboard?.writeText(copyEl.dataset.copyText || "").catch(() => {});
      copyEl.textContent = t(uiState.lang, "copiedBtn");
      return;
    }
    const tabBtn = e.target.closest("[data-view]");
    if (tabBtn) { uiState.noticeMsg = ""; uiState.view = tabBtn.dataset.view; renderActiveView(); return; }
    const actionEl = e.target.closest("[data-action]");
    if (actionEl) {
      const act = actionEl.dataset.action;
      if (act !== "toggle-more" && moreMenu && !moreMenu.hidden) {
        moreMenu.hidden = true;
        document.getElementById("btn-more")?.setAttribute("aria-expanded", "false");
      }
      if (act === "toggle-lang") { uiState.lang = uiState.lang === "zh" ? "en" : "zh"; renderActiveView(); }
      else if (act === "toggle-doc-drawer") {
        if (uiState.view !== "docs") { uiState.view = "docs"; uiState.docDrawerOpen = true; }
        else uiState.docDrawerOpen = !uiState.docDrawerOpen;
        renderActiveView();
      }
      else if (act === "close-doc-drawer") { uiState.docDrawerOpen = false; renderActiveView(); }
      else if (act === "toggle-more") {
        moreMenu.hidden = !moreMenu.hidden;
        actionEl.setAttribute("aria-expanded", String(!moreMenu.hidden));
      }
      else if (act === "toggle-only-issues") { uiState.boundaryOnlyIssues = !uiState.boundaryOnlyIssues; renderActiveView(); }
      else if (act === "toggle-swimlane") { uiState.roadmapSwimlane = !uiState.roadmapSwimlane; renderActiveView(); }
      else if (act === "run-tests") {
        await postAction("/api/tests/run", {}, (out) => {
          const code = out?.result?.exit_code ?? out?.exit_code ?? (out?.ok ? 0 : 1);
          showNotice(code === 0 ? t(uiState.lang, "testPassed") : t(uiState.lang, "testFailed"), code === 0);
        });
      }
      else if (act === "mark-reviewed") {
        if (typeof window.confirm === "function" && !window.confirm(t(uiState.lang, "confirmMarkReviewed"))) return;
        await postAction("/api/review/mark", {}, () => showNotice(t(uiState.lang, "btnMarkReviewed"), true));
      }
      return;
    }
    const clearEl = e.target.closest("[data-clear-filters]");
    if (clearEl) { uiState.boundaryDomain = ""; uiState.boundaryOnlyIssues = false; uiState.roadmapState = ""; uiState.expandedKey = ""; renderActiveView(); return; }
    const bmodeEl = e.target.closest("[data-bmode]");
    if (bmodeEl) { uiState.noticeMsg = ""; uiState.boundarySubMode = bmodeEl.dataset.bmode; uiState.expandedKey = ""; renderActiveView(); return; }
    const rmodeEl = e.target.closest("[data-rmode]");
    if (rmodeEl) { uiState.noticeMsg = ""; uiState.roadmapSubMode = rmodeEl.dataset.rmode; uiState.expandedKey = ""; renderActiveView(); return; }
    const rstateEl = e.target.closest("[data-rstate]");
    if (rstateEl) { uiState.roadmapState = rstateEl.dataset.rstate; renderActiveView(); return; }
    const dtabEl = e.target.closest("[data-dtab]");
    if (dtabEl) { uiState.docDrawerTab = dtabEl.dataset.dtab; renderDocDrawerHtml(); return; }
    const diagEl = e.target.closest("[data-diagram-idx]");
    if (diagEl) { uiState.overviewDiagramIdx = Number(diagEl.dataset.diagramIdx || 0); renderActiveView(); return; }
    const zoomEl = e.target.closest("[data-zoom-domain]");
    if (zoomEl) { uiState.boundaryDomain = zoomEl.dataset.zoomDomain; uiState.view = "boundaries"; uiState.boundarySubMode = "map"; renderActiveView(); return; }
    const domEl = e.target.closest("[data-open-domain]");
    if (domEl) { uiState.view = "boundaries"; uiState.boundarySubMode = "matrix"; uiState.boundaryDomain = domEl.dataset.openDomain || ""; uiState.expandedKey = ""; renderActiveView(); return; }
    const grpEl = e.target.closest("[data-toggle-group]");
    if (grpEl) {
      const gid = grpEl.dataset.toggleGroup;
      if (uiState.collapsedGroups.has(gid)) uiState.collapsedGroups.delete(gid);
      else uiState.collapsedGroups.add(gid);
      renderActiveView();
      return;
    }
    const approveEl = e.target.closest("[data-approve-task]");
    if (approveEl) { const aid = approveEl.dataset.approveTask; await postAction("/api/tasks/approve", { task_id: aid }, () => showNotice(t(uiState.lang, "btnApproveInline"), true), `inline-err-${aid}`); return; }
    const blockerEl = e.target.closest("[data-submit-blocker]");
    if (blockerEl) {
      const tid = blockerEl.dataset.submitBlocker;
      const picked = document.querySelector(`input[name="inline-blocker-${tid}"]:checked`)?.value || "";
      const custom = document.getElementById(`inline-custom-${tid}`)?.value?.trim() || "";
      const resolution = custom || picked;
      if (!resolution) { showNotice(t(uiState.lang, "blockerPickRequired"), false, `inline-err-${tid}`); return; }
      await postAction("/api/tasks/resolve-blocker", { task_id: tid, resolution }, () => showNotice(t(uiState.lang, "btnSubmitBlocker"), true), `inline-err-${tid}`);
      return;
    }
    const selDoc = e.target.closest("[data-select-doc],[data-jump-doc]");
    if (selDoc) { jumpToDoc(selDoc.dataset.selectDoc || selDoc.dataset.jumpDoc); return; }
    const linkEl = e.target.closest("[data-doc-link]");
    if (linkEl) {
      e.preventDefault();
      const rawHref = String(linkEl.dataset.docLink || "");
      const fragment = rawHref.includes("#") ? rawHref.split("#").slice(1).join("#") : "";
      const target = resolveDocLinkPath(linkEl.dataset.baseDoc || uiState.selectedDocPath, rawHref);
      const docs = uiState.graph?.repo_docs || [];
      const hit = docs.find((d) => d.path === target || d.path === `${target}/README.md`);
      if (hit) { jumpToDoc(hit.path, fragment); return; }
      const modEntry = Object.entries(uiState.graph?.capsules || {}).find(([, cap]) => (cap.telemetry?.files || []).some((f) => f.path === target));
      if (modEntry) {
        const [mid] = modEntry;
        uiState.view = "boundaries"; uiState.boundarySubMode = "matrix"; uiState.boundaryDomain = ""; uiState.boundaryOnlyIssues = false;
        uiState.expandedKey = `bnd-mod::${mid}`;
        renderActiveView();
        fetchContextLazy(mid);
        return;
      }
      showNotice(`${t(uiState.lang, "docMissingLink")} ${target}`, false);
      return;
    }
    const hashLink = e.target.closest('.md-prose a[href^="#"]');
    if (hashLink && !hashLink.dataset.docLink) {
      e.preventDefault();
      scrollDocToFragment(hashLink.getAttribute("href").slice(1));
      return;
    }
    const jumpBack = e.target.closest("#jump-back-btn");
    if (jumpBack && uiState.jumpHistory.length) {
      const prev = uiState.jumpHistory.pop();
      uiState.selectedDocPath = prev.path;
      renderActiveView();
      window.scrollTo({ top: prev.scrollY || 0 });
      return;
    }
    const secEl = e.target.closest("[data-jump-sec]");
    if (secEl) { scrollDocToFragment(secEl.dataset.jumpSec); return; }
    const noteEl = e.target.closest(".sidenote-item[data-anchor-sec]");
    if (noteEl && !e.target.closest("button,a")) { scrollDocToFragment(noteEl.dataset.anchorSec); return; }
    const doneEl = e.target.closest("[data-jump-done-tasks]");
    if (doneEl) { uiState.view = "roadmap"; uiState.roadmapSubMode = "tasks"; uiState.roadmapState = "done"; uiState.roadmapArchived = true; uiState.expandedKey = ""; renderActiveView(); return; }
    const trEl = e.target.closest("[data-jump-trace],[data-open-trace]");
    if (trEl) { uiState.view = "roadmap"; uiState.roadmapSubMode = "trace"; uiState.expandedKey = `rm-tr::${trEl.dataset.jumpTrace || trEl.dataset.openTrace}`; renderActiveView(); return; }
    const modEl = e.target.closest("[data-open-module]");
    if (modEl) { const mid = modEl.dataset.openModule; uiState.boundaryDomain = ""; uiState.boundaryOnlyIssues = false; uiState.view = "boundaries"; uiState.boundarySubMode = "matrix"; uiState.expandedKey = `bnd-mod::${mid}`; renderActiveView(); fetchContextLazy(mid); return; }
    const expRow = e.target.closest("[data-expand-key]");
    if (expRow) {
      const k = expRow.dataset.expandKey;
      uiState.expandedKey = uiState.expandedKey === k ? "" : k;
      renderActiveView();
      if (uiState.expandedKey === k && expRow.dataset.contextQ) fetchContextLazy(expRow.dataset.contextQ);
    }
  });
  const setLinked = (sec, active) => {
    if (!sec) return;
    document.querySelectorAll(".sidenote-item[data-anchor-sec]").forEach((el) => {
      if (el.dataset.anchorSec === sec) el.classList.toggle("is-linked", active);
    });
  };
  document.addEventListener("mouseover", (e) => { const h = e.target.closest?.(".md-prose [data-sec], .md-prose [data-sec-owner]"); if (h) setLinked(h.dataset.sec || h.dataset.secOwner, true); });
  document.addEventListener("mouseout", (e) => { const h = e.target.closest?.(".md-prose [data-sec], .md-prose [data-sec-owner]"); if (h) setLinked(h.dataset.sec || h.dataset.secOwner, false); });
  window.addEventListener("resize", () => { if (uiState.view === "docs") alignDocSidenotes(true); });
}

async function initApp() {
  bindEvents();
  const applyLang = (g) => (String(g?.project?.web_default_lang || g?.project?.language || "zh").startsWith("en") ? "en" : "zh");
  const isStatic = Boolean(window.__PERSPECTIVE_DATA__);
  uiState.graph = isStatic ? window.__PERSPECTIVE_DATA__ : await (await fetch("/api/graph")).json();
  uiState.staticMode = isStatic;
  uiState.lang = applyLang(uiState.graph);
  uiState.diffBase = "";
  uiState.diff = uiState.graph?.initial_diff || null;
  if (!isStatic) await fetchDiff();
  renderActiveView();
}

initApp();
