# Engineering Discipline Template

这是一个与具体业务、框架和运行时无关的工程模板仓库。它不包含产品实现，
只提供：

- 可复用的目录骨架；
- 契约优先的开发纪律；
- 前端、后端和跨端变更模板；
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
4. 在写首个受治理的产品变更前完成当前态 `ARCHITECTURE.md` 和相关契约。
5. 只有契约已落盘且冲突已对账后，才开始对应范围的实现。
6. 如果由 agent 推进 material/high-risk 变更，按
   `docs/contracts/agent-execution-discipline.md` 选择执行与独立评审深度。
7. 配置 `architecture-rules.toml`，或明确记录为什么不适用。
8. 使用 Python 3.11+ 运行单元测试和 `python3 scripts/check_docs.py`。
9. 将 `templates/ci/docs-check.example.yml` 适配到项目自己的 CI。

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
- 后端明确状态所有权、失败和恢复；
- agent 风险决定执行深度，高风险设计与验收使用真实独立上下文；
- 开发者拥有方向和优先级，框架只提供事实、风险、建议与有限执行门；
- onboarding 先保全当前事实，再按 observed → baselined →
  scoped_enforcement → adopted 渐进收紧；
- 任务、任务组、目标与发布门分别关闭，不以低层完成冒充高层完成；
- 原始输入与派生表示分层，数据删除、迁移与 GC 保留可验证证据；
- 规则尽量进入环境，而不是依赖记忆；
- 计划、契约、Issue 和证据不互相冒充。

视口数量、测试框架、目录深度、发布平台和文件行数阈值都应由实际项目
重新决定。
