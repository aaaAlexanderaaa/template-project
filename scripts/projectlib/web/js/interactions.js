// Role: Document-level keyboard and hover listeners: Esc closes the more menu or doc drawer and returns focus,
// Enter/Space toggles focusable expandable rows, and hovering prose highlights the matching sidenotes.
// Out of scope: uiState ownership, click routing, and rendering (app.js); HTML string assembly (views.js).
// Anchors: spec=ui.perspective-web, ADR-007, SRC-026

const NATIVE_CONTROLS = "button,a,input,select,textarea,summary";
const PROSE_ANCHORS = ".md-prose [data-sec], .md-prose [data-sec-owner]";

function closeMoreMenuWithFocus() {
  const moreMenu = document.getElementById("more-menu");
  if (!moreMenu || moreMenu.hidden) return false;
  moreMenu.hidden = true;
  const btnMore = document.getElementById("btn-more");
  btnMore?.setAttribute("aria-expanded", "false");
  btnMore?.focus();
  return true;
}

function setSidenoteLinked(sec, active) {
  if (!sec) return;
  document.querySelectorAll(".sidenote-item[data-anchor-sec]").forEach((el) => {
    if (el.dataset.anchorSec === sec) el.classList.toggle("is-linked", active);
  });
}

export function bindKeyboardAndHover(uiState, { renderActiveView, toggleExpandRow }) {
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      if (closeMoreMenuWithFocus()) return;
      if (uiState.docDrawerOpen) {
        uiState.docDrawerOpen = false;
        renderActiveView();
        document.getElementById("btn-doc-drawer")?.focus();
      }
      return;
    }
    if (e.key !== "Enter" && e.key !== " ") return;
    const target = e.target;
    if (!target?.closest || target.closest(NATIVE_CONTROLS)) return;
    const expRow = target.closest("tr[data-expand-key]");
    if (expRow) {
      e.preventDefault();
      toggleExpandRow(expRow, true);
    }
  });
  const linkFrom = (e, active) => {
    const h = e.target.closest?.(PROSE_ANCHORS);
    if (h) setSidenoteLinked(h.dataset.sec || h.dataset.secOwner, active);
  };
  document.addEventListener("mouseover", (e) => linkFrom(e, true));
  document.addEventListener("mouseout", (e) => linkFrom(e, false));
}
