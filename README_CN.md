# Engineering Discipline Template

[English](README.md) | [中文](README_CN.md)

这是一个与具体业务、框架和运行时无关的工程模板仓库。它不包含产品实现。
它最重要的产物不是目录、模板或检查器，而是这些载体背后的判断与交付纪律。

本仓库是一个 harness：一种工作制度，让一个高局部智能、低原生执行功能、
会借工具产生现实副作用的认知主体可以被长期委托，并让它的失败沉淀为组织学习，
而不是组织负债。这里的一切都服务于被请求的可观察结果；契约、测试、文档和检查
守护意图、暴露错误，但完成它们本身不等于完成了任务。

另外两条观察塑造了这套纪律：所有者的注意力是最贵的资源，算力是最便宜的，
所以默认把成本推向机器一侧——同时保持成本意识，因为配额和熔断保护的是账号与
注意力，而不是为了节省算力；未经验证的声称不为真，无论它听起来多可信。这套
纪律自 2026-07 起在维护者自己的项目里持续被使用并修正，经验回流是常态实践；
独立采用仍是开放前沿。

## 带走价值排序

当一个 agent 进入本仓库并自行判断应该带走什么时，先按适用广度、下游杠杆、
出错代价、可迁移性和目标项目依赖程度分配注意力：

| 基础优先级 | 优先理解 | 为什么先看 | 现有 owner |
|---|---|---|---|
| **P0** | 人与 agent 的交互和认知纪律 | 它决定事实是否被查清、问题是否问对、用户权威和任务范围是否被保留，并影响之后的每一次判断 | [development discipline](docs/contracts/development-discipline.md) § research-unknowns – causal-mechanism；[governance boundary](docs/contracts/governance-decision-boundary.md)（全部 invariant） |
| **P1** | 当前事实、权威、所有权、依赖边界与历史债务 | 它决定会不会覆盖现有真相、复制规则或把局部债务扩散到整个项目 | [architecture](ARCHITECTURE.md)；[development discipline](docs/contracts/development-discipline.md) § one-owner – coherent-end-state；[project adoption](docs/contracts/project-adoption.md) § current-vs-target – visible-debt |
| **P2** | 完整终态、风险分级、按目标选择验证方法、类别级防护、失败恢复，以及「未命名就会渗到全系统」的识别规则 | 它决定如何把正确理解变成可验证的完整交付，以及一个未声明的默认会不会变成日后的全量切换 | [agent execution](docs/contracts/agent-execution-discipline.md) § risk-selects-depth – smallest-route；[development discipline](docs/contracts/development-discipline.md) § outcomes-first – decisions-not-volume；识别规则见 [foundational runtime](docs/contracts/foundational-runtime-discipline.md) |
| **P3** | 前端、后端、跨端、样式、数据、运维、安全、性能、时钟/日历、演示数据等条件性纪律 | 它们在目标项目激活相关边界时价值很高，并应按真实风险上调 | [development discipline](docs/contracts/development-discipline.md) 的对应领域契约及被激活的 concern owner；时间与演示的不变量：[foundational runtime](docs/contracts/foundational-runtime-discipline.md) |
| **P4** | 文档拓扑、模板、adoption stage、policy manifest、检查器和 CI 示例 | 它们承载或执行前面的纪律，但可复制性不等于价值优先级 | [documentation map](docs/README.md)；[documentation harness](docs/contracts/documentation-harness.md) |

这是**注意力与提炼顺序**，不是文档权威顺序，也不是要求完整照搬。目标项目的
事实可以让 P3 中的相关领域升到 P1/P2；例如有复杂 UI 时，用户状态、交互、
可访问性和样式所有权立即前移。学习和采用使用同一排序，只是后者涉及实际写入和
治理授权。先带走方法，再决定是否需要本仓库的文件和工具。

文档检查器只依赖 Python 标准库，最低版本为 Python 3.11。

