// Role: Zero-dependency Markdown, GFM table, alert callout, required-reading anchor, and heading-slug renderer.
// Out of scope: Network fetches, UI translations (i18n.js), Mermaid SVG math (diagrams.js), and DOM events (app.js).
// Anchors: spec=ui.perspective-web, docs/README.md#language-standard, SRC-007, SRC-013

import { escHtml } from "./i18n.js";

export function slugifyHeading(text) {
  return String(text ?? "")
    .replace(/[`*_~[\]()]/g, "")
    .trim()
    .toLowerCase()
    .replace(/[^\p{L}\p{N}_\s-]/gu, "")
    .replace(/\s/g, "-");
}

export function stripCommentsOutsideCode(rawLine, inComment = false) {
  const s = String(rawLine ?? "");
  let out = "", inTick = false, i = 0;
  if (inComment) {
    const end = s.indexOf("-->");
    if (end < 0) return { text: "", inComment: true };
    i = end + 3;
    inComment = false;
  }
  while (i < s.length) {
    if (s[i] === "`") { inTick = !inTick; out += s[i++]; continue; }
    if (!inTick && s.startsWith("<!--", i)) {
      const end = s.indexOf("-->", i + 4);
      if (end >= 0) { i = end + 3; continue; }
      return { text: out, inComment: true };
    }
    out += s[i++];
  }
  return { text: out, inComment: false };
}

function _mdInline(rawText, baseDocPath = "") {
  const codes = [];
  let clean = String(rawText ?? "").replace(/`([^`]+)`/g, (_m, code) => {
    codes.push(code);
    return `\x00C${codes.length - 1}\x00`;
  });
  clean = clean.replace(/<!--[\s\S]*?-->/g, "");
  let out = escHtml(clean);
  out = out.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_m, label, url) => {
    if (/^(https?:|mailto:|file:)/.test(url)) return `<a href="${url}" target="_blank" rel="noopener">${label}</a>`;
    if (url.startsWith("#")) return `<a href="${url}">${label}</a>`;
    if (/^(?![a-z][a-z0-9+.-]*:)[^\s"]+$/i.test(url)) return `<a href="#doc" data-doc-link="${url}" data-base-doc="${escHtml(baseDocPath)}">${label}</a>`;
    return label;
  });
  out = out.replace(/\*\*([\s\S]+?)\*\*/g, "<strong>$1</strong>");
  out = out.replace(/(^|[^*])\*([^*\n]+?)\*/g, "$1<em>$2</em>");
  out = out.replace(/\x00C(\d+)\x00/g, (_m, idx) => `<code>${escHtml(codes[Number(idx)] ?? "")}</code>`);
  return out;
}

export function renderMarkdownToHtml(markdown, renderMermaidFn, baseDocPath = "") {
  const lines = String(markdown ?? "").replace(/\r\n/g, "\n").split("\n");
  const out = [];
  let inCode = false, inComment = false, codeLang = "", codeBuf = [], secIdx = 0, currentSec = "";
  let listType = "", currentLi = null, tableRows = [], paraBuf = [], bqBuf = [];
  const secAttr = () => (currentSec ? ` data-sec-owner="${currentSec}"` : "");

  const flushPara = () => {
    if (paraBuf.length) {
      out.push(`<p${secAttr()}>${_mdInline(paraBuf.join(" "), baseDocPath)}</p>`);
      paraBuf = [];
    }
  };
  const flushBq = () => {
    if (!bqBuf.length) return;
    const cm = bqBuf[0].match(/^\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*(.*)$/i);
    if (cm) {
      const kind = cm[1].toLowerCase();
      const rest = [cm[2], ...bqBuf.slice(1)].filter(Boolean).map((l) => _mdInline(l, baseDocPath)).join("<br />");
      out.push(`<div class="callout-block callout-${kind}"${secAttr()}><div class="callout-title">${escHtml(cm[1].toUpperCase())}</div>${rest ? `<p>${rest}</p>` : ""}</div>`);
    } else {
      out.push(`<blockquote${secAttr()}>${bqBuf.map((l) => _mdInline(l, baseDocPath)).join("<br />")}</blockquote>`);
    }
    bqBuf = [];
  };
  const flushLi = () => {
    if (!currentLi) return;
    let html = _mdInline(currentLi.main.join(" "), baseDocPath);
    if (currentLi.subs?.items.length) {
      const subHtml = currentLi.subs.items.map((it) => `<li>${_mdInline(it.join(" "), baseDocPath)}</li>`).join("");
      html += `<${currentLi.subs.type}>${subHtml}</${currentLi.subs.type}>`;
    }
    out.push(`<li>${html}</li>`);
    currentLi = null;
  };
  const flushList = () => { flushLi(); if (listType) { out.push(`</${listType}>`); listType = ""; } };
  const flushTable = () => {
    if (!tableRows.length) return;
    const body = tableRows.slice(1).filter((r) => !r.every((c) => /^:?-{2,}:?$/.test(c)));
    const ths = tableRows[0].map((c) => `<th>${_mdInline(c, baseDocPath)}</th>`).join("");
    const trs = body.map((r) => `<tr>${r.map((c) => `<td>${_mdInline(c, baseDocPath)}</td>`).join("")}</tr>`).join("");
    out.push(`<div class="md-table-wrap"${secAttr()}><table class="md-table"><thead><tr>${ths}</tr></thead><tbody>${trs}</tbody></table></div>`);
    tableRows = [];
  };

  for (const raw of lines) {
    const fence = raw.match(/^(?:```|~~~)\s*([a-zA-Z0-9_-]*)\s*$/);
    if (fence) {
      flushPara(); flushBq(); flushList(); flushTable();
      if (!inCode) { inCode = true; codeLang = fence[1].toLowerCase(); codeBuf = []; }
      else {
        const block = codeBuf.join("\n");
        out.push(codeLang === "mermaid" && typeof renderMermaidFn === "function" ? `<div class="diagram-box"${secAttr()}>${renderMermaidFn(block, "")}</div>` : `<pre${secAttr()}><code>${escHtml(block)}</code></pre>`);
        inCode = false; codeLang = ""; codeBuf = [];
      }
      continue;
    }
    if (inCode) { codeBuf.push(raw); continue; }
    if (!inComment) {
      const reqMatch = raw.trim().match(/^<!--\s*required-reading:\s*([a-z0-9][a-z0-9-]*)\s*-->$/i);
      if (reqMatch) {
        flushPara(); flushBq(); flushList(); flushTable();
        out.push(`<span id="${escHtml(reqMatch[1])}" data-sec-slug="${escHtml(reqMatch[1])}" class="rule-anchor"${secAttr()}></span>`);
        continue;
      }
    }
    const cRes = stripCommentsOutsideCode(raw, inComment);
    inComment = cRes.inComment;
    const cleanRaw = cRes.text;
    const trimmed = cleanRaw.trim();
    if (!trimmed) { if (!inComment && !raw.trim()) { flushPara(); flushBq(); flushLi(); flushTable(); } continue; }
    if (trimmed.startsWith(">")) { flushPara(); flushList(); flushTable(); bqBuf.push(trimmed.slice(1).trim()); continue; }
    flushBq();
    if (trimmed.startsWith("|") && trimmed.endsWith("|")) { flushPara(); flushList(); tableRows.push(trimmed.slice(1, -1).split("|").map((s) => s.trim())); continue; }
    flushTable();
    const h = trimmed.match(/^(#{1,4})\s+(.+)$/);
    if (h) {
      flushPara(); flushList(); secIdx += 1;
      currentSec = `sec-${secIdx}`;
      const slug = slugifyHeading(h[2]);
      const alt = slug.replace(/-+/g, "-");
      const slugAttr = slug ? ` data-sec-slug="${escHtml(slug)}"` : "";
      const altAttr = alt && alt !== slug ? ` data-sec-alt="${escHtml(alt)}"` : "";
      out.push(`<h${h[1].length} id="${currentSec}" data-sec="${currentSec}"${slugAttr}${altAttr}>${_mdInline(h[2], baseDocPath)}</h${h[1].length}>`);
      continue;
    }
    if (/^-{3,}$/.test(trimmed)) { flushPara(); flushList(); out.push("<hr />"); continue; }
    if (listType && currentLi && /^\s{2,}(?:[-*]|\d+\.)\s+/.test(cleanRaw)) {
      const subOl = cleanRaw.match(/^\s{2,}\d+\.\s+(.+)$/), subUl = cleanRaw.match(/^\s{2,}[-*]\s+(.+)$/);
      const subType = subOl ? "ol" : "ul", subTxt = (subOl ? subOl[1] : subUl[1]).trim();
      if (!currentLi.subs || currentLi.subs.type !== subType) currentLi.subs = { type: subType, items: [] };
      currentLi.subs.items.push([subTxt]);
      continue;
    }
    const ul = !/^\s{2,}/.test(cleanRaw) ? trimmed.match(/^[-*]\s+(.+)$/) : null;
    if (ul) { flushPara(); flushLi(); if (listType !== "ul") { flushList(); listType = "ul"; out.push(`<ul${secAttr()}>`); } currentLi = { main: [ul[1]], subs: null }; continue; }
    const ol = !/^\s{2,}/.test(cleanRaw) ? trimmed.match(/^\d+\.\s+(.+)$/) : null;
    if (ol) { flushPara(); flushLi(); if (listType !== "ol") { flushList(); listType = "ol"; out.push(`<ol${secAttr()}>`); } currentLi = { main: [ol[1]], subs: null }; continue; }
    if (listType && currentLi) {
      if (currentLi.subs?.items.length) currentLi.subs.items[currentLi.subs.items.length - 1].push(trimmed);
      else currentLi.main.push(trimmed);
      continue;
    }
    flushList(); paraBuf.push(trimmed);
  }
  flushPara(); flushBq(); flushList(); flushTable();
  if (inCode && codeBuf.length) out.push(`<pre${secAttr()}><code>${escHtml(codeBuf.join("\n"))}</code></pre>`);
  return out.join("\n");
}

