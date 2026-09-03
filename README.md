# DesignOdyssey — HLD, LLD & AI-aware System Design

Interview-ready preparation from **junior (SDE-1 / L3)** through **staff/principal (L6–L8)**. Classic product and infrastructure design plus the AI layer that 2026 loops actually probe.

This document is a **living tracker**, not a book substitute. Use it to sequence work, pick problems at your level, and score mocks. Depth lives in the books, papers, and blogs linked below.

---

## 0. How to use this document

- Copy the **Progress Tracker** (Section 11) into your notes and update it weekly.
- Every concept is tagged:
  - 🟦 **Fundamental** — CAP, consensus, indexing, isolation, SOLID
  - 🟩 **Current practice** — industry consensus that can shift in a few years
  - 🟨 **Vendor / cloud** — AWS/GCP/Azure or product-specific
  - 🟧 **Emerging** — know it exists; over-invest only if the role needs it
- **Never spend more than two weeks on pure theory before a timed mock.** Pattern recognition under time pressure is the skill being graded.
- **Draw a design before you read anyone's answer.** Memorizing answers without a framework fails the first follow-up.
- Some links are **stable domains** (engineering blogs reorganize URLs). Search the site for the post title if a deep link 404s.

### What interviewers grade in 2026 (all levels)

Across Hello Interview, DesignGurus, interviewing.io write-ups, and company blogs, rubrics cluster on the same four themes (wording differs by company):

1. **Problem navigation** — requirements, scope, assumptions, time management
2. **Solution design** — coherent architecture, data model, APIs, justified scale
3. **Technical excellence** — correct primitives, current tech, trade-offs including **cost**
4. **Communication** — structure, collaboration, driving vs waiting to be led

**What moved since ~2021:** cost reasoning and operational maturity (observability, rollback, on-call) are graded explicitly at senior+. **AI-adjacent literacy** (where a model/retrieval/GPU sits, latency/cost/failure) is expected in general SWE loops when the product has an ML surface — not only in ML-specialist roles. Over-proposing multi-region active-active or event sourcing without a requirement is a **negative** judgment signal.

---

## 1. Critical review of the previous plan

The prior README was a strong **staff-track Java/Spring** plan. It was *not* a complete junior-to-staff curriculum and it under-mapped the books and problem sets interviewers still use.

### What was already correct (keep)

- 2026 rubric: trade-offs, capacity math *used* in decisions, cost, ops, driving the room
- PACELC, consistency models, Raft, Dynamo, Spanner as non-negotiable papers at senior+
- Hands-on projects (toy Raft, sharded KV, saga, outbox, Resilience4j, OpenTelemetry)
- Kafka **KRaft-only as of 4.0** (released 18 Mar 2025) — still accurate
- OpenTelemetry **CNCF graduation** (project graduated 11 May 2026; CNCF announcement 21 May 2026)
- Senior vs staff behavioral table and mock scoring rubric
- “Right-size the architecture” as a first-class skill

### Gaps vs the canon (filled in this revision)

| Source | Gap in the old plan | Now |
|---|---|---|
| **Alex Xu Vol. 1** | Problem list omitted unique ID generator, search autocomplete, consistent hashing as a *design*, and the “scale from 0 → millions” / estimation chapters as dedicated skills | Section 4 + Phase 1b + master HLD list |
| **Alex Xu Vol. 2** | Almost unused: proximity/geo, maps, distributed MQ, metrics/alerting, hotel reservation, email, S3/object storage, leaderboard, digital wallet, stock exchange | Master HLD list + Phase 9 |
| **DDIA (Kleppmann)** | Strong on replication/sharding/consensus; thin on encoding/schema evolution, isolation levels, unreliable clocks, CDC, column vs row, batch vs stream as *derived data* | Phase 1–3 + DDIA map in Section 3 |
| **Levels** | Written only for 10+ YOE Java → staff | Four tracks (Section 2) |
| **LLD** | Short Java list; little SOLID, UML, Java 21 virtual threads, machine-coding cadence | Phase LLD + expanded problem list |
| **AI engineering** | Four “staff-signal” problems bolted on | Full **basic / intermediate / advanced** ladder woven into HLD (Phase AI) |
| **Caching & estimation** | Mentioned in failure modes, not taught as primitives | Phase 1b |
| **Geo, bloom filters, Merkle trees, WAL, erasure coding** | Ride-sharing only; crawler without bloom/URL frontier detail | Phase 2 / 9 |
| **Service mesh stats** | Cited “~50% → 42% YoY” without naming the survey | Two *different* CNCF numbers, labeled (Appendix) |

### Honest limits of any roadmap

Interview reports on Glassdoor/Blind/Hello Interview are **noisy**. Companies rotate questions. This plan covers the **stable primitives** and the **current rotation**. It does not guarantee a specific prompt. Depth on 8–12 designs beats shallow coverage of 40.

---

## 2. Four tracks and timelines

Pick **one** primary track. Do not mix “junior breadth” with “staff papers” in the same week.

| | **Junior / SDE-1** | **Mid / SDE-2** | **Senior** | **Staff / Principal** |
|---|---|---|---|---|
| Typical titles | Google L3; Amazon SDE-1 ≈ L4 | Google L4; Amazon SDE-2 ≈ L5 | Google L5; Amazon Senior SDE ≈ L6 | Google L6+; Amazon Principal ≈ L7 |
| HLD in loop? | Often **no** or a light 30-min; **LLD / machine coding** is the design round at many companies (Amazon, Uber, Flipkart, Atlassian, many India product firms) | Usually **one** HLD | One or two HLD; depth + trade-offs | HLD is a **hiring bar** round; you drive scope, cost, org, AI/ops |
| Duration @ 8–10 hrs/wk | **14–16 weeks** | **16–20 weeks** | **20–24 weeks** | **22–24 weeks** *or* **10–12 weeks intensive** (~18–20 hrs/wk) |
| Books | Xu Vol. 1 Ch. 1–3, 4, 6, 8; primer GitHub | Xu Vol. 1 full; DDIA Ch. 3, 5, 6 | Xu Vol. 1 + selected Vol. 2; DDIA Parts I–II | Both Xu volumes; DDIA full; 4–6 papers |
| Mocks start | Week 3 (LLD first) | Week 4 | Week 6–8 | Week 3 (intensive) or Week 8 (standard) |
| AI depth | Basic: where LLM/RAG sits, caching, rate limits | Intermediate: hybrid retrieval, evals, cost/token | Intermediate + serving sketch | Advanced: GPU, batching, KV cache, evals, agents as *systems* |

