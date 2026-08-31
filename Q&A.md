# Q&A — System Design (HLD & LLD) and AI engineering

Companion to [`README.md`](./README.md). Use this **after** you have attempted a design yourself. These are **talking tracks**, not scripts. Interviewers punish memorized component lists.

**How to practice:** Cover the question, sketch for 15 minutes, then read the “strong answer includes” bullets and the follow-ups.

**Living question sources** (re-check before a loop): Section 10.

---

## 1. Fundamentals (all levels)

### Q1. What is CAP, and why do people mis-state it?

**Ask:** Explain CAP. When does it apply?

**Strong answer includes:** CAP is about a **partition** (network split). You cannot have linearizable consistency **and** availability **for all clients** during a partition. It is not “pick two of three for all time.” Many systems are CA when the network is healthy. **PACELC** adds: if no partition, you still trade latency vs consistency (e.g. sync vs async replication).

**Follow-ups:** Dynamo vs Spanner. Is MongoDB CP or AP? (Depends on write concern / read concern — do not slogan.)

**Refs:** [Jepsen](https://jepsen.io/consistency) • DDIA Ch. 9 • Abadi PACELC (search).

---

### Q2. Strong vs eventual vs causal consistency — give a product example.

**Strong answer includes:** Strong/linearizable: “read sees the latest write” as if one copy (leader reads, Spanner, consensus). Eventual: replicas converge; stale reads OK (feeds, DNS). Causal: if A happened-before B, everyone sees A then B (comment threads). Read-your-writes / monotonic reads as **session** guarantees.

**Follow-up:** What does a news feed actually need? (Usually session + eventual globally.)

---

### Q3. How does Raft elect a leader?

**Strong answer includes:** Terms, randomized timeouts, majority votes, only one leader per term, log matching. Why majority: two leaders cannot both have majority. **KRaft** is Kafka’s Raft-based metadata quorum (not “Kafka uses ZK” in 4.x).

**Follow-up:** What happens to committed vs uncommitted entries on failover?

**Refs:** [raft.github.io](https://raft.github.io/) • [Kafka 4.0](https://kafka.apache.org/blog/2025/03/18/apache-kafka-4.0.0-release-announcement/).

---

### Q4. Quorum: why W + R > N?

**Strong answer includes:** Overlap of write set and read set so a reader hits at least one node that saw the write (under the model’s assumptions). Trade-off: W=N R=1 vs W=1 R=N vs W=R=(N+1)/2. Sloppy quorum / hinted handoff (Dynamo) weakens this — say so.

**Refs:** [Dynamo paper](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf).

---

### Q5. B-tree vs LSM-tree — when would you pick each?

**Strong answer includes:** B-tree: in-place pages, good point reads, write amplification from page splits; classic OLTP (InnoDB). LSM: memtable + sorted SSTables, fast sequential writes, compaction cost, read amplification (bloom filters help). LSM for high write ingest (Cassandra, RocksDB, time-series).

**Follow-up:** What is a WAL for?

**Refs:** DDIA Ch. 3 • Postgres/RocksDB docs.

---

### Q6. Isolation: what is write skew?

**Strong answer includes:** Two transactions read overlapping state, each writes a *different* row, both commit; invariant broken (two doctors on call, both go off). Snapshot isolation can miss this; serializable / SSI / SELECT FOR UPDATE / constraints as fixes. **Hotel rooms and seats** are the interview application.

**Refs:** DDIA Ch. 7.

---

### Q7. Snowflake IDs vs UUID vs DB autoincrement.

**Strong answer includes:** Autoincrement: simple, hotspot, not distributed. UUID v4: unique, 128-bit, random → index fragmentation. UUID v7: time-ordered (newer option — mention if current). Snowflake-class: 64-bit, time + worker + sequence, sortable, clock-skew risk, worker-id assignment (etcd). **Do not skip clock going backwards.**

**Follow-up:** How many IDs per ms per worker with 12 sequence bits? (4096.)

---

### Q8. Consistent hashing — why virtual nodes?

**Strong answer includes:** Map keys and nodes onto a ring; successor owns the key. Add/remove moves only a fraction of keys. Virtual nodes smooth imbalance and make heterogeneous capacity easier.

**Follow-up:** How do you migrate data without downtime? (Shadow, dual-write, range lock, Vitess-style.)

---

### Q9. At-least-once vs exactly-once.

**Strong answer includes:** Networks retry → at-least-once is the honest default. “Exactly-once” is **idempotent processing + dedup + (maybe) transactional produce/consume** (Kafka EOS has caveats across systems). Payments: **idempotency keys** (Stripe model). Dual-write problem → **outbox**.

**Refs:** [Stripe idempotency](https://stripe.com/blog/idempotency) • [Outbox](https://microservices.io/patterns/data/transactional-outbox.html).

---

### Q10. Estimate: 100M DAU, 5 posts/day average, 200 bytes/post. Storage for 5 years? QPS?

**Strong answer includes:** Write QPS ≈ 100e6 * 5 / 86400 ≈ 5800 average; peak 5–10×. Storage ≈ 100e6 * 5 * 365 * 5 * 200 ≈ 1.8e14 bytes ≈ **~180 TB** raw, more with replication/indexes. **Then use the numbers** (shard count, cache size). Wrong units fail.

**Refs:** Xu Vol. 1 Ch. 2 • [Latency numbers](https://gist.github.com/jboner/2841832) (orders of magnitude).

---

## 2. HLD — foundational

### Q11. Design a URL shortener.

**Strong answer includes:** Requirements (custom aliases? expiry? analytics?). 7-char base62 vs hash vs counter+encode. 301 vs 302 (cache vs stats). DB schema `(short_id PK, long_url, created, owner)`. Bloom filter for collisions if hashing. Cache hot redirects. Unique ID service. Scale reads ≫ writes.

**Follow-ups:** Hot key (celebrity link)? Analytics pipeline? GDPR delete?

**Refs:** Xu V1 Ch. 8 • [system-design-primer Pastebin](https://github.com/donnemartin/system-design-primer).

---

### Q12. Design a distributed rate limiter.

**Strong answer includes:** Token bucket vs leaky vs sliding window log vs sliding window counter. Placement: gateway vs service vs mesh. Redis + Lua for atomicity. Fail **open vs closed**. Per-tenant, per-endpoint, concurrent inflight. Stripe’s layered limiters (request, concurrent, etc.).

**Follow-ups:** Multi-region (eventual counters vs sticky region). Clock skew.

**Refs:** Xu V1 Ch. 4 • [Stripe rate limiters](https://stripe.com/blog/rate-limiters).

---

### Q13. Design a unique ID generator.

See Q7, then add: throughput (millions/s), availability (local generation), coordination only at worker-id lease. Alternatives: Instagram shard-id in PK, Sonyflake, Leaf (Meituan — search).

---

### Q14. Design a key-value store / cache.

**Strong answer includes:** API get/put/delete. Memory + persistence (WAL, snapshot). Consistent hashing, replication factor, leader vs leaderless. LRU/LFU/TTL. Cache stampede (lock, singleflight, probabilistic early expire). Persistence vs cache-aside.

**Follow-ups:** Split brain. Hot key. Rebalance.

**Refs:** Xu V1 Ch. 5–6 • Dynamo.

---

### Q15. Design a web crawler.

**Strong answer includes:** URL frontier (priority, politeness per host), DNS cache, robots.txt, bloom/seen-set, canonicalization, DFS vs BFS vs freshness, sitemap, renderer for JS (cost). Storage: HTML vs parsed. Respect crawl-delay.

**Follow-up:** How do you detect you’ve already seen a URL? Duplicate content?

**Refs:** Xu V1 Ch. 9.

---

## 3. HLD — intermediate

### Q16. Design Twitter / Instagram feed.

**Strong answer includes:** Fan-out on write (push to followers’ timelines) vs fan-out on read (pull from followees) vs hybrid (celebrity). Graph store vs cache of timeline. Media CDN. Ranking (Phase AI if ML ranker). Pagination cursors. Celebrity / “Taylor Swift problem.”

**Refs:** Xu V1 Ch. 11 • [TAO paper](https://www.usenix.org/system/files/conference/atc13/atc13-bronson.pdf) for graph reads.

---

### Q17. Design a notification system.

**Strong answer includes:** Priority, dedup, quiet hours, templates, channels (push, email, SMS, in-app). Queue per channel, retries, provider failover. User prefs store. Fan-out from events. Idempotent send. Metrics: delivery, opt-out.

**Refs:** Xu V1 Ch. 10.

---

### Q18. Design WhatsApp-style chat.

**Strong answer includes:** WS vs long poll vs SSE. Connection gateway (sticky). Message store (user inbox vs channel log). Online presence (heartbeat, Redis). Group fan-out. Encryption (E2E as a **constraint** — metadata still stored). Ordering per conversation. Media via object store + CDN.

**Follow-up:** Multi-device sync. Offline queue.

**Refs:** Xu V1 Ch. 12.

---

### Q19. Design search autocomplete.

**Strong answer includes:** Trie / ternary search tree vs cached top-k per prefix. Frequency ranking, personalization, typo (fuzzy). Update pipeline (batch vs stream). Sharding by prefix. Abuse / privacy (don’t leak rare private queries).

**Refs:** Xu V1 Ch. 13.

---

### Q20. Design Uber-style dispatch.

**Strong answer includes:** Location stream (throttled), geo index (geohash/H3/quadtree), matching (closest, ETA, fairness), surge as **pricing service**, trip state machine, notifications. Consistency: double-dispatch. Map/ETA as dependency.

**Refs:** Xu V2 proximity • Uber engineering (H3, marketplace — search blog).

---

### Q21. Design a distributed message queue.

**Strong answer includes:** Produce/consume API, persistence, replication, partitioning vs global order, at-least-once, consumer groups, dead letter, retention, backpressure. **Do not only say “Kafka.”** Compare log vs competing-consumers queue (SQS-style). Kafka 4 / KRaft if they go there.

**Refs:** Xu V2 Ch. 4.

---

### Q22. Design metrics monitoring and alerting.

**Strong answer includes:** Pull vs push, cardinality explosion, downsample, TSDB, recording rules, alert manager (group, inhibit, silence), on-call. SLIs vs raw metrics.

**Refs:** Xu V2 Ch. 5 • [SRE monitoring](https://sre.google/sre-book/monitoring-distributed-systems/).

---

### Q23. Design a gaming leaderboard.

**Strong answer includes:** Redis sorted sets, shard by game/season, hot top-N cache, cheat detection as async, replay. Why not SQL `ORDER BY score` at 10M writes/s.

**Refs:** Xu V2 Ch. 10.

---

## 4. HLD — advanced

### Q24. Design YouTube / Netflix streaming.

**Strong answer includes:** Upload → virus/scan → transcode ladder → packaging (HLS/DASH) → origin → CDN. Metadata DB. DRM. Playback tokens. Comments as separate scale. Cost of transcode vs storage.

**Refs:** Xu V1 Ch. 14 • Netflix tech blog (encoding, Open Connect — search).

---

### Q25. Design Google Drive / Dropbox.

**Strong answer includes:** Chunking, metadata service vs block servers, sync protocol, conflict (last-write vs versions), sharing ACLs, dedup, client notification.

**Refs:** Xu V1 Ch. 15 • [GFS](https://pdos.csail.mit.edu/6.824/papers/gfs.pdf).

---

### Q26. Design S3-like object storage.

**Strong answer includes:** PUT/GET/LIST, immutable objects, metadata index, data nodes, replication vs **erasure coding**, durability math, multipart, strong vs eventual listing. Control plane vs data plane.

**Refs:** Xu V2 Ch. 9.

---

### Q27. Design a payment system.

**Strong answer includes:** Idempotency keys, state machine (authorized → captured), ledger (double entry), PSP integration, webhooks, reconciliation, PCI scope minimization, saga for order+pay, exactly-once **business** effect. Failures: unknown PSP result.

**Refs:** Xu V2 Ch. 11 • [Stripe idempotency](https://stripe.com/blog/idempotency) • [Stripe API versioning](https://stripe.com/blog/api-versioning).

---

### Q28. Design a digital wallet.

**Strong answer includes:** Strong consistency on balances, ledger first, no lost updates, multi-currency, holds/authorizations, audit. 2PC vs single-ledger service.

**Refs:** Xu V2 Ch. 12.

---

### Q29. Design hotel reservation / ticket inventory.

**Strong answer includes:** Oversell vs lock, isolation (Q6), inventory rows vs Redis holds with TTL, payment timeout release, calendar sharding. Double-booking is the crux.

**Refs:** Xu V2 Ch. 7.

---

### Q30. Design ad-click aggregation.

**Strong answer includes:** Huge write QPS, exactly-once **counting** (or bounded error), stream + batch reconcilation, fraud, keyed state, watermark/late events.

**Refs:** Xu V2 Ch. 6 • Netflix Keystone / Flink blogs.

---

### Q31. Design collaborative documents.

**Strong answer includes:** OT vs CRDT, presence, persist ops, compact snapshots, conflict UX. Figma/CRDT vs Google OT narrative.

**Refs:** Figma multiplayer engineering post (search).

---

### Q32. Design a stock exchange matching engine.

**Strong answer includes:** Single-threaded matching per symbol (or deterministic parallel), order book, sequencing, persistence of the log, latency budget, fairness. **Staff only** unless they ask.

**Refs:** Xu V2 Ch. 13.

---

### Q33. Design multi-region checkout with data residency.

**Strong answer includes:** RPO/RTO, active-active conflict vs regional pin, GDPR data stays in-region, inventory vs payments consistency, cost of dual-write. **Do not default to global Spanner.**

---

## 5. LLD / OOD

### Q34. Design a parking lot (LLD).

**Strong answer includes:** Vehicle types, spots, entry/exit, ticket, pricing strategy (Strategy), occupancy index. No god `ParkingLot` doing payment + UI + persistence. Multi-floor.

**Follow-up:** EV charging, valet, reservations (OCP).

---

### Q35. Design an elevator system.

**Strong answer includes:** Separate **car** (state machine: idle/moving/doors) from **controller** (assignment). Hall vs cabin requests. SCAN/LOOK vs nearest-car; starvation. Thread-safe request queues. Strategy for dispatch.

**Follow-up:** Peak morning up-peak.

---

### Q36. Design LRU cache.

**Strong answer includes:** HashMap + doubly linked list, O(1) get/put. Thread safety (striping vs one lock). Capacity, eviction callback. LFU as follow-up (frequency lists).

---

### Q37. Design movie ticket booking (concurrency).

**Strong answer includes:** Seat as resource, hold vs confirm, optimistic version vs pessimistic lock vs DB unique `(show, seat)`. Idempotent book. Timeout of holds. **This is not a microservices question.**

---

### Q38. Design Splitwise.

**Strong answer includes:** Graph of balances vs simplified debts, expense with splits (equal, percent, shares), currency. Consistency of the ledger. Simplify algorithm as optional.

---

### Q39. Design a logging framework.

**Strong answer includes:** Logger, levels, appenders, formatters, async vs sync, MDC/context, backpressure when disk is slow. Singleton debate.

---

### Q40. Design a thread pool.

**Strong answer includes:** Worker threads, blocking queue, rejection policy, `keepAlive`, graceful `shutdown`/`awaitTermination`. Virtual threads **vs** a pool: cheap blocking I/O, not faster CPU work.

**Follow-up:** A tiny JDBC pool still bottlenecks under virtual threads. Structured concurrency is **preview** through JDK 25 — don’t claim it as production-default on Java 21 LTS.

---

### Q41. Design HashMap (Java-style).

**Strong answer includes:** Array of buckets, hash, collision (list → tree in Java 8+), load factor, resize, `equals`/`hashCode` contract. ConcurrentHashMap: bins, not one giant lock.

---

### Q42. SOLID — give an example from your elevator/parking design.

**Strong answer includes:** SRP: scheduler ≠ door motor. OCP: new `PricingStrategy` without editing callers. LSP: don’t make `Square` inherit `Rectangle` if it breaks setters. ISP: don’t force `FlyingCar` on `ParkingSpot`. DIP: depend on `Dispatcher` interface.

---

### Q43b. Design Unix `find` (Amazon-reported OOD).

**Strong answer includes:** Walker vs **Specification** predicates (`Name`, `Size`, `AND`/`OR`). New filter without editing DFS. Not a mini-Elasticsearch.

**Refs:** [LeetCode discuss — Amazon Unix file search](https://leetcode.com/discuss/interview-question/609070/amazon-ood-design-unix-file-search-api/)

---

### Q43. Which patterns do you actually use in LLD interviews?

**Strong answer includes:** Strategy (pricing, dispatch, payment), State (elevator, order), Observer (displays), Factory (vehicles), Decorator (streams/IO), Command (undo). **Anti-signal:** decorating every class with a pattern name.

**Refs:** [Refactoring.Guru](https://refactoring.guru/design-patterns).

---

## 6. AI engineering — basic

### Q44. Where would you put an LLM in a support product?

**Strong answer includes:** Not “replace the DB.” Flow: auth → retrieve trusted docs → build prompt with citations → generate → filter → stream to UI. Sync vs async. Human escalation. Cost cap per ticket.

---

### Q45. Design a RAG chatbot (the 2026 default AI HLD).

**Strong answer includes:**

1. Requirements: latency (TTFT vs total), languages, citations required?, stale-doc SLA, PII, cost/month.
2. Ingest: parse, chunk (size/overlap), metadata (ACL, time), embed, upsert index. Re-embed on model change.
3. Query: rewrite, **hybrid BM25 + dense**, fuse (RRF), rerank top 20–50, pack context.
4. Generate: system prompt, tool-less first; stream tokens.
5. Eval: retrieval recall, faithfulness, toxic/PII tests; golden set in CI.
6. Fallback: keyword search, template, human.
7. Ops: traces, token spend, index lag.

**Weak:** “We use LangChain and Pinecone” with no chunking/eval/ACL.

**Follow-ups:** How do you stop the model answering from parametric memory when docs disagree? (Prompt + refuse if retrieval empty; citations.)

---

### Q46. RAG vs fine-tuning vs prompt-only.

**Strong answer includes:** Prompt: quick, limited knowledge. RAG: **changing** corpus, citations, ACL. Fine-tune: style/format, stable domain, expensive to refresh. LoRA: cheaper adapter, still stale on facts. Mix: fine-tune format + RAG facts.

---

### Q47. Semantic cache vs exact cache vs prefix cache.

**Strong answer includes:** Exact: hash of prompt+params → stored **answer**. Semantic: embed query, nearest neighbor — **skips the LLM**, wrong-near-match and staleness risk; isolate tenants. **Prefix/prompt cache:** reuse **KV** for an *exact* token prefix; still generates a **fresh** completion (OpenAI/Anthropic product behavior). Put stable system/tools first, user text last.

**Refs:** [OpenAI prompt caching](https://openai.com/index/api-prompt-caching/) • [Anthropic prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)

---

### Q48. Token rate limiting.

**Strong answer includes:** QPS is the wrong unit. Budget input+output tokens, reserved vs on-demand, fair queuing, cheaper model cascade when over budget.

---

## 7. AI engineering — intermediate

### Q49. Hybrid search — why not vectors only?

**Strong answer includes:** Dense retrieval misses SKUs, error codes, names. BM25 catches lexical. Fuse then cross-encoder rerank. Operational: two indexes must stay in sync.

---

### Q50. How do you evaluate a RAG system?

**Strong answer includes:** Offline golden Q/A with graded docs; recall@k, MRR; answer quality (human + LLM-judge calibrated on a labeled subset); online: thumbs, regeneration, escalation rate, latency, cost. **Eval is part of the design**, not a footnote.

---

### Q51. Design semantic search (enterprise).

**Strong answer includes:** ACL-aware retrieval (filter in query, not after generate), incremental index, connectors, multilingual, hybrid, rerank, feedback loop. Same bones as RAG without generation — or with a extractive snippet.

---

### Q52. Feature store / embeddings in recsys.

**Strong answer includes:** Offline training vs online serving features must match (training-serving skew). Candidate retrieval (ANN) → ranker → re-ranker / rules. Michelangelo-style: train, deploy, monitor, freeze feature views.

**Refs:** [Uber Michelangelo](https://www.uber.com/blog/michelangelo-machine-learning-platform/) • [Uber generative AI on Michelangelo](https://www.uber.com/blog/from-predictive-to-generative-ai/).

---

### Q53. Guardrails and prompt injection.

**Strong answer includes:** Untrusted retrieved text and user input can override instructions. Treat tools as **authz** (allowlist, human-in-the-loop for side effects). Output filters. Isolation of system prompt. OWASP LLM Top 10 vocabulary.

**Refs:** [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/).

---

## 8. AI engineering — advanced

### Q54. Design LLM inference serving for millions of users.

**Strong answer includes:** Gateway (auth, quota, routing) → scheduler → GPU workers. **Prefill vs decode** different compute. **Continuous batching** (iteration-level) vs static batch. **KV cache** memory bound; **PagedAttention**-style paging. Prefix cache for shared system prompts. Autoscale on queue time and KV memory, not only CPU. Fallback model. Multi-region: cache locality vs GPU cost. Observability: TTFT, TPOT, tokens/s, GPU util, preemptions.

**Refs:** [vLLM PagedAttention](https://vllm.ai/blog/2023-06-20-vllm) • [vLLM anatomy](https://vllm.ai/blog/2025-09-05-anatomy-of-vllm) • [Anyscale continuous batching](https://www.anyscale.com/blog/continuous-batching-llm-inference).

---

### Q55. Why is KV cache the bottleneck?

**Strong answer includes:** Each decode step attends to all prior tokens; cache grows with batch × layers × seqlen. Fragmentation if you preallocate max length. Paging reduces waste (~last block only). Sharing prefixes via copy-on-write.

---

### Q56. Model routing / cascade.

**Strong answer includes:** Classifier or heuristic sends easy queries to small/cheap model; escalate on low confidence. Quality vs cost vs latency. A/B and eval gates.

---

### Q57. Distribute model weights to thousands of machines.

**Strong answer includes:** Size (tens–hundreds of GB), bandwidth, P2P (BitTorrent-like), chunked checksums, staged rollout, GPU RAM vs disk cache, failure resume. Same family as “design a file distribution system” with **version pinning**.

---

### Q58. Design a coding copilot / agent.

**Strong answer includes:** Context assembly (open files, repo search, RAG on code), model, tool calls (test runner, editor) with **sandbox and permissions**, loop limit, diff review, secrets not in prompts. MCP as a **tool protocol**, not a magic architecture. Eval on SWE-bench-style suites if they go there — know it exists.

---

### Q59. GPU multi-tenancy.

**Strong answer includes:** Time-slicing vs MIG vs one-model-per-GPU. Noisy neighbor on KV memory. Fairness, preemption of long generations. Cost attribution per tenant/token.

---

### Q60. Quantization in an interview — what to say.

**Strong answer includes:** Lower precision → more throughput / less memory, possible quality drop. Choose via **eval set**, not blog numbers. Speculative decoding: draft model + verify — latency trick, extra complexity.

---

## 9. Cross-cutting probes (use in every mock)

Interviewers often ignore your pretty diagram and ask:

- What is the **partition key** and the hottest key?
- What does the **user see** if Redis is down? If the LLM is down?
- How do you **roll back** a bad deploy / a bad prompt / a bad index?
- What is the **SLO** and the error budget?
- What does this **cost** at 10× traffic?
- How do you **test** the failure path?
- Who **on-calls** this, and what pages?

If you cannot answer these, the design is not senior-ready.

---

## 10. Reference links — latest questions and study feeds

Revisit these in the **month of your interviews**. Feeds beat static PDFs.

### Question databases and guided practice

| Resource | What you get |
|---|---|
| [Hello Interview — System Design in a Hurry](https://www.hellointerview.com/learn/system-design/in-a-hurry/introduction) | Framework, level expectations, staff guidance |
| [Hello Interview — question reports](https://www.hellointerview.com/premium/questions) | Community-reported prompts (filter System Design / LLD / company) |
| [Hello Interview — guided practice](https://www.hellointerview.com/practice/overview) | Timed HLD/LLD with feedback |
| [donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer) | Concepts + worked HLD/OOD |
| [ashishps1/awesome-system-design-resources](https://github.com/ashishps1/awesome-system-design-resources) | Curated free HLD list |
| [ashishps1/awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design) | LLD problems + links |
| [Hello Interview practice](https://www.hellointerview.com/practice/system-design) | Current HLD rotation (Bitly → ChatGPT) |
| [interviewing.io HLD guide](https://interviewing.io/guides/system-design-interview) | Rubric from mock interviewers |
| [DesignGurus — System Design Interview](https://www.designgurus.io/system-design-interview) | 2026-oriented concept + question patterns |
| [ByteByteGo](https://blog.bytebytego.com/) | Visual explainers aligned with Xu |
| [interviewing.io blog](https://interviewing.io/blog) | Interviewer-side write-ups |
| [Exponent system design](https://www.tryexponent.com/guides/system-design-interview) | Company-flavored guides |
| [AlgoMaster system design](https://algomaster.io/learn/system-design-interviews/design-unique-id-generator) | Individual problem walkthroughs (example ID generator) |

### Books (buy/legal)

- *System Design Interview* Vol. 1 & 2 — Alex Xu (Vol. 2 with Sahn Lam)
- *Designing Data-Intensive Applications* — Martin Kleppmann (**1e** mapping in README; **2e** Mar 2026 — map by topic, not chapter number)
- *Site Reliability Engineering* and *SRE Workbook* — [sre.google](https://sre.google/)

### Papers (primary sources)

- [Dynamo](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)
- [Raft](https://raft.github.io/)
- [Spanner](https://research.google/archive/spanner.html)
- [GFS](https://pdos.csail.mit.edu/6.824/papers/gfs.pdf)
- [TAO](https://www.usenix.org/system/files/conference/atc13/atc13-bronson.pdf)
- [PagedAttention paper](https://arxiv.org/abs/2309.06180) • [Orca / continuous batching (OSDI 2022)](https://www.usenix.org/conference/osdi22/presentation/yu)
- vLLM / PagedAttention: [vLLM blog 2023](https://vllm.ai/blog/2023-06-20-vllm)

### Company engineering blogs (search within)

- [Netflix Tech Blog](https://netflixtechblog.com/) — streaming, Keystone, chaos
- [Uber Engineering](https://www.uber.com/blog/engineering/) — marketplace, Michelangelo, Schemaless
- [Meta Engineering](https://engineering.fb.com/)
- [Stripe blog](https://stripe.com/blog) — idempotency, rate limits, API versioning, billing
- [LinkedIn Engineering](https://www.linkedin.com/blog/engineering) — Kafka, Espresso, feed
- [Airbnb Engineering](https://medium.com/airbnb-engineering)
- [AWS Architecture Blog](https://aws.amazon.com/blogs/architecture/)
- [Google SRE](https://sre.google/)
- [Cloudflare Blog](https://blog.cloudflare.com/)
- [Databricks Blog](https://www.databricks.com/blog)
- [Snowflake Engineering](https://www.snowflake.com/en/engineering-blog/)
- [OpenAI](https://openai.com/blog/) / [Anthropic](https://www.anthropic.com/engineering) — API and infra posts as they ship

### Independent / specialist

- [Jepsen](https://jepsen.io/)
- [Martin Fowler](https://martinfowler.com/)
- [microservices.io](https://microservices.io/) (Chris Richardson)
- [High Scalability](http://highscalability.com/)
- [Julia Evans](https://jvns.ca/)
- [Murat Demirbas](https://muratbuffalo.blogspot.com/)
- [Brendan Gregg](https://www.brendangregg.com/)
- [KDnuggets — answering AI system design](https://www.kdnuggets.com/how-to-answer-ai-system-design-interview-questions) (practitioner framing; verify against primary docs)

### Specs and current platform facts

- [Apache Kafka 4.0 announcement](https://kafka.apache.org/blog/2025/03/18/apache-kafka-4.0.0-release-announcement/)
- [OpenTelemetry docs](https://opentelemetry.io/docs/) • [CNCF OTel graduation](https://www.cncf.io/announcements/2026/05/21/cloud-native-computing-foundation-announces-opentelemetrys-graduation-solidifying-status-as-the-de-facto-observability-standard/)
- [Kubernetes Gateway API](https://kubernetes.io/docs/concepts/services-networking/gateway/)
- [CNCF State of Cloud Native Q3 2025](https://www.cncf.io/wp-content/uploads/2025/11/cncf_report_stateofcloud_111025a.pdf) (mesh adoption among developers)
- [OWASP API Security](https://owasp.org/www-project-api-security/)
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

### Company-specific loop intel (noisy — use as a checklist)

- Hello Interview company pages: [Meta](https://www.hellointerview.com/exams/meta), [Google](https://www.hellointerview.com/exams/google), [Amazon](https://www.hellointerview.com/exams/amazon), [OpenAI](https://www.hellointerview.com/exams/openai), [Anthropic](https://www.hellointerview.com/exams/anthropic) (URLs may redirect — search “Hello Interview &lt;company&gt; SWE”)
- Official prep: Amazon Leadership Principles + SDE FAQ; Google “how we interview”; Meta engineering career posts

**Hygiene:** Prefer **primary blogs and papers** over SEO “top 40 questions 2026” listicles. Use listicles only to **spot-check** that your practice set still matches the rotation, then return to Xu/DDIA/this Q&A.

---

## 11. Suggested mock order (if you only do 12)

1. URL shortener 2. Rate limiter 3. Unique IDs 4. LRU (LLD) 5. Parking lot or elevator (LLD) 6. News feed 7. Chat 8. Ticket booking (LLD concurrency) 9. Payments 10. RAG chatbot 11. KV store or object storage 12. LLM serving **or** multi-region checkout (level-dependent)

Score each with the rubric in [`README.md`](./README.md) Section 10.
