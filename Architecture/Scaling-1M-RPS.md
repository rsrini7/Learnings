# Scaling to 1 Million RPS: Technical Insights

https://www.youtube.com/watch?v=W4EwfEU8CGA

### Video Overview
The YouTube video titled "Let’s Handle 1 Million Requests per Second, It’s Scarier Than You Think!" (uploaded by Cododev on February 5, 2026) is a comprehensive tutorial and benchmark demonstration on scaling a backend service to handle over 1 million HTTP requests per second (RPS). It focuses on building a simple URL shortener-like API using Node.js (with custom frameworks like Cpeak), C++ (with Drogon), PostgreSQL for persistent storage, and Redis for in-memory caching. The setup runs on high-end AWS infrastructure, emphasizing real-world costs, performance bottlenecks, and optimizations. The video runs approximately 2.5 hours, covering theory, code implementation, load testing with AutoCannon, and extreme scaling challenges. Source code is available on GitHub for Node.js, C++, and tester setups.

The content simulates enterprise-scale loads (e.g., comparable to AWS IAM's 400 million RPS globally) and highlights the "scary" aspects: massive costs (tens of thousands USD/month), potential for costly bugs (e.g., O(n) algorithms wasting resources), and the need for rigorous monitoring.

### Extracted Complete Content
Based on the video's transcript and detailed segmentation, here's a structured breakdown of the content. This is derived from the full spoken narrative, code demos, and on-screen benchmarks. I've organized it chronologically with timestamps for reference.

#### Introduction and Prerequisites (00:00–08:23)
- **Core Goal**: Achieve 1M+ RPS on a single endpoint, handling JSON payloads (e.g., 30–32 KB responses). Compares to real-world systems like Uber, Netflix, and AWS services.
- **Mindset Emphasis**: Treat scaling as high-stakes engineering—monitor CPU, memory, network; avoid assumptions; test iteratively.
- **Prerequisites**:
  - Basic SQL (SELECT/INSERT/UPDATE).
  - Backend API knowledge (HTTP routes, JSON handling).
  - Fundamentals: CPU cores/threads, memory vs. disk I/O, networking.
  - Node.js basics (system-level, not frontend).
  - SSH/terminal proficiency.
- No prior C++ or advanced AWS needed; concepts are language-agnostic.

#### CPU Fundamentals and Threading (08:23–16:32)
- **CPU Utilization Explained**:
  - Formula per core: `(Total Time - Idle Time) / Total Time * 100`.
  - Multi-core total can exceed 100% (e.g., 1200% on 12 cores).
- **Demo**: Single-threaded Node.js loop hits 100% on one core; 12 threads hit 1200%. Stresses thread synchronization to avoid race conditions.
- **Insight**: At scale, idle CPU is wasted money—aim for full utilization without bottlenecks.

#### Node.js Setup and Initial Benchmarks (16:32–24:01)
- **Simple Server**: Node.js with a `/simple` GET route returning `{"message": "hi"}`.
- **Load Testing Tool**: AutoCannon (command: `autocannon -c 20 -d 20 -p 2 -m GET http://localhost:3001/simple`).
  - Parameters: `-c` (connections), `-d` (duration), `-p` (pipelining), `-w` (workers).
  - Concurrency: `-c * -p * -w`.
- **Results**: ~18,000 RPS on local machine (Mac Studio, 12 cores).
- **Frameworks Compared**:
  - Express: Baseline, ~8,000 RPS on complex routes.
  - Fastify: ~66,000 RPS.
  - Cpeak (custom, 500 LOC, zero deps): Matches Fastify, chosen for readability and speed.

#### Clustering for Multi-Core Scaling (24:01–34:24)
- **Tool**: PM2 for clustering (`pm2 start ecosystem.json`).
- **Results**: Single instance ~8,000 RPS; 12 clustered instances ~50,000 RPS. Reduces idle CPU from 70% to 0%.
- **Config Example** (ecosystem.config.cjs):
  ```javascript
  module.exports = {
    apps: [{
      name: 'app',
      script: './cpeak.js',
      instances: 'max', // Use all cores
      exec_mode: 'cluster',
    }]
  };
  ```

#### AWS Infrastructure Setup (34:24–46:00)
- **Instances**:
  - Server/Tester: c8i.32xlarge (128 vCPUs, 256 GB RAM, 50 Gbps network, ~$6/hour or $4,380/month).
  - Database: RDS PostgreSQL db.m5.16xlarge (64 vCPUs, 256 GB RAM, ~$6/hour).
- **Networking**: Private VPC, public IPs for access.
- **Monitoring**: `mpstat 1` for CPU idle, `free -h` for memory.
- **Simple Route Benchmark**: 6M RPS, network-bound at 6 GB/s (50 Gbps limit).

#### Complex Route and Database Writes (46:00–1:01:50)
- **PATCH Route**: Handles JSON body, returns 32 KB response. ~100,000 RPS, network-bound.
- **Postgres Insert**: Table (`codes`: ID, created_at, code). Seed script populates 10M records.
- **Benchmark**: 300 connections → 35,000 RPS; errors at higher concurrency due to 3,000 IOPS limit.
- **Optimization**: Upgrade to 12,000 IOPS → 66,000 RPS. Cost: +$1,000/month.
- **Lesson**: Direct DB writes don't scale; use batching.

#### Database Reads and Optimizations (1:01:50–1:24:10)
- **Routes**:
  - v1: `SELECT * ORDER BY RANDOM()` – O(n), fails at scale.
  - v2: `SELECT COUNT(*)` – O(n), slow.
  - v3: `SELECT MAX(ID)` + random ID – Indexed, better.
  - v4: Dual indexed lookups – 400,000 RPS.
- **With 10M Records**: Random queries take 40s+; indexed scale to 400k RPS.
- **Bottleneck**: DB CPU at 100%; scaling costs $14k–$33k/month.

#### Redis Integration for Speed (1:24:10–1:51:52)
- **Why Redis**: 10x faster than disk; in-memory.
- **Architecture**: Write to Redis queue (`sync_queue`), batch-sync to Postgres via `sync.js`.
- **Migration**: `npm run migrate` – Transfers 10M records in 2,000 batches; uses 20 GB memory.
- **ID Strategy**: Switch to `crypto.randomUUID()` (128-bit) to avoid uniqueness checks. Collision risk: ~86,000 years at 1M RPS.
- **Benchmark**: Writes ~100,000 RPS (3x Postgres); reads scale well.
- **Clustering**: `redis.sh --setup` creates 30 clusters (15 masters + 15 replicas). Env: `REDIS_CLUSTER=true`.
- **Results**: Handles >100k RPS per instance; sharding auto-manages data.

#### C++ Rewrite for Peak Performance (1:51:52–2:09:01)
- **Why C++**: Node.js/Go/Java insufficient for 1M RPS with payloads.
- **Tools**: Drogon (HTTP framework), RapidJSON (JSON parser).
- **Optimizations**: Disable compression/logging; native threading.
- **Benchmark**: 1.2M RPS at 70% CPU on c8gn.48xlarge (192 cores, 384 GB RAM, 600 Gbps, ~$11/hour).
- **Amdahl's Law**: C++ 99% parallelizable → 66x speedup vs. Node.js 95% → 18x.

#### Final Colossal Test (2:09:01–2:35:18)
- **Setup**: Server (c8gn.48xlarge) + 60 testers (c8gn.2xlarge, 8 cores each, total ~$28/hour).
- **Tool**: AutoCannon via AWS SSM; aggregate logs to S3/CloudWatch.
- **Results**: 2B requests, 60 TB data, 1M RPS, 0.000002% errors, 0% CPU idle.
- **Load Balancer Note**: NLB limits at 165 LCUs; pre-reserve for high traffic.
- **Total Cost**: ~$2,000 for the test month ($1,200 compute, $800 DB).

#### Outro
- **Key Takeaways**: Possible but expensive/complex. Use distributed systems, in-memory stores, efficient algos. Global clusters for production.

### Validation
The video's claims were cross-checked against external sources, GitHub code, and industry benchmarks:

- **Performance Numbers**: Plausible. Redis on AWS ElastiCache can hit 500M RPS per cluster with microsecond latency on large nodes (e.g., r7g.4xlarge >1M RPS/node). Node.js benchmarks show 1,000–10,000 RPS on single-core setups, scaling to 100k+ with clustering. C++ with optimized frameworks like Drogon achieves 1M+ RPS on high-core machines, as per repo benchmarks (1.2M RPS, 40 GB/s throughput).
- **Redis vs. Postgres**: Video's shift to Redis for speed aligns with cases where Postgres outperforms untuned Redis for certain workloads, but Redis excels in in-memory scenarios (e.g., Valkey/Redis forks hitting 999k RPS on c8g.2xl). GitHub migration script confirms batch-sync approach.
- **AWS Costs**: Approximate match—c8i.32xlarge ~$4,380/month on-demand (730 hours * $6); c8gn.48xlarge ~$8,030/month ($11/hour). RDS Postgres with 12k IOPS adds ~$1,000. Total setups align with $10k–$50k/month for extreme scaling.
- **Code Integrity**: GitHub repos are clean and match video:
  - Node.js: PM2 clustering, Redis cluster script, migration handles 10M records.
  - C++: Drogon handler for PATCH, RapidJSON for JSON—embeds libs for zero deps.
  - Tester: `commands.sh` orchestrates 60-instance AutoCannon runs, aggregating 2B requests.
- **Potential Biases**: Video avoids "AI-generated code" and focuses on raw engineering. External critiques note Node.js dissatisfaction at scale (e.g., one company switched to Go for 800k users), validating the C++ pivot.

No major discrepancies; numbers are aggressive but feasible on specified hardware.

### Insights for Developers
- **Optimization Mindset**: Profile everything—CPU idle signals inefficiency. Use tools like `mpstat` and AutoCannon early. Avoid O(n) ops (e.g., `ORDER BY RANDOM()`) on large datasets; prefer indexed random access.
- **Framework Choices**: Start with lightweight like Cpeak/Fastify over Express for 2–3x RPS gains. For ultimate speed, learn C++ basics—Drogon/RapidJSON reduce overhead vs. V8 JSON in Node.js.
- **Database Patterns**: Direct Postgres writes cap at ~66k RPS; queue in Redis and batch-sync. Use UUIDs over sequential IDs to eliminate contention (collision math: birthday paradox formula).
- **Testing Practices**: Simulate production with multi-worker AutoCannon. Aggregate logs via scripts for distributed tests. Benchmark iteratively: local → clustered → cloud.
- **Code Snippets from GitHub**:
  - Redis Migration (Node.js): Batches inserts to avoid overload.
    ```javascript
    // Simplified from migrate script
    const batchSize = 5000;
    for (let i = 0; i < totalRecords / batchSize; i++) {
      await client.multi().sadd('codes_unique', ids).exec(); // Dedupe set
    }
    ```
  - C++ Handler:
    ```cpp
    // From main.cc
    app().registerHandler("/patch", [](const HttpRequestPtr& req, auto&& callback) {
        rapidjson::Document doc; // Build 30KB JSON
        // ... Populate doc ...
        rapidjson::StringBuffer buffer;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buffer);
        doc.Accept(writer);
        auto resp = HttpResponse::newHttpResponse();
        resp->setBody(buffer.GetString());
        callback(resp);
    });
    ```

### Key Points for Architects
Use tables for clarity:

#### Benchmark Summary
| Scenario | RPS Achieved | Bottleneck | Optimization |
|----------|--------------|------------|--------------|
| Node.js Simple GET (Local) | 18,000 | Single thread | Clustering (PM2) → 50,000 |
| AWS PATCH (32 KB) | 100,000 | Network (50 Gbps) | Upgrade to 600 Gbps instance |
| Postgres Write | 66,000 | IOPS (3,000→12,000) | Batch via Redis queue |
| Postgres Read (Indexed) | 400,000 | DB CPU | In-memory Redis |
| Redis Write | 100,000 | Single instance | Clustering (30 nodes) |
| C++ Full Test | 1,200,000 | CPU/Network | Native threading, fast JSON |

#### Cost Breakdown (Monthly, Approximate On-Demand us-east-1)
| Component | Instance Type | Cost | Notes |
|-----------|---------------|------|-------|
| Server | c8i.32xlarge | $4,380 | 128 vCPUs, 50 Gbps |
| Tester (x1) | c8i.32xlarge | $4,380 | For initial tests |
| DB | db.m5.16xlarge + 12k IOPS | $4,380 + $1,000 | 64 vCPUs |
| Peak Test (Server + 60 Testers) | c8gn.48xlarge + 60x c8gn.2xlarge | $8,030 + $20,800 | 600 Gbps, short-duration |
| Total Extreme | - | $30k–$50k | Includes data transfer |

- **Scaling Strategy**: Vertical first (bigger instances), then horizontal (Redis clusters, load balancers). Pre-reserve NLB capacity for >100k connections.
- **Trade-offs**: Redis reduces DB costs but uses more RAM (20 GB for 10M records). C++ outperforms but increases dev complexity.
- **Security/Production Notes**: Add auth/encryption; hire pen-testers. Use global clusters (e.g., AWS multi-AZ) for HA.
- **Broader Lessons**: 1M RPS is achievable but "scary"—focus on cost calculators, monitoring (CloudWatch), and efficient algos to avoid financial pitfalls. For real apps, combine with CDNs and edge computing.