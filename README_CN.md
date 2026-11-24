# 工程纪律模板仓库（template-project）

> **English version**: [README.md](README.md)

`template-project` 是一套面向人机协作编程的**工程纪律模板**（`discipline_version = "2026.11.1"`）。仓库的核心产品是可直接迁移到任意新旧软件项目中的工程规则、架构边界规范、设计审批门禁、独立评审流程与起步模板，用来按项目阶段加速并增强 AI 协作，主动补齐成熟工程实践，让持续成长的代码库保持清晰、模块化、可追溯，并始终对齐负责人的真实意图。

`scripts/` 下的 Python 检查脚本与本地概览服务是**通用辅助工具**，用来确定性校验文档链路、静态边界与文件行数，并把这套纪律稳定落盘到下游项目。

## 这套模板能为项目带来什么

1. **清晰的顶层协作规则（[AGENTS.md](AGENTS.md)）**：明确优先级顺序、写代码前的三视角判断、按对象触发的强制动作，以及防止偷工减料的红线。
2. **五要素架构说明与模块化契约（[docs/contracts/](docs/contracts/README.md)）**：要求系统与模块说明写清定位与边界、端到端运行/控制逻辑（`mermaid`）、清晰接口与禁止耦合、唯一状态真源与硬约束、模块入口与自动校验，并使用平实直接的表达（[docs/README.md](docs/README.md#language-standard)）。
3. **可追溯的需求—决策—任务链路（[docs/sources.toml](docs/sources.toml)、[docs/work.toml](docs/work.toml)）**：将项目负责人原话（`SRC-*`）、架构决策（`ADR-*`）、设计稿（`docs/design/`）、模块规格（`docs/specs/`）与任务单（`T-*`）双向关联；产品方向与界面方案未经负责人明确批准不得开工实现。
4. **以读者为中心的信息组织与分层前端规范（[information-organization.md](docs/contracts/information-organization.md)、[frontend-and-visual-discipline.md](docs/contracts/frontend-and-visual-discipline.md)）**：文档、界面与知识内容按读者的任务来组织；界面先守原则和可测量的最佳实践底线（如 WCAG 2.2 AA），再套用负责人偏好和参考产品。
5. **开放且闭环的独立评审机制（[docs/guides/grill.md](docs/guides/grill.md)、[templates/independent-review.md](templates/independent-review.md)）**：独立评审必须在全新隔离上下文中开展，屏蔽作者辩解，先做不设限的全局架构/一致性/可用性检查，涉及覆盖面与时效时先列预期清单再对照、时效以评审时检索到的带日期来源为准，整改后送回原评审方复验闭环。
6. **不失真的下游迁移模板（[templates/](templates/README.md)、[.agents/skills/](.agents/skills/onboard-discipline/SKILL.md)）**：在新建（`init`）与接入（`onboard`）时保留完整核心纪律，同时彻底剥离本模板内部示例域名。

## 快速开始

### 1. 基于本模板新建产品仓库

```bash
python3 scripts/project.py init --target /path/to/new-repo --name "我的项目" --lang zh
```

### 2. 为现有仓库接入或升级工程纪律

```bash
python3 scripts/read_rules.py onboard --target /path/to/existing-repo
```

### 3. 本地校验与状态查看

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/check_docs.py --strict
python3 scripts/project.py status
```

## 核心入口文件

| 文件 | 作用 |
|---|---|
| [AGENTS.md](AGENTS.md) | 每次会话首先遵守的工作协议与防偷懒红线 |
| [ARCHITECTURE.md](ARCHITECTURE.md) | 仓库定位、核心运行/评审闭环逻辑、硬约束与状态归属、四大子系统及迁移路径 |
| [docs-policy.toml](docs-policy.toml) | 行数上限（源码 500 行、样式 300 行）、阶段配置与评审间隔策略 |
| [docs/README.md](docs/README.md) | 文档目录总索引、平实语言标准与改前加载指南 |
| [docs/design/perspective-web.md](docs/design/perspective-web.md) | 按 `SRC-022` 与 `ADR-005` 批准落地的四视角本地项目透视网站规格（`T-204` 待验收） |
| [templates/README.md](templates/README.md) | 迁移到下游项目时使用的起步模板清单 |
