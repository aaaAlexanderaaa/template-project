---
doc_type: authority-map
status: current
authority: normative
---

# 文档分工与平实语言规范

## 1. 单一事实来源分工

| 事实类别 | 唯一源文件 |
|---|---|
| 系统目标与顶层数据流 | `ARCHITECTURE.md` |
| 业务域说明与成熟度阶段 | `docs/specs/<domain>/README.md` |
| 模块职责范围、对外承诺与依赖边界 | `docs/specs/<domain>/<module>.md` |
| 前端界面设计稿与负责人批准状态 | `docs/design/<surface>.md` |
| 跨模块权衡与架构决策 | `docs/decisions/ADR-*.md` |
| 用户原话诉求与提出场景 | `docs/sources.toml` |
| 里程碑分栏与任务队列 | `docs/work.toml` |
| 协作模式、源码目录与文件行数上限 | `docs-policy.toml` |

## 2. 改代码前五步上下文核对

<!-- required-reading: task-context -->
### 任务上下文检查

在修改行为之前，先从以下五个唯一真源读取必要事实：

1. **目标结果与负责人原话**：阅读当前任务诉求，并运行 `python3 scripts/project.py context <路径或编号>` 查看关联的 `SRC-*` 原话与既有 `ADR-*` 决策。
2. **代码归属与所属模块**：打开对应的 `docs/specs/.../*.md` 规格，核对 `owns` 覆盖的实际源文件。
3. **当前阶段与协作模式**：确认域成熟度（`prototype | usable | stable`）与 `docs-policy.toml` 中的 `[collaboration]` 配置。
4. **模块边界与体积预算**：核对模块 `depends_on`、`architecture-rules.toml`（可选）以及单文件源码/样式行数上限。
5. **真实端到端验证**：验证目标功能本身跑通，并确认未引入意外副作用。
<!-- /required-reading: task-context -->

## 3. 平实语言规范

<!-- required-reading: language-standard -->
### 语言规范

本项目所有自建文档、规格说明、决策记录、任务单与前端界面文案均必须使用平实、直接的中文（`docs/sources.toml` 保留负责人一字不改的原话；`docs/contracts/` 与 `docs/guides/` 为上游同步的通用基准规则原文）：

- 直接说明每个模块或界面是什么、怎么运行、解决什么问题。
- 禁止造生僻概念词、打比方、同页混用冲突编号、堆砌免责套话或向读者直接暴露后台枚举原词。
<!-- /required-reading: language-standard -->
