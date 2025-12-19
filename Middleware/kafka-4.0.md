**Apache Kafka 4.0 Details:**

* **Cloud-Native Focus:** The primary theme of Kafka 4.0 is its continued evolution towards being more cloud-native (from video).
   
* **ZooKeeper Removal (KIP-500):**
    * ZooKeeper has been fully removed and deprecated (from video)
    * KRaft is now the standard for metadata management, offering improved scalability and resilience (from video).
    * This change simplifies cloud deployments by eliminating a component that posed networking challenges (from video).
   
* **KIP-848: New Consumer Rebalance Protocol**
    * "Lightweight Clients, Stable and Rapid Rebalances": Experience significantly faster and more stable consumer group rebalances[cite: 1].
    * **Scalability and Efficiency:**
        * Broker-driven rebalancing: Shifts coordination from clients to brokers, reducing client overhead[cite: 2].
        * Multi-threaded broker processing: Parallelizes rebalances, handling large groups efficiently[cite: 2, 3].
    * Improved Heartbeat API: Provides more efficient communication between clients and brokers with less network traffic[cite: 3].
    * **Simplified Management:** Server-side configuration of heartbeats, timeouts, and assignors streamlines consumer setup[cite: 4].
    * **Optimized Rebalancing:** Incremental, multi-threaded rebalancing allows for faster partition assignment for new consumers[cite: 5].
    * **Server Enabled, Client Opt-In:**
        * Enabled by default on Kafka 4.0 servers[cite: 6].
        * Clients activate with group.protocol=consumer[cite: 6].
    * **Enhanced Monitoring:** New metrics provide deeper insights into rebalance performance[cite: 7].
    * This protocol shifts rebalance functionality from the client to the broker (from video)
    * This is beneficial for cloud deployments, providing better control over consumer groups and rebalances (from video).
    * Enhanced metrics are included for better observability during rebalances (from video).
   
* **KIP-932: Queues for Kafka (early access)**
    * **What it is:**
        * Introduces a new way to consume messages in Kafka, enabling cooperative consumption through "share groups"[cite: 8].
        * Decouples consumers from partitions, so multiple consumers can read the same partition[cite: 9].
        * Designed for queuing use cases, where higher throughput and parallel processing are desired[cite: 9].
    * **New Features:**
        * KafkaShareConsumer: A new client interface for interacting with share groups[cite: 10].
        * Kafka CLI:
            * kafka-console-share-consumer.sh: For consuming data using a share group[cite: 10].
            * kafka-share-groups.sh: For managing share groups[cite: 11].
        * AdminClient: Includes new methods for managing share groups[cite: 11].
        * Metrics: Share groups have their own metrics (e.g., consumer lag) for monitoring and scaling[cite: 12].
        * New APIs: Introduces ShareGroupHeartbeat, ShareGroupDescribe, ShareFetch, and ShareAcknowledge to support share groups[cite: 13].
    * The goal of this release is to test the new share group functionality[cite: 14].
    * **NOT FOR PRODUCTION USE**[cite: 15].
    * Undocumented configs necessary in the server.properties file[cite: 15].
    * Cannot upgrade clusters if share groups are enabled[cite: 15].
    * Introduces share groups as an experimental feature, which is the beginning of queue functionality in Kafka (from video).
    * Share groups allow multiple consumers to consume from the same partition (from video).
    * This feature is **not for production use** and requires an undocumented configuration (from video).
   
* **KIP-1106: Add Duration-Based Offset Reset Option for Consumer Clients**
    * KIP-405 added tiered storage, which made auto.offset.reset=earliest less fun[cite: 16].
    * New duration-based offset reset: by\_duration[cite: 16].
    * No change to the existing semantics and default value of auto.offset.reset[cite: 17].
    * KafkaConsumer: Updated auto.offset.reset config option to support new config value of the format by\_duration:<duration>[cite: 18, 19].
    * This automatically resets the offsets back by configured duration[cite: 19].
    * KafkaShareConsumer: Add support for by\_duration:<duration> config value for share.auto.offset.reset[cite: 19].
    * Kafka Streams: Deprecate existing Topology.AutoOffsetReset enum, add a new class org.apache.kafka.streams.AutoOffsetReset to capture the reset strategies[cite: 20].
    * Adds the option to reset consumer offsets by duration (from video).
    * This is particularly useful for tiered storage, preventing the need to read through large amounts of old data (from video).
   
