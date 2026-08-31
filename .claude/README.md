# Project agents and skills

Scaffolding for Claude Code in this repository. Both directories are project-scoped — they apply to anyone working in this repo, and are versioned with it.

## Agents — `.claude/agents/*.md`

A subagent runs in its own context window with its own tool set, and reports back a result. Use one when a task is self-contained and you do not want its intermediate output in the main conversation.

| Agent | Use it for |
|---|---|
| `fact-checker` | Verifying version claims, dates, statistics, and links against primary sources |
| `qa-author` | Drafting or tightening `Q&A.md` entries in the house format |
| `roadmap-editor` | Editing `README.md` phases, concept tables, calendars, problem lists |
| `mock-interviewer` | Running a timed HLD/LLD mock and scoring it against the Section 10 rubric |

Invoke by naming one ("use the fact-checker on Section 12"), or let Claude select based on the `description` field.

### Adding one

```markdown
---
name: agent-name
description: One or two sentences on when to use this agent. This is what Claude matches against, so describe the trigger, not the implementation.
tools: Read, Grep, Glob, Bash    # optional; omit to inherit all tools
model: sonnet                     # optional: sonnet | opus | haiku | inherit
---

The system prompt. Write it as instructions to the agent: what to read first,
what the rules are, what to output.
```

Keep `description` trigger-shaped — it decides whether the agent gets picked. Narrow `tools` for read-only agents; a reviewer that cannot write cannot accidentally rewrite the thing it reviews.

## Skills — `.claude/skills/<name>/SKILL.md`

A skill is a procedure loaded into the current turn — a checklist Claude follows in place of improvising. Use one for a repeatable workflow with steps that are easy to get subtly wrong.

| Skill | Use it for |
|---|---|
| `add-question` | Adding a `Q&A.md` entry with correct placement, numbering, and cross-refs |
| `link-audit` | Sweeping both documents for link rot and proposing replacements |
| `convention-check` | Validating numbering, table shapes, tags, and tracker sync before a commit |

Invoke as `/add-question`, or let Claude match on the description.

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
