# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

DesignOdyssey is a **content repository**, not a software project: a self-study curriculum for HLD/LLD/AI system-design interviews, spanning junior (SDE-1) through staff/principal and on to an architect overlay. It is written as a **continuously updated reference**, so prose never describes the document's own past — no “previously”, no “new in this revision”, no changelog of what a section used to say. State what is true now; Section 15 carries the protocol for keeping it that way, and git carries the history. Everything of substance lives in one long Markdown file at the root, `README.md`. There is no build, no test suite, no package manager, and no application code — work here is editing prose, tables, and links.

`hld/` and `lld/` are placeholder IntelliJ Java modules: each has an `.iml` declaring a `src/` source root and an empty `src/` directory on disk (untracked, since git does not store empty directories). `hld/README.md` holds a short FR-vs-NFR note; `lld/README.md` is a stub that points back to Phase LLD and Section 7 of the root README rather than duplicating them. If Java example code is ever added, these modules are where it belongs.

`mocks/` holds one dated scorecard per mock interview, written by the `mock-interviewer` agent and committed so it can compare runs over time. `mocks/README.md` documents the filename convention and the YAML frontmatter schema — the frontmatter is what makes scores and recurring weaknesses machine-readable, so preserve it exactly when editing a scorecard by hand.

There is **no `docs/` directory, and analysis output does not become a committed report.** This repository is a live reference, not an archive: the current state of every claim lives in `README.md` Section 12, and git carries the history. Anything that would read as a snapshot of its own date — a gap analysis, an audit, a review, a changelog — belongs in the conversation and the commit message, not in a tracked file. When such an analysis finds something, fold the *finding* into `README.md` and let the report itself go. (`.claude/docs/` is unrelated and does exist — see **Agents and skills** below.)

`.idea/` is untracked; the root `.gitignore` covers it along with Python artifacts from `interview-curator/` and macOS cruft.

## Document architecture

**`README.md`** is the roadmap and the whole of the curriculum. Numbered top-level sections 0–15: how to use the doc and what is really in the repo (Section 0), a five-stage ladder with entry gates plus five week-by-week calendars and the arithmetic behind every timeline (Section 2), a map of which chapters of Alex Xu Vol. 1/Vol. 2 and DDIA to read or skip (Section 3), the **phase-by-phase syllabus** (Section 4), master problem lists (Sections 6–7), a mock scoring rubric (Section 10), a progress tracker to copy out (Section 11), a dated "verified current-state" appendix (Section 12), the canonical link index (Section 13), the repo's own agent/mock/curator tooling (Section 14), and the maintenance protocol — what to re-check, when, and the rules that do not bend (Section 15).

Eleven **Mermaid** diagrams are embedded (track structure, stage gates, phase dependencies, the scale ladder, RAG, LLM serving, cells, expand/contract, a feed sketch, an LLD class sketch). They are validated by rendering, not by eye — see the note under **Verification**. Add one only where prose cannot carry the point, and keep each small.

Two independent numbering schemes coexist and inline references sometimes conflate them: `README.md` has **Sections** 0–15 *and* **Phases** (0, 1, 1b, 2, 2b, 3, 3b, 4, 5, 6, 6b, 7, 8, AI, 9, 10, LLD, 11) inside Section 4. Before "fixing" a reference like `(Section 8)`, work out whether the author meant the section or the like-numbered phase — the Interview OS and the mock intensive are **Phases** 0 and 11, and the like-numbered Sections are different material. Every current reference has been checked, so treat a mismatch you find as a real bug rather than a documented quirk.

New material is added under **sub-numbers** (2.0, 2.5, 2.6, 6.1), **lettered phases** (2b, 3b, 6b) or a new trailing section, never by renumbering — inline references depend on the existing numbers.

## Conventions to preserve when editing

**Concept tables in Section 4 phases** come in two shapes, both in use: the full `| Concept | Type | Time | Why interviews | Resource |` (Phases 1, 2b, 3b, 6b, 10) and a compact `| Concept | Type | Time | Resource |` (Phases 1b, 2, 3, 4, 5, 6, 7, 8). Prefer the full shape for new tables; do **not** "fix" a compact one by inventing a *Why interviews* column. *Type* is one of the four legend tags defined in Section 0 and *Time* is an hour estimate — keep the estimate, because Section 2.6 sums that column to derive the stage budgets, and a row without it silently shrinks the total:

- 🟦 Fundamental — durable (CAP, consensus, indexing, isolation, SOLID)
- 🟩 Current practice — industry consensus that can shift
- 🟨 Vendor / cloud — AWS/GCP/Azure or product-specific
- 🟧 Emerging — know it exists; do not over-invest

