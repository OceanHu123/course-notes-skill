# DEMO-OSTEP — The Abstraction: The Process (sample notes)

> Real Tier-0 run: source = [OSTEP Ch.4](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-intro.pdf) (Remzi & Andrea Arpaci-Dusseau, free chapter).  
> Written with the `course-notes` skill template; technical terms kept as in the text.

## Overview

- **Topic**: the process abstraction, CPU virtualization (time sharing), process API outline, creation steps, three states, OS data structures (PCB / process list)
- **Material**: `cpu-intro.pdf` pp.1–13 (book chapter 4)
- **Week**: Demo / OS intro week

## Section notes

### 1. Crux: how to fake many CPUs? (pp.1–2)

- Informal definition of a **process**: a **running program**. A program on disk is inert; the OS turns it into something useful by running it.
- Users want many programs at once (browser, mail, game, …) even though there are only a few physical CPUs.
- Answer: **virtualize the CPU** via **time sharing** — run A a bit, stop, run B, and so on. Illusion of many virtual CPUs; cost is that each runs a bit slower when sharing.
- Counterpart: **space sharing** (divide a resource in space, e.g. disk blocks assigned to files) vs time sharing (divide in time).

### 2. Mechanism vs policy (pp.2–3)

- **Mechanism**: answers *how?* Example: how does a **context switch** move the CPU from A to B.
- **Policy**: answers *which?* Example: which process should run now (**scheduling policy**).
- Classic OS design: separate the two so you can change policy without rewriting low-level mechanisms (modularity).

### 3. Machine state of a process (pp.2–3)

What makes up a process:

- **Memory / address space** — instructions and data the process can address
- **Registers** — including **PC / IP** (next instruction) and **stack pointer** / frame pointer
- **I/O state** — e.g. list of open files

### 4. What a process API must provide (p.3)

Modern OSes roughly expose:

| API | Role |
|---|---|
| Create | Shell command / double-click → new process |
| Destroy | Force-kill a runaway process |
| Wait | Wait until a process finishes |
| Misc control | Suspend / resume, etc. |
| Status | Runtime, current state, … |

(Concrete `fork` / `exec` details appear in later chapters; this chapter only sketches the interface.)

### 5. From program to process: what the OS does (pp.4–5)

Steps visible in the text:

1. **Load** code + static data into the address space (early OSes: eager; modern: often lazy — ties into paging later)
2. Allocate and initialize the **stack** (locals, args, return addresses; UNIX also sets up `main`'s `argc` / `argv`)
3. Possibly allocate an initial **heap** (for `malloc` / `free`; grow later via the OS)
4. I/O setup: UNIX defaults to three fds — stdin / stdout / stderr
5. Jump to entry point **`main()`** and hand the CPU to the new process

- **Figure 4.1** (p.4): caption shows Program → Loading → Process (code / static / heap / stack). Do not invent arrow semantics beyond the text.

### 6. Three process states and transitions (pp.5–7)

Simplified states:

| State | Meaning |
|---|---|
| **Running** | Executing instructions on a processor |
| **Ready** | Runnable, but the OS has not chosen it right now |
| **Blocked** | Waiting on an event (classic: disk I/O); cannot run yet |

Transitions (text + Figure 4.2 caption):

- Ready ↔ Running: OS **schedules** / **deschedules**
- Running → Blocked: process initiates I/O (etc.)
- Blocked → Ready: event completes (e.g. I/O done)

Two traces:

- **CPU-only** (Figure 4.3): alternate Running/Ready until one finishes.
- **With I/O** (Figure 4.4): when Process0 blocks, CPU can run Process1 → better **utilization**. Whether to switch back to Process0 as soon as I/O completes is a **scheduler policy** question (left open on purpose).

### 7. OS data structures (pp.7–9)

- The OS keeps a **process list** (aka task list): who is ready, who is running, who is blocked; on I/O completion, wake the right process.
- Per-process descriptor often called a **PCB (Process Control Block)** / process descriptor.
- xv6 example (Figure 4.5, p.8): `struct context` saves registers to stop/resume; `enum proc_state` includes `UNUSED, EMBRYO, SLEEPING, RUNNABLE, RUNNING, ZOMBIE` — finer than the textbook three-state model.
- **Register context**: when stopped, registers are saved to memory; restoring them resumes the process — part of a **context switch** (covered later).
- **Zombie**: exited but not yet reaped by the parent’s `wait()`, so the parent can read the exit code (UNIX: 0 = success, non-zero = failure).

### 8. What the chapter is building toward (pp.9–13)

- The process is a core OS abstraction; later chapters deepen **mechanisms** (how to switch) and **policies** (whom to schedule).
- Vocabulary first: process / address space / time sharing / mechanism vs policy will keep recurring.

## Comparison tables

| | Mechanism | Policy |
|---|---|---|
| Question | *How?* | *Which?* |
| Example | How context switch works | Which process runs now |
| Swapability | Keep mechanisms stable | Policies often swappable |

| | Time sharing | Space sharing |
|---|---|---|
| Division | In time | In space |
| Example | CPU | Disk blocks for files |

| | Program | Process |
|---|---|---|
| Where | Image on disk | Running instance |
| State | No live register / runtime context | Address space, registers, open files, … |

## Cheat sheet

| Term | One-liner |
|---|---|
| Process | A running program |
| Address space | Memory the process can legally address |
| Time sharing | Time-slice the CPU to fake many CPUs |
| Context switch | Low-level stop-A / start-B (later chapter) |
| PCB | Struct describing one process |
| Ready / Running / Blocked | Runnable not running / running / waiting |
| Zombie | Exited, waiting for parent to reap |
| Eager vs lazy load | Load all upfront vs load on demand |

## Easy to mix up

- **Process ≠ program**: one program can have zero or many process instances.
- **Blocked ≠ Ready**: Blocked cannot run until an event; after I/O it becomes Ready, not necessarily Running.
- **Descheduled ≠ Blocked**: Ready↔Running is the scheduler; Blocked is the process waiting on something.
- **Textbook three states vs xv6 many states**: exam questions about `SLEEPING` / `ZOMBIE` use the implementation view, not Figure 4.2’s minimal model.

## Link to homework / exams

- “Why can the CPU stay busy with I/O-heavy workloads?” → Blocked processes yield the CPU; scheduler runs Ready ones.
- “Why does `wait()` exist?” → Reap zombies and read exit codes; the kernel does not erase everything the instant a process exits.
- Next chapters usually cover the **process API** (`fork` / `exec` / `wait`) and **limited direct execution** — learn this chapter’s vocabulary first.

## Unread figures

| Page | Figure | Handling |
|---|---|---|
| p.4 | Figure 4.1 Loading | Covered by caption + text steps; no invented arrows |
| p.6 | Figure 4.2 state diagram | Transitions taken from the prose |
| pp.6–7 | Figures 4.3 / 4.4 traces | Table text extracted; good for review |
| p.8 | Figure 4.5 xv6 `proc` | Fields taken from the extracted code |

## Optional next steps

1. From memory, redraw Ready / Running / Blocked transitions (pp.6–7)
2. Read the next OSTEP chapter on the process API (`fork` / `exec` / `wait`)
3. Ask the skill: `quiz me on this PDF`