export function scrollDocToFragment(fragment) {
  if (!fragment || typeof document === "undefined") return;
  const raw = String(fragment).replace(/^#/, "");
  const norm = raw.toLowerCase().replace(/[^a-z0-9\u4e00-\u9fff]+/gi, "-").replace(/^-+|-+$/g, "");
  const escSel = (s) => (window.CSS?.escape ? window.CSS.escape(s) : s.replace(/"/g, ""));
  const el = document.getElementById(raw)
    || document.querySelector(`[data-sec-slug="${escSel(raw)}"]`)
    || document.querySelector(`[data-sec-alt="${escSel(raw)}"]`)
    || (norm ? (document.querySelector(`[data-sec-slug="${escSel(norm)}"]`) || document.querySelector(`[data-sec-alt="${escSel(norm)}"]`)) : null);
  if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
}

let _sidenoteSheet = null;
export function alignDocSidenotes(enabled) {
  const clearRules = () => { try { if (_sidenoteSheet) _sidenoteSheet.replaceSync(""); } catch { /* noop */ } };
  if (!enabled || typeof document === "undefined") { clearRules(); return; }
  const rail = document.querySelector(".reading-grid .sidenote-rail");
  const prose = document.querySelector(".reading-grid .reading-platter");
  if (!rail || !prose || typeof CSSStyleSheet === "undefined" || !("adoptedStyleSheets" in document)) { clearRules(); return; }
  const items = [...rail.querySelectorAll(".sidenote-item[data-note-id]")];
  if (!items.length) { clearRules(); return; }
  if (!_sidenoteSheet) {
    _sidenoteSheet = new CSSStyleSheet();
    document.adoptedStyleSheets = [...document.adoptedStyleSheets, _sidenoteSheet];
  }
  _sidenoteSheet.replaceSync("");
  const escSel = (s) => (window.CSS?.escape ? window.CSS.escape(s) : String(s).replace(/"/g, ""));
  const railTop = rail.getBoundingClientRect().top;
  const ordered = items.map((item, idx) => {
    const sec = item.dataset.anchorSec || "";
    const anchor = sec ? prose.querySelector(`[data-sec="${escSel(sec)}"], [data-sec-owner="${escSel(sec)}"]`) : null;
    const fallbackOff = item.dataset.noteId === "note-summary" ? 0 : 1e6 + idx;
    const topOff = anchor ? Math.max(0, anchor.getBoundingClientRect().top - railTop) : fallbackOff;
    return { item, idx, topOff };
  }).sort((a, b) => a.topOff - b.topOff || a.idx - b.idx);
  for (const ent of ordered) rail.appendChild(ent.item);
  let prevBottom = 0;
  const rules = [];
  ordered.forEach(({ item, topOff }, idx) => {
    const minY = idx === 0 ? 8 : prevBottom + 14;
    const clampedTop = Math.max(minY, Math.round(topOff));
    const marginTop = clampedTop - minY;
    const h = Math.ceil(item.getBoundingClientRect().height || 48);
    if (marginTop > 0) rules.push(`.sidenote-item[data-note-id="${escSel(item.dataset.noteId)}"] { margin-top: ${marginTop}px; }`);
    prevBottom = clampedTop + h;
  });
  _sidenoteSheet.replaceSync(rules.length ? `@container workspace (min-width: 1025px) { ${rules.join(" ")} }` : "");
}
