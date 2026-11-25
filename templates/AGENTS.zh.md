# 项目协作规范

本仓库遵循工程纪律模板（当前 `discipline_version` 见 `docs-policy.toml`），用来守住平实表达、唯一真源、清晰边界、真实运行验收与负责人拍板权。

## 1. 优先级顺序

1. **数据安全与交付目标**：保护用户数据、凭据与破坏性边界，交付可实际运行的真实结果，不拿清单充当完工。
2. **统一用语与唯一真源**：每个核心概念只用一个名字，每项状态值、阈值或对外承诺只保留一个唯一权威源文件。
3. **先用平实直接的中文、写清边界与拆分样式**：本项目的文档、规格、决策记录、产品自身命令行输出与报错文案（遵循 `docs/README.md#language-standard`）直接说明对象是什么、怎么工作、解决什么问题（模板配套的 `scripts/*.py` 仓库检查工具提供中文状态概览与开发者诊断提示）；模块规格 `owns` 认领的每个源码与样式文件开头都写 `# Role:` 职责头注释；样式按底层变量与组件目录隔离。
4. **按成熟度与协作模式分级的真实验收**：根据域阶段（`prototype` 0->0.1、`usable` 0.1->1、`stable` 1->N）及 `docs-policy.toml` 中的 `[collaboration]` 模式（`interactive` 交互或受 `templates/charter.md` 约束的 `unattended` 无人值守）执行端到端验证。
5. **需求—决策—任务同步**：需求或方向变化时同步更新 `docs/sources.toml`、`docs/decisions/`、`docs/design/`、`docs/specs/` 与 `docs/work.toml`。

## 2. 写代码前的三视角判断与主动补全

1. **执行者视角**：分清哪些是 `docs/sources.toml` 与当前规格里已定约束、哪些仍待负责人决策；已定约束直接执行。
2. **协作者视角**：按设计稳定度控制节奏；`0->0.1` 原型先跑通关键路径，方向收敛后及时沉淀模块边界。
3. **架构师视角**：先查所属域阶段（`docs/specs/<领域>/README.md`，默认值在 `docs-policy.toml`）。当非专业架构背景的负责人用大白话提需求时，主动把运行/控制逻辑、唯一状态归属、异常处理和禁止耦合写进 `ARCHITECTURE.md` 与模块规格，不把模糊片段原样照抄成系统架构。

## 3. 按对象触发的强制动作

| 涉及对象或场景 | 必须执行的动作 |
|---|---|
| 任何人类或 AI 可读文本（文档、产品命令行与报错、界面文案） | 直接讲清对象是什么、怎么运行、解决什么问题；不造黑话、不混用冲突编号、不堆砌免责套话（见 `docs/README.md#language-standard`）。 |
| 系统与模块架构说明 | 必须写清五部分：定位与非目标、端到端运行/控制逻辑（`mermaid`）、清晰接口与禁止耦合、唯一状态真源与硬约束、模块入口与自动校验（见 `docs/contracts/architecture-and-modularity.md#decomposition-and-ownership`）。 |
| 跨内存/数据库/API/DOM/URL/配置的共享状态 | 指定唯一权威真源，其余视图由真源计算得到（见 `docs/contracts/architecture-and-modularity.md#single-source-of-state`）。 |
| 产品方向、交互流程或 UI 界面方案（`docs/design/`） | 做任何产品或界面设计前，先运行 `python3 scripts/read_rules.py prepare --concern frontend` 阅读规则。原则和可测量的 WCAG 2.2 AA 底线永远优先于风格偏好（随模板下发的默认风格是 calm-platter：浅灰底、单块白色内容面板）；做完写码前 `/grill` 并拿到负责人有记录的方案批准之前，不写界面代码。 |
| 为读者组织信息（文档结构、导航、界面内容、知识或参考内容） | 组织文档、界面或知识内容前，先运行 `python3 scripts/read_rules.py prepare --concern information` 阅读规则。从读者的任务出发，结论先行。 |
| 新增文件、源码或样式膨胀 | 新增或扩写文件前，先运行 `python3 scripts/read_rules.py prepare --concern architecture`（样式另加 `--concern css`）。规格 `owns` 认领的每个源码与样式文件开头写 `# Role:` 头注释；在超过 `docs-policy.toml` 的行数上限之前按职责拆分，不能靠把代码挤成更少的行。 |
| 影响项目方向的新要求、权衡决策或变更 | 先运行 `python3 scripts/read_rules.py prepare --concern lineage`。把负责人原话写入 `docs/sources.toml`；支撑跨模块决策的原话只写进该 ADR 的 `sources` 并填好 `affects`，不要再抄进模块规格（`check_docs.py` 会报出重复）。 |
| 任务执行、审查节奏或无人值守模式 | 先运行 `python3 scripts/read_rules.py prepare --concern verification`。完整交付并按领域阶段和 `[collaboration]` 模式做真实验证（`unattended` 不越出 `templates/charter.md`）；何时做 `/grill` 由负责人决定，agent 只提醒。 |
| 独立评审与整体验收 | 加载 `.agents/skills/grill/SKILL.md`，并运行 `python3 scripts/read_rules.py prepare --concern review`。评审方在没看过作者解释的全新上下文中工作，只报告发现，状态由负责人决定。 |
| 纪律接入或版本同步升级 | 先运行 `python3 scripts/read_rules.py prepare --concern onboarding`。升级用 `python3 <模板路径>/scripts/project.py init --target . --sync`，再按 `docs/contracts/adoption-and-synchronization.md` 里比当前版本新的升级说明处理。本仓库自有文件保持不动。 |

## 4. 防偷懒与防失真红线

- **必须走通真实执行路径与行为验收**：用真实命令行、服务或界面跑通检验，不只靠 mock 单元测试。
- **独立评审必须开放、不受作者解释影响且闭环**：禁止预先把评审员限死在局部代码清单里，禁止塞入作者辩解词，禁止跳过全局一致性/架构审查，禁止未送回原评审方复验就宣称闭环完成。
- **严禁把未批准设计当成默认同意**：在 `docs/work.toml` 明确标记 `blocked` 与待选方案，等负责人明确拍板后再动实现代码。
- **已授权任务一次交付到位**：完整完成实现、集成与校验，不半途甩出待办清单让负责人收尾。

## 5. 常用导航、身份确认与校验命令

- 修改不熟悉文件前加载上下文：`python3 scripts/project.py context <路径或编号>`
- 查看项目状态、目录分工与阻塞项：`python3 scripts/project.py status`（`python3 scripts/project.py serve` 以本地网页显示同样的信息）
- 评审手册、技能与记录单：`docs/guides/grill.md`、`.agents/skills/grill/SKILL.md`、`templates/independent-review.md`
- 确认 `docs-policy.toml` 中保留 `identity = "product"` 而非模板身份。
- 提交前运行测试与规范校验：

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/check_docs.py   # 项目稳定后在 CI 里加 --strict：提醒级问题也会让检查失败
```
