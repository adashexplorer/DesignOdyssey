# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

DesignOdyssey is a **content repository**, not a software project: a self-study curriculum for HLD/LLD/AI system-design interviews, spanning junior (SDE-1) through staff/principal. Everything of substance lives in two long Markdown files at the root. There is no build, no test suite, no package manager, and no application code — work here is editing prose, tables, and links.

`HighLevelDesign/` and `LowLevelDesign/` are placeholder IntelliJ Java modules: each has an `.iml` declaring a `src/` source root and an empty `src/` directory on disk (untracked, since git does not store empty directories). `HighLevelDesign/README.md` holds a short FR-vs-NFR note; `LowLevelDesign/README.md` is empty. If Java example code is ever added, these modules are where it belongs.

`.idea/` is untracked and there is no root `.gitignore`.

## Document architecture

The two root files are a **paired system** and are meant to be read in a specific order — the README explicitly tells the reader to attempt a design first, then open `Q&A.md`. Edits to one usually imply an edit to the other.

- **`README.md`** — the roadmap. Numbered top-level sections 0–13: how to use the doc, four tracks with week-by-week calendars (Section 2), a map of which chapters of Alex Xu Vol. 1/Vol. 2 and DDIA to read or skip (Section 3), the **phase-by-phase syllabus** (Section 4), master problem lists (Sections 6–7), a mock scoring rubric (Section 10), a progress tracker to copy out (Section 11), a dated "verified current-state" appendix (Section 12), and the canonical link index (Section 13).
- **`Q&A.md`** — the companion answer bank: Q1–Q60 grouped fundamentals → HLD foundational/intermediate/advanced → LLD/OOD → AI basic/intermediate/advanced, plus cross-cutting probes and a living link section.

Two independent numbering schemes coexist and inline references sometimes conflate them: `README.md` has **Sections** 0–13 *and* **Phases** (0, 1, 1b, 2–9, AI, LLD, 11) inside Section 4. Before "fixing" a reference like `(Section 8)`, work out whether the author meant the section or the like-numbered phase — several existing refs point at the wrong one.

## Conventions to preserve when editing

**Concept tables in Section 4 phases** use the column shape `| Concept | Type | Time | Why interviews | Resource |`, where *Type* is one of the four legend tags defined in Section 0 and *Time* is an hour estimate:

- 🟦 Fundamental — durable (CAP, consensus, indexing, isolation, SOLID)
- 🟩 Current practice — industry consensus that can shift
- 🟨 Vendor / cloud — AWS/GCP/Azure or product-specific
- 🟧 Emerging — know it exists; do not over-invest

**Q&A entries** follow a fixed skeleton, each separated by `---`:

```
### Q<n>. <Question title>

**Ask:** <optional: how an interviewer phrases it>

**Strong answer includes:** <the talking track>

**Weak:** <optional: the answer that fails>

**Follow-ups:** <probes, often with the expected answer in parentheses>

**Refs:** <links • book chapters, bullet-separated with •>
```

Question numbers are **stable identifiers**. Insert a new question with a letter suffix at its topical position (`Q43b` sits before `Q43`) rather than renumbering the file.

**Voice:** imperative and opinionated — "do this week", "weak:", "junior: skip implementation". Answers state trade-offs and name what fails an interview. Do not soften this into neutral encyclopedia prose, and do not pad sections with generic advice; the README explicitly positions itself as a sequencing tool, not a book substitute.

## Factual and link hygiene

This repo's value depends on claims being current and attributable, and it enforces that on itself:

- Time-sensitive claims (Kafka KRaft-only in 4.0, OpenTelemetry CNCF graduation, CNCF survey numbers) are consolidated in **Section 12** and dated. Anything new of that kind belongs there with its date and a primary source, not scattered inline.
- Never merge two different surveys into one trend line — Section 12 deliberately keeps the CNCF *annual survey* (organizations) and *State of Cloud Native Development* (developers) service-mesh numbers separate and labeled. Preserve that separation for any similar statistic.
- Prefer **stable domains** over deep links for engineering blogs, which reorganize URLs; Section 0 tells readers to search the site by post title when a deep link 404s.
- Papers link to primary sources (Raft, Dynamo, Spanner, GFS, TAO, PagedAttention, Orca); books are referenced by chapter, never linked to pirated copies.

## Agents and skills

Project-scoped definitions live in `.claude/` and are versioned with the repo. See `.claude/README.md` for the file formats and how to add more.

- **Agents** (`.claude/agents/`): `fact-checker` (verify claims and links against primary sources, read-only), `qa-author` (draft `Q&A.md` entries in the house format), `roadmap-editor` (edit README phases, tables, calendars), `mock-interviewer` (run a timed mock, score against the Section 10 rubric).
- **Skills** (`.claude/skills/`): `add-question`, `link-audit`, `convention-check`.

## Verification

There is nothing to compile or run. Useful checks after an edit:

```bash
grep -n "^#\{1,3\} " README.md            # section/heading outline
grep -o "^### Q[0-9]*[a-z]*\." "Q&A.md"     # question numbering integrity
grep -o "](http[^)]*)" README.md "Q&A.md"   # links, if spot-checking for rot
```

The `convention-check` skill runs the full set (numbering, entry skeleton, tag legend, table shapes, cross-references, tracker sync, dated claims); `link-audit` sweeps for link rot.

Render the Markdown (GitHub-flavored: tables, emoji tags, nested links) before committing — table pipe alignment and the tag legend are the parts that break silently.
