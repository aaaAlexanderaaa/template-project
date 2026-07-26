# Engineering Discipline Template

这是一个与具体业务、框架和运行时无关的工程模板仓库。它不包含产品实现，
只提供：

- 可复用的目录骨架；
- 契约优先的开发纪律；
- 前端、后端和跨端变更模板；
- 计划、Issue、验证与交接模板；
- 最小文档生命周期自检。

## 使用方式

1. 复制或以本仓库作为新项目起点。
2. 在写产品代码前完成 `ARCHITECTURE.md`。
3. 阅读 `docs/README.md`，确定文档权威顺序。
4. 将 `templates/` 中需要的模板复制到对应 `docs/` 目录并填写。
5. 只有契约已落盘且冲突已对账后，才开始实现。
6. 运行 `python3 scripts/check_docs.py` 检查文档生命周期和引用。
7. 将 `templates/ci/docs-check.example.yml` 适配到项目自己的 CI。

## 目录

```text
.
├── AGENTS.md                 # 自动化开发者的工作入口
├── CONTRIBUTING.md           # 人与自动化开发者共享的推进流程
├── ARCHITECTURE.md           # 待项目填写的结构权威模板
├── docs/
│   ├── README.md             # 文档权威与生命周期地图
│   ├── contracts/            # 当前、长期有效的规范
│   ├── design/               # UI surface 的 raw ↔ translated 契约
│   ├── plans/                # 一次变更的执行计划
│   ├── issues/               # 缺陷及审计发现的生命周期
│   ├── guides/               # 操作和维护说明
│   └── evidence/             # 可复核的持久证据
├── templates/                # 可复制模板，不具有项目行为权威
├── scripts/                  # 纪律的最小机械执行面
├── src/                      # 产品代码占位，当前为空
├── tests/                    # 产品测试占位，当前为空
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
- 规则尽量进入环境，而不是依赖记忆；
- 计划、契约、Issue 和证据不互相冒充。

视口数量、测试框架、目录深度、发布平台和文件行数阈值都应由实际项目
重新决定。
