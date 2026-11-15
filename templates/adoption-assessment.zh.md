---
doc_type: guide
status: current
authority: guidance
---

# 存量项目接入评估单

在存量代码库启用规则强制拦截之前，先盘点客观事实：

- **项目定位与当前阶段**：`prototype` | `usable` | `stable`
- **源码目录与现有工具链**：实际 `source_roots` 及测试命令
- **规则适用性盘点**：
  - 本地已满足的条款（写出已有文件或检查命令）
  - 本期要落地的条款（列出目标业务域与模块规格）
  - 经核对不适用的条款（写出客观仓库依据）
- **接入阶段推进计划**：`observed`（只提示）→ `scoped_enforcement`（局部启用）→ `adopted`（全面对齐）
