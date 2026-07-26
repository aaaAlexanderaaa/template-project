# Engineering Discipline Template

这是一个与具体业务、框架和运行时无关的工程模板仓库。它不包含产品实现，
只提供：

- 可复用的目录骨架；
- 契约优先的开发纪律；
- 前端、后端和跨端变更模板；
- 样式所有权纪律：层级、值分层与可覆盖面的模板，以及可选的
  `style-ownership.toml` 声明（不生成该文件的项目不受任何约束）；
- 计划、Issue、验证与交接模板；
- 面向 AI agent 的风险分级、七阶段执行、独立评审与换上下文验收模板；
- 证据保全型数据边界模板；
- 不替代开发者优先级与产品判断的有限治理边界；
- 面向新项目与运行中项目的 AI 引导式渐进 onboarding；
- 可配置、带夹具测试的文档纪律检查器。

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
6. 只有契约已落盘且冲突已对账后，才开始对应范围的实现。
7. 如果由 agent 推进 material/high-risk 变更，按
   `docs/contracts/agent-execution-discipline.md` 选择执行与独立评审深度。
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

- 契约先于实现；
- 当前权威可识别；
- 冲突必须对账；
- 计划面向完整终态；
- 缺陷按类别修复并增加类级护栏；
- 前端穷尽状态并结合感知与结构证据；
- 样式有唯一所有者：层级顺序、共享视觉值的分层与可覆盖面都显式声明，
  消费方只组合已发布的契约，越权升级记为有主、有回收条件的债务；
- 后端明确状态所有权、失败和恢复；
- agent 风险决定执行深度，高风险设计与验收使用真实独立上下文；
- 开发者拥有方向和优先级，框架只提供事实、风险、建议与有限执行门；
- onboarding 先保全当前事实，再按 observed → baselined →
  scoped_enforcement → adopted 渐进收紧；
- 任务、任务组、目标与发布门分别关闭，不以低层完成冒充高层完成；
- 原始输入与派生表示分层，数据删除、迁移与 GC 保留可验证证据；
- 规则尽量进入环境，而不是依赖记忆；
- 计划、契约、Issue 和证据不互相冒充。

视口数量、测试框架、目录深度、发布平台、样式方案（CSS 组织方式、令牌命名与
主题实现）和文件行数阈值都应由实际项目重新决定。
