# Role: Tests calm-platter web workbench views, SVG renderers, standalone IIFE boot, and scale constraints.
# Out of scope: HTTP socket routes and CLI command integration (covered by test_project_cli_and_server.py).
# Anchors: spec=ui.perspective-web, SRC-005, SRC-007, SRC-010, SRC-013

from __future__ import annotations

import ast
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from projectlib.briefing_pack import serialize_perspective_payload  # noqa: E402
from projectlib.loader import load_project_graph  # noqa: E402
from projectlib.server import export_standalone_html  # noqa: E402


def _collect_python_rule_ids() -> set[str]:
    """Extract all static `rule_id` string literals emitted across scripts/projectlib."""
    rule_ids: set[str] = set()
    for py_file in sorted((SCRIPTS_DIR / "projectlib").glob("*.py")):
        tree = ast.parse(py_file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Dict):
                for k, v in zip(node.keys, node.values):
                    if isinstance(k, ast.Constant) and k.value == "rule_id" and isinstance(v, ast.Constant) and isinstance(v.value, str):
                        rule_ids.add(v.value)
            elif isinstance(node, ast.keyword) and node.arg == "rule_id" and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                rule_ids.add(node.value.value)
            elif isinstance(node, ast.Call):
                fn = node.func
                fname = fn.id if isinstance(fn, ast.Name) else (fn.attr if isinstance(fn, ast.Attribute) else "")
                if fname in ("emit", "ValidationFinding") and node.args:
                    arg0 = node.args[0]
                    if isinstance(arg0, ast.Constant) and isinstance(arg0.value, str):
                        rule_ids.add(arg0.value)
    return rule_ids


