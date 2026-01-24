# 📘 **Scaling PostgreSQL at OpenAI — Verified & Updated Notes**

![DB/assets/ScallingPostgresOpenAI.png](assets/ScallingPostgresOpenAI.png)

OpenAI runs **PostgreSQL (often called Postgres)** as a core database powering **ChatGPT and the API** — serving **~800 million users and millions of database queries per second (QPS)**. ([OpenAI][1])

---

## 🧠 **1. Core Architecture (What It Is Right Now)**

### 🏗️ **Primary & Replica Setup**

* **One primary PostgreSQL instance** for *all writes* (on Azure Database for PostgreSQL). ([OpenAI][1])
* **~50 read-only replicas** distributed globally to handle most *read queries*. ([OpenAI][1])
* Replicas allow low-latency reads all over the world. ([OpenAI][1])

### 🌍 **High Availability**

* The primary runs in **High Availability (HA) mode** with a **hot standby** ready to take over on failure. ([AdwaitX News][2])
* During outages, reads on replicas can continue even if writes stop. ([AdwaitX News][2])

### 🚫 **No Sharding Yet**

* OpenAI *has not sharded PostgreSQL itself* yet — the current setup stays on one primary because:

  * Sharding would require huge application changes across many services.
  * Their workload remains **mostly read-heavy**, so a single primary still scales well. ([OpenAI][1])

---

## ⚠️ **2. Main Challenges They Faced**

### 📈 **Huge Load Growth**

* Database traffic grew **10× over one year** — pushing the system to its limits. ([OpenAI][1])

### 🧾 **Write Pressure**

* PostgreSQL’s **MVCC (multiversion concurrency control)** creates new row versions on updates, which:

  * Amplifies writes.
  * Causes *table and index bloat*.
  * Requires careful vacuum tuning. ([OpenAI][1])

### ⚙️ **Primary Bottleneck**

* All writes go to one machine → *write spikes* (e.g., feature launches, cache failure) can overload the primary. ([OpenAI][1])

### 💻 **Expensive Queries & CPU Usage**

* Complex queries (e.g., multi-table joins) can saturate CPU, slowing everything down. ([OpenAI][1])

### 🔌 **Connection Limits**

* Too many open connections slow the database; Postgres has a finite limit per instance. ([OpenAI][1])

### 📊 **Replica Load & Lag**

* More replicas means more replication traffic from the primary and potential lag challenges. ([Microsoft][3])

---

## ⚙️ **3. Key Optimizations & How They Work**

The goal is **reduce load on the primary** while still delivering reliable, low-latency service. ([OpenAI][1])

---

### 🔥 A. **Reduce Write Load**

* Offload *write-heavy, shardable data* to external systems (e.g., Azure CosmosDB). ([OpenAI][1])
* Fix application bugs that trigger unnecessary writes. ([OpenAI][1])
* Use techniques like “lazy writes” to smooth spike patterns. ([OpenAI][1])

> *Meaning*: Postgres doesn’t have to process every update — reducing bottlenecks.

---

### 📊 B. **Read Offloading & Replica Use**

* Most reads go to replicas, freeing the primary to focus mostly on writes. ([OpenAI][1])
* Even some queries involved in write transactions are carefully routed to replicas where safe. ([OpenAI][1])

> *Meaning*: Reads are cheap and fast, writes are heavy — treat them differently.

---

### 🧠 C. **Query Optimization**

* Avoid costly multi-table joins where unnecessary. ([OpenAI][1])
* Move heavy logic into application code when possible. ([OpenAI][1])
* Use timeouts to prevent long queries from holding resources. ([Hacker News][4])

---

### 🔌 D. **Connection Pooling (PgBouncer)**

* PgBouncer drastically reduces connection overhead.
* Result: **connection timing dropped from ~50 ms to ~5 ms**. ([Microsoft][3])

> *Meaning*: The database spends less time setting up connections and more time handling queries.

---

### 🗃️ E. **Caching + Cache Locking**

* A separate cache layer *fronts* reads; database only hit when the cache misses.
* “Cache locking” prevents everyone from hitting the DB at once on a miss. ([Microsoft][3])

> *Meaning*: Reduces sudden spikes and “thundering herd” problems.

---

### 📊 F. **Workload Isolation**

* Separate high-priority traffic from lower-priority workloads.
* Heavy jobs are run on *separate Postgres instances* where possible. ([Microsoft][3])

---

### 🔁 G. **Read Replication Enhancements**

* Nearly 50 replicas globally — gives low latency for end users. ([OpenAI][1])
* OpenAI is exploring *cascading replica replication* — where replicas feed other replicas — to reduce load on the primary. ([Microsoft][3])

---

### 🚦 H. **Rate Limiting & Safety Layers**

* Rate limits at multiple levels (app, pooler, proxy, queries) help dampen load spikes. ([Microsoft][3])
* Avoid supply/demand loops where retries worsen overload. ([Microsoft][3])

---

### 🧱 I. **Schema & Change Controls**

* Avoid major schema rewrites on live systems, because they lock tables. ([Microsoft][3])
* New tables and write-heavy things go to sharded systems by default. ([OpenAI][1])

---

## 🚀 **4. Results (What This Achieved)**

✅ **Millions of QPS handleable on Postgres** (combined read + writes). ([Microsoft][3])
✅ **Low latency** — typical p99 ~ double-digit milliseconds for clients. ([LinkedIn][5])
✅ **Five-nines availability** (99.999%) most of the time. ([LinkedIn][5])
✅ Few serious Postgres-related incidents — better stability after optimization. ([Microsoft][3])
✅ Plenty of headroom before sharding becomes necessary. ([OpenAI][1])

---

## 🛠️ **5. Future Directions**

🔹 Keep optimizing current Postgres setup (better headroom). ([OpenAI][1])
🔹 Roll out cascading replication safely. ([Microsoft][3])
🔹 Migrate more write-heavy workloads to shardable systems. ([OpenAI][1])
🔹 Consider adding real Postgres sharding if write pressure eventually demands it. ([OpenAI][1])

---

## 💡 **Key Takeaways (Simplified)**

✔ **Postgres can scale very far if most traffic is reads.** ([OpenAI][1])
✔ **Offload writes and aggressive caching save tons of load.** ([Microsoft][3])
✔ **Connection pooling and rate limits prevent overload.** ([Microsoft][3])
✔ **One primary + many replicas works when engineered right.** ([LinkedIn][5])

---

[1]: https://openai.com/index/scaling-postgresql/?utm_source=chatgpt.com "Scaling PostgreSQL to power 800 million ChatGPT users"
[2]: https://www.adwaitx.com/openai-postgresql-800-million-chatgpt-users-scaling/?utm_source=chatgpt.com "OpenAI Scales PostgreSQL to 800M Users"
[3]: https://www.microsoft.com/en-us/startups/blog/openai-and-postgresql-scaling-with-microsoft-azure/?utm_source=chatgpt.com "How OpenAI scaled with Azure Database for PostgreSQL"
[4]: https://news.ycombinator.com/item?id=46725300&utm_source=chatgpt.com "Scaling PostgreSQL to power 800M ChatGPT users"
[5]: https://www.linkedin.com/posts/srinivasnarayanan_scaling-postgresql-to-power-800-million-chatgpt-activity-7420728382046412800-yr05?utm_source=chatgpt.com "Scaling PostgreSQL to power 800 million ChatGPT users"

Youtube References:

- https://www.youtube.com/watch?v=ubpUjovBMAM
- https://www.youtube.com/watch?v=dApJ8X9XW9M