* **KIP-1102: Clients re-bootstrapping based on timeout or error code**
    * KIP-899 Limitations: Re-bootstrapping only occurred when no brokers were available[cite: 21].
    * Clients could get stuck with stale metadata if connected to some brokers[cite: 22].
    * **KIP-1102 Improvements:**
        * Proactive re-bootstrapping: Introduces a metadata refresh timeout (default 5 minutes)[cite: 23].
        * Clients re-bootstrap if no metadata update is received within this time[cite: 24].
        * Server-triggered re-bootstrapping: Brokers/proxies can now return a REBOOTSTRAP\_REQUIRED error code, explicitly telling clients to re-bootstrap[cite: 25].
        * Default in 4.0: metadata.recovery.strategy defaults to rebootstrap for new clients, improving resilience out-of-the-box[cite: 26].
    * Improves the bootstrapping process (where clients discover broker metadata) (from video).
    * Proactive and server-triggered re-bootstrapping prevents issues with stale metadata, especially after long client downtimes (from video).
   
* **KIP-966: Eligible Leader Replicas (part 1)**
    * Part 1 (Included in Kafka 4.0): Enhanced Data Safety (No Unclean Leader Election):
        * Introduces Eligible Leader Replicas (ELR): A subset of ISR replicas guaranteed to have complete data up to the high-watermark[cite: 27, 28].
        * ELRs are safe for leader election, preventing data loss[cite: 28].
        * ELR tracking: Managed by the KRaft controller, stored in PartitionRecord, no performance impact[cite: 29].
        * DescribeTopicPartitions API introduced (default in 3.9, so not new in 4.0)[cite: 29, 30].
        * Admin clients now use this API instead of the Metadata API[cite: 30].
        * Requires minimum metadata version 4.0 IV1[cite: 31].
        * Note: ELR is not enabled by default in 4.0. May become default in 4.1[cite: 31].
    * Protects against data loss in specific scenarios involving single in-sync replicas (from video).
    * Introduces "eligible leader replicas" which are guaranteed to have data up to the watermark (from video).
   
* **KIP-1076 & KIP-1091: Unlocking Kafka Streams Observability**
    * **Before KIP-1076 & KIP-1091**
        * Manual and cumbersome health assessment[cite: 32].
        * Developers had to instrument and export metrics[cite: 32].
        * Operators relied on dashboards for application health[cite: 32].
    * **KIP-1076 Highlights**
        * Extends KIP-714 (AK 3.7 in Feb, 2024) for Kafka Streams applications[cite: 32].
        * Cluster operators can pull application metrics from the application[cite: 32].
    * **KIP-1091 Highlights**
        * Adds state metrics for each StreamThread and the client instance itself[cite: 32].
        * Provides detailed visibility into application state[cite: 32].
    * KIP-1076 allows the cluster to pull observability data from Kafka Streams clients (from video).
    * KIP-1091 extends this with specific metadata about stream threads (from video).
   
* **KIP-1112: Custom Processor Wrapping**
    * **Before KIP-1112**
        * Cross-cutting logic required manual integration into each processor[cite: 33].
        * DSL users lacked a straightforward method to apply these altogether[cite: 33].
        * Resulted in duplicated code and increased maintenance efforts[cite: 33].
    * **KIP-1112 Highlights**
        * Introduces ProcessorWrapper interface[cite: 33].
        * Inject custom logic around both Processor API and DSL processors seamlessly[cite: 33].
    * Enables custom code to be run automatically within Kafka Streams DSL methods (from video).
    * This facilitates cross-cutting concerns like logging within DSL calls (from video).
   
* **KIP-1104: Extract ForeignKey from Key in KTable Join**
    * **Before KIP-1104**
        * Foreign key extractor function could only access the record value[cite: 34].
        * Required duplicating the record key into the value if one wants to use the key for FK joins[cite: 34].
        * More work, more storage overhead[cite: 34].
    * **KIP-1104 Highlights**
        * Foreign keys can now be extracted from both the record key and record value[cite: 34].
        * Simplifies the join process with a more intuitive API[cite: 34].
    * Allows extracting a foreign key from the key of a message, simplifying join operations (from video).
   
* **KIP-1065: Better Reliability with Automatic Retry Mechanisms**
    * **Before KIP-1065**
        * Persistent errors (e.g., broker unavailable, missing output topic)[cite: 35].
        * Default retry mechanism until timeout without the ability to break the retry loop, even after timeout[cite: 35].
        * Expensive task recovery[cite: 35].
    * **KIP-1065 Improvements**
        * Enables users to break retry loops[cite: 35].
        * "RETRY" option in ProductionExceptionHandler[cite: 35].
        * Custom handlers for more control: Retry, Fail gracefully, Drop record and continue[cite: 35].
    * Improves logging and handling of errors when output topics are unavailable (from video).
   
* **Summary of Key Changes:**
    * ZooKeeper is replaced by KRaft for metadata management (from video).
    * Queue functionality is in progress, with share groups as the first step (from video).
    * Users are advised to read the release notes for complete details (from video).