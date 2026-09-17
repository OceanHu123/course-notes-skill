# COMPXXXX Week 3 — Processes & Memory（样例笔记）

> 匿名示例：课程代码与页码已脱敏。真实笔记由 skill 按同样模板生成，并落到 `~/notes/<course>/<topic>.md`。

## 总览

- **主题**：process vs thread、地址空间、基础 IPC
- **材料**：Lecture PDF p.1–18；Lab slides 3–7
- **对应周次**：Week 3

## 分部分详解

### 1. Process 是什么（p.2–5）

- Process = 正在运行的程序 + 它自己的 **address space**、文件描述符、凭证
- 每个 process 有独立的虚拟地址空间；互相默认看不到对方内存
- `fork` 复制父进程；子进程拿到自己的 PID，共享只读页直到写时复制（COW）

### 2. Thread（p.6–9）

- Thread 共享同一 address space，但有自己的栈与寄存器上下文
- 同 process 内线程通信便宜，但需要同步（锁 / 原子操作）
- 对比：多 process 隔离更强，切换与 IPC 更贵

### 3. 内存视图（p.10–14）

- 用户态常见布局：text / data / heap / stack（具体布局因 OS 与架构而异）
- Stack 向下长、heap 向上长是常见示意，考试常考「谁在涨、冲突会怎样」
- 页表把虚拟地址映射到物理页；缺页会触发 fault 再由内核处理

### 4. Lab 要点（slides 3–7）

- 观察 `/proc/<pid>/maps`（或等价工具）看映射区间
- 区分「进程间共享文件」与「共享内存段」：后者要显式建立

## 对比表格

| | Process | Thread |
|---|---|---|
| Address space | 各自独立 | 共享 |
| 崩溃影响 | 通常只倒自己 | 可能拖垮同 process 其它 thread |
| 通信 | pipe / socket / shm… | 直接读写共享变量（需同步） |
| 创建成本 | 相对高 | 相对低 |

## 速查表

| 概念 | 一句话 |
|---|---|
| PID | 进程标识 |
| Address space | 该进程能合法访问的虚拟地址集合 |
| COW | 写时才真正复制物理页 |
| IPC | 进程间通信的统称 |

## 易混点

- **Process ≠ Program**：program 是磁盘上的映像；process 是运行中的实例
- **共享库被映射 ≠ 共享可写内存**：映射同一 `.so` 不等于可以随意改对方数据
- **并发 vs 并行**：多线程可以并发；是否并行取决于核数与调度

## 与作业 / 考试的关联

- 作业若要求「子进程改内存父进程看不到」→ 考的是独立 address space + 非共享可写映射
- 若要「多 worker 算同一缓冲区」→ 更可能是 threads 或显式 shared memory，而不是裸 `fork`

## 未读图页清单

- p.12 拓扑示意图：OCR 无法还原箭头含义 → **此页为图，未读**（需对照原 PDF）
