// Role: Plain Chinese/English UI copy, enum translators, middle truncation, and SVG label wrapping.
// Out of scope: Markdown-to-HTML parsing (markdown.js), SVG layout math (charts.js/diagrams.js), and DOM events (app.js).
// Anchors: spec=ui.perspective-web, docs/README.md#language-standard, SRC-007, SRC-010, SRC-013

export const I18N = {
  zh: {
    brandFallback: "项目全景",
    tabOverview: "导览",
    tabBoundaries: "架构与边界",
    tabRoadmap: "推进与溯源",
    tabDocs: "全库文档",
    btnDocDrawer: "文档目录",
    btnCloseDrawer: "收起目录",
    btnRunTests: "运行测试",
    btnMarkReviewed: "标记已评审",
    staticReadonlyTip: "离线快照模式只读，请运行 python3 scripts/project.py serve 操作写盘与测试",
    docDrawerOnlyDocsTip: "展开文档目录与全文检索抽屉",
    statusLive: "本地服务",
    statusStatic: "离线快照",
    actionNeededHead: "待负责人决定或验收",
    actionCalmNote: "当前没有阻塞问题或待确认验收项。",
    btnApproveInline: "确认验收通过",
    btnSubmitBlocker: "写入决定并恢复",
    blockerCustomLabel: "或填写新的文字决定（逐字写入 sources.toml）：",
    blockerPickRequired: "请先选择预设方案，或在下方填写具体决定。",
    overviewIntroTitle: "项目定位与端到端运行逻辑",
    starterDocsTitle: "新访客建议先读这几篇",
    dirTableTitle: "仓库目录分工（点击行展开文件清单）",
    colDirPath: "目录",
    colDirRole: "职责说明",
    colDirDomain: "归属业务域",
    colDirFiles: "文件 / 文档",
    colDirLoc: "代码与文档行数",
    colHiddenMid1: "已收起 1 列",
    colHiddenNarrow2: "已收起 2 列",
    colHiddenNarrow3: "已收起 3 列",
    subModeBoundariesMatrix: "模块边界表",
    subModeBoundariesMap: "依赖关系图",
    subModeBoundariesFindings: "自动检查明细",
    filterAllDomains: "全部子系统",
    filterOnlyIssues: "仅看异常",
    clearFilters: "清空筛选条件",
    emptyFiltered: "当前筛选条件下无匹配记录",
    colModName: "模块与职责",
    colModStage: "阶段 / 状态",
    colModLoc: "行数 / 上限",
    colModDeps: "越界与滞后",
    colModDomain: "所属子系统",
    findingColRule: "检查项与说明",
    findingColLoc: "所在文件",
    findingColSev: "级别",
    subModeRoadmapTasks: "路线图与任务",
    subModeRoadmapTrace: "需求与决策溯源",
    subModeRoadmapDiff: "提交对照与测试",
    filterAllStates: "全部状态",
    showSwimlane: "切换多域泳道图",
    parentPathPrefix: "当前位置：",
    colTaskItem: "子系统 / 里程碑 / 任务",
    colTaskState: "当前状态",
    colTaskSignoff: "验收",
    colTaskSources: "需求与决策",
    srcTraceHead: "需求原话与决策溯源表（点击行展开完整原话、ADR 与任务）",
    diffBaseLabel: "对比基线：",
    diffNoBase: "仅当前工作区改动",
    diffClean: "当前区间无文件变动。",
    diffHeadFile: "变动文件",
    diffHeadDomain: "归属域 / 模块",
    diffHeadDelta: "行数变化",
    ctxPart1: "1. 归属与对外承诺",
    ctxPart2: "2. 上游原话与关联决策",
    ctxPart3: "3. 物理实测数据与完整路径",
    ctxPart4: "4. 下一步确认与直达入口",
    ctxNoActionNeeded: "常规结构信息，当前无需负责人介入决定。",
    provHuman: "人类原话与审批",
    provAi: "AI 维护规格",
    provFact: "脚本实测事实",
    sidenoteTitle: "页边批注与溯源",
    sidenoteToggle: "查看批注与溯源",
    docDrawerTree: "目录树",
    docDrawerSearch: "全文检索",
    docDrawerNotes: "本文批注",
    docSearchPlaceholder: "搜索文档标题、路径或正文内容…",
    allCategories: "全部分类",
    btnJumpBack: "返回",
    copyBtn: "复制",
    copiedBtn: "已复制",
    readDocBtn: "打开文档",
    backAllDomains: "返回全项目关系图",
    filesUnit: "个文件",
    docsUnit: "篇文档",
    domainsUnit: "个子系统",
    linesUnit: "行",
    docLagUnit: "次提交滞后",
    violationsUnit: "条越界",
    noneText: "无",
    drawerClose: "关闭",
    drawerSources: "关联用户原话",
    drawerDecisions: "相关决策",
    drawerCommits: "近期提交记录",
    docMissingLink: "未在活跃索引中找到对应文件：",
    findingsClean: "严格校验通过：当前未发现断链、越界引用或套话。",
    testPassed: "全部测试通过",
    testFailed: "存在失败用例",
    drawerMermaidRaw: "查看图表源码",
    modulesUnit: "个模块",
    colTraceImpact: "影响对象与状态",
    colTraceLinks: "关联需求 / ADR / 任务",
    codeLocLabel: "代码行数",
    docLocLabel: "文档行数",
    subsystemsTitle: "子系统边界、设计依据与不做什么",
    showCompletedArchived: "已完成 / 已归档里程碑",
    templateGuideNote: "模板仓库导读：先通过下方 3–4 篇入门文档掌握结构，再用 project.py init 带走全套规则与模板。",
    dayZeroNote: "当前代码尚未声明正式模块规格，下表由目录扫描实时生成。",
    filterTodoStates: "待开始",
    drawerModules: "归属模块",
    drawerAffectedModules: "受影响模块",
    drawerNonGoals: "不做什么",
    tasksUnit: "项任务",
    testRunTitle: "最近一次本地测试执行记录",
    testRunExit: "退出码",
    diffStaticNotice: "离线快照仅展示生成瞬间的未提交改动；启动本地服务后可实时切换基线或重测。",
    archSummaryTitle: "全局架构主线（来自 ARCHITECTURE.md）",
    readArchBtn: "阅读 ARCHITECTURE.md 全文",
    docOutlineHead: "当前文档章节大纲",
    confirmMarkReviewed: "确认把当前状态记为最近一次独立评审基准吗？这会更新本地评审锚点并清零提交滞后提示。",
    statusShowingPrefix: "当前显示 ",
    findingsUnit: "条检查结果",
    lineageUnit: "个溯源节点",
    changedFilesUnit: "个变动文件",
    decisionsUnit: "项决策",
    sourcesUnit: "条原话",
    testRunEmpty: "尚未记录本地测试运行结果；在本地服务模式下点击顶部「运行测试」即可执行。",
  },
  en: {
    brandFallback: "Project Overview",
    tabOverview: "Overview",
    tabBoundaries: "Boundaries",
    tabRoadmap: "Roadmap",
    tabDocs: "Documents",
    btnDocDrawer: "Doc Index",
    btnCloseDrawer: "Hide Index",
    btnRunTests: "Run Tests",
    btnMarkReviewed: "Mark Reviewed",
    staticReadonlyTip: "Offline snapshot is read-only. Start python3 scripts/project.py serve for live writes.",
    docDrawerOnlyDocsTip: "Open document contents & search drawer",
    statusLive: "Local server",
    statusStatic: "Offline snapshot",
    actionNeededHead: "Owner Decisions & Sign-Offs Needed",
    actionCalmNote: "No blocked questions or pending sign-offs right now.",
    btnApproveInline: "Approve Outcome",
    btnSubmitBlocker: "Save Decision",
    blockerCustomLabel: "Or write a custom decision (stored verbatim in sources.toml):",
    blockerPickRequired: "Choose an option or enter a decision before submitting.",
    overviewIntroTitle: "Project Purpose & Runtime Flow",
    starterDocsTitle: "Recommended First Reads for Newcomers",
    dirTableTitle: "Directory Responsibilities (click any row to inspect docs)",
    colDirPath: "Directory",
    colDirRole: "Responsibility",
    colDirDomain: "Domain",
    colDirFiles: "Files / Docs",
    colDirLoc: "LOC",
    colHiddenMid1: "1 col hidden",
    colHiddenNarrow2: "2 cols hidden",
    colHiddenNarrow3: "3 cols hidden",
    subModeBoundariesMatrix: "Module Matrix",
    subModeBoundariesMap: "Dependency Map",
    subModeBoundariesFindings: "Check Findings",
    filterAllDomains: "All domains",
    filterOnlyIssues: "Issues only",
    clearFilters: "Clear filters",
    emptyFiltered: "No records match the current filters",
    colModName: "Module & Promise",
    colModStage: "Stage / Health",
    colModLoc: "LOC / Cap",
    colModDeps: "Violations & Lag",
    colModDomain: "Domain",
    findingColRule: "Finding",
    findingColLoc: "File",
    findingColSev: "Severity",
    subModeRoadmapTasks: "Roadmap & Tasks",
    subModeRoadmapTrace: "Lineage & ADRs",
    subModeRoadmapDiff: "Git Diff & Tests",
    filterAllStates: "All states",
    showSwimlane: "Toggle swimlane SVG",
    parentPathPrefix: "Scope: ",
    colTaskItem: "Domain / Milestone / Task",
    colTaskState: "Status",
    colTaskSignoff: "Sign-off",
    colTaskSources: "Sources & ADRs",
    srcTraceHead: "Verbatim Sources & Decisions (click row for full lineage)",
    diffBaseLabel: "Compare baseline:",
    diffNoBase: "Working tree changes",
    diffClean: "No modified files in this range.",
    diffHeadFile: "Changed File",
    diffHeadDomain: "Domain / Module",
    diffHeadDelta: "Line Delta",
    ctxPart1: "1. Ownership & Promise",
    ctxPart2: "2. Verbatim Quotes & Decisions",
    ctxPart3: "3. Measured Telemetry & Full Paths",
    ctxPart4: "4. Required Action & Jump Links",
    ctxNoActionNeeded: "Routine structural record; no owner decision required.",
    provHuman: "Human quote & approval",
    provAi: "AI-maintained spec",
    provFact: "Measured fact",
    sidenoteTitle: "Margin Notes & Provenance",
    sidenoteToggle: "Show margin notes",
    docDrawerTree: "Contents",
    docDrawerSearch: "Search",
    docDrawerNotes: "Page Notes",
    docSearchPlaceholder: "Search doc title, path, or body content…",
    allCategories: "All categories",
    btnJumpBack: "Back to",
    copyBtn: "Copy",
    copiedBtn: "Copied",
    readDocBtn: "Open Document",
    backAllDomains: "Back to all domains",
    filesUnit: "files",
    docsUnit: "docs",
    domainsUnit: "domains",
    linesUnit: "lines",
    docLagUnit: "commits lag",
    violationsUnit: "violations",
    noneText: "None",
    drawerClose: "Close",
    drawerSources: "Verbatim quotes",
    drawerDecisions: "Related ADRs",
    drawerCommits: "Recent commits",
    docMissingLink: "Document not found in active index:",
    findingsClean: "Strict validation passed cleanly.",
    testPassed: "All tests passed",
    testFailed: "Tests failed",
    drawerMermaidRaw: "View diagram source",
    modulesUnit: "modules",
    colTraceImpact: "Impact & Status",
    colTraceLinks: "Linked Sources / ADRs / Tasks",
    codeLocLabel: "Code lines",
    docLocLabel: "Doc lines",
    subsystemsTitle: "Subsystem Boundaries, Non-Goals & Decisions",
    showCompletedArchived: "Completed / Archived",
    templateGuideNote: "Discipline template guide: start with the 3–4 key docs below, then run project.py init in target repos.",
    dayZeroNote: "No formal module specs declared yet; rows below come from direct directory scanning.",
    filterTodoStates: "Planned / Todo",
    drawerModules: "Modules",
    drawerAffectedModules: "Affected Modules",
    drawerNonGoals: "Non-goals",
    tasksUnit: "tasks",
    testRunTitle: "Latest Local Test Run",
    testRunExit: "Exit code",
    diffStaticNotice: "Offline snapshot shows the dirty diff captured at export time; run local serve to compare refs live.",
    archSummaryTitle: "System Architecture Summary (from ARCHITECTURE.md)",
    readArchBtn: "Read ARCHITECTURE.md",
    docOutlineHead: "Current Document Outline",
    confirmMarkReviewed: "Record the current repository state as the latest independent review anchor? This resets review lag counters.",
    statusShowingPrefix: "Showing ",
    findingsUnit: "findings",
    lineageUnit: "lineage items",
    changedFilesUnit: "changed files",
    decisionsUnit: "ADRs",
    sourcesUnit: "SRCs",
    testRunEmpty: "No local test run recorded yet; click Run Tests in local server mode.",
  },
};