**Rule for all tracks:** junior candidates who dump Kubernetes + Kafka + Spanner on a parking-lot LLD **fail**. Staff candidates who only recite Xu diagrams without cost/failure **fail**.

### 2.1 Junior — 16-week calendar (8–10 hrs/week)

| Weeks | Focus | Outcome |
|---|---|---|
| 1–2 | Interview OS (Section 8), OOP/SOLID, 4 GoF patterns you will actually use | Can run a 45-min LLD without freezing |
| 3–5 | LLD classics: parking lot, LRU, rate limiter, logger, vending machine | Working code + class diagram |
| 6–8 | Concurrency: thread safety, producer-consumer, Java 21 virtual threads *or* language equivalent | Ticket booking / cache under races |
| 9–11 | HLD fundamentals: scale ladder, estimation, caching, SQL vs NoSQL, load balancer, unique IDs, URL shortener, rate limiter | First timed 45-min HLD |
| 12–13 | Feed **or** chat **or** notifications (pick one) | One end-to-end product design |
| 14 | AI basic: RAG chatbot sketch, no GPU deep dive | Know when to retrieve vs generate |
| 15–16 | Mocks + weak spots | 4–6 timed mocks |

### 2.2 Mid — 20-week calendar

Junior plan compressed into weeks 1–8, then: KV store, news feed, chat, notification, web crawler, autocomplete; DDIA Ch. 5–6; one geo **or** metrics design; AI intermediate (hybrid search + evals); mocks from week 4 (1/week) then 2/week in the last month.

### 2.3 Senior — 24-week standard (employed, ~8–10 hrs/week)

| Weeks | Phases |
|---|---|
| 1 | Interview OS + 2026 rubric |
| 2–4 | Distributed fundamentals + DDIA Ch. 5–9 core ideas |
| 5–7 | Data layer + encoding/CDC/isolation |
| 8–9 | Messaging, streams, outbox, CQRS |
| 10–11 | APIs, gateways, rate limiting |
| 12–13 | Reliability |
| 14–15 | Multi-region, DR, cost |
| 16–17 | Observability, deploy, on-call |
| 18 | Security |
| 19–21 | Two specializations (Xu Vol. 2 + AI serving **or** payments **or** storage) |
| Parallel | LLD 2–3 hrs/week |
| 20–24 | Mock intensive (Section 11) |

### 2.4 Staff — intensive 12-week (loop scheduled, ~18–20 hrs/week)

Same as the former “ACTIVE PLAN,” with **AI ladder in weeks 7–8** (not a skim) and **Xu Vol. 2** problems mixed into mocks.

| Week | HLD (main) | LLD (evenings) | Hands-on | Mocks |
|---|---|---|---|---|
| **1** | Interview OS + CAP/PACELC, consistency, Raft | OOD patterns + SOLID | Toy Raft election | Baseline diagnostic |
| **2** | Idempotency, failure detection, indexing, sharding, replication, **unique IDs** | Thread pools, locks vs CAS, virtual threads | Sharded KV + consistent hashing | 1 untimed framework mock |
| **3** | 2PC/Saga, isolation, distributed SQL landscape, **encoding/CDC** | In-memory rate limiter | Saga + compensations | 2 timed (URL shortener, rate limiter) |
| **4** | Kafka/KRaft, EOS, CQRS, event sourcing, outbox, **batch vs stream (DDIA 10–11)** | Movie booking concurrency | Event-sourced order + outbox | 2 timed |
| **5** | API/gateway + reliability + **estimation drills** | Elevator or parking lot | Resilience4j + chaos | 2 timed |
| **6** | Multi-region/DR/cost + OTel/SLOs | LRU/LFU + thread safety | Failover sim + OTel | 2 HLD + 1 LLD |
| **7** | Security + **AI basic+intermediate** (RAG, hybrid retrieval, evals, cost) | Notification dispatcher | OAuth2 + mTLS | 2 timed (incl. RAG chatbot) |
| **8** | **AI advanced** (LLM serving, batching, KV cache, GPU) + one Xu Vol. 2 (payments **or** object storage **or** metrics) | Distributed cache LLD | Optional: vLLM docs skim | 3 adversarial mocks |
| **9** | Weak spots + geo **or** leaderboard **or** hotel inventory | Chess or Splitwise | — | 3 mocks |
| **10** | Staff polish: drive room, cost/ops/org unprompted | Catch-up LLD | — | 3 incl. 60-min deep dive |
| **11** | Optional: stock exchange / video / multi-region checkout / weight distribution | — | — | 3 mocks |
| **12** | Taper — no new theory | — | — | 1–2 confidence mocks |

If the loop is sooner: drop week 11, then merge 9–10.

---

## 3. Map to the three books (and what to skip)

### 3.1 *System Design Interview – An Insider’s Guide* (Alex Xu), Volume 1

Use this for **how to talk in 45 minutes** and for the classic product set. It is not a distributed-systems textbook.

| Chapter | Interview use | Track |
|---|---|---|
| 1 Scale from zero to millions | Vertical/horizontal scale, cache, CDN, DB replica, shard — **must be fluent** | All |
| 2 Back-of-envelope | QPS, storage, bandwidth; **use the numbers later** | Mid+ |
| 3 Framework | Clarify → estimate → design → deep dive | All |
| 4 Rate limiter | Token/leaky/sliding window; Redis | All |
| 5 Consistent hashing | Ring, virtual nodes, rebalance | Mid+ |
| 6 Key-value store | The “mini Dynamo” | Senior+ |
| 7 Unique ID generator | UUID vs ticket vs **Snowflake**; clock skew | **All (was missing)** |
| 8 URL shortener | Hash, 301 vs 302, bloom, DB | All |
| 9 Web crawler | Frontier, politeness, bloom, DFS vs BFS | Mid+ |
| 10 Notification | Fan-out, queues, APNs/FCM | Mid+ |
| 11 News feed | Fan-out on write vs read | Mid+ |
| 12 Chat | WS vs long poll, presence, message store | Mid+ |
| 13 Search autocomplete | Trie vs cache, ranking | **Mid+ (was missing)** |
| 14 YouTube | Upload, transcode, CDN | Senior+ |
| 15 Google Drive | Metadata vs block, sync | Senior+ |

