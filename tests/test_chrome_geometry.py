# Role: Real headless Chromium geometry, responsive breakpoint, 500-task scale, and live-mode DOM tests.
# Out of scope: Static HTML/regex unit tests (test_web_workbench.py) and raw HTTP auth unit tests (test_project_cli_and_server.py).

from __future__ import annotations

import json
import os
import re
import socket
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from projectlib.briefing_pack import serialize_perspective_payload  # noqa: E402
from projectlib.loader import load_project_graph  # noqa: E402
from projectlib.server import create_perspective_server, export_standalone_html  # noqa: E402

CHROME_CANDIDATES = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
)

PROBE_JS = r"""
<script>
(function(){
  const report = { errors: [], viewport: { w: window.innerWidth, h: window.innerHeight } };
  window.addEventListener("error", (e) => report.errors.push(String(e.message || e.error || e)));
  try {
    const rect = (el) => {
      if (!el) return null;
      const r = el.getBoundingClientRect();
      return { x: Math.round(r.left * 10) / 10, right: Math.round(r.right * 10) / 10, w: Math.round(r.width * 10) / 10, h: Math.round(r.height * 10) / 10, top: Math.round(r.top * 10) / 10 };
    };
    const click = (sel) => document.querySelector(sel)?.click();
    const snapTabs = () => ({
      topbar: rect(document.getElementById("topbar")),
      brand: rect(document.getElementById("brand-title")),
      center: rect(document.getElementById("view-tabs")),
      rightWrap: rect(document.querySelector(".topbar-right")),
      overview: rect(document.getElementById("tab-overview")),
      boundaries: rect(document.getElementById("tab-boundaries")),
      roadmap: rect(document.getElementById("tab-roadmap")),
      docs: rect(document.getElementById("tab-docs")),
      lang: rect(document.getElementById("btn-lang")),
    });
    report.tabs = {};
    report.views = {};
    for (const [name, sel] of [["overview", "#tab-overview"], ["boundaries", "#tab-boundaries"], ["roadmap", "#tab-roadmap"], ["docs", "#tab-docs"]]) {
      click(sel);
      report.tabs[name] = snapTabs();
      const vp = document.getElementById("view-" + name);
      const tbl = vp?.querySelector(".data-table");
      const pri2 = vp?.querySelector(".col-pri-2");
      const pri3 = vp?.querySelector(".col-pri-3");
      const scroller = vp?.querySelector(".platter-scroll");
      const sb = document.getElementById("statusbar");
      report.views[name] = {
        docOverflowX: document.documentElement.scrollWidth - window.innerWidth,
        bodyH: document.body.getBoundingClientRect().height,
        statusbarHidden: sb.hidden,
        statusbarRect: rect(sb),
        platterRect: rect(vp?.querySelector(".platter")),
        tableScrollOverflow: tbl ? tbl.scrollWidth - tbl.clientWidth : 0,
        scrollerCanScroll: scroller ? scroller.scrollHeight > scroller.clientHeight : false,
        pri2Display: pri2 ? getComputedStyle(pri2).display : null,
        pri3Display: pri3 ? getComputedStyle(pri3).display : null,
        statusCounts: document.getElementById("status-counts")?.textContent || "",
      };
      const firstExp = vp?.querySelector("tr.data-row[data-expand-key]");
      if (firstExp) {
        firstExp.click();
        const card = vp.querySelector(".inline-expand-card");
        report.views[name].expandedRowCountAfter = vp.querySelectorAll(".inline-expand-row").length;
        report.views[name].inlineCardMarginTop = card ? getComputedStyle(card).marginTop : null;
        report.views[name].inlineCardMarginBottom = card ? getComputedStyle(card).marginBottom : null;
        report.views[name].expDocOverflowX = document.documentElement.scrollWidth - window.innerWidth;
        report.views[name].cardOverflowX = card ? card.scrollWidth - card.clientWidth : 0;
        const tblExp = vp.querySelector(".data-table");
        report.views[name].expTableOverflow = tblExp ? tblExp.scrollWidth - tblExp.clientWidth : 0;
      }
      if (name === "roadmap") {
        const pills = [...vp.querySelectorAll("[data-rstate]")].map((b) => [b.dataset.rstate, Number((b.textContent || "").trim().split(/\s+/).pop() || 0)]);
        report.views.roadmap.filterSum = { all: pills.find(([k]) => k === "")?.[1] || 0, sum: pills.filter(([k]) => k !== "").reduce((a, [, v]) => a + v, 0) };
        report.views.roadmap.d2Pad = parseFloat(getComputedStyle(vp.querySelector(".tree-cell-d2") || vp).paddingLeft || "0");
        report.views.roadmap.d4Pad = vp.querySelector(".tree-cell-d4") ? parseFloat(getComputedStyle(vp.querySelector(".tree-cell-d4")).paddingLeft || "0") : null;
        click('[data-rmode="trace"]');
        click('tr[data-expand-key="rm-tr::ADR-005"]');
        report.views.roadmap.adr5SvgRect = rect(vp.querySelector(".inline-expand-row svg"));
        report.views.roadmap.traceDocOverflowX = document.documentElement.scrollWidth - window.innerWidth;
        const tblTr = vp.querySelector(".data-table");
        report.views.roadmap.traceTableOverflow = tblTr ? tblTr.scrollWidth - tblTr.clientWidth : 0;
        click('[data-rmode="tasks"]');
      }
      if (name === "docs") {
        click("#btn-doc-drawer");
        report.views.docs.drawerOpenAfterClick = !document.getElementById("doc-drawer").hidden;
        report.views.docs.sidenotes = [...vp.querySelectorAll(".sidenote-item")].map((n) => rect(n));
        const resHtml = document.getElementById("drawer-doc-results")?.innerHTML || "";
        report.views.docs.tocBeforeCats = resHtml.indexOf("ctx-section") <= resHtml.indexOf("drawer-cat-group");
        report.views.docs.selectedDocCountInDrawer = document.querySelectorAll("#doc-drawer [data-select-doc]").length;
        const searchInput = document.getElementById("drawer-doc-search");
        if (searchInput) {
          searchInput.focus();
          searchInput.value = "ADR";
          searchInput.dispatchEvent(new Event("input", { bubbles: true }));
          report.views.docs.activeElementAfterSearchInput = document.activeElement?.id || "";
          report.views.docs.filteredDocCount = document.querySelectorAll("#doc-drawer [data-select-doc]").length;
          searchInput.value = "";
          searchInput.dispatchEvent(new Event("input", { bubbles: true }));
        }
        const contractBtn = document.querySelector('#doc-drawer [data-select-doc="docs/contracts/architecture-and-modularity.md"]');
        if (contractBtn) {
          contractBtn.click();
          const sticky = vp.querySelector(".reading-sticky-path");
          report.views.docs.stickyOverflowX = sticky ? sticky.scrollWidth - sticky.clientWidth : null;
          report.views.docs.longDocOverflowX = document.documentElement.scrollWidth - window.innerWidth;
        }
        document.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape", bubbles: true }));
        report.views.docs.drawerClosedByEsc = document.getElementById("doc-drawer").hidden;
        report.views.docs.focusAfterEsc = document.activeElement?.id || "";
      }
    }
    click("#tab-boundaries");
    const kbRow = document.querySelector("#view-boundaries tr[data-expand-key]");
    if (kbRow) {
      const kbKey = kbRow.dataset.expandKey;
      kbRow.focus();
      kbRow.dispatchEvent(new KeyboardEvent("keydown", { key: "Enter", bubbles: true, cancelable: true }));
      const afterKb = document.querySelector(`#view-boundaries tr[data-expand-key="${kbKey}"]`);
      report.kbToggle = { expanded: afterKb?.dataset.expanded || "", focusedKey: document.activeElement?.dataset?.expandKey || "" };
    }
    click("#tab-overview");
    const beforeLang = snapTabs();
    click("#btn-lang");
    report.langToggle = { before: beforeLang, after: snapTabs() };
    report.enOverviewOverflowX = document.documentElement.scrollWidth - window.innerWidth;
    const cbEn = document.querySelector("#view-overview .canvas-bar");
    report.enCanvasOverflowX = cbEn ? cbEn.scrollWidth - cbEn.clientWidth : 0;
    click("#tab-overview");
    report.selectVisible = getComputedStyle(document.querySelector(".view-select-wrap")).display;
    report.navTabsDisplay = getComputedStyle(document.getElementById("view-tabs")).display;
    report.moreBtnDisplay = getComputedStyle(document.querySelector(".more-wrap")).display;
    report.inlineStyleCount = document.querySelectorAll("[style]").length;
  } catch (err) {
    report.errors.push(String(err && err.stack ? err.stack : err));
  }
  const out = document.createElement("pre");
  out.id = "chrome-probe-json";
  out.textContent = JSON.stringify(report);
  document.body.appendChild(out);
})();
</script>
"""


