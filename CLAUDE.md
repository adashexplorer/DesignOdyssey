# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

DesignOdyssey is a **content repository**, not a software project: a self-study curriculum for HLD/LLD/AI system-design interviews, spanning junior (SDE-1) through staff/principal. Everything of substance lives in one long Markdown file at the root, `README.md`. There is no build, no test suite, no package manager, and no application code — work here is editing prose, tables, and links.

`hld/` and `lld/` are placeholder IntelliJ Java modules: each has an `.iml` declaring a `src/` source root and an empty `src/` directory on disk (untracked, since git does not store empty directories). `hld/README.md` holds a short FR-vs-NFR note; `lld/README.md` is empty. If Java example code is ever added, these modules are where it belongs.

`mocks/` holds one dated scorecard per mock interview, written by the `mock-interviewer` agent and committed so it can compare runs over time. `mocks/README.md` documents the filename convention and the YAML frontmatter schema — the frontmatter is what makes scores and recurring weaknesses machine-readable, so preserve it exactly when editing a scorecard by hand.

`.idea/` is untracked; the root `.gitignore` covers it along with Python artifacts from `interview-curator/` and macOS cruft.

## Document architecture

**`README.md`** is the roadmap and the whole of the curriculum. Numbered top-level sections 0–13: how to use the doc, four tracks with week-by-week calendars (Section 2), a map of which chapters of Alex Xu Vol. 1/Vol. 2 and DDIA to read or skip (Section 3), the **phase-by-phase syllabus** (Section 4), master problem lists (Sections 6–7), a mock scoring rubric (Section 10), a progress tracker to copy out (Section 11), a dated "verified current-state" appendix (Section 12), and the canonical link index (Section 13).

Two independent numbering schemes coexist and inline references sometimes conflate them: `README.md` has **Sections** 0–13 *and* **Phases** (0, 1, 1b, 2–9, AI, LLD, 11) inside Section 4. Before "fixing" a reference like `(Section 8)`, work out whether the author meant the section or the like-numbered phase — several existing refs point at the wrong one.

## Conventions to preserve when editing

**Concept tables in Section 4 phases** use the column shape `| Concept | Type | Time | Why interviews | Resource |`, where *Type* is one of the four legend tags defined in Section 0 and *Time* is an hour estimate:

- 🟦 Fundamental — durable (CAP, consensus, indexing, isolation, SOLID)
- 🟩 Current practice — industry consensus that can shift
- 🟨 Vendor / cloud — AWS/GCP/Azure or product-specific
- 🟧 Emerging — know it exists; do not over-invest

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
```

The `convention-check` skill will run the full set (tag legend, table shapes, cross-references, tracker sync, dated claims) and `link-audit` will sweep for link rot — neither is written yet.

Render the Markdown (GitHub-flavored: tables, emoji tags, nested links) before committing — table pipe alignment and the tag legend are the parts that break silently.
