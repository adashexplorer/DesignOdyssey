# Project agents and skills

Scaffolding for Claude Code in this repository. Everything here is project-scoped — it applies to anyone working in this repo, and is versioned with it.

## Layout

Three directories, split by **how a file gets used**, not by what it contains:

| Directory | What lives there | How it loads |
|---|---|---|
| `agents/` | Subagent definitions — one `name` per file | Scanned recursively by Claude Code |
| `skills/` | Procedures a person or Claude invokes | Matched by description, or `/name` |
| `docs/` | Shared reference material | Read **by path**, only because an agent's prompt names it |

The split matters: `agents/` is scanned, so a file without valid frontmatter sitting there is at best ignored and at worst confusing. Shared prose that several agents read — the panel charter is the current example — belongs in `docs/`.

## Agents — `.claude/agents/**/*.md`

A subagent runs in its own context window with its own tool set, and reports back a result. Use one when a task is self-contained and you do not want its intermediate output in the main conversation.

Claude Code scans this directory **recursively**, so related agents can live in a subfolder — the panel does, in `agents/panel/`. The path is purely organizational: an agent is identified and invoked by its `name` frontmatter field alone, which must be unique across the whole tree. `/doctor` reports duplicates.

| Agent | Use it for | Status |
|---|---|---|
| `interview-panel` | **Orchestrator.** Runs a full multi-round loop: plans the rounds, dispatches the seats below, keeps them blind to each other, then convenes the committee for a HIRE / NO HIRE | built |
| `panel-hld-architect` | Seat — broad HLD design round. Requirements, estimation, data model, APIs, architecture | built |
| `panel-hld-deepdive` | Seat — one component for the whole round. Depth, failure modes, consistency, behaviour when stuck | built |
| `panel-lld-design` | Seat — LLD/OOD round. Class model, SOLID, extensibility, concurrency, testability | built |
| `panel-lld-machine-coding` | Seat — 90–120 min build round. Working demonstrable code, modularity, the live extension test | built |
| `panel-bar-raiser` | Seat — outside the hiring team. Cost, ops, blast radius, scope, and the level verdict | built |
| `panel-committee` | Reads only the sealed scorecards; weights the rounds, decides HIRE / NO HIRE, writes the packet | built |
| `mock-interviewer` | Single-round alternative: research 10 sourced questions, run one timed mock, or grade a written answer | built |
| `fact-checker` | Verifying version claims, dates, statistics, and links against primary sources | planned |
| `roadmap-editor` | Editing `README.md` phases, concept tables, calendars, problem lists | planned |

Invoke by naming one ("use the mock-interviewer on the parking lot"), or let Claude select based on the `description` field.

**Not a subagent:** the daily reading-list curator is a *Python-driven prompt*, not a Claude Code agent. It lives at `interview-curator/prompt.md`, is read by `interview-curator/curator_agent.py`, and runs from `.github/workflows/daily-brief.yml`. Edit it there — a copy in `agents/` would not be loaded and would drift.

### Adding one

```markdown
---
name: agent-name
description: One or two sentences on when to use this agent. This is what Claude matches against, so describe the trigger, not the implementation.
tools: Read, Grep, Glob, Bash    # optional; omit to inherit all tools
model: sonnet                     # optional: sonnet | opus | haiku | fable,
---                               #   a full ID like claude-opus-5, or inherit

The system prompt. Write it as instructions to the agent: what to read first,
what the rules are, what to output.
```

Keep `description` trigger-shaped — it decides whether the agent gets picked. Narrow `tools` for read-only agents; a reviewer that cannot write cannot accidentally rewrite the thing it reviews.

### Choosing a model

Every agent here declares a `model`, matched to the work rather than defaulted. Omitting the field is also fine — the agent then follows the main conversation — but state the choice deliberately, because a grader silently running on whatever the session happens to be set to produces scores you cannot compare across runs.

**Precedence is fixed: `opus` and `sonnet` first, `haiku` last.** The dividing line is not cost, it is whether the work *decides* anything.

| Precedence | Model | Use it for | In this repo |
|---|---|---|---|
| 1st | `opus` | Open-ended judgment, arithmetic that decides an outcome, evidence hygiene on live web research | `panel-hld-deepdive`, `panel-bar-raiser`, `panel-committee`, `mock-interviewer` |
| 1st | `sonnet` | Grading where explicit 1/3/5 anchors carry the load, plus orchestration | `panel-hld-architect`, `panel-lld-design`, `panel-lld-machine-coding`, `interview-panel` |
| last | `haiku` | **Writing up already-decided content only** — formatting a packet, assembling a tracker row, transcribing a settled scorecard | no agent's default; permitted as a write-up pass after the committee has decided |

Never grade, score, or judge on `haiku`, and never dispatch a panel seat on it: a seat rates a person's competence and must justify every rating with a quote. Haiku may render the words *after* the ratings, the score and the verdict exist — it never produces them. The test: **if the pass would have to decide anything, it is not a write-up pass.**

**An orchestrator can override per dispatch.** The `Agent` tool takes a `model` parameter that beats frontmatter, so `interview-panel` picks each round's model by candidate level: sonnet where the anchors are coarse, opus where a 4 must be told from a 5. Its table is in `agents/panel/interview-panel.md` §2. Frontmatter is the default for standalone use; the override is what makes a loop efficient.

### Adding a panel seat

A seat is an agent plus a contract. Five steps, and the last two are the ones people forget:

1. **Write `agents/panel/panel-<seat>.md`.** Open by pointing at `.claude/docs/panel-charter.md` — that is where the turn protocol, evidence rule, scale, and scorecard schema come from, so the seat file only carries what is *unique* to this seat.
2. **Give it disjoint competencies.** A seat that grades what another seat grades makes the loop score double-count. Copy an existing seat's two tables — weights by level, and 1/3/5 anchors — and state plainly what the seat must *not* grade.
3. **Check the anchors.** Any weight column must map straight 3s → 6.0 and straight 5s → 10.0. That holds automatically for uniform ratings under any weighting, so a failure means a dimension is missing an anchor, not that the weights are wrong.
4. **Add a round weight** to the table in `panel-committee.md`, or the committee cannot score the round.
5. **Add it to the loop menu and the model table** in `interview-panel.md` — the menu, or nothing will ever dispatch it; the model table, or it silently runs on its frontmatter default at every level.

The obvious next seat is **AI** — `mock-interviewer` already carries an AI-round rubric (pipeline, retrieval-or-serving depth, evals, token/GPU cost, safety) that no panel seat currently owns.

## Skills — `.claude/skills/<name>/SKILL.md`

A skill is a procedure loaded into the current turn — a checklist Claude follows in place of improvising. Use one for a repeatable workflow with steps that are easy to get subtly wrong.

**None of these are written yet — `.claude/skills/` is empty.** They are the planned set;
until one exists, do the work by hand.

| Skill | Use it for | Status |
|---|---|---|
| `link-audit` | Sweeping `README.md` for link rot and proposing replacements | planned |
| `convention-check` | Validating table shapes, tags, and tracker sync before a commit | planned |

Once written, invoke as `/link-audit`, or let Claude match on the description.

### Adding one

```markdown
---
name: skill-name
description: What it does and when to use it. Match on the user's words, not internal jargon.
---

# Title

Numbered steps. Include the exact commands to run and what a bad result looks
like. Supporting files can live beside SKILL.md and be referenced by path.
```

## Which to write

Reach for a **skill** when the answer is "here are the steps and the commands." Reach for an **agent** when the work needs its own context — a long search, a review pass, a role to play — and you only want the conclusion back.