def _build_scale_payload(base_payload: dict) -> dict:
    domains, tk_seq = [], 1
    for d in range(1, 13):
        dom_id = f"dom-{d:02d}"
        dom_obj = {
            "id": dom_id, "name": f"Subsystem {d}", "stage": "stable" if d <= 4 else ("usable" if d <= 8 else "prototype"),
            "promise": f"Promise {d}", "loc": d * 1200, "file_count": d * 4, "violations": 1 if d == 3 else 0,
            "oversized_files": 0, "max_git_lag": d % 3,
            "modules": [{"id": f"{dom_id}.core", "title": f"Core {d}", "stage": "usable", "summary": f"Mod {d}", "promise": f"Promise {d}", "doc_path": f"docs/specs/{dom_id}/README.md", "loc": 220, "max_loc": 450, "file_count": 3, "depends_on": [f"dom-{d-1:02d}.core"] if d > 1 else [], "violations": [], "files": [{"path": f"src/{dom_id}/core.py", "lines": 180, "max_lines": 450}]}],
            "mermaids": [], "now_milestones": [], "next_milestones": [], "later_milestones": [], "done_milestones": [],
        }
        for s_idx, slot in enumerate(("now_milestones", "next_milestones", "later_milestones")):
            ms_id = f"M-{d}-{s_idx+1}"
            tasks = []
            for k in range(14):
                if tk_seq > 500:
                    break
                tid = f"T-{tk_seq:03d}"
                tasks.append({"id": tid, "title": f"L{(k % 4) + 1} Scale Task {tid}", "depth": (k % 3) + 2, "state": "blocked" if k % 7 == 0 else ("ready_for_check" if k % 5 == 0 else "done"), "human_check": "pending" if k % 5 == 0 else "approved", "specs": [f"{dom_id}.core"], "sources": ["SRC-001"], "decisions": ["ADR-001"]})
                tk_seq += 1
            if tasks:
                dom_obj[slot].append({"id": ms_id, "name": f"Milestone {ms_id}", "done_tasks": len(tasks), "total_tasks": len(tasks), "tasks": tasks})
        domains.append(dom_obj)
    while tk_seq <= 500:
        tid = f"T-{tk_seq:03d}"
        domains[0]["now_milestones"][0]["tasks"].append({"id": tid, "title": f"Extra {tid}", "depth": 4, "state": "active", "human_check": "not_required", "specs": ["dom-01.core"], "sources": [], "decisions": []})
        tk_seq += 1
    docs = [{"path": f"docs/specs/dom-{(i % 12) + 1:02d}/doc-{i+1}.md", "title": f"Scale Doc {i+1}", "category": "spec", "summary": f"Summary {i+1}", "line_count": 80 + (i % 60), "owner_module": f"dom-{(i % 12) + 1:02d}.core", "body_markdown": f"# Heading {i+1}\n\nParagraph {i+1}."} for i in range(200)]
    out = dict(base_payload)
    out["domains"], out["domain_edges"], out["repo_docs"] = domains, [], docs
    return out