Write the tag as a **literal emoji character**, never an escape sequence: a row that reads `\U0001f7e6` instead of 🟦 renders as raw text, drops out of the legend and is skipped by any script that sums the *Time* column by tag. Some rows carry a compound tag (`🟨/🟧`, `🟧→🟩`); count those too when totalling hours.

**Voice:** imperative and opinionated — "do this week", "weak:", "junior: skip implementation". Answers state trade-offs and name what fails an interview. Do not soften this into neutral encyclopedia prose, and do not pad sections with generic advice; the README explicitly positions itself as a sequencing tool, not a book substitute.

## Factual and link hygiene

This repo's value depends on claims being current and attributable, and it enforces that on itself:

- Time-sensitive claims (Kafka KRaft-only in 4.0, OpenTelemetry CNCF graduation, CNCF survey numbers) are consolidated in **Section 12** and dated. Anything new of that kind belongs there with its date and a primary source, not scattered inline.
- Never merge two different surveys into one trend line — Section 12 deliberately keeps the CNCF *annual survey* (organizations) and *State of Cloud Native Development* (developers) service-mesh numbers separate and labeled. Preserve that separation for any similar statistic.
- Prefer **stable domains** over deep links for engineering blogs, which reorganize URLs; Section 0 tells readers to search the site by post title when a deep link 404s.
- Papers link to primary sources (Raft, Dynamo, Spanner, GFS, TAO, PagedAttention, Orca); books are referenced by chapter, never linked to pirated copies.

## Agents and skills

Project-scoped definitions live in `.claude/` and are versioned with the repo. See `.claude/README.md` for the file formats and how to add more.

- **Agents** (`.claude/agents/`) — `mock-interviewer` (single round, or 10 researched questions, or a graded written answer) sits at the top level. Planned, not yet written: `fact-checker`, `roadmap-editor`. Everything under `agents/` is a real agent definition with `name` frontmatter; keep it that way.
- **Not an agent:** the daily reading-list curator is a Python-driven prompt at `interview-curator/prompt.md`, read by `interview-curator/curator_agent.py` and run from `.github/workflows/daily-brief.yml`. Edit it there.
- **The panel** (`.claude/agents/panel/`) — `interview-panel` orchestrates a full loop across five seats (`panel-hld-architect`, `panel-hld-deepdive`, `panel-lld-design`, `panel-lld-machine-coding`, `panel-bar-raiser`), then `panel-committee` weights the rounds and decides HIRE / NO HIRE. Claude Code scans `.claude/agents/` **recursively**, and a subfolder does not change how an agent is invoked — identity comes only from the `name` frontmatter field, which must stay unique across the whole tree.
- **Shared reference** (`.claude/docs/`) — material agents read **by path**, as opposed to definitions (`agents/`) or invoked procedures (`skills/`). Nothing here is loaded automatically; a file matters only because some agent's prompt names it. Keep it out of `agents/`, which is scanned for definitions. Today it holds `panel-charter.md` — the contract every seat obeys: turn protocol, evidence-with-quotes rule, the 1–5 scale anchored to Section 10, and the sealed-scorecard schema. Seats stay blind to each other during a loop; only `panel-committee` sees everything. **Edit the charter, not seven seat files, when a shared rule changes.**
- **Skills** (`.claude/skills/`) — the directory is **empty**; `add-question`, `link-audit`, and `convention-check` are planned, not yet written. Do the equivalent work by hand until they exist.

## Verification

There is nothing to compile or run. Useful checks after an edit:

```bash
grep -n "^#\{1,3\} " README.md      # section/heading outline
grep -o "](http[^)]*)" README.md    # links, if spot-checking for rot
grep -c '```mermaid' README.md      # diagram count (11 as of 26 Sep 2026)
```

**Validate Mermaid by rendering it, never by eye.** GitHub silently shows a broken diagram as an
error box, and the failure modes (an unquoted label, a reserved word as a node id) look fine in a
diff. Extract each block and render it with a **mermaid 11.x** CLI, which is the GitHub-compatible
line:

```bash
npx -y @mermaid-js/mermaid-cli@11 -i diagram.mmd -o /tmp/out.svg
```

A non-empty SVG means it parses. Keep diagrams small and split rather than growing one — a tangled
graph is a worse failure than no graph.

The `convention-check` skill will run the full set (tag legend, table shapes, cross-references, tracker sync, dated claims) and `link-audit` will sweep for link rot — neither is written yet.

Render the Markdown (GitHub-flavored: tables, emoji tags, nested links) before committing — table pipe alignment and the tag legend are the parts that break silently.