## 使用方式

1. 阅读 `docs/README.md`，确定文档权威顺序。
2. 新项目以本仓库为起点；运行中项目先按
   `docs/guides/onboarding.md` 做只读盘点，不要直接覆盖已有权威。
3. 使用 `templates/adoption-assessment.md` 记录当前事实、治理范围、优先级
   权威与 adoption 阶段，并由项目所有者确认。
4. 在 `docs-policy.toml` 中声明这些决定（见下节「按项目规模伸缩」）：
   `[adoption].stage`、`source_roots`、`managed_paths` 与
   `[templates].profile`。检查器读取这些字段，而不是假设某一种项目形态。
5. 在写首个受治理的产品变更前完成当前态 `ARCHITECTURE.md` 和相关契约。
   日期时间和操作员可见的演示数据是 [development § activate-concerns](docs/contracts/development-discipline.md#activate-concerns-instead-of-expanding-ceremony) concern：用到时再读，不要在
   用不到时填一份踩坑表。
6. material 交付必须先落盘契约；只读调查无法回答的技术事实，可以先走 [development § contract-first](docs/contracts/development-discipline.md#contract-before-material-delivery-evidence-before-certainty)
   的一次性受控实验路径，实验结果不能直接成为产品行为。
7. 如果由 agent 推进变更，按
   [agent-execution § smallest-route](docs/contracts/agent-execution-discipline.md#the-harness-selects-the-smallest-executable-route) 选择最小执行路径；只有
   high-risk 路径要求独立设计评审与换上下文验收。
8. 配置 `architecture-rules.toml`，或明确记录为什么不适用。
9. 使用 Python 3.11+ 运行单元测试和 `python3 scripts/check_docs.py`。
10. 将 `templates/ci/docs-check.example.yml` 适配到项目自己的 CI。

## 按项目规模伸缩

模板不假设项目大小，也不要求先完成迁移才能接入 CI。四个旋钮都在
`docs-policy.toml` 里：

| 旋钮 | 作用 | 常见取值 |
|---|---|---|
| `[adoption].stage` | 采用阶段是否阻断构建 | `observed`/`baselined` 只报告并返回 0；`scoped_enforcement`/`adopted` 阻断 |
| `[adoption].source_roots` | 什么算产品代码 | `["src"]`、`["app", "lib"]`、`["packages"]`、`["cmd", "internal"]` |
| `[adoption].managed_paths` | `scoped_enforcement` 下受治理的边界 | `["packages/billing/**"]` |
| `[templates].profile` | 需要哪些模板（分层累积） | `minimal` / `standard` / `full` |

由此得到的工作方式：

- **小项目：** `profile = "minimal"` 只保留契约、计划、Issue 与指南四个模板，
  其余可以直接删除；文档里残留的引用降级为 advisory，不会让构建变红。
- **运行中的项目：** 第一天就可以把检查器放进 CI。`stage = "observed"` 会把
  未完成的采用工作打印出来并返回 0，随阶段推进逐步收紧。
- **非 `src/` 布局：** 代码若落在所有 `source_roots` 之外，检查器会指名报告，
  而不是在空集合上给出一个无意义的绿灯。这条同样受 stage 影响：早期阶段只报告，
  所以还没配好布局也能先把检查接进 CI。仓库根目录下的文件（`setup.py`、
  `conftest.py`、`vite.config.ts` 等）从不计入产品代码；工具目录写进
  `harness_paths`，它接受 `tools/**` 这样的 glob。
- **CI：** 结构性问题是 error；仅因日期推移产生的问题（过期 target、逾期
  promise、pending 证据超期）默认是 advisory。把 `--strict` 放到定时任务里，
  日期变化就不会让一个无关的 PR 失败。设为 `off` 的规则在 `--strict` 下仍然
  保持关闭——关掉它是项目自己的决定。

## 目录

```text
.
├── README.md                 # 英文首页
├── README_CN.md              # 中文首页
├── AGENTS.md                 # 自动化开发者的工作入口
├── CONTRIBUTING.md           # 人与自动化开发者共享的推进流程
├── ARCHITECTURE.md           # 待项目填写的结构权威模板
├── architecture-rules.toml   # 可机器执行的基础架构边界规则
├── docs-policy.toml          # 文档老化、模板和 adoption 策略
├── docs/
│   ├── README.md             # 文档权威与生命周期地图
│   ├── contracts/            # 当前、长期有效的规范
│   ├── design/               # UI surface 的 raw ↔ translated 契约
│   ├── plans/                # 一次变更的执行计划
│   ├── issues/               # 缺陷及审计发现的生命周期
│   ├── guides/               # 操作和维护说明
│   └── evidence/             # 可复核的持久证据
├── templates/                # 可复制模板，不具有项目行为权威
├── scripts/                  # 可移植纪律的机械执行面
├── src/                      # 产品代码占位，当前为空
├── tests/                    # 检查器夹具测试；采用后继续增加产品测试
├── tmp/                      # 本地临时证据，gitignored
└── archive/                  # 本地替换备份，gitignored
```

## 迁移原则

应该迁移的是方法，而不是原项目的工具或数字：

- 契约先于 material 交付，技术未知先调查或做有边界、可清理的实验；
- 当前权威可识别；
- 冲突必须对账；
- 计划面向完整终态；
- 缺陷按类别修复；存在可重复兄弟机制且成本相称时增加类级护栏；
- 前端穷尽状态并结合感知与结构证据；
- 前端视觉与文案从 raw brief 翻译：设计候选和探针只提供证据，接受后的方向
  才进入 surface/style owner，缺失的产品意图仍交还人类决定；
- 样式有唯一所有者：层级顺序、共享视觉值的分层与可覆盖面都显式声明，
  消费方只组合已发布的契约，越权升级记为有主、有回收条件的债务；
- 后端明确状态所有权、失败和恢复；
- Scoped time policy and demonstration temporal promises follow the
  [current runtime owner](docs/contracts/foundational-runtime-discipline.md).
  For authorized lightweight delivery, follow the
  [current execution route](docs/contracts/agent-execution-discipline.md#the-harness-selects-the-smallest-executable-route).
- agent 风险决定执行深度，高风险设计与验收使用真实独立上下文；
- 被激活的质量关注点只在一个规范契约中拥有边界，计划只记录链接、步骤和证据；
- 开发者拥有方向和优先级，框架只提供事实、风险、建议与有限执行门；
- 陌生引用与可核查事实不靠猜测补全；优先查原始或官方来源，工具不可用时先找
  保持语义与证据强度的替代路径；
- 技术事实先调查、可逆工程选择由执行者完成，产品意图、重大取舍与风险接受才
  交还用户选择；相互依赖的决定按先决条件逐项确定，并在交付前明确授权。
  已有明确指令覆盖共同理解时，不重复确认。分析以讲清因果机制、适用边界及
  关键隐含问题为标准；
- onboarding 先保全当前事实，再按 observed → baselined →
  scoped_enforcement → adopted 渐进收紧；
- 任务、任务组、目标与发布门分别关闭，不以低层完成冒充高层完成；
- 原始输入与派生表示分层，数据删除、迁移与 GC 保留可验证证据；
- 规则尽量进入环境，而不是依赖记忆；
- 计划、契约、Issue 和证据不互相冒充。
- 文档治理同时管理增量与存量：更新、合并、沉淀、退役和删除临时证据；
  不用文件数、行数或统一保留年龄代替质量判断。

视口数量、测试框架、目录深度、发布平台、样式方案（CSS 组织方式、令牌命名与
主题实现）和文件行数阈值都应由实际项目重新决定。

## 许可证

本仓库以 [MIT License](LICENSE) 发布。