class ChromeGeometryTests(unittest.TestCase):
    def _chrome_bin(self) -> str:
        for cand in CHROME_CANDIDATES:
            if Path(cand).is_file():
                return cand
        self.skipTest("Google Chrome binary not installed")
        return ""

    def _run_chrome(self, chrome: str, html_path: Path, width: int, height: int, work_dir: Path, tag: str) -> dict:
        ud = work_dir / f"ud_{tag}"
        proc = subprocess.run(
            [
                chrome,
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                f"--user-data-dir={ud}",
                f"--window-size={width},{height}",
                "--virtual-time-budget=3000",
                "--dump-dom",
                html_path.as_uri(),
            ],
            capture_output=True,
            text=True,
            timeout=25,
            check=False,
        )
        if proc.returncode != 0 and (proc.returncode == 21 or "bootstrap_check_in" in proc.stderr):
            self.skipTest("Headless Chrome Crashpad Mach lookup blocked inside nested sandbox")
        self.assertEqual(proc.returncode, 0, proc.stderr[-800:])
        m = re.search(r'<pre id="chrome-(?:probe|live)-json">(.*?)</pre>', proc.stdout, flags=re.S)
        self.assertIsNotNone(m, f"Missing Chrome probe output at width={width}")
        return json.loads(m.group(1))

    def test_chrome_responsive_geometry_scale_and_live_mode(self) -> None:
        chrome = self._chrome_bin()
        payload = serialize_perspective_payload(load_project_graph(ROOT))
        scale_json = json.dumps(_build_scale_payload(payload), ensure_ascii=False).replace("</", "<\\/")

        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            tmp_path = Path(tmp)
            snap_txt = export_standalone_html(ROOT, tmp_path / "real.html").read_text(encoding="utf-8")
            real_probe = tmp_path / "real_probe.html"
            real_probe.write_text(snap_txt.replace("</body>", PROBE_JS + "\n</body>"), encoding="utf-8")

            scale_txt = re.sub(
                r"window\.__PERSPECTIVE_DATA__\s*=\s*.*?</script>",
                lambda _m: f"window.__PERSPECTIVE_DATA__ = {scale_json};\n</script>",
                snap_txt,
                count=1,
                flags=re.S,
            )
            scale_probe = tmp_path / "scale_probe.html"
            scale_probe.write_text(scale_txt.replace("</body>", PROBE_JS + "\n</body>"), encoding="utf-8")

            for w, h in ((540, 900), (800, 900), (1024, 900), (1280, 900), (2560, 1200)):
                rep = self._run_chrome(chrome, real_probe, w, h, tmp_path, f"real_{w}")
                self.assertEqual(rep["errors"], [], f"JS errors at {w}: {rep['errors']}")
                self.assertEqual(rep["inlineStyleCount"], 0)
                self.assertEqual(rep["tabs"]["overview"]["topbar"]["h"], 32)
                for vn in ("overview", "boundaries", "roadmap", "docs"):
                    v = rep["views"][vn]
                    self.assertLessEqual(v["docOverflowX"], 1, f"Overflow at {w} in {vn}: {v}")
                    self.assertLessEqual(v["tableScrollOverflow"], 1, f"Table scroll at {w} in {vn}")
                    if v.get("expDocOverflowX") is not None:
                        self.assertLessEqual(v["expDocOverflowX"], 1, f"Expanded overflow at {w} in {vn}: {v}")
                        self.assertLessEqual(v["cardOverflowX"], 1, f"Expanded card overflow at {w} in {vn}: {v}")
                        self.assertLessEqual(v["expTableOverflow"], 1, f"Expanded table overflow at {w} in {vn}: {v}")
                    if vn in ("boundaries", "roadmap"):
                        self.assertFalse(v["statusbarHidden"])
                        self.assertEqual(v["statusbarRect"]["h"], 28)
                        self.assertLessEqual(v["bodyH"], h + 1)
                    else:
                        self.assertTrue(v["statusbarHidden"])
                self.assertLessEqual(rep["views"]["roadmap"]["traceDocOverflowX"], 1, f"Trace expand overflow at {w}: {rep['views']['roadmap']}")
                self.assertLessEqual(rep["views"]["roadmap"]["traceTableOverflow"], 1, f"Trace expand table overflow at {w}: {rep['views']['roadmap']}")
                self.assertLessEqual(rep["enOverviewOverflowX"], 1, f"EN overview overflow at {w}: {rep}")
                self.assertLessEqual(rep["enCanvasOverflowX"], 1, f"EN canvas-bar overflow at {w}: {rep}")
                self.assertIsNotNone(rep["views"]["docs"]["stickyOverflowX"])
                self.assertLessEqual(rep["views"]["docs"]["stickyOverflowX"], 1, f"Docs sticky path overflow at {w}: {rep['views']['docs']}")
                self.assertLessEqual(rep["views"]["docs"]["longDocOverflowX"], 1, f"Docs long doc overflow at {w}: {rep['views']['docs']}")
                fs = rep["views"]["roadmap"]["filterSum"]
                self.assertTrue(fs["all"] > 0 and fs["sum"] == fs["all"])
                if w == 540:
                    self.assertEqual(rep["navTabsDisplay"], "none")
                    self.assertNotEqual(rep["selectVisible"], "none")
                    self.assertNotEqual(rep["moreBtnDisplay"], "none")
                    self.assertEqual(rep["views"]["boundaries"]["pri2Display"], "none")
                    self.assertEqual(rep["views"]["boundaries"]["pri3Display"], "none")
                elif w in (800, 1024):
                    self.assertEqual(rep["views"]["boundaries"]["pri3Display"], "none")
                    if w == 800:
                        self.assertNotEqual(rep["views"]["boundaries"]["pri2Display"], "none")
                    self.assertNotEqual(rep["moreBtnDisplay"], "none")
                    ov = rep["tabs"]["overview"]
                    self.assertLessEqual(ov["brand"]["right"], ov["center"]["x"] + 1)
                    self.assertLessEqual(ov["center"]["right"], ov["rightWrap"]["x"] + 1)
                else:
                    self.assertNotEqual(rep["views"]["boundaries"]["pri2Display"], "none")
                    self.assertNotEqual(rep["views"]["boundaries"]["pri3Display"], "none")
                    base_ov = rep["tabs"]["overview"]
                    for vn in ("boundaries", "roadmap", "docs"):
                        for k in ("overview", "boundaries", "roadmap", "docs", "lang"):
                            self.assertLessEqual(abs(rep["tabs"][vn][k]["x"] - base_ov[k]["x"]), 0.5)
                    for k in ("overview", "boundaries", "roadmap", "docs", "lang"):
                        self.assertLessEqual(abs(rep["langToggle"]["after"][k]["x"] - rep["langToggle"]["before"][k]["x"]), 0.5)
                    notes = rep["views"]["docs"]["sidenotes"]
                    for i in range(1, len(notes)):
                        self.assertGreaterEqual(notes[i]["top"], notes[i - 1]["top"] + notes[i - 1]["h"] - 1)
                if w == 2560:
                    for vn in ("overview", "boundaries", "roadmap"):
                        pr = rep["views"][vn]["platterRect"]
                        self.assertLessEqual(pr["w"], 1200)
                        self.assertLessEqual(abs(pr["x"] - (2560 - pr["right"])), 4)
                self.assertEqual(rep["views"]["boundaries"]["expandedRowCountAfter"], 1)
                self.assertEqual(rep["views"]["boundaries"]["inlineCardMarginTop"], "12px")
                self.assertEqual(rep["views"]["boundaries"]["inlineCardMarginBottom"], "12px")
                self.assertTrue(rep["views"]["docs"]["drawerOpenAfterClick"])
                self.assertTrue(rep["views"]["docs"]["tocBeforeCats"])
                self.assertEqual(rep["views"]["docs"]["activeElementAfterSearchInput"], "drawer-doc-search")
                self.assertGreaterEqual(rep["views"]["docs"]["filteredDocCount"], 1)
                self.assertTrue(rep["views"]["docs"]["drawerClosedByEsc"])
                self.assertEqual(rep["views"]["docs"]["focusAfterEsc"], "btn-doc-drawer")
                self.assertEqual(rep["kbToggle"]["expanded"], "true")
                self.assertTrue(rep["kbToggle"]["focusedKey"])

            scale_rep = self._run_chrome(chrome, scale_probe, 1280, 900, tmp_path, "scale_1280")
            self.assertEqual(scale_rep["errors"], [])
            self.assertIn("500 / 500", scale_rep["views"]["roadmap"]["statusCounts"])
            self.assertGreater(scale_rep["views"]["roadmap"]["d4Pad"], scale_rep["views"]["roadmap"]["d2Pad"])
            self.assertTrue(scale_rep["views"]["roadmap"]["scrollerCanScroll"])
            self.assertEqual(scale_rep["views"]["docs"]["selectedDocCountInDrawer"], 200)

            # Live-mode fetch verification (socketpair HTTP API + button non-shift + toast)
            live_repo = tmp_path / "live_repo"
            subprocess.run([sys.executable, "-B", str(SCRIPTS_DIR / "project.py"), "init", "--target", str(live_repo), "--name", "Live Repo", "--lang", "en"], check=True, capture_output=True)
            for cmd in (["git", "init"], ["git", "config", "user.email", "t@e.com"], ["git", "config", "user.name", "T"], ["git", "add", "."], ["git", "commit", "-m", "init"]):
                subprocess.run(cmd, cwd=live_repo, check=True, capture_output=True)
            (live_repo / "README.md").write_text("# Live Repo\nModified.\n", encoding="utf-8")

            def _disp(srv, method: str, path: str, body=None, headers=None) -> str:
                hdrs = {"Host": "127.0.0.1", "Connection": "close", **(headers or {})}
                raw = json.dumps(body).encode("utf-8") if body is not None else b""
                if body is not None:
                    hdrs["Content-Type"] = "application/json"
                    hdrs["Content-Length"] = str(len(raw))
                req = f"{method} {path} HTTP/1.1\r\n" + "".join(f"{k}: {v}\r\n" for k, v in hdrs.items()) + "\r\n"
                c_s, s_s = socket.socketpair()
                t = threading.Thread(target=lambda: (srv.RequestHandlerClass(s_s, ("127.0.0.1", 0), srv), s_s.close()), daemon=True)
                t.start()
                c_s.sendall(req.encode("utf-8") + raw)
                chunks = []
                while ch := c_s.recv(65536):
                    chunks.append(ch)
                t.join(5)
                c_s.close()
                return b"".join(chunks).partition(b"\r\n\r\n")[2].decode("utf-8")

            srv = create_perspective_server(live_repo, host="127.0.0.1", port=0)
            try:
                g_txt = _disp(srv, "GET", "/api/graph")
                d_txt = _disp(srv, "GET", "/api/diff")
                tok = json.loads(g_txt)["csrf_token"]
                t_txt = _disp(srv, "POST", "/api/tests/run", {}, {"X-Project-Token": tok})
            finally:
                srv.server_close()

            live_snap = export_standalone_html(live_repo, tmp_path / "live_snap.html").read_text(encoding="utf-8")
            live_html = re.sub(r"<script>\s*window\.__PERSPECTIVE_DATA__\s*=.*?</script>", "", live_snap, count=1, flags=re.S)
            shim = f"""<meta name="project-csrf" content="{tok}" /><script>
window.__LIVE_API__={{graph:{g_txt},diff:{d_txt},tests:{t_txt}}};
window.fetch=(u)=>String(u||"").startsWith("/api/tests/run")
  ?new Promise(r=>setTimeout(()=>r(new Response(JSON.stringify(window.__LIVE_API__.tests),{{status:200}})),30))
  :Promise.resolve(new Response(JSON.stringify(String(u||"").startsWith("/api/diff")?window.__LIVE_API__.diff:window.__LIVE_API__.graph),{{status:200}}));
</script>"""
            live_js = r"""<script>(async function(){
  const rep={errors:[]};window.addEventListener("error",e=>rep.errors.push(String(e.message||e)));
  const sleep=ms=>new Promise(r=>setTimeout(r,ms));
  for(let i=0;i<40&&!document.querySelector("#view-overview .platter");i++)await sleep(20);
  document.getElementById("tab-roadmap").click();document.querySelector('[data-rmode="diff"]').click();
  rep.diffRows=document.querySelectorAll("#view-roadmap .data-row").length;
  const btn=document.getElementById("btn-run-tests"),w0=btn.getBoundingClientRect().width;btn.click();await sleep(10);
  rep.btnWidthShift=Math.abs(btn.getBoundingClientRect().width-w0);
  for(let i=0;i<60&&document.getElementById("action-toast").hidden;i++)await sleep(20);
  rep.toastHidden=document.getElementById("action-toast").hidden;
  const out=document.createElement("pre");out.id="chrome-live-json";out.textContent=JSON.stringify(rep);document.body.appendChild(out);
})();</script>"""
            live_file = tmp_path / "live.html"
            live_file.write_text(live_html.replace("</head>", shim + "\n</head>", 1).replace("</body>", live_js + "\n</body>", 1), encoding="utf-8")
            lrep = self._run_chrome(chrome, live_file, 1280, 900, tmp_path, "live_1280")
            self.assertEqual(lrep["errors"], [])
            self.assertGreaterEqual(lrep["diffRows"], 1)
            self.assertLessEqual(lrep["btnWidthShift"], 0.5)
            self.assertFalse(lrep["toastHidden"])


if __name__ == "__main__":
    unittest.main()