class WebWorkbenchTests(unittest.TestCase):
    def test_svg_chart_renderers_produce_clean_markup_on_real_graph(self) -> None:
        if not shutil.which("node"):
            self.skipTest("node binary not available")
        payload = serialize_perspective_payload(load_project_graph(ROOT))
        self.assertEqual(payload["project"]["web_default_lang"], "zh")
        self.assertIn("initial_diff", payload)
        js_src_dir = ROOT / "scripts" / "projectlib" / "web" / "js"
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "package.json").write_text('{"type": "module"}\n', encoding="utf-8")
            for js_file in js_src_dir.glob("*.js"):
                shutil.copy2(js_file, tmp_path / js_file.name)
            script = f"""
import {{ renderTimelineSvg, renderProvenanceSvg, renderDomainMapSvg, renderModuleMapSvg }} from "./charts.js";
import {{ renderMermaidSvg }} from "./diagrams.js";
import {{ renderDocReader, renderDirectoryDrawer, renderModuleDetail, renderTraceDetail }} from "./drawer.js";
import {{ trDiffDomain }} from "./i18n.js";

const data = {json.dumps(payload, ensure_ascii=False)};
const els = new Map();
globalThis.document = {{
  getElementById(id) {{
    if (!els.has(id)) els.set(id, {{ textContent: "", innerHTML: "", classList: {{ remove() {{}}, add() {{}} }}, focus() {{}} }});
    return els.get(id);
  }}
}};

const outputs = [];
const record = (label, text) => {{
  const s = String(text || "");
  for (const bad of ["[object Object]", "undefined", "NaN", "svg-edge-violation", "0 条越界"]) {{
    if (s.includes(bad)) throw new Error(label + " leaked " + bad + ": " + s.slice(0, 240));
  }}
  outputs.push(s);
}};

const tlZh = renderTimelineSvg(data, "zh");
record("timeline-zh", tlZh);
record("timeline-en", renderTimelineSvg(data, "en"));
if (!tlZh.includes("svg-box-focus")) throw new Error("Timeline missing svg-box-focus for current ADR");
if (trDiffDomain("zh", "Shared Docs & Config") !== "共享文档与配置") throw new Error("Shared Docs & Config zh mismatch");
const adr5Node = data.provenance_nodes.find((n) => n.id === "ADR-005");
if (!adr5Node) throw new Error("Missing ADR-005 provenance node");
const adr5Svg = renderProvenanceSvg(adr5Node, "zh");
const vbM = adr5Svg.match(/viewBox="0 0 (\\d+) (\\d+)"/);
if (!vbM || Number(vbM[2]) >= 900) throw new Error("ADR-005 provenance SVG too tall: " + (vbM && vbM[2]));
const doneNode = data.provenance_nodes.find((n) => (n.trace?.verified_done_count || 0) > 0);
if (!doneNode || !renderProvenanceSvg(doneNode, "zh").includes('data-jump-done-tasks="1"')) throw new Error("Provenance done summary box missing jump-done-tasks attribute");
const domZh = renderDomainMapSvg(data.domains, data.domain_edges, "zh");
const domEn = renderDomainMapSvg(data.domains, data.domain_edges, "en");
record("domainMap-zh", domZh);
record("domainMap-en", domEn);
if (!domZh.includes("svg-box-sage") || !domZh.includes("<marker") || !domZh.includes("marker-end=") || !domEn.includes("lines")) {{
  throw new Error("Domain map missing sage highlight, arrows, or lines LOC");
}}
for (const d of data.domains) {{
  const locStr = String(d.loc || 0);
  if (!domZh.includes(locStr) || !domEn.includes(locStr)) throw new Error("Domain map chopped LOC for " + d.id);
}}
if (domEn.includes(">Engineering Contract<") || domEn.includes(">Document &amp; Code Grap<")) {{
  throw new Error("Domain map broke English word mid-token: " + domEn);
}}
if (/>行<\\/text>/.test(domZh)) throw new Error("Domain map wrapped orphan 行: " + domZh);

for (const dom of data.domains) {{
  for (const lang of ["zh", "en"]) {{
    const modSvg = renderModuleMapSvg(dom, lang);
    record(`modMap:${{dom.id}}:${{lang}}`, modSvg);
    if (!modSvg.includes("<svg")) throw new Error("Module map missing <svg: " + dom.id);
    for (const m of dom.modules || []) {{
      if (!modSvg.includes(String(m.loc || 0))) throw new Error("Module map chopped LOC for " + m.id);
    }}
    if (dom.id === "discipline" && !modSvg.includes("skills")) throw new Error("Module map chopped discipline.guides-and-skills");
    if (dom.id === "graph-engine" && !modSvg.includes(" Q ")) throw new Error("graph-engine skip-column edge did not bypass middle column");
  }}
}}
for (const pn of data.provenance_nodes) {{
  const pSvg = renderProvenanceSvg(pn, "zh");
  record("provSvg:" + pn.id, pSvg);
  if (pn.id === "ADR-002" && !pSvg.includes("and work queues")) throw new Error("ADR-002 provenance dropped trailing text");
  renderTraceDetail(pn.id, data, "zh");
  record("traceDrawer:" + pn.id, els.get("drawer-body").innerHTML);
}}
for (const modId of Object.keys(data.capsules)) {{
  renderModuleDetail(modId, data, "zh");
  record("modDrawer:" + modId, els.get("drawer-body").innerHTML);
}}
const docsMap = new Map(data.repo_docs.map((d) => [d.path, d]));
for (const doc of data.repo_docs) {{
  renderDocReader(doc, "zh");
  const body = els.get("drawer-body").innerHTML;
  record("docReader:" + doc.path, body);
  if (doc.path.endsWith(".toml") && !body.includes('<pre class="log-pre"><code>')) {{
    throw new Error("TOML doc missing raw code block: " + doc.path);
  }}
  if (doc.path === "docs/README.md") {{
    if (body.includes("<!-- required-reading") || body.includes("**plain,")) throw new Error("docs/README.md leaked comment or broken bold");
    if (!body.includes('id="language-standard"')) throw new Error("docs/README.md missing required-reading fragment anchor");
    if (!body.includes("<strong>plain, direct English</strong>") || !body.includes("<ol") || !body.includes("<ul><li>")) {{
      throw new Error("docs/README.md missing nested list or bold formatting");
    }}
  }}
}}
for (const dir of data.directory_map) {{
  renderDirectoryDrawer(dir, docsMap, "zh");
  record("dirDrawer:" + dir.path, els.get("drawer-body").innerHTML);
}}

let seqChecked = false, archChecked = false, engineLayerChecked = false;
for (const m of [...(data.system_mermaids || []), ...data.domains.flatMap((d) => d.mermaids || [])]) {{
  const mSvg = renderMermaidSvg(m.code, "zh");
  record("mermaid:" + m.source, mSvg);
  if (!mSvg.includes("<svg")) throw new Error("Mermaid missing <svg: " + m.source);
  if ((m.source || "").includes("exemplar-checkout.md")) {{
    seqChecked = true;
    if ((mSvg.match(/<line /g) || []).length !== 3 || !mSvg.includes("svg-edge-dashed")) throw new Error("Bad checkout sequence SVG");
  }}
  if ((m.source || "").includes("ARCHITECTURE.md") && m.code.includes("Review -->|Needs Product Choice| Owner")) {{
    archChecked = true;
    const ownerRect = mSvg.match(/<g><title>Owner Goal &amp; Verbatim Quotes \\(docs\\/sources\\.toml\\)<\\/title><rect x="([^"]+)" y="([^"]+)" width="([^"]+)" height="([^"]+)"/);
    const dashedPaths = [...mSvg.matchAll(/<path d="([^"]+)" class="svg-edge-dashed"/g)].map((x) => x[1]);
    if (!ownerRect || dashedPaths.length === 0) throw new Error("Missing Owner rect or dashed back-edge in ARCHITECTURE.md#1");
    const [rx] = ownerRect.slice(1).map(Number);
    const minX = Math.min(...dashedPaths.map((p) => Math.min(...[...p.matchAll(/[MLQ]\\s*(-?\\d+(?:\\.\\d+)?)\\s+(-?\\d+(?:\\.\\d+)?)/g)].map((x) => Number(x[1])))));
    if (minX >= rx) throw new Error("Back-edge did not route outside col-0 gutter");
  }}
  if ((m.source || "").includes("docs/specs/graph-engine/README.md") && m.code.includes("CLI --> Core")) {{
    engineLayerChecked = true;
    const packRect = mSvg.match(/<g><title>context_pack, briefing_pack, server &amp; toml_writer<\\/title><rect x="([^"]+)" y="([^"]+)" width="([^"]+)"/);
    if (!packRect) throw new Error("Missing Pack rect in graph-engine/README.md");
    const packRight = Number(packRect[1]) + Number(packRect[3]);
    const maxX = Math.max(...[...mSvg.matchAll(/[MLQ]\\s*(-?\\d+(?:\\.\\d+)?)\\s+(-?\\d+(?:\\.\\d+)?)/g)].map((x) => Number(x[1])));
    if (maxX <= packRight) throw new Error("CLI-->Core did not route outside Pack");
  }}
}}
if (!seqChecked || !archChecked || !engineLayerChecked) throw new Error("Expected Mermaid diagrams missing from payload");
console.log("SVG_OK:" + outputs.length);
"""
            (tmp_path / "verify.mjs").write_text(script, encoding="utf-8")
            proc = subprocess.run(["node", "verify.mjs"], cwd=tmp_path, capture_output=True, text=True, check=False)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("SVG_OK:", proc.stdout)

    def test_web_views_scale_bundle_and_calm_platter_constraints(self) -> None:
        web_dir = ROOT / "scripts" / "projectlib" / "web"
        css_files = sorted((web_dir / "styles").glob("*.css"))
        js_files = sorted((web_dir / "js").glob("*.js"))
        self.assertTrue(css_files and js_files)
        for cf in css_files:
            lines = cf.read_text(encoding="utf-8").splitlines()
            self.assertLessEqual(len(lines), 300, f"{cf.name} exceeds 300 lines ({len(lines)})")
        for jf in js_files:
            lines = jf.read_text(encoding="utf-8").splitlines()
            self.assertLessEqual(len(lines), 500, f"{jf.name} exceeds 500 lines ({len(lines)})")

        index_html = (web_dir / "index.html").read_text(encoding="utf-8")
        self.assertNotIn('style="', index_html)
        all_css = "\n".join(cf.read_text(encoding="utf-8") for cf in css_files)
        for req in ("--bg-canvas: #F5F5F7", "--bg-platter: #FFFFFF", "--topbar-height: 32px", "--statusbar-height: 28px", "@container workspace", "scrollbar-gutter: stable", "tabular-nums"):
            self.assertIn(req, all_css)

        stripped_css = re.sub(r"/\*.*?\*/", "", all_css, flags=re.S)
        for banned in (r"border-left:\s*[34]px", r"linear-gradient", r"#000000", r"translateY\(-"):
            self.assertIsNone(re.search(banned, stripped_css), f"Banned CSS rule matched: {banned}")
        for m in re.finditer(r"\.data-table\s*\{([^}]*)\}", stripped_css):
            self.assertNotIn("overflow-x: auto", m.group(1))

        if not shutil.which("node"):
            self.skipTest("node binary not available")

        rule_ids = sorted(_collect_python_rule_ids())
        self.assertGreaterEqual(len(rule_ids), 25)
        graph = load_project_graph(ROOT)
        payload = serialize_perspective_payload(graph)
        ge_dom = next(d for d in payload["domains"] if d["id"] == "graph-engine")
        self.assertTrue(ge_dom["non_goals"], f"Expected non-empty non_goals for graph-engine: {ge_dom}")
        from projectlib.context_pack import build_context_pack
        t204_pack = build_context_pack(graph, "T-204")
        t204_src_ids = [s["id"] for s in t204_pack["verbatim_sources"]]
        self.assertEqual(t204_src_ids[:2], ["SRC-012", "SRC-013"])
        self.assertEqual(payload["project"]["web_default_lang"], "zh")
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "package.json").write_text('{"type": "module"}\n', encoding="utf-8")
            for jf in js_files:
                shutil.copy2(jf, tmp_path / jf.name)

            snap_path = export_standalone_html(ROOT, tmp_path / "snap.html")
            snap_html = snap_path.read_text(encoding="utf-8")
            self.assertNotIn('style="', snap_html)
            self.assertNotIn("cdn.jsdelivr.net", snap_html)
            self.assertNotIn('<script type="module"', snap_html)
            script_match = re.findall(r"<script>\n?(.*?)\n?</script>", snap_html, flags=re.S)
            self.assertGreaterEqual(len(script_match), 2)
            iife_code = script_match[-1]

            base_state = {
                "lang": "zh", "view": "overview", "overviewDiagramIdx": 0, "boundarySubMode": "matrix",
                "boundaryDomain": "", "boundaryOnlyIssues": False, "roadmapSubMode": "tasks", "roadmapState": "",
                "roadmapArchived": False, "roadmapSwimlane": False, "selectedDocPath": "AGENTS.md",
                "docDrawerOpen": False, "docDrawerTab": "tree", "docQuery": "", "docCategory": "all",
                "expandedKey": "", "contextCache": {}, "diffBase": "", "jumpHistory": [], "noticeMsg": "",
                "isRefreshing": False, "staticMode": False,
            }
            verify_js = f"""
import vm from "node:vm";
import {{ trRuleId, trDiffDomain }} from "./i18n.js";
import {{ renderMarkdownToHtml }} from "./markdown.js";
import {{ extractMarkdownHeadings, renderDocContentAndSidenotes, buildDocDrawerResultsHtml, extractArchitectureHighlights, taskPackFromGraph }} from "./drawer.js";
import {{ renderOverviewView, renderBoundariesView, renderRoadmapView, renderDocsView }} from "./views.js";

const data = {json.dumps(payload, ensure_ascii=False)};
const baseState = {json.dumps(base_state, ensure_ascii=False)};
const allRuleIds = {json.dumps(rule_ids)};
const docPackFixture = {json.dumps(build_context_pack(graph, "docs/work.toml"), ensure_ascii=False)};

const archHigh = extractArchitectureHighlights(data.project.architecture_markdown);
if (archHigh.length !== 5 || archHigh.some((x) => !x.summary)) {{
  throw new Error("Expected 5 non-empty ARCHITECTURE.md highlights: " + JSON.stringify(archHigh));
}}
if (!renderMarkdownToHtml("Write `<!-- required-reading: task-context -->` here.", null, "docs/README.md").includes("required-reading: task-context")) {{
  throw new Error("Backticked HTML comment was stripped");
}}
const cmHtml = renderMarkdownToHtml("# Heading 1 <!-- hidden -->\\n\\nParagraph with <!-- mid\\nmulti --> text.", null, "docs/README.md");
const cmHeads = extractMarkdownHeadings("# Heading 1 <!-- hidden -->\\n\\nParagraph");
if (cmHeads[0]?.slug !== "heading-1" || cmHeads[0]?.text !== "Heading 1" || !cmHtml.includes('data-sec-slug="heading-1"') || cmHtml.includes("multi")) {{
  throw new Error("Inline/multiline comment mismatch: " + JSON.stringify(cmHeads) + " / " + cmHtml);
}}
const fndGraph = {{ ...data, findings: [{{ rule_id: "custom:no_direct_sql", severity: "error", path: "docs/work.toml", line: 0, message: "Bad work ref", module: "", domain: "" }}] }};
const fndOut = renderBoundariesView(fndGraph, {{ ...baseState, lang: "zh", boundarySubMode: "findings", expandedKey: "bnd-fnd::0", contextCache: {{ "docs/work.toml": docPackFixture }} }});
if (fndOut.html.includes("<strong></strong>") || fndOut.html.includes("docs/work.toml:0") || !fndOut.html.includes("Bad work ref") || fndOut.html.includes("custom:") || fndOut.html.includes("_sql")) {{
  throw new Error("Non-module finding expand regression: " + fndOut.html);
}}
const rmEntry = data.repo_docs.find((d) => d.path === "README.md");
if (!rmEntry || rmEntry.title.includes("`") || rmEntry.summary.includes("请查看 README_CN")) {{
  throw new Error("README metadata regression: " + JSON.stringify(rmEntry));
}}
const t204Ms = data.domains.flatMap((d) => d.now_milestones || []).find((m) => (m.tasks || []).some((t) => t.id === "T-204"));
const t204Obj = t204Ms?.tasks.find((t) => t.id === "T-204");
const t204Pack = taskPackFromGraph(data, data.domains.find((d) => d.id === "perspective-ui"), t204Ms, t204Obj);
if (t204Pack.verbatim_sources[0]?.id !== "SRC-012" || t204Pack.verbatim_sources[1]?.id !== "SRC-013") {{
  throw new Error("Expected taskPackFromGraph T-204 SRC-012/SRC-013 first");
}}

for (const rid of allRuleIds) {{
  for (const lang of ["zh", "en"]) {{
    const txt = trRuleId(lang, rid);
    if (!txt || txt.includes("_")) throw new Error(`trRuleId(${{lang}}, ${{rid}}) returned raw snake_case: ${{txt}}`);
  }}
}}

function checkOut(label, res, lang) {{
  const html = String(res?.html || "");
  for (const bad of ["[object Object]", "undefined", "NaN"]) {{
    if (html.includes(bad)) throw new Error(label + " leaked " + bad);
  }}
  const visible = html.replace(/<[^>]+>/g, " ");
  for (const rawKey of ["drawerMermaidRaw", "modulesUnit", "tasksUnit", "colTraceImpact", "colTraceLinks", "codeLocLabel", "docLocLabel", "subsystemsTitle", "showCompletedArchived", "docLagUnit", "testRunTitle"]) {{
    if (visible.includes(rawKey)) throw new Error(label + " leaked raw i18n key: " + rawKey);
  }}
  if (lang === "zh") {{
    for (const raw of ["ready_for_check", "not_required", "pending_owner_choice"]) {{
      if (visible.includes(raw)) throw new Error(label + " leaked raw enum in visible text: " + raw);
    }}
  }}
  return html;
}}

for (const lang of ["zh", "en"]) {{
  const ov = renderOverviewView(data, {{ ...baseState, lang, expandedKey: "ov-dir::docs" }});
  checkOut("overview:" + lang, ov, lang);
  for (const bm of ["matrix", "map", "findings"]) {{
    const out = renderBoundariesView(data, {{ ...baseState, lang, boundarySubMode: bm, expandedKey: bm === "matrix" ? "bnd-mod::ui.perspective-web" : "" }});
    checkOut("boundaries:" + bm + ":" + lang, out, lang);
    if (!out.statusLeft.includes("/")) throw new Error("Missing statusLeft ratio in boundaries:" + bm);
  }}
  for (const rm of ["tasks", "trace", "diff"]) {{
    const ek = rm === "tasks" ? "rm-tk::T-204" : (rm === "trace" ? "rm-tr::SRC-013" : "");
    const out = renderRoadmapView(data, {{ ...baseState, lang, roadmapSubMode: rm, expandedKey: ek }});
    checkOut("roadmap:" + rm + ":" + lang, out, lang);
    if (!out.statusLeft.includes("/")) throw new Error("Missing statusLeft ratio in roadmap:" + rm);
    if (rm === "tasks") {{
      const pills = [...out.html.matchAll(/data-rstate="([^"]*)"[^>]*>([^<]+)</g)].map((m) => [m[1], Number(m[2].trim().split(/\\s+/).pop())]);
      const allCnt = pills.find(([k]) => k === "")?.[1] || 0;
      const sum = pills.filter(([k]) => k !== "").reduce((a, [, v]) => a + v, 0);
      if (allCnt <= 0 || sum !== allCnt) throw new Error(`Filter pill sum mismatch: sum=${{sum}} all=${{allCnt}}`);
    }}
  }}
  const specDoc = renderDocsView(data, {{ ...baseState, lang, selectedDocPath: "docs/specs/graph-engine/README.md" }});
  checkOut("docs:" + lang, specDoc, lang);
  if (!specDoc.sidenotes || specDoc.sidenotes.length < 2) throw new Error("Missing rich sidenotes on spec doc");
  const modDoc = renderDocsView(data, {{ ...baseState, lang, selectedDocPath: "docs/specs/perspective-ui/context-pack.md" }});
  checkOut("docs-mod:" + lang, modDoc, lang);
  if (!modDoc.sidenotes || modDoc.sidenotes.length < 3) throw new Error("Missing rich sidenotes on module doc");
  const adrDocEntry = data.repo_docs.find((d) => d.path.includes("ADR-005"));
  if (!adrDocEntry) throw new Error("Missing ADR-005 doc entry");
  const adrDoc = renderDocsView(data, {{ ...baseState, lang, selectedDocPath: adrDocEntry.path }});
  checkOut("docs-adr:" + lang, adrDoc, lang);
  if (!adrDoc.sidenotes || !adrDoc.sidenotes.some((n) => n.id.includes("SRC-013"))) throw new Error("Missing SRC-013 sidenote on ADR-005");
  const htmlDoc = renderDocsView(data, {{ ...baseState, lang, selectedDocPath: "docs/design/frontend-design-options.html" }});
  checkOut("docs-html:" + lang, htmlDoc, lang);
  if (htmlDoc.html.includes("<!doctype") || htmlDoc.html.includes("<style>")) throw new Error("HTML doc leaked raw markup tags");
  const diffWithFiles = renderRoadmapView(data, {{
    ...baseState, lang, roadmapSubMode: "diff",
    diff: {{ domains: [{{ domain: "Shared Docs & Config", files: 1, changed_files: [{{ path: "README.md", added: 3, deleted: 1, status: "modified" }}] }}] }},
  }});
  checkOut("diff-files:" + lang, diffWithFiles, lang);
  if (lang === "zh" && !diffWithFiles.html.includes("共享文档与配置")) throw new Error("Diff view failed to translate Shared Docs & Config");
  const strNgGraph = {{ ...data, domains: data.domains.map((d) => ({{ ...d, non_goals: "String non-goal A; String non-goal B" }})) }};
  renderOverviewView(strNgGraph, {{ ...baseState, lang }});
  renderDocContentAndSidenotes(data.repo_docs.find((d) => d.path.includes("specs/")), strNgGraph, lang);
  const drawerTree = buildDocDrawerResultsHtml(data, {{ ...baseState, lang, docDrawerTab: "tree", selectedDocPath: "docs/README.md" }});
  if (drawerTree.html.indexOf("ctx-section") > drawerTree.html.indexOf("drawer-cat-group")) {{
    throw new Error("Drawer TOC should render before document category list");
  }}
}}

// Large-scale synthetic stress graph: 12 domains, 500 tasks across 4 levels/slots, 200 repo_docs
const scaleDomains = [];
let tkSeq = 1;
const slots = ["now_milestones", "next_milestones", "later_milestones", "done_milestones"];
for (let d = 1; d <= 12; d++) {{
  const domId = `dom-${{String(d).padStart(2, "0")}}`;
  const domObj = {{
    id: domId, name: `Subsystem ${{d}}`, stage: d <= 4 ? "stable" : (d <= 8 ? "usable" : "prototype"),
    promise: `Promise ${{d}}`, non_goals: "Out of scope A; Out of scope B", loc: d * 1200, file_count: d * 4,
    violations: d === 3 ? 1 : 0, oversized_files: 0, max_git_lag: d % 3,
    modules: [{{
      id: `${{domId}}.core`, title: `Core ${{d}}`, stage: "usable", summary: `Module ${{d}}`, promise: `Promise ${{d}}`,
      doc_path: `docs/specs/${{domId}}/README.md`, loc: 220, max_loc: 450, file_count: 3,
      depends_on: d > 1 ? [`dom-${{String(d - 1).padStart(2, "0")}}.core`] : [], violations: [],
      files: [{{ path: `src/${{domId}}/core.py`, lines: 180, max_lines: 450 }}],
    }}],
    mermaids: [], now_milestones: [], next_milestones: [], later_milestones: [], done_milestones: [],
  }};
  for (let s = 0; s < 3; s++) {{
    const msId = `M-${{d}}-${{s + 1}}`;
    const tasks = [];
    for (let k = 0; k < 14 && tkSeq <= 500; k++) {{
      const tid = `T-${{String(tkSeq).padStart(3, "0")}}`;
      tasks.push({{
        id: tid, title: `Scale Task ${{tid}}`, depth: (k % 3) + 2,
        state: k % 7 === 0 ? "blocked" : (k % 5 === 0 ? "ready_for_check" : "done"),
        human_check: k % 5 === 0 ? "pending" : "approved", specs: [`${{domId}}.core`], sources: ["SRC-001"], decisions: ["ADR-001"],
      }});
      tkSeq++;
    }}
    if (tasks.length) domObj[slots[s]].push({{ id: msId, name: `Milestone ${{msId}}`, done_tasks: tasks.length, total_tasks: tasks.length, tasks }});
  }}
  scaleDomains.push(domObj);
}}
while (tkSeq <= 500) {{
  const tid = `T-${{String(tkSeq).padStart(3, "0")}}`;
  scaleDomains[0].now_milestones[0].tasks.push({{ id: tid, title: `Extra ${{tid}}`, depth: 4, state: "active", human_check: "not_required", specs: ["dom-01.core"], sources: [], decisions: [] }});
  tkSeq++;
}}
const scaleDocs = Array.from({{ length: 200 }}, (_, i) => ({{
  path: `docs/specs/dom-${{String((i % 12) + 1).padStart(2, "0")}}/doc-${{i + 1}}.md`,
  title: `Scale Doc ${{i + 1}}`, category: "spec", summary: `Doc summary ${{i + 1}}`, line_count: 80 + (i % 60),
  owner_module: `dom-${{String((i % 12) + 1).padStart(2, "0")}}.core`, body_markdown: `# Heading ${{i + 1}}\\n\\nPlain paragraph ${{i + 1}}.`,
}}));
const scaleGraph = {{ ...data, domains: scaleDomains, domain_edges: [], repo_docs: scaleDocs }};
const rmScale = renderRoadmapView(scaleGraph, {{ ...baseState, lang: "zh" }});
if (!rmScale.statusLeft.includes("500 / 500") || !rmScale.statusLeft.includes("项任务") || !rmScale.html.includes("tree-cell-d4")) throw new Error("Scale roadmap check failed: " + rmScale.statusLeft);
renderBoundariesView(scaleGraph, {{ ...baseState, lang: "zh" }});
renderDocsView(scaleGraph, {{ ...baseState, lang: "zh", selectedDocPath: scaleDocs[199].path }});

const iifeSrc = {json.dumps(iife_code)};
const domMap = new Map();
const makeEl = (id = "") => ({{
  id, textContent: "", innerHTML: "", hidden: false, disabled: false, title: "", value: "", dataset: {{}},
  options: [{{}}, {{}}, {{}}, {{}}], style: {{}}, classList: {{ toggle() {{}}, add() {{}}, remove() {{}} }},
  setAttribute() {{}}, addEventListener() {{}}, querySelector() {{ return null; }}, querySelectorAll() {{ return []; }},
  closest() {{ return null; }}, getBoundingClientRect() {{ return {{ top: 0, bottom: 0, left: 0 }}; }},
}});
for (const eid of ["brand-title", "brand-meta", "tab-overview", "tab-boundaries", "tab-roadmap", "tab-docs", "view-select", "btn-doc-drawer", "btn-run-tests", "btn-mark-reviewed", "btn-lang", "btn-more", "more-menu", "topbar", "doc-drawer", "view-overview", "view-boundaries", "view-roadmap", "view-docs", "statusbar", "status-counts", "status-telemetry", "jump-back-btn"]) {{
  domMap.set(eid, makeEl(eid));
}}
const sandbox = {{
  window: {{ __PERSPECTIVE_DATA__: data, location: {{ reload() {{}} }}, scrollTo() {{}}, addEventListener() {{}} }},
  document: {{
    body: makeEl("body"), addEventListener() {{}},
    getElementById(id) {{ if (!domMap.has(id)) domMap.set(id, makeEl(id)); return domMap.get(id); }},
    querySelector(sel) {{ if (sel.includes("project-csrf")) return {{ content: "tok" }}; return null; }},
    querySelectorAll() {{ return []; }},
  }},
  navigator: {{ clipboard: {{ writeText: async () => {{}} }} }},
  console, setTimeout, clearTimeout,
}};
sandbox.window.window = sandbox.window;
vm.runInNewContext(iifeSrc, sandbox);
if (!domMap.get("btn-run-tests").disabled || !domMap.get("btn-mark-reviewed").disabled || domMap.get("btn-doc-drawer").disabled) {{
  throw new Error("Expected staticMode disabled-in-place run/mark and enabled doc drawer button");
}}
if (!domMap.get("view-overview").innerHTML.includes("platter")) throw new Error("IIFE boot did not render overview platter");
if (domMap.get("btn-lang").textContent !== "EN") throw new Error("Expected template-project default Chinese UI");
console.log("WEB_SCALE_OK");
"""
            (tmp_path / "verify_web.mjs").write_text(verify_js, encoding="utf-8")
            proc = subprocess.run(["node", "verify_web.mjs"], cwd=tmp_path, capture_output=True, text=True, check=False)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn("WEB_SCALE_OK", proc.stdout)


if __name__ == "__main__":
    unittest.main()
