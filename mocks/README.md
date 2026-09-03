# Mock scorecards

One file per mock, written by the `mock-interviewer` agent at the end of a round. These are
the agent's memory: at the start of every mock it reads the most recent few, so it can
compare scores, spot a weakness that keeps recurring, and avoid re-asking a problem you
have already done.

Committed on purpose — mirrors `interview-curator/output/`, and a trend you cannot see
across machines is not a trend.

## Naming

Single round, from `mock-interviewer`:

```
mocks/YYYY-MM-DD-<problem-slug>-<level>.md
```

A full loop, from `interview-panel` — one file per seat plus the committee packet, all
sharing a `loop_id`:

```
mocks/loop-YYYY-MM-DD-<slug>-<seat>.md
mocks/YYYY-MM-DD-<slug>-<level>-packet.md
```

e.g. `mocks/2026-09-02-distributed-rate-limiter-senior.md`, or
`mocks/loop-2026-09-03-ride-dispatch-hld-deepdive.md`. If a name is taken, the agent appends
`-2` rather than overwriting — a re-run is a separate data point.

**`loop_id` is what keeps the arithmetic honest.** Without it, four rounds of one loop look
like four independent mocks and the Mock avg counts one candidate four times. Seat files
always carry it; single-round files never do.

## Format

YAML frontmatter, then the report body verbatim. **The frontmatter is the machine-readable
part**; if it is malformed the trend silently breaks, so it comes first and is exact.

```markdown
---
date: 2026-09-02
problem: Distributed rate limiter
problem_tier: foundational        # foundational | intermediate | advanced (README §6/§7)
level: senior                     # junior | senior | staff
format: 45-min HLD                # the Section 5 format actually used
round_type: HLD                   # HLD | LLD | AI — which dimension set was scored
score: 6.6
verdict: hire
hints_spent: 1
ratings:                          # dimension: rating (1-5) or n/a
  requirements: 4
  estimation: 3
  data_model: 4
  apis: 3
  trade_offs: 3
  reliability: 2
  ai: n/a
  communication: 4
weaknesses:                        # short slugs, stable across runs so recurrence is detectable
  - no-fallback-on-redis-outage
  - capacity-math-unused
---

<the eleven-part report>
```

Panel seat files add `seat:`, `loop_id:`, `model:`, and — for the bar raiser —
`level_verdict:` and optional `bar_concern:`. The committee packet adds `loop_id:`,
`loop_score:`, `decision:` (`HIRE` / `NO HIRE`), and `round_weights:`.

**`model:`** records which model graded the round, because the panel picks per round by
level. Two loops graded on different models are not identical instruments — keep the field
so a score delta can be read honestly rather than over-interpreted.

## Field notes

- **`problem_tier`** is what keeps scores comparable. A 7.2 on a foundational problem and a
  7.2 on an advanced one are different results; without the tier, a "trend" is noise.
- **`round_type`** records which dimension set produced the score. HLD, LLD, and AI rounds
  are scored on different dimensions, so a delta across types compares only the /10, never
  the per-dimension ratings.
- **`weaknesses`** are short kebab-case slugs, reused verbatim across runs. That reuse is
  the whole recurrence mechanism — a rephrased slug reads as a brand-new weakness and the
  "recurring — 3rd time" flag never fires.
- **`ratings`** keys follow the dimension names of the set named in `round_type`.

## Mock average

Section 11 of the root `README.md` has a **Mock avg** column. It is the mean of `score`
across the files here — filtered to one level and one `round_type` when you want it to mean
something.

**Count each loop once.** For files carrying a `loop_id`, use the packet's `loop_score`, not
the individual seat scores; averaging the seats in alongside single-round mocks weights one
candidate four or five times over.