export function t(lang, key) {
  const table = I18N[lang] || I18N.zh;
  return table[key] ?? I18N.en[key] ?? key;
}

export function escHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

export function truncMiddle(text, head = 16, tail = 14) {
  const s = String(text ?? "");
  if (s.length <= head + tail + 3) return s;
  return `${s.slice(0, head)}...${s.slice(s.length - tail)}`;
}

export function fmtNum(val) {
  const n = Number(val);
  return Number.isFinite(n) ? n.toLocaleString("en-US") : "0";
}

export function fmtStatusCount(lang, shown, total, unitKey) {
  return `${t(lang, "statusShowingPrefix")}${fmtNum(shown)} / ${fmtNum(total)} ${t(lang, unitKey)}`;
}

export function wrapTextLines(text, maxChars = 22) {
  const str = String(text ?? "").trim();
  if (!str) return [""];
  const wOf = (s) => {
    let w = 0;
    for (const c of s) w += /[^\x00-\x7f]/.test(c) ? 1.85 : 1;
    return w;
  };
  const tokens = str.match(/[\x60A-Za-z0-9_.'’&+→<>(),:;/-]+|\s+|./gu) || [];
  const lines = [];
  let buf = "";
  const pushHard = (part) => {
    for (const ch of part) {
      if (buf && wOf(buf + ch) > maxChars) {
        lines.push(buf.trim());
        buf = ch === " " ? "" : ch;
      } else buf += ch;
    }
  };
  for (const tok of tokens) {
    if (/^\s+$/.test(tok)) { if (buf && !buf.endsWith(" ") && wOf(buf) + 1 <= maxChars) buf += " "; continue; }
    if (wOf(tok) > maxChars) {
      for (const sub of tok.match(/[^./_-]+[./_-]?/g) || [tok]) {
        if (buf && wOf(buf.trimEnd()) + wOf(sub) > maxChars) { lines.push(buf.trim()); buf = ""; }
        if (wOf(sub) > maxChars) pushHard(sub);
        else buf += sub;
      }
      continue;
    }
    if (buf && wOf(buf) + wOf(tok) > maxChars) { lines.push(buf.trim()); buf = tok; }
    else buf += tok;
  }
  if (buf.trim()) lines.push(buf.trim());
  return lines.length ? lines : [str];
}

export function trStage(lang, stage) {
  const m = { prototype: { zh: "原型探索期", en: "Prototype" }, usable: { zh: "可用建设期", en: "Usable" }, stable: { zh: "稳定维护期", en: "Stable" } };
  return m[stage]?.[lang] || stage || "";
}

export function trTaskState(lang, state) {
  const m = {
    done: { zh: "已完成", en: "Done" }, active: { zh: "推进中", en: "Active" }, doing: { zh: "推进中", en: "Active" },
    ready_for_check: { zh: "待人工验收", en: "Ready for check" }, blocked: { zh: "等待拍板", en: "Needs decision" }, todo: { zh: "计划中", en: "Planned" },
  };
  return m[state]?.[lang] || state || "";
}

export function trHumanCheck(lang, val) {
  const m = { approved: { zh: "已验收", en: "Approved" }, pending: { zh: "待验收", en: "Pending" }, not_required: { zh: "无需单独验收", en: "Not required" }, not_needed: { zh: "无需单独验收", en: "Not required" } };
  return m[val]?.[lang] || val || "";
}

export function trDecisionStatus(lang, status) {
  const m = { current: { zh: "现行有效", en: "Current" }, accepted: { zh: "现行有效", en: "Current" }, superseded: { zh: "已被替代", en: "Superseded" }, proposed: { zh: "提议中", en: "Proposed" } };
  return m[status]?.[lang] || status || "";
}

export function trCategory(lang, cat) {
  const m = {
    entry: { zh: "入口约定", en: "Entry Docs" }, contract: { zh: "工程契约", en: "Contracts" }, guide: { zh: "操作指南", en: "Guides" },
    skill: { zh: "工作技能", en: "Skills" }, spec: { zh: "模块规格", en: "Specs" }, design: { zh: "界面设计", en: "Design" },
    decision: { zh: "架构决策", en: "ADRs" }, template: { zh: "起步模板", en: "Templates" }, config: { zh: "规则配置", en: "Config" },
  };
  return m[cat]?.[lang] || cat || "";
}

export function trDiffDomain(lang, name) {
  if (name === "unclaimed_or_docs" || name === "Shared Docs & Config") return lang === "zh" ? "共享文档与配置" : "Shared Docs & Config";
  return name;
}

export function trSeverity(lang, sev) {
  const m = { error: { zh: "阻断错误", en: "Error" }, warn: { zh: "需关注", en: "Warning" }, warning: { zh: "需关注", en: "Warning" }, advisory: { zh: "建议核对", en: "Advisory" }, info: { zh: "提示", en: "Info" } };
  return m[sev]?.[lang] || sev || "";
}

export function trFileStatus(lang, status) {
  const m = { modified: { zh: "已修改", en: "Modified" }, added: { zh: "新增", en: "Added" }, deleted: { zh: "已删除", en: "Deleted" }, renamed: { zh: "重命名", en: "Renamed" }, untracked: { zh: "未跟踪", en: "Untracked" } };
  return m[status]?.[lang] || status || "";
}

export function trRuleId(lang, ruleId) {
  const m = {
    copied_checkout: { zh: "副本仓库尚未完成初始化切换", en: "Copied template checkout needs init" },
    unknown_source: { zh: "引用了未登记的用户原话编号", en: "Unknown source ID" },
    unknown_dependency: { zh: "声明了不存在的模块依赖", en: "Unknown module dependency" },
    unknown_supersedes: { zh: "替代了不存在的决策编号", en: "Unknown superseded ADR" },
    unknown_affect: { zh: "影响了不存在的模块", en: "Unknown affected module" },
    unknown_superseded_by: { zh: "指向了不存在的替代决策", en: "Unknown replacement ADR" },
    unknown_milestone_dep: { zh: "依赖了不存在的里程碑", en: "Unknown milestone dependency" },
    unknown_milestone: { zh: "任务归属里程碑不存在", en: "Unknown milestone ID" },
    unknown_spec: { zh: "关联了未定义的模块规格编号", en: "Unknown module spec ID" },
    unknown_task_specs: { zh: "任务关联了未定义的模块规格编号", en: "Task references unknown module spec ID" },
    unknown_decision: { zh: "关联了不存在的决策编号", en: "Unknown decision ID" },
    orphan_source: { zh: "存在未落地的用户原话", en: "Unlinked source quote" },
    broken_link: { zh: "文档链接指向无效目标", en: "Broken documentation link" },
    broken_fragment: { zh: "文档章节锚点不存在", en: "Missing heading anchor" },
    unclaimed_source: { zh: "源码未被任何模块认领", en: "Unclaimed source file" },
    ambiguous_ownership: { zh: "同一源码被多个模块认领", en: "Overlapping module ownership" },
    undeclared_import: { zh: "存在未声明的跨模块导入", en: "Undeclared cross-module import" },
    layer_violation: { zh: "违反模块分层依赖规则", en: "Layer dependency rule violation" },
    file_size_budget: { zh: "文件行数超出预算上限", en: "File exceeds line budget" },
    missing_role_header: { zh: "核心文件缺少职责头注释", en: "Missing Role header comment" },
    catchall_directory: { zh: "存在未明确分工的杂物目录名", en: "Catch-all directory name" },
    git_doc_lag: { zh: "代码改动后文档长期未同步", en: "Docs lag behind commits" },
    arch_manifest: { zh: "架构规则清单配置异常", en: "Invalid architecture-rules.toml manifest" },
    project_language_mismatch: { zh: "文档或界面未保持项目主语言", en: "Language mismatch with docs-policy" },
    startup_disclaimer: { zh: "正文中出现空洞免责套话", en: "Empty startup disclaimer phrasing" },
    plain_language_jargon: { zh: "正文中混入生造词或黑话", en: "Coined jargon in plain copy" },
    unresolved_placeholder: { zh: "存在未替换的占位符", en: "Unresolved template placeholder" },
    incomplete_spec_structure: { zh: "模块规格缺少五要素必备章节", en: "Spec missing required sections" },
    toml_syntax: { zh: "配置文件 TOML 语法错误", en: "TOML syntax error" },
    frontmatter: { zh: "文档头元数据格式错误", en: "Invalid frontmatter metadata" },
    source_id: { zh: "用户原话编号格式或重复异常", en: "Invalid or duplicate source ID" },
    duplicate_id: { zh: "同一编号在清单中重复出现", en: "Duplicate ID definition" },
    oversized_file: { zh: "文件行数超出预算上限", en: "Oversized code file" },
    missing_file_role: { zh: "缺少文件职责说明", en: "Missing file Role header" },
    import_boundary: { zh: "跨模块越界导入", en: "Cross-module boundary violation" },
    doc_lag: { zh: "文档同步滞后", en: "Documentation lag" },
  };
  const hit = m[ruleId]?.[lang];
  if (hit) return hit;
  const cleanRule = String(ruleId || "").replace(/^custom:/i, "").replace(/[-_:]+/g, " ").trim();
  return lang === "zh"
    ? (cleanRule ? `自定义架构规则（${cleanRule}）` : "自定义架构规则")
    : (cleanRule ? `Architecture rule: ${cleanRule}` : "Architecture rule");
}