### 3.2 Volume 2 (Xu & Lam)

Use after Vol. 1. Each chapter is a **domain crux**, not a new framework.

| Chapter | Crux interviewers pull on |
|---|---|
| Proximity service | Geohash / quadtree, load on hot cells |
| Nearby friends | Realtime location, pub/sub, privacy |
| Google Maps | Tiles, routing graph, ETA |
| Distributed message queue | Durability, ordering, delivery, consumer groups |
| Metrics monitoring | Time-series, downsample, alert fan-out |
| Ad click aggregation | Exactly-once-ish counting, λ-architecture / streaming |
| Hotel reservation | Inventory, double-booking, isolation |
| Distributed email | Mailbox sharding, send vs store |
| S3-like object storage | Data vs metadata, erasure coding, durability 11 nines narrative |
| Gaming leaderboard | Sorted sets, sharding hot keys |
| Payment system | Idempotency, ledger, PSP, reconciliation |
| Digital wallet | Strong consistency on balances, dual ledger |
| Stock exchange | Matching engine, determinism, latency |

### 3.3 *Designing Data-Intensive Applications* (Kleppmann)

This is the **why**. Interview prep that only reads Xu is easy to crack with “what happens if the leader dies?”

**Edition note (2026):** Kleppmann + Riccomini **2e** shipped March 2026 ([Kleppmann’s announcement](https://martin.kleppmann.com/2026/03/24/designing-data-intensive-applications-2e.html)). Chapter **numbers and MapReduce emphasis changed**. The table below is **1e**, which is still what most notes, blogs, and interviewers share. If you own 2e, map by *topic name* (replication, partitioning, isolation, streams), not chapter number.

| DDIA | Interview talking points | When to read |
|---|---|---|
| Ch. 1 Reliability, scalability, maintainability | Latency percentiles, operability | All (skim) |
| Ch. 2 Data models | Relational vs document vs graph; query shapes | Mid+ |
| Ch. 3 Storage | **B-tree vs LSM**, WAL, compaction, OLTP vs OLAP, column stores | Mid+ |
| Ch. 4 Encoding | JSON vs Avro/Protobuf, **schema evolution**, compatibility | Senior+ |
| Ch. 5 Replication | Single-leader, multi-leader, leaderless, lag, failover | **All mid+ (highest ROI)** |
| Ch. 6 Partitioning | Key range vs hash, secondary indexes, rebalance, request routing | **All mid+** |
| Ch. 7 Transactions | Isolation levels, lost update, write skew, SSI | Senior+ |
| Ch. 8 Trouble with distributed systems | Unreliable clocks, truth vs majority, network partitions | Senior+ |
| Ch. 9 Consistency & consensus | Linearizability, total order broadcast, Raft/Paxos *ideas* | Senior+ |
| Ch. 10 Batch | MapReduce/Spark as derived data; not “Hadoop trivia” | Senior / data-heavy roles |
| Ch. 11 Stream | Messaging vs log, windows, exactly-once claims | Senior+ |
| Ch. 12 Future | Unbundling DB; CDC as integration | Staff skim |

**Time-boxed DDIA:** If you have one weekend before onsites, read **Ch. 5 and 6 only** (~4–6 hours). Do not attempt the whole book in three days.

**Other books (optional):** *Understanding Distributed Systems* (Costa) for a shorter theory pass; Google SRE book (free) for SLOs/overload; *Designing Machine Learning Systems* (Huyen) if the loop is ML-platform heavy.

**Grokking catalog split:** Original *Grokking the System Design Interview* now lives at [DesignGurus](https://www.designgurus.io/course/grokking-the-system-design-interview) (classic ~15 problems). [Educative’s “Grokking”](https://www.educative.io/courses/grokking-the-system-design-interview) is a **diverged** catalog (Maps, ChatGPT, etc.). Do not treat them as the same course.

---

## 4. Phase-by-phase roadmap

### Phase 0 — Interview operating system (Week 1 of every track)

**Outcome:** You can run the framework from memory. You stop giving 2019-era “just add Kafka” answers.

**7-step framework (use this every HLD mock):**

1. **Clarify & scope** (functional + non-functional). State assumptions. Cut scope out loud.
2. **Back-of-envelope** (users, QPS, storage, bandwidth, machines). Write units.
3. **APIs** (or events). Idempotency, pagination, error model.
4. **Data model** (entities, access patterns, partition key, indexes).
5. **High-level diagram** (clients → edge → services → data stores → async).
6. **Deep dives** (1–2 bottlenecks the interviewer cares about).
7. **Failure, ops, cost, evolution** (degraded path, SLO, rollback, $). Senior+ do this **unprompted**.

Xu’s published framework is 4 steps (clarify, estimate, design, deep dive). The extra three are what 2026 senior+ loops actually grade. In a **30-minute** screen, collapse 2 and 7.

**Do this week:** Write the 7 steps on one page. Read 3 recent debriefs for *your* target companies (Hello Interview question DB, team blogs — not only Glassdoor).

---

### Phase 1 — Distributed systems fundamentals

**Outcome:** Derive trade-offs; do not recite CAP as “choose two.”

| Concept | Type | Time | Why interviews | Resource |
|---|---|---|---|---|
| CAP (and common mis-statements) | 🟦 | 1.5 h | Every DB answer | [Jepsen analyses](https://jepsen.io/analyses) — skim 2–3 DBs you know |
| PACELC | 🟦 | 1 h | Latency vs consistency when *no* partition | Search: Abadi PACELC (2010) |
| Consistency models | 🟦 | 2.5 h | “How consistent does this *need* to be?” | [Jepsen consistency](https://jepsen.io/consistency) |
| Consensus, Raft, quorum W+R>N | 🟦 | 4 h | etcd, KRaft, locks | [raft.github.io](https://raft.github.io/) |
| Clocks: Lamport, vector, HLC, NTP failure | 🟦 | 2 h | Conflicts, Snowflake, Spanner | Dynamo §versioning; DDIA Ch. 8 |
| Gossip, phi-accrual, membership | 🟩 | 1 h | Discovery, Cassandra-style | Hayashibara phi-accrual paper (search) |
| Idempotency & delivery semantics | 🟦 | 1.5 h | Payments, queues | [Stripe — idempotency](https://stripe.com/blog/idempotency) |
| Unreliable networks / partial failure | 🟦 | 1 h | Staff follow-ups | DDIA Ch. 8 |

**Papers (senior+; ~5–8 h):**

- [Raft paper](https://raft.github.io/)
- [Dynamo (SOSP 2007)](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)
- [Spanner](https://research.google/pubs/pub39966/) (or [archive](https://research.google/archive/spanner.html)) — TrueTime
- Supplementary: [GFS](https://pdos.csail.mit.edu/6.824/papers/gfs.pdf), [TAO (USENIX ATC 2013)](https://www.usenix.org/system/files/conference/atc13/atc13-bronson.pdf)

**Hands-on:** Toy Raft leader election (~200 lines). Junior: skip implementation; watch the Raft visualization.

---

### Phase 1b — Scale ladder, estimation, caching, IDs (was under-taught)

| Concept | Type | Time | Resource |
|---|---|---|---|
| Scale from 1 user → millions (Xu Ch. 1) | 🟦 | 3 h | Xu Vol. 1 Ch. 1; [system-design-primer](https://github.com/donnemartin/system-design-primer) |
| Back-of-envelope (Xu Ch. 2) | 🟦 | 2 h | Powers of 2, latency numbers; [Jeff Dean / Colin Scott numbers](https://gist.github.com/jboner/2841832) (order-of-magnitude, not gospel) |
| Cache hierarchy: client, CDN, app, Redis, DB | 🟦 | 2 h | Invalidation, stampede, TTL vs write-through vs write-back |
| Bloom filters, HyperLogLog, Count-Min | 🟦 | 1.5 h | Crawler URL seen-set; cardinality |
| Merkle trees / anti-entropy | 🟦 | 1 h | Dynamo; object storage integrity |
| Unique IDs: UUID, DB ticket, Snowflake | 🟦 | 2 h | Xu Vol. 1 Ch. 7; clock monotonicity |

---

### Phase 2 — Data layer

**Outcome:** Pick storage from **access patterns** in under five minutes.

| Concept | Type | Time | Resource |
|---|---|---|---|
| SQL vs NoSQL by query, not fashion | 🟦 | 1.5 h | Drill on 5 problems from Section 6 |
| B-tree vs LSM, WAL, compaction, write amp | 🟦 | 3 h | [PostgreSQL index types](https://www.postgresql.org/docs/current/indexes-types.html); RocksDB wiki (LSM) |
| Isolation levels, write skew | 🟦 | 2 h | DDIA Ch. 7; hotel/booking designs |
| Sharding: range, hash, consistent hash, directory; reshard | 🟦 | 3 h | [Stanford CS168 consistent hashing notes](https://web.stanford.edu/class/cs168/l/l1.pdf) |
| Replication topologies | 🟦 | 2 h | Dynamo + [PostgreSQL HA](https://www.postgresql.org/docs/current/high-availability.html) |
| 2PC, Saga, TCC, outbox | 🟦 | 3 h | [microservices.io Saga](https://microservices.io/patterns/data/saga.html) |
| CDC | 🟩 | 1 h | Debezium mental model; DDIA Ch. 11–12 |
| Distributed SQL / NewSQL | 🟨/🟧 | 2 h | [Cockroach architecture](https://www.cockroachlabs.com/docs/stable/architecture/overview) |
| Search (inverted index) vs OLTP | 🟩 | 1.5 h | Elasticsearch reference — inverted index |
| Time-series / metrics stores | 🟩 | 1 h | Xu Vol. 2 metrics chapter ideas; Prometheus/VictoriaMetrics docs (skim) |
| Object storage vs file vs block | 🟦 | 1.5 h | Xu Vol. 2 S3 chapter; GFS paper |
| Vector / hybrid search | 🟧→🟩 | 2 h | pgvector docs; Phase AI |

**2026 note:** Distributed SQL is mature in lanes (Cockroach/Yugabyte Postgres-compat multi-region; TiDB MySQL+HTAP; Spanner GCP). The common production *and interview* mistake is adopting it before single-region Postgres/MySQL + replicas + boring sharding is insufficient. Say that out loud.

**Blogs:** [Uber Schemaless](https://www.uber.com/blog/schemaless-part-one-mysql-datastore/) (search if URL moves); [Vitess](https://vitess.io/docs/); Meta TAO paper above.

**Hands-on (mid+):** Docker Compose sharded KV: consistent hashing, leader replication, heartbeat, 3-step saga.

---

### Phase 3 — Messaging, streaming, derived data

| Concept | Type | Time | Resource |
|---|---|---|---|
| Kafka: partitions, ISR, RF, min.insync.replicas | 🟦 | 2 h | [Kafka docs](https://kafka.apache.org/documentation/) Design + Implementation |
| KRaft (ZK removed in 4.0) | 🟩 | 2 h | [Kafka 4.0 announcement](https://kafka.apache.org/blog/2025/03/18/apache-kafka-4.0.0-release-announcement/); [KRaft guide](https://developer.confluent.io/learn/kraft/); KIP-500 |
| EOS (idempotent producer + txn API) | 🟦 | 1.5 h | Kafka transactions docs |
| Consumer rebalance, cooperative sticky | 🟩 | 1 h | Kafka consumer docs |
| CQRS, event sourcing, snapshotting | 🟦 | 2–2.5 h | Fowler CQRS; Azure CQRS/ES; [microservices.io ES](https://microservices.io/patterns/data/event-sourcing.html) |
| Transactional outbox | 🟦 | 1.5 h | [Outbox pattern](https://microservices.io/patterns/data/transactional-outbox.html) |
| Backpressure | 🟦 | 1.5 h | [Reactive Streams](https://www.reactive-streams.org/) |
| Batch vs stream (DDIA 10–11) | 🟦 | 2 h | When Spark/Flink vs Kafka Streams |
| Design a **message queue** (not only “use Kafka”) | 🟦 | 3 h | Xu Vol. 2 Ch. 4 |

**Verified:** Kafka 4.0 (18 Mar 2025) is KRaft-only. ZK clusters must migrate (typically via 3.9 bridge) *before* 4.x. Dedicated controllers in production. If your stories are ZK-era, translate them.

**Blogs:** [Netflix Keystone](https://netflixtechblog.com/keystone-real-time-stream-processing-platform-a3ee651812a); [LinkedIn Engineering](https://www.linkedin.com/blog/engineering) (Kafka origin); Confluent KRaft guide.

---

### Phase 4 — APIs and edge

| Concept | Type | Time | Resource |
|---|---|---|---|
| REST maturity, versioning, cursor pagination, idempotency keys | 🟦 | 2 h | [Stripe idempotency](https://stripe.com/blog/idempotency); [Stripe API versioning](https://stripe.com/blog/api-versioning) |
| GraphQL vs REST vs gRPC | 🟦 | 1.5 h | [gRPC intro](https://grpc.io/docs/what-is-grpc/introduction/); [GraphQL learn](https://graphql.org/learn/) |
| BFF | 🟩 | 0.5 h | [Sam Newman BFF](https://samnewman.io/patterns/architectural/bff/) |
| Gateway: authn/z, rate limit, shape, protocol | 🟦 | 1.5 h | [Kong concepts](https://docs.konghq.com/gateway/latest/); [Envoy overview](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/arch_overview) |
| Kubernetes Gateway API | 🟩 | 2 h | [Gateway API](https://kubernetes.io/docs/concepts/services-networking/gateway/) |
| Mesh vs gateway (N-S vs E-W) | 🟦 | 1 h | Istio “what is Istio”; **when not to mesh** |
| Rate limiter algorithms (distributed) | 🟦 | 2 h | [Stripe rate limiters](https://stripe.com/blog/rate-limiters); Xu Ch. 4 |
| AI/LLM gateway (token meter, route, cache) | 🟧 | 1 h | Kong/Envoy AI gateway docs — shape only unless AI-infra role |

---

### Phase 5 — Reliability

| Concept | Type | Time | Resource |
|---|---|---|---|
| Circuit breaker, bulkhead | 🟦 | 1.5 h | Resilience4j docs *or* equivalent |
| Retry + full jitter | 🟦 | 1 h | AWS Architecture Blog: exponential backoff and jitter |
| Deadline / timeout budgets | 🟦 | 1 h | [gRPC deadlines](https://grpc.io/docs/guides/deadlines/) |
| Load shedding, priority, overload | 🟦 | 1 h | [SRE book — overload](https://sre.google/sre-book/handling-overload/) |
| Graceful degradation | 🟩 | 1 h | Practice: name the user-visible fallback |
| Chaos basics | 🟩 | 1 h | [principlesofchaos.org](https://principlesofchaos.org/) |

Interviewers now ask **what the user sees**, **why that threshold**, and **how you test fallback without taking prod down**.

---

### Phase 6 — Scale, multi-region, DR, cost

| Concept | Type | Time | Resource |
|---|---|---|---|
| LB algorithms; L4 vs L7 | 🟦 | 2.5 h | Matt Klein load balancing post (search); Envoy L3/L4 vs L7 |
| CDN, invalidation, edge | 🟦/🟩 | 1.5 h | [Cloudflare Learning — CDN](https://www.cloudflare.com/learning/cdn/what-is-a-cdn/) |
| Active-passive vs active-active, residency | 🟦 | 2 h | AWS Architecture Blog (search multi-region) |
| RPO/RTO | 🟦 | 1.5 h | AWS Well-Architected Reliability |
| Cost-aware scaling | 🟩 | 1 h | Well-Architected Cost Optimization |
| Geo: geohash, quadtree, S2 | 🟦 | 2 h | Xu Vol. 2 proximity; Uber H3 blog (search) |

Cost is a **graded line** at senior+. Unjustified global active-active is a miss.

---

### Phase 7 — Observability and deploy

| Concept | Type | Time | Resource |
|---|---|---|---|
| Logs, metrics, traces | 🟦 | 1.5 h | [OTel primer](https://opentelemetry.io/docs/concepts/observability-primer/) |
| OpenTelemetry | 🟩 | 3 h | [opentelemetry.io/docs](https://opentelemetry.io/docs/); [CNCF graduation](https://www.cncf.io/announcements/2026/05/21/cloud-native-computing-foundation-announces-opentelemetrys-graduation-solidifying-status-as-the-de-facto-observability-standard/) |
| SLI/SLO/error budgets | 🟦 | 2 h | [SRE workbook — SLOs](https://sre.google/workbook/implementing-slos/) |
| Golden signals | 🟦 | 0.5 h | [SRE book — monitoring](https://sre.google/sre-book/monitoring-distributed-systems/) |
| Profiling (4th signal) | 🟧 | 0.5 h | OTel profiling — skim |
| Blue-green, canary, flags, rollback | 🟦 | 1.5 h | Fowler BlueGreen; K8s rolling update |
| On-call as a design constraint | 🟩 | 1 h | [SRE — being on-call](https://sre.google/sre-book/being-on-call/) |
| Mesh choice | 🟨/🟧 | 1.5 h | Istio ambient; Cilium mesh — **warrant vs overhead** |

---

### Phase 8 — Security architecture

| Concept | Type | Time | Resource |
|---|---|---|---|
| AuthN vs AuthZ, session vs token | 🟦 | 1 h | [Auth0 — authn vs authz](https://auth0.com/docs/get-started/identity-fundamentals/authentication-and-authorization) |
| OAuth2, OIDC, JWT pitfalls | 🟦 | 3 h | [oauth.net/2](https://oauth.net/2/); [OIDC](https://openid.net/connect/) |
| Zero Trust | 🟩 | 1 h | [NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final) |
| mTLS, secrets (KMS/Vault) | 🟩 | 1.5 h | Vault docs overview |
| API security | 🟦 | 1 h | [OWASP API Security Top 10](https://owasp.org/www-project-api-security/) |
| Encryption, PII, tokenization | 🟦 | 1 h | OWASP Cryptographic Storage cheat sheet |
| Prompt injection, data exfil via LLM | 🟧 | 1 h | OWASP LLM Top 10 — Phase AI |

---

### Phase AI — AI engineering ladder (integrated with HLD)

Treat this as **systems design with a probabilistic, expensive component**, not as ML theory. You do **not** need to derive attention math. You **do** need latency, cost, failure, eval, and data flow.

#### Basic (every mid+ SWE in 2026; junior if the company ships AI)

- Where the model sits: synchronous API vs async jobs vs streaming tokens
- RAG at box level: ingest → chunk → embed → index → retrieve → prompt → generate → return
- Why **not** dump the whole corpus into the prompt (context limits, cost, recency)
- Caching: **exact** response hash vs **semantic** nearest-neighbor (wrong-match risk) vs **prefix/KV cache** (same token prefix, *new* completion — OpenAI/Anthropic prompt caching). These are three different mechanisms.
- Rate limits and tenant quotas in **tokens**, not only QPS
- Fallback: smaller model, keyword search, “I don’t know”, human handoff
- PII: what must not go to a third-party LLM

**Resources:** [Hello Interview — ML / system design tracks](https://www.hellointerview.com/learn/system-design/in-a-hurry/introduction); OpenAI / Anthropic API docs (rate limits, caching if offered); [OWASP Top 10 for LLM apps](https://owasp.org/www-project-top-10-for-large-language-model-applications/).

#### Intermediate (senior generalist; mid at AI-product companies)

- Chunking, overlap, metadata filters **before** ANN; **hybrid BM25 + dense**, RRF (typical \(k=60\)), cross-encoder rerank of ~50–200 → 3–10 chunks
- Embedding model versioning (index rebuild when the model changes)
- Eval: golden set, retrieval recall@k, answer faithfulness; LLM-as-judge with a human-labeled subset
- RAG vs fine-tune vs prompt vs LoRA — decision from **data volatility and task**
- Online vs offline indexes; staleness SLA
- Feature store / embedding pipeline (batch + nearline) — [Uber Michelangelo](https://www.uber.com/blog/michelangelo-machine-learning-platform/) and [generative follow-up](https://www.uber.com/blog/from-predictive-to-generative-ai/)
- Guardrails: input/output filters, tool-call allowlists
- Observability: traces around retrieval + generation; cost per request

**Vector store pick (heuristic, not a benchmark):** [pgvector](https://github.com/pgvector/pgvector) if Postgres + mid scale + SQL FTS; Pinecone/Weaviate when you want managed hybrid; Milvus at large N / more ops; [FAISS](https://github.com/facebookresearch/faiss) is a **library**, you own HA. Filtered ANN is the hard part.

**Resources:** [vLLM PagedAttention](https://vllm.ai/blog/2023-06-20-vllm); [Anthropic contextual retrieval](https://www.anthropic.com/engineering/contextual-retrieval); [OpenAI prompt caching](https://openai.com/index/api-prompt-caching/).

#### Advanced (staff, ML platform, inference infra, frontier-lab adjacent)

- Prefill vs decode; **continuous batching**; **KV cache**; PagedAttention; prefix/prompt cache
- Quantization (FP8/INT8/AWQ etc.) as a **latency/quality/cost** lever, not a buzzword
- Speculative decoding: **latency at low batch**, can *hurt* a saturated GPU (not a throughput silver bullet)
- Prefill/decode **disaggregation** (DistServe-class): different hardware/SLOs; KV transfer; cold start is **minutes**
- GPU packing, multi-tenant fairness; autoscale on **queue depth + KV occupancy**, not CPU HPA
- Model **router** (one call) vs **cascade** (small then escalate — FrugalGPT-shaped; high escalate-rate kills savings)
- Distributing **weights** (Xu-style “huge file to thousands of machines”)
- Agents: tool calling, loops, MCP as an integration pattern — **scope and kill-switch**, not a 20-agent diagram
- Safety evals, prompt injection as an authz problem

**Resources:** [vLLM anatomy (2025)](https://vllm.ai/blog/2025-09-05-anatomy-of-vllm); [Anyscale continuous batching](https://www.anyscale.com/blog/continuous-batching-llm-inference); [Netflix in-house LLM serving](https://netflixtechblog.com/in-house-llm-serving-at-netflix-a5a8e799ea2c); [Meta inference parallelism (2025)](https://engineering.fb.com/2025/10/17/ai-research/scaling-llm-inference-innovations-tensor-parallelism-context-parallelism-expert-parallelism/). Stripe has **no** public LLM-fleet design post — use [idempotency](https://stripe.com/blog/idempotency) for payments, not an invented serving architecture.

**Hands-on (pick one):** Local RAG (chunk a folder, pgvector, one LLM API) **or** read vLLM serving docs and explain continuous batching on a whiteboard.

---

### Phase 9 — Specialized deep dives (pick by track)

| Specialization | Hours | Crux | Resource |
|---|---|---|---|
| Search | 6 | Inverted index, sharding, hybrid lexical+vector | ES docs; Phase AI intermediate |
| File / object storage | 5–8 | Chunk vs object, metadata, EC vs replication | GFS; Xu Vol. 2 S3 |
| Realtime / collab | 4 | WS/SSE, presence, OT vs CRDT | [Figma multiplayer](https://www.figma.com/blog/how-figmas-multiplayer-technology-works/) (search if moved) |
| Recsys + embeddings | 6 | Candidate gen → rank → re-rank; feature store | Michelangelo; Netflix tech blog recsys |
| Payments / wallet | 6 | Idempotency, ledger, saga, PCI boundary | Stripe blogs; Xu Vol. 2 |
| Geo | 5 | Geohash hotspots, maps tiles | Xu Vol. 2 Ch. 1–3 |
| Metrics | 4 | TSDB, scrape vs push, alert | Xu Vol. 2; SRE monitoring |
| Video | 6 | Transcode ladder, CDN, DRM | Xu Vol. 1 YouTube |
| Matching engine | 8 | Determinism, sequencing | Xu Vol. 2 stock exchange — staff only |

Standard path: **two** deep dives. Intensive: **one** plus AI advanced.

---

### Phase LLD — parallel every week

**Two formats — do not mix the deliverable**

| Format | Produce | Typical |
|---|---|---|
| **Whiteboard OOD** | Requirements, 8–15 class boxes, 2–3 methods, trade-offs | 45–60 min (US Amazon/Google/Meta often) |
| **Machine coding** | Compiling in-memory app + driver + review | **90–120 min** + ~30 min review (Flipkart, Uber India, many India product firms; Atlassian **code design** is closer to this) |

Drawing load balancers in LLD (or class diagrams in HLD) is a common miss.

**What “good” looks like**

| Level | Bar |
|---|---|
| Junior | Entities, responsibilities, one diagram, happy path code, basic SOLID |
| Mid | Strategy/state where it earns its keep; concurrency on shared resources; tests for races |
| Senior | Minimal patterns, extension points for the *next two* requirements, lock granularity |
| Staff | Same plus: API between packages, failure modes, observability hooks, “what we would not build”; LLD as **domain/API evolution**, not parking-lot trivia |

**Fundamentals**

- SOLID, DRY, KISS, YAGNI — **name a violation in your own sketch**. Rule of three: a pattern when the **third** variant appears (or they ask for extensibility).
- **Tier-1 patterns:** Strategy, State, Observer, Factory. **Tier-2:** Decorator, Command, Builder, Chain of Responsibility (logger), Template Method, Composite (file tree), Specification (Unix `find`). Singleton only if you can say why DI is usually better.
- UML: class + sequence for the critical path — correct arrows on the **hinge** classes beat complete getters
- Concurrency: thread pools, locks vs CAS, `ConcurrentHashMap` (not Java 7 segments). **Virtual threads (JEP 444, final in 21):** cheap blocking I/O, not faster CPU; a tiny JDBC pool still bottlenecks. **Scoped values** finalized in JDK 25 (prefer over `ThreadLocal` with millions of VTs). **Structured concurrency** is still **preview** through 25 — do not claim it as production-default on Java 21 LTS without `--enable-preview`.
- Machine coding: compiling code > pretty UML; YAGNI on Redis locks for a single-process round

**Resources:** [Refactoring.Guru](https://refactoring.guru/design-patterns) • [system-design-primer OOD](https://github.com/donnemartin/system-design-primer) • [ashishps1/awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design) • [Hello Interview LLD](https://www.hellointerview.com/learn/low-level-design/in-a-hurry/patterns) • [JEP 444](https://openjdk.org/jeps/444)

---

### Phase 11 — Mock intensive

- Self-record against Section 10 rubric; note evidence, not vibes
- You need **another human** for follow-ups (peer, interviewing.io, Exponent, Hello Interview coaches)
- Last week: **taper**. No new frameworks.

---

## 5. Timeboxed interview formats

**30 min:** Requirements 3 → data+API 7 → architecture 10 → 1–2 trade-offs 5 → bottlenecks 3. Skip deep math (2 min max).

**45 min (most common HLD):** Full 7-step at moderate depth: req 5, estimate 5, API 5, data 5, diagram 15, failure/trade-off 7, summary 3.

**60 min staff/deep dive:** Same, but one component for 15+ minutes. **Name the follow-up before they ask** (“on leader death…”).

**LLD 45–60 min:** Clarify 3–5 min → nouns/variation axes 5 → diagram 10 → code `park()`/`book()`/`split()` 15–20 → concurrency/OCP 5–10.

**Machine coding 90–120 min:** Working driver, in-memory, demo; patterns + races in the review.

**AI HLD 45 min:** Requirements (latency, cost cap, hallucination policy, data sensitivity) 7 → pipeline diagram 10 → retrieval **or** serving deep dive 15 → evals + fallback + observability 8 → summary 5.

---

## 6. Master HLD problem list (by complexity and book coverage)

Do **depth on a subset**. Numbers in parentheses: Xu volume.

**Foundational (junior+):**

1. URL shortener (V1.8) 2. Rate limiter (V1.4) 3. Unique ID generator (V1.7) 4. Key-value / cache (V1.5–6) 5. Web crawler (V1.9)

**Intermediate:**

6. News feed (V1.11) 7. Notifications (V1.10) 8. Chat (V1.12) 9. Autocomplete (V1.13) 10. Ride-sharing dispatch 11. Proximity / “nearby” (V2.1–2) 12. Distributed message queue (V2.4) 13. Metrics & alerting (V2.5) 14. Leaderboard (V2.10) 15. Multi-tenant rate-limited API platform 16. Job scheduler 17. Ticketmaster / booking (HLD) 18. Matching apps (Tinder-style) — Hello Interview medium rotation

**Advanced:**

16. Drive / file sync (V1.15) 17. Object storage S3-like (V2.9) 18. Search 19. YouTube / streaming (V1.14) 20. Maps (V2.3) 21. Ad click aggregation (V2.6) 22. Hotel reservation (V2.7) 23. Payments (V2.11) 24. Digital wallet (V2.12) 25. Email (V2.8) 26. Multi-region checkout + inventory 27. Collaborative editing (OT/CRDT) 28. Global CDN

**Staff-signal / 2026 AI + infra:**

29. LLM serving at scale (batching, KV cache, GPU, fallback) 30. RAG support chatbot (hybrid retrieval, evals, PII) 31. Semantic search / hybrid index 32. Copilot / agent with tools (authz, loop limits) 33. Recsys with two-tower / embeddings + ranker 34. Distribute model weights under bandwidth caps 35. Stock exchange matching (V2.13) 36. Realtime gaming presence + leaderboard

---

## 7. Master LLD / OOD problem list

**Junior:** Parking lot • Vending machine • Library (Book vs **BookCopy**) • Logger • LRU cache • Tic-tac-toe / snake & ladder • Meeting scheduler (data model)

**Mid:** Elevator (SCAN/LOOK, hall vs cabin) • Movie booking (seat locks) • ATM / banking • Hotel booking (inventory) • Splitwise • In-memory rate limiter • Pub-sub • Thread pool • HashMap internals (Java) • Connection pool • Amazon locker • Unix `find` (Specification + walker)

**Senior:** Chess • Distributed cache library (not cluster) • Notification dispatcher • Ride matching (in-process) • File system (Composite) • Copy-on-write document • Parking + EV/charging (OCP) • Payment processor LLD (idempotency)

**Concurrency-heavy:** Ticket booking • Producer-consumer blocking queue • Web crawler worker pool (LLD)

For each: class diagram, sequence for the hottest path, compiling code, tests that **fail if you remove the lock**.

---

## 8. Why experienced engineers fail (2026)

1. No trade-offs stated. 2. Skip scoping. 3. Capacity math unused. 4. “Add servers” with no cost. 5. Over-engineering (active-active, ES, NewSQL) without need. 6. No ops (SLO, rollback, on-call). 7. Shallow data model. 8. Weak failure/degraded path. 9. Not driving (senior→staff gap). 10. Silent on AI when the product is clearly ML/LLM. 11. (Java) Spring trivia instead of architecture. 12. (Junior) Patterns as wallpaper. 13. (AI round) No evals, no token cost, no hallucination policy.

---

## 9. Senior vs staff vs junior signals

| Signal | Junior | Senior | Staff |
|---|---|---|---|
| Requirements | Asks when prompted | Clarifies NFRs | Scopes in/out unprompted |
| Trade-offs | Names two options | Defends a choice | Surfaces cost/ops first |
| Scale | Knows cache + replica | Designs from numbers | Questions the numbers |
| Failure | Retries | Named patterns | Thresholds, fallback, test |
| AI | “Call OpenAI” | RAG + cache + fallback | Serving, evals, GPU $, safety |
| Org | — | Mentions teams | Contracts, blast radius |

---

## 10. Mock scoring rubric (1–5)

| Dimension | 1 | 3 (solid senior / strong mid) | 5 (staff) |
|---|---|---|---|
| Requirements | Jumped in | Good clarifying Qs | Scoped + non-obvious constraints |
| Estimation | Skipped | Math once | Numbers drive choices |
| Data model | “A database” | Schema + index | Access patterns + partition key |
| APIs | Missing | Clean REST/RPC | Versioning, idempotency, pagination |
| Trade-offs | None | When asked | Proactive + cost/ops |
| Reliability | None | Named patterns | Threshold + fallback + test |
| AI (if relevant) | Ignored | Boxes for retrieve+generate | Eval, cost, GPU, safety |
| Communication | Passive | Structured | Drove time + summary |

---

## 11. Progress tracker

| Phase | Status | Weak spots | Mock avg | Revisit |
|---|---|---|---|---|
| 0 Interview OS | ☐ | | | |
| 1 Distributed fundamentals | ☐ | | | |
| 1b Scale, cache, IDs | ☐ | | | |
| 2 Data layer | ☐ | | | |
| 3 Messaging / derived data | ☐ | | | |
| 4 API / edge | ☐ | | | |
| 5 Reliability | ☐ | | | |
| 6 Multi-region / cost | ☐ | | | |
| 7 Observability | ☐ | | | |
| 8 Security | ☐ | | | |
| AI Basic / Int / Adv | ☐ / ☐ / ☐ | | | |
| 9 Specializations | ☐ | | | |
| LLD | ☐ | | | |
| Mocks | ☐ | | | |

---

## 12. Appendix — verified current-state (as of Aug 2026)

- **Kafka:** ZooKeeper support removed in **4.0.0** (announced 18 Mar 2025). Upgrade path: ZK → KRaft on 3.9.x (bridge), then 4.x. Dedicated controller quorum is the usual production topology. [Upgrade notes](https://kafka.apache.org/40/getting-started/upgrade/).
- **OpenTelemetry:** CNCF **graduated** 11 May 2026; public announcement 21 May 2026. Default interview vocabulary is OTLP, not a vendor SDK.
- **Service mesh — do not mix surveys:**
  - CNCF **Annual Survey 2024**: mesh in production for a few/most apps **~50% (2023) → ~42% (2024)** among *organizations* ([Linux Foundation / CNCF annual survey PDF](https://www.linuxfoundation.org/hubfs/Research%20Reports/cncf_annual_survey24_031225a.pdf)).
  - CNCF **State of Cloud Native Development Q3 2025**: *developer* service-mesh use **18% (Q3 2023) → 8% (Q3 2025)** ([report PDF](https://www.cncf.io/wp-content/uploads/2025/11/cncf_report_stateofcloud_111025a.pdf)), with cost/complexity and meshes folding into platform layers as explanations.
  - Interview takeaway is unchanged: **justify a mesh**; sidecar vs ambient (Istio) vs eBPF (Cilium) is secondary.
- **Gateway API:** GA; Envoy Gateway / Istio typically high conformance. AI gateways exist for token metering — emerging, not a default box on every diagram.
- **Distributed SQL:** No single winner; premature adoption is the usual mistake.
- **Interview logistics:** Some firms have tightened in-person / no-AI-tooling rules. The 45–60 min collaborative HLD is still the core format. Grading weights cost, ops, and AI-adjacent literacy more than in 2021.

---

## 13. Canonical resource index

**Books:** Xu Vol. 1 & 2; Kleppmann DDIA; Google SRE book (free); (optional) Chip Huyen *Designing Machine Learning Systems*.

**Open primers:** [donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer) • [ashishps1/awesome-system-design-resources](https://github.com/ashishps1/awesome-system-design-resources) • [Hello Interview — in a hurry](https://www.hellointerview.com/learn/system-design/in-a-hurry/introduction) • [Hello Interview practice catalog](https://www.hellointerview.com/practice/system-design) • [ByteByteGo](https://blog.bytebytego.com/) • [DesignGurus](https://www.designgurus.io/system-design-interview) • [interviewing.io HLD guide](https://interviewing.io/guides/system-design-interview)

**Company engineering:** [Netflix Tech Blog](https://netflixtechblog.com/) • [Uber Engineering](https://www.uber.com/blog/engineering/) • [Meta Engineering](https://engineering.fb.com/) • [Google Research / SRE](https://sre.google/) • [AWS Architecture Blog](https://aws.amazon.com/blogs/architecture/) • [Stripe blog](https://stripe.com/blog) • [LinkedIn Engineering](https://www.linkedin.com/blog/engineering) • [Airbnb Engineering](https://medium.com/airbnb-engineering) • [Cloudflare Blog](https://blog.cloudflare.com/) (Durable Objects: [docs](https://developers.cloudflare.com/durable-objects/)) • [Databricks Blog](https://www.databricks.com/blog) • [Snowflake blog](https://www.snowflake.com/blog/)

**Individuals / independent:** [Martin Fowler](https://martinfowler.com/) • [Jepsen / Aphyr](https://jepsen.io/) • [Julia Evans](https://jvns.ca/) • [High Scalability](http://highscalability.com/) (incl. Google back-of-envelope post) • [Murat Demirbas](https://muratbuffalo.blogspot.com/) • [Marc Brooker](https://brooker.co.za/blog/) • [Brendan Gregg](https://www.brendangregg.com/)

**Papers:** Dynamo, Raft, Spanner, GFS, TAO, Bigtable, Chubby; AI: [PagedAttention](https://arxiv.org/abs/2309.06180), [Orca / continuous batching](https://www.usenix.org/conference/osdi22/presentation/yu)

**Mocks / question feeds:** [Hello Interview questions](https://www.hellointerview.com/premium/questions) • [interviewing.io](https://interviewing.io/) • [Exponent](https://www.tryexponent.com/) • Glassdoor/Blind *as color, not as answer keys*

**Latest-question hygiene:** Re-check Hello Interview + company blogs **30 days before** your loop. This README’s problem list is the stable core; the long tail moves.

---

*Ask for a mock on a named problem, a weak-spot drill, or a design review against the rubric.*
