# 项目协作规范

本仓库遵循工程纪律模板（`discipline_version = "2026.11"`），用来守住平实表达、唯一真源、清晰边界、真实运行验收与负责人拍板权。

## 1. 优先级顺序

1. **数据安全与交付目标**：保护用户数据、凭据与破坏性边界，交付可实际运行的真实结果，不拿清单充当完工。
2. **统一用语与唯一真源**：每个核心概念只用一个名字，每项状态值、阈值或对外承诺只保留一个唯一权威源文件。
3. **先用平实直接的中文、写清边界与拆分样式**：本项目的文档、规格、决策记录、产品自身命令行输出与报错文案（遵循 `docs/README.md#language-standard`）直接说明对象是什么、怎么工作、解决什么问题（模板配套的 `scripts/*.py` 仓库检查工具提供中文状态概览与开发者诊断提示）；核心源码保留 `# Role:` 职责头注释；样式按底层变量与组件目录隔离。
4. **按成熟度与协作模式分级的真实验收**：根据域阶段（`prototype` 0->0.1、`usable` 0.1->1、`stable` 1->N）及 `docs-policy.toml` 中的 `[collaboration]` 模式（`interactive` 交互或受 `templates/charter.md` 约束的 `unattended` 无人值守）执行端到端验证。
5. **需求—决策—任务同步**：需求或方向变化时同步更新 `docs/sources.toml`、`docs/decisions/`、`docs/design/`、`docs/specs/` 与 `docs/work.toml`。

## 2. 写代码前的三视角判断与主动补全

1. **执行者视角**：分清哪些是 `docs/sources.toml` 与当前规格里已定约束、哪些仍待负责人决策；已定约束直接执行。
2. **协作者视角**：按设计稳定度控制节奏；`0->0.1` 原型先跑通关键路径，方向收敛后及时沉淀模块边界。
3. **架构师视角**：先查所属域阶段（`docs-policy.toml`）。当非专业架构背景的负责人用大白话提需求时，主动把运行/控制逻辑、唯一状态归属、异常处理和禁止耦合写进 `ARCHITECTURE.md` 与模块规格，不把模糊片段原样照抄成系统架构。

## 3. 按对象触发的强制动作

| 涉及对象或场景 | 必须执行的动作 |
|---|---|
| 任何人类或 AI 可读文本（文档、产品命令行与报错、界面文案） | 直接讲清对象是什么、怎么运行、解决什么问题；不造黑话、不混用冲突编号、不堆砌免责套话（见 `docs/README.md#language-standard`）。 |
| 系统与模块架构说明 | 必须写清五部分：定位与非目标、端到端运行/控制逻辑（`mermaid`）、清晰接口与禁止耦合、唯一状态真源与硬约束、模块入口与自动校验（见 `docs/contracts/architecture-and-modularity.md#decomposition-and-ownership`）。 |
| 跨内存/数据库/API/DOM/URL/配置的共享状态 | 指定唯一权威真源，其余视图由真源计算得到（见 `docs/contracts/architecture-and-modularity.md#single-source-of-state`）。 |
| 产品方向、交互流程或 UI 界面方案（`docs/design/`） | 按四层顺序设计：先守原则，再达到可测量的最佳实践底线（WCAG 2.2 AA 对比度、键盘操作、焦点可见、各种状态），再套用本项目负责人的偏好（负责人另行记录前沿用随模板下发的 calm-platter 默认风格），最后参考成熟产品；偏好不得压过上两层。先给出清晰对比方案并做 `/grill` 质询，拿到负责人明确拍板后再写前端实现；历史草稿或旧代码一律视为未批准（见 `docs/contracts/frontend-and-visual-discipline.md`）。 |
| 为读者组织信息（文档结构、导航、界面内容、知识或参考内容） | 先定读者和任务，结论先行；每一层只用一种组织方式；细节分层展开并带着上下文；按读者的问题选表格、步骤、图、正文或时间线；知识内容按真实影响面定范围，现状类事实标注日期，宣称覆盖完整要有对照证据（见 `docs/contracts/information-organization.md`）。 |
| 新增文件、源码或样式膨胀 | 核对 `owns` 归属与 `# Role:` 头注释，守住单文件 500 行源码 / 300 行样式上限，禁止设立 `utils/`、`helpers/`、`common/` 杂物目录。 |
| 影响项目方向的新要求、权衡决策或变更 | 只把对项目发展方向产生实质性影响的负责人原话按时间正序、未经删改翻译地写入 `docs/sources.toml`（`SRC-*`），同步维护 ADR 与模块规格并在 `docs/work.toml` 关联编号。 |
| 任务执行、审查节奏或无人值守模式 | 完整闭环交付授权任务，遵守 `docs-policy.toml` 的 `[collaboration]` 与 `templates/charter.md` 边界；需要 `/grill` 时加载 `.agents/skills/grill/SKILL.md`（见 `docs/contracts/delivery-and-verification.md`）。 |
| 独立评审与整体验收 | 在全新隔离上下文中执行，屏蔽作者自我辩解，先做不设限的整体架构/一致性/可用性检查；整改后必须送回原评审方与新视角复验闭环，并用真实运行路径验收。涉及覆盖面与时效时，评审方先不看交付物列出预期清单再对照，时效以评审时实际检索到的带日期来源为准，任何模型或个人的记忆都不算证据；评审方只报告发现，阶段性状态由负责人确认（见 `docs/contracts/delivery-and-verification.md#independent-review-definition`）。 |
| 纪律接入或版本同步升级 | 运行 `python3 scripts/read_rules.py onboard --target <路径>` 并遵守 `docs/contracts/adoption-and-synchronization.md`，保留本仓库自有规格与决策。 |

## 4. 防偷懒与防失真红线

- **必须走通真实执行路径与行为验收**：用真实命令行、服务或界面跑通检验，不只靠 mock 单元测试。
- **独立评审必须开放、盲审且闭环**：禁止预先把评审员限死在局部代码清单里，禁止塞入作者辩解词，禁止跳过全局一致性/架构审查，禁止未送回原评审方复验就宣称闭环完成。
- **严禁把未批准设计当成默认同意**：在 `docs/work.toml` 明确标记 `blocked` 与待选方案，等负责人明确拍板后再动实现代码。
- **已授权任务一次交付到位**：完整完成实现、集成与校验，不半途甩出待办清单让负责人收尾。

## 5. 常用导航、身份确认与校验命令

- 修改不熟悉文件前加载上下文：`python3 scripts/project.py context <路径或编号>`
- 查看项目状态、目录分工与阻塞项：`python3 scripts/project.py status`（仅在界面方案已批准时使用 `project.py serve`）
- 评审手册、技能与记录单：`docs/guides/grill.md`、`.agents/skills/grill/SKILL.md`、`templates/independent-review.md`
- 确认 `docs-policy.toml` 中保留 `identity = "product"` 而非模板身份。
- 提交前运行测试与规范校验：

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/check_docs.py
```
