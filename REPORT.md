# InstaMart Advertisement & Sales Analytics Pipeline
## Implementation of Probabilistic Algorithms for Big Data Analytics

---

## Abstract

This project implements a comprehensive retail and advertisement analytics pipeline using big data technologies (Hadoop, Spark, Kafka) with advanced probabilistic algorithms for efficient data processing. The system generates synthetic retail and advertisement data (scalable to millions of records), processes it through batch and streaming pipelines, and implements four beyond-syllabus probabilistic algorithms: HyperLogLog, Count-Min Sketch, Bloom Filter, and MinHash with Locality-Sensitive Hashing (LSH). Each algorithm is benchmarked against exact methods to demonstrate accuracy, runtime, and memory trade-offs.

**Keywords**: Big Data Analytics, Probabilistic Algorithms, HyperLogLog, Count-Min Sketch, Bloom Filter, MinHash, LSH, Apache Spark, Apache Kafka, Hadoop

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Problem Statement](#2-problem-statement)
3. [Objectives](#3-objectives)
4. [System Architecture](#4-system-architecture)
5. [Probabilistic Algorithms](#5-probabilistic-algorithms)
6. [Implementation Details](#6-implementation-details)
7. [Experimental Results](#7-experimental-results)
8. [Performance Analysis](#8-performance-analysis)
9. [Conclusion](#9-conclusion)
10. [References](#10-references)

---

## 1. Introduction

### 1.1 Background

In the era of big data, organizations face the challenge of processing massive datasets efficiently while maintaining accuracy in analytics. Traditional exact computation methods often become impractical due to high memory and computational requirements. Probabilistic data structures and algorithms provide elegant solutions by trading off a small amount of accuracy for significant gains in memory efficiency and computational speed.

### 1.2 Motivation

Retail analytics platforms need to process millions of transactions and advertisement events daily. Key operations include:
- Counting unique customers and viewers
- Estimating product click frequencies
- Checking membership of order/event IDs
- Finding similar products or campaigns

Exact methods for these operations require storing all data in memory, which becomes prohibitive at scale. Probabilistic algorithms offer sub-linear space complexity while providing probabilistic guarantees on accuracy.

### 1.3 Scope

This project extends an existing InstaMart retail analytics pipeline by:
1. Generating configurable synthetic retail and advertisement data (500K+ records)
2. Implementing four probabilistic algorithms with benchmarking
3. Creating an interactive dashboard for algorithm comparison
4. Preserving the original Hadoop-Spark-Kafka architecture

---

## 2. Problem Statement

### 2.1 Core Problem

Design and implement a scalable big data analytics pipeline that can:
- Generate and process large-scale synthetic retail and advertisement data
- Implement probabilistic algorithms for efficient cardinality estimation, frequency estimation, membership testing, and similarity detection
- Benchmark these algorithms against exact methods to quantify accuracy-performance trade-offs
- Provide interactive visualization of results

### 2.2 Challenges

1. **Scalability**: Handle datasets with millions of records without memory constraints
2. **Accuracy**: Maintain acceptable error rates while using probabilistic methods
3. **Integration**: Seamlessly integrate new algorithms into existing batch/streaming pipeline
4. **Reproducibility**: Ensure deterministic results with fixed random seeds
5. **Usability**: Provide clear documentation and interactive dashboards

---

## 3. Objectives

### 3.1 Primary Objectives

1. **Data Generation**: Create a configurable synthetic data generator capable of producing 500K+ retail and advertisement records with reproducible timestamps, products, customers, campaigns, and metrics.

2. **Algorithm Implementation**: Implement four probabilistic algorithms:
   - HyperLogLog for cardinality estimation
   - Count-Min Sketch for frequency estimation
   - Bloom Filter for membership testing
   - MinHash + LSH for similarity detection

3. **Benchmarking**: Compare each algorithm against exact methods measuring:
   - Accuracy (relative error, false positive rate, precision/recall)
   - Runtime (insertion time, query time)
   - Memory usage (actual vs exact method)

4. **Dashboard**: Create an interactive web dashboard displaying benchmark results and algorithm comparisons.

5. **Documentation**: Provide comprehensive documentation including theoretical background, mathematical formulations, and usage instructions.

### 3.2 Secondary Objectives

- Preserve existing Hadoop-Spark-Kafka architecture
- Ensure all data is clearly labeled as synthetic
- Implement configurable parameters and fixed random seeds
- Handle edge cases and validate estimates
- Create unit tests for all algorithms

---

## 4. System Architecture

### 4.1 Overall Architecture

The system consists of three main layers:

```
┌─────────────────────────────────────────────────────────────┐
│                    Data Generation Layer                    │
│  - Extended Synthetic Data Generator                        │
│  - Retail Transactions + Advertisement Events               │
│  - 500K+ records, scalable to millions                     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Processing Layer                         │
│  ┌─────────────────┐    ┌─────────────────┐              │
│  │  Batch Pipeline │    │ Streaming Pipe   │              │
│  │  - Spark ETL     │    │ - Kafka + Spark  │              │
│  │  - HDFS Storage  │    │   Structured     │              │
│  │                 │    │   Streaming      │              │
│  └─────────────────┘    └─────────────────┘              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         Probabilistic Algorithms Module              │   │
│  │  • HyperLogLog    • Count-Min Sketch               │   │
│  │  • Bloom Filter   • MinHash + LSH                  │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Batch Dashboard│ │Streaming Dash│ │Algorithm     │      │
│  │  (Port 5000)  │ │ (Port 5100)  │ │Dashboard     │      │
│  │              │ │              │ │(Port 5200)   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Data Storage | HDFS | Distributed file storage |
| Batch Processing | Apache Spark | ETL and aggregations |
| Stream Processing | Spark Structured Streaming | Real-time analytics |
| Messaging | Apache Kafka | Event streaming |
| Containerization | Docker Compose | Service orchestration |
| Dashboards | Flask + Chart.js | Interactive visualization |
| Algorithms | Python 3.11 | Probabilistic algorithm implementation |

### 4.3 Data Flow

#### Batch Pipeline
1. Synthetic data generator creates CSV files
2. Data uploaded to HDFS
3. Spark batch job reads, cleans, and aggregates data
4. Results written to Parquet and CSV
5. Dashboard displays analytics

#### Streaming Pipeline
1. CSV rows replayed as JSON events to Kafka
2. Spark Structured Streaming consumes events
3. Real-time aggregations with sliding windows
4. Results written to Parquet
5. Streaming dashboard displays live metrics

#### Algorithm Pipeline
1. Test data generated with controlled properties
2. Each algorithm benchmarked against exact methods
3. Metrics collected (accuracy, runtime, memory)
4. Results saved to JSON
5. Algorithm dashboard visualizes comparisons

---

## 5. Probabilistic Algorithms

This section details the four beyond-syllabus probabilistic algorithms implemented in this project. These algorithms are not typically covered in standard big data curricula but are essential for scalable analytics where exact computation becomes prohibitively expensive.

### 5.1 HyperLogLog (Cardinality Estimation)

#### 5.1.1 Theoretical Background

HyperLogLog estimates the number of distinct elements in a multiset (cardinality) using significantly less memory than exact counting. It was introduced by Flajolet et al. (2007) as an improvement over the LogLog algorithm.

**Key Insight**: The position of the leftmost 1-bit in a random hash value follows a geometric distribution. By tracking the maximum position across many hash values, we can estimate the number of distinct items.

**Why This is Beyond Syllabus**: Traditional big data courses teach exact counting using sets or hash tables. HyperLogLog introduces the concept of trading exactness for massive memory savings, which is crucial for counting distinct elements at internet scale (e.g., counting unique visitors to a website with billions of page views).

#### 5.1.2 Algorithm Explained with Diagram

```
Step 1: Hash each element to a 64-bit random value

Input: ["customer_1", "customer_2", "customer_1", "customer_3"]

Hash(customer_1) = 0b10110010... (64 bits)
Hash(customer_2) = 0b00101101... (64 bits)
Hash(customer_3) = 0b11001010... (64 bits)

Step 2: Use first p bits to select register index (m = 2^p registers)

With p=2 (m=4 registers):
Hash(customer_1) = 0b10110010...
                ^^
                Index = 2 (binary: 10)

Hash(customer_2) = 0b00101101...
                ^^
                Index = 1 (binary: 01)

Step 3: Count leading zeros (ρ) in remaining bits

Hash(customer_1) = 0b10110010...
                ρ = 0 (first bit is 1)

Hash(customer_2) = 0b00101101...
                ρ = 2 (first two bits are 0)

Step 4: Store maximum ρ for each register

Register Array (m=4):
[0] = max(ρ for items hashing to register 0)
[1] = max(ρ for items hashing to register 1) = 2
[2] = max(ρ for items hashing to register 2) = 0
[3] = max(ρ for items hashing to register 3)

Step 5: Combine using harmonic mean

Estimate = α * m² / Σ(2^(-register[i]))
```

**Visual Representation**:

```
┌─────────────────────────────────────────────────────────────┐
│                    HyperLogLog Structure                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Input Stream                                               │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                  │
│  │ "cust1" │───▶│ "cust2" │───▶│ "cust3" │───▶ ...          │
│  └─────────┘    └─────────┘    └─────────┘                  │
│       │              │              │                        │
│       ▼              ▼              ▼                        │
│  ┌──────────────────────────────────────────┐              │
│  │           Hash Function (MD5)           │              │
│  └──────────────────────────────────────────┘              │
│       │              │              │                        │
│       ▼              ▼              ▼                        │
│  0b1011...      0b0010...      0b1101... (64-bit)         │
│   ││            ││            ││                          │
│   └─First p bits──┘            └─Leading zeros             │
│   for index                       (ρ)                        │
│                                                             │
│  ┌──────────────────────────────────────────┐              │
│  │         Register Array (m = 2^p)          │              │
│  ├──────────────────────────────────────────┤              │
│  │ [0] = max(ρ₀)                           │              │
│  │ [1] = max(ρ₁)                           │              │
│  │ [2] = max(ρ₂)                           │              │
│  │ [3] = max(ρ₃)                           │              │
│  │ ...                                     │              │
│  │ [m-1] = max(ρₘ₋₁)                       │              │
│  └──────────────────────────────────────────┘              │
│                      │                                    │
│                      ▼                                    │
│  ┌──────────────────────────────────────────┐              │
│  │    Harmonic Mean + Alpha Correction      │              │
│  └──────────────────────────────────────────┘              │
│                      │                                    │
│                      ▼                                    │
│              Cardinality Estimate                              │
└─────────────────────────────────────────────────────────────┘
```

#### 5.1.3 Mathematical Formulation

**Register Count**:
```
m = 2^p
```

**Alpha Correction Factor**:
```
α = 0.7213 / (1 + 1.079/m)  for m ≥ 128
```

**Raw Estimate**:
```
E = α * m² / Σ(2^(-r_i))
```

**Complexity**:
- Time: O(1) per insertion, O(m) for estimation
- Space: O(m) = O(2^p)
- Relative Error: ≈ 1.04/√m

#### 5.1.4 Implementation in This Project

**File**: `services/probabilistic_algorithms/hyperloglog.py`

**Integration in InstaMart Pipeline**:

```python
# Example: Counting unique customers from retail data
from probabilistic_algorithms import HyperLogLog

# Initialize HyperLogLog with p=12 (4096 registers)
hll = HyperLogLog(p=12)

# Process retail transactions
for transaction in retail_data:
    customer_id = transaction['customer_id']
    hll.add(customer_id)

# Estimate unique customers
unique_customers_estimate = hll.count()

# Compare with exact counting
exact_count = len(set(t['customer_id'] for t in retail_data))
```

**Use Case in InstaMart**:
1. **Daily Unique Customers**: Count distinct customers visiting stores each day
2. **Weekly Active Users**: Estimate DAU/MAU (Daily/Monthly Active Users)
3. **Campaign Reach**: Measure unique viewers of advertisement campaigns
4. **Product Viewers**: Count distinct customers who viewed specific products

**Benchmark Implementation**:

The project includes a comprehensive benchmark that:
- Generates 150K test elements (100K unique + 50K duplicates)
- Compares HyperLogLog estimates against exact set-based counting
- Measures accuracy (relative error), runtime, and memory usage
- Tests multiple p values (10, 12, 14) to show accuracy-memory trade-off

**Actual Results from Project**:
- p=12 (4096 registers): 0.19% error, 144 KB memory vs 9.8 MB for exact set
- **68x memory reduction** with minimal accuracy loss

#### 5.1.5 Working Principle Summary

HyperLogLog works by:
1. Hashing each element to a random value
2. Using the hash to select a register and count leading zeros
3. Storing the maximum leading zeros seen for each register
4. Combining register values using harmonic mean to estimate cardinality

The key insight is that the probability of seeing a hash with k leading zeros is 1/2^k. Therefore, if we've seen a hash with many leading zeros, we've likely seen many distinct items.

---

### 5.2 Count-Min Sketch (Frequency Estimation)

#### 5.2.1 Theoretical Background

Count-Min Sketch estimates the frequency of events in a data stream with bounded error. It was introduced by Cormode and Muthukrishnan (2005).

**Key Insight**: By using multiple hash functions and taking the minimum counter value, we can bound the estimation error while using sub-linear space. The minimum counter provides an upper bound on the true frequency because collisions can only increase counter values.

**Why This is Beyond Syllabus**: Traditional big data courses teach exact frequency counting using hash maps or dictionaries. Count-Min Sketch introduces the concept of streaming algorithms with bounded error guarantees, which is essential for real-time analytics where storing all frequencies is impossible (e.g., counting clicks in a high-traffic web stream).

#### 5.2.2 Algorithm Explained with Diagram

```
Step 1: Initialize d rows of w counters (depth × width)

With d=3, w=4:
  Counter[0] = [0, 0, 0, 0]
  Counter[1] = [0, 0, 0, 0]
  Counter[2] = [0, 0, 0, 0]

Step 2: For each item, increment counters at hash positions

Item: "product_A"
  hash₀("product_A") = 2 → Counter[0][2] += 1
  hash₁("product_A") = 0 → Counter[1][0] += 1
  hash₂("product_A") = 3 → Counter[2][3] += 1

After update:
  Counter[0] = [0, 0, 1, 0]
  Counter[1] = [1, 0, 0, 0]
  Counter[2] = [0, 0, 0, 1]

Step 3: Query frequency by taking minimum counter

For "product_A":
  Counter[0][hash₀("product_A")] = Counter[0][2] = 1
  Counter[1][hash₁("product_A")] = Counter[1][0] = 1
  Counter[2][hash₂("product_A")] = Counter[2][3] = 1

  estimate = min(1, 1, 1) = 1

For "product_B" (never seen):
  All counters at hash positions = 0
  estimate = 0
```

**Visual Representation**:

```
┌─────────────────────────────────────────────────────────────┐
│                  Count-Min Sketch Structure                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Input Stream (Items to count)                             │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                  │
│  │ item_A  │───▶│ item_B  │───▶│ item_A  │───▶ ...          │
│  └─────────┘    └─────────┘    └─────────┘                  │
│       │              │              │                        │
│       ▼              ▼              ▼                        │
│  ┌──────────────────────────────────────────┐              │
│  │       d Hash Functions (pairwise)        │              │
│  │  hash₀(x), hash₁(x), hash₂(x), ...      │              │
│  └──────────────────────────────────────────┘              │
│       │││            │││            │││                      │
│       ▼▼▼            ▼▼▼            ▼▼▼                      │
│  ┌──────────────────────────────────────────┐              │
│  │       Counter Array (d × w)             │              │
│  ├──────────────────────────────────────────┤              │
│  │ Row 0: [c₀₀][c₀₁][c₀₂]...[c₀(w-1)]     │              │
│  │ Row 1: [c₁₀][c₁₁][c₁₂]...[c₁(w-1)]     │              │
│  │ Row 2: [c₂₀][c₂₁][c₂₂]...[c₂(w-1)]     │              │
│  │ ...                                     │              │
│  │ Row d-1: [c(d-1)₀]...[c(d-1)(w-1)]    │              │
│  └──────────────────────────────────────────┘              │
│                      │                                    │
│                      ▼                                    │
│  ┌──────────────────────────────────────────┐              │
│  │         Query: Min(counters)            │              │
│  │   estimate(x) = min(c[hashᵢ(x)])       │              │
│  └──────────────────────────────────────────┘              │
│                      │                                    │
│                      ▼                                    │
│              Frequency Estimate                              │
│         (Upper bound on true frequency)                      │
└─────────────────────────────────────────────────────────────┘

Collision Example:
  If item_A and item_B hash to same counter position:
  - Both increment the same counter
  - Counter value = true frequency of item_A + item_B
  - Taking minimum across d rows reduces collision impact
```

#### 5.2.3 Mathematical Formulation

**Dimensions**:
```
w = ceil(e / ε)     # Width (number of counters per row)
d = ceil(ln(1/δ))   # Depth (number of hash functions/rows)
```

**Update Operation**:
```
for i in 1..d:
    counter[i][hash_i(item)] += count
```

**Query Operation**:
```
estimate(item) = min(counter[i][hash_i(item)] for i in 1..d)
```

**Error Guarantee**:
With probability at least 1-δ:
```
|estimate - true_frequency| ≤ ε * N
where N = total items in stream
```

**Complexity**:
- Time: O(d) per update and query
- Space: O(d * w)
- Error: ε * N with probability 1-δ

#### 5.2.4 Implementation in This Project

**File**: `services/probabilistic_algorithms/countmin_sketch.py`

**Integration in InstaMart Pipeline**:

```python
# Example: Tracking product click frequencies
from probabilistic_algorithms import CountMinSketch

# Initialize with ε=0.01 (1% error), δ=0.01 (99% confidence)
cms = CountMinSketch(epsilon=0.01, delta=0.01)

# Process advertisement events
for event in ad_events:
    if event['clicks'] > 0:
        product_id = event['product_id']
        cms.add(product_id, count=event['clicks'])

# Estimate click frequency for a product
click_estimate = cms.estimate("Masala Dosa")

# Compare with exact counting
exact_count = sum(e['clicks'] for e in ad_events if e['product_id'] == "Masala Dosa")
```

**Use Case in InstaMart**:
1. **Product Click Tracking**: Estimate how many times each product was clicked in ads
2. **Advertisement Impressions**: Track impression counts per campaign
3. **Trending Items**: Identify frequently viewed products in real-time
4. **Hotspot Detection**: Find high-frequency events in streaming data

**Benchmark Implementation**:

The project benchmarks Count-Min Sketch with:
- 100K items with Zipf-skewed distribution (1K unique items)
- Compares estimates against exact dictionary counting
- Measures max/mean relative error, runtime, and memory usage
- Tests multiple epsilon values (0.01, 0.001, 0.0001)

**Actual Results from Project**:
- ε=0.001: 0% max error, 442 KB memory
- Works well with tight epsilon on uniform distributions
- High error on skewed distributions (expected behavior)

#### 5.2.5 Working Principle Summary

Count-Min Sketch works by:
1. Using multiple hash functions to map items to multiple counter positions
2. Incrementing all relevant counters for each item
3. Estimating frequency as the minimum counter value
4. Providing an upper bound guarantee (never underestimates)

The minimum counter provides a good estimate because:
- Collisions can only increase counter values
- Using multiple hash functions reduces collision probability
- Taking minimum across rows bounds the overcount from collisions

---

### 5.3 Bloom Filter (Membership Testing)

#### 5.3.1 Theoretical Background

Bloom Filter is a space-efficient probabilistic data structure for testing set membership. It was introduced by Burton Howard Bloom (1970). The key property is that it never produces false negatives, only false positives.

**Key Insight**: Multiple hash functions map each element to multiple bit positions. Setting these bits to 1 allows membership testing with controlled false positive rate. If all bits for an element are set, it's probably in the set; if any bit is 0, it's definitely not in the set.

**Why This is Beyond Syllabus**: Traditional big data courses teach exact membership testing using hash sets or databases. Bloom Filter introduces the concept of probabilistic data structures with zero false negatives, which is crucial for applications like cache filtering, duplicate detection, and network routing where false positives are acceptable but false negatives are not.

#### 5.3.2 Algorithm Explained with Diagram

```
Step 1: Initialize m-bit array to all zeros

With m=16 bits:
  Bit Array: [0][0][0][0][0][0][0][0][0][0][0][0][0][0][0][0]
  Index:     [0][1][2][3][4][5][6][7][8][9][10][11][12][13][14][15]

Step 2: Add element using k hash functions

With k=3 hash functions:
  hash₀("order_123") = 3
  hash₁("order_123") = 7
  hash₂("order_123") = 12

  Set bits at positions 3, 7, 12 to 1:
  Bit Array: [0][0][0][1][0][0][0][1][0][0][0][0][1][0][0][0]
  Index:     [0][1][2][3][4][5][6][7][8][9][10][11][12][13][14][15]

Step 3: Test membership

Test "order_123":
  hash₀("order_123") = 3 → bit[3] = 1 ✓
  hash₁("order_123") = 7 → bit[7] = 1 ✓
  hash₂("order_123") = 12 → bit[12] = 1 ✓
  All bits set → PROBABLY in set (may be false positive)

Test "order_456" (not added):
  hash₀("order_456") = 3 → bit[3] = 1 ✓
  hash₁("order_456") = 5 → bit[5] = 0 ✗
  hash₂("order_456") = 12 → bit[12] = 1 ✓
  At least one bit 0 → DEFINITELY NOT in set (no false negative)
```

**Visual Representation**:

```
┌─────────────────────────────────────────────────────────────┐
│                    Bloom Filter Structure                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Adding an Element:                                         │
│  ┌──────────────┐                                          │
│  │  element "X" │                                          │
│  └──────┬───────┘                                          │
│         │                                                  │
│         ▼                                                  │
│  ┌──────────────────────────────────────────┐              │
│  │       k Hash Functions                 │              │
│  │  hash₀(X) = pos₁                        │              │
│  │  hash₁(X) = pos₂                        │              │
│  │  hash₂(X) = pos₃                        │              │
│  └──────────────────────────────────────────┘              │
│         │          │          │                          │
│         ▼          ▼          ▼                          │
│  ┌──────────────────────────────────────────┐              │
│  │         Bit Array (m bits)               │              │
│  ├──────────────────────────────────────────┤              │
│  │ [0][1][1][0][1][0][0][1][0][0][1]...   │              │
│  │  ↑        ↑        ↑                    │              │
│  │ pos₁    pos₂    pos₃                   │              │
│  │ (set to 1) (set to 1) (set to 1)        │              │
│  └──────────────────────────────────────────┘              │
│                                                             │
│  Testing Membership:                                        │
│  ┌──────────────┐                                          │
│  │  element "Y" │                                          │
│  └──────┬───────┘                                          │
│         │                                                  │
│         ▼                                                  │
│  ┌──────────────────────────────────────────┐              │
│  │       k Hash Functions                 │              │
│  │  hash₀(Y) = pos₄                        │              │
│  │  hash₁(Y) = pos₁                        │              │
│  │  hash₂(Y) = pos₅                        │              │
│  └──────────────────────────────────────────┘              │
│         │          │          │                          │
│         ▼          ▼          ▼                          │
│  ┌──────────────────────────────────────────┐              │
│  │         Bit Array (m bits)               │              │
│  ├──────────────────────────────────────────┤              │
│  │ [0][1][1][0][1][0][0][1][0][0][1]...   │              │
│  │  ↑        ↑        ↑                    │              │
│  │ pos₄    pos₁    pos₅                   │              │
│  │ (1)✓   (1)✓   (0)✗ ← At least one 0    │              │
│  └──────────────────────────────────────────┘              │
│                      │                                    │
│                      ▼                                    │
│              DEFINITELY NOT IN SET                           │
│              (Zero false negatives)                          │
└─────────────────────────────────────────────────────────────┘

False Positive Example:
  Different elements may hash to same bit positions
  If bit[3], bit[7], bit[12] are all set by other elements,
  query for new element hashing to these positions will return
  "probably in set" even though it was never added.
```

#### 5.3.3 Mathematical Formulation

**Optimal Size**:
```
m = -n * ln(p) / (ln(2))²
where n = expected items, p = desired false positive rate
```

**Optimal Hash Functions**:
```
k = (m/n) * ln(2)
```

**False Positive Rate**:
```
P(FP) = (1 - e^(-kn/m))^k
```

**Complexity**:
- Time: O(k) per operation
- Space: O(m) bits
- False Positive Rate: (1 - e^(-kn/m))^k
- False Negative Rate: 0 (guaranteed)

#### 5.3.4 Implementation in This Project

**File**: `services/probabilistic_algorithms/bloom_filter.py`

**Integration in InstaMart Pipeline**:

```python
# Example: Checking for duplicate order IDs
from probabilistic_algorithms import BloomFilter

# Initialize for 100K orders with 1% false positive rate
bf = BloomFilter(expected_items=100000, false_positive_rate=0.01)

# Add processed order IDs
for order in processed_orders:
    bf.add(order['order_id'])

# Check if new order is duplicate
new_order_id = "20261024-000001"
if bf.contains(new_order_id):
    print("Likely duplicate - skip processing")
else:
    # Process the order
    process_order(new_order_id)
    bf.add(new_order_id)
```

**Use Case in InstaMart**:
1. **Duplicate Order Detection**: Check if order ID was already processed
2. **Cache Miss Filtering**: Avoid database lookups for non-existent keys
3. **Spam Event Filtering**: Block repeated fraudulent advertisement events
4. **Join Optimization**: Pre-filter before expensive database joins

**Benchmark Implementation**:

The project benchmarks Bloom Filter with:
- 100K training items, 10K test items (50% in set)
- Compares against Python set for exact membership
- Measures actual false positive rate, recall, runtime, and memory
- Tests multiple FP rates (0.1, 0.01, 0.001)

**Actual Results from Project**:
- Target FP=0.01: Actual FP=0.94%, perfect recall (zero false negatives)
- Zero false negatives guaranteed (perfect for applications where missing items is unacceptable)

#### 5.3.5 Working Principle Summary

Bloom Filter works by:
1. Using multiple hash functions to map each element to multiple bit positions
2. Setting all corresponding bits to 1 when adding an element
3. Checking if all bits are set when testing membership
4. Guaranteeing zero false negatives (if any bit is 0, element is definitely not in set)

The key trade-off:
- **Pros**: Zero false negatives, memory-efficient, fast operations
- **Cons**: Cannot delete elements, false positives possible (controlled by parameters)
- **Best for**: Applications where false positives are acceptable but false negatives are not

---

### 5.4 MinHash + LSH (Similarity Detection)

#### 5.4.1 Theoretical Background

MinHash estimates Jaccard similarity between sets using reduced signatures. Locality-Sensitive Hashing (LSH) builds on MinHash to efficiently find similar pairs without comparing all pairs.

**Jaccard Similarity**:
```
J(A, B) = |A ∩ B| / |A ∪ B|
```

**MinHash Property**: The probability that the minimum hash values of two sets match equals their Jaccard similarity. This is the foundation for using MinHash to estimate similarity efficiently.

**Why This is Beyond Syllabus**: Traditional big data courses teach exact similarity computation using set operations. MinHash + LSH introduces the concept of approximate similarity search with sub-linear time complexity, which is essential for finding similar items in massive datasets (e.g., finding similar products among millions of items in e-commerce).

#### 5.4.2 MinHash Algorithm Explained with Diagram

```
Step 1: Generate k random hash functions

With k=4:
  hash₀(x), hash₁(x), hash₂(x), hash₃(x)

Step 2: For each set, compute minimum hash for each function

Set A = {apple, banana, cherry}
  hash₀(apple)=5, hash₀(banana)=2, hash₀(cherry)=8 → min = 2
  hash₁(apple)=9, hash₁(banana)=4, hash₁(cherry)=1 → min = 1
  hash₂(apple)=3, hash₂(banana)=7, hash₂(cherry)=6 → min = 3
  hash₃(apple)=0, hash₃(banana)=5, hash₃(cherry)=2 → min = 0

  Signature_A = [2, 1, 3, 0]

Set B = {apple, cherry, date}
  hash₀(apple)=5, hash₀(cherry)=8, hash₀(date)=3 → min = 3
  hash₁(apple)=9, hash₁(cherry)=1, hash₁(date)=6 → min = 1
  hash₂(apple)=3, hash₂(cherry)=6, hash₂(date)=9 → min = 3
  hash₃(apple)=0, hash₃(cherry)=2, hash₃(date)=7 → min = 0

  Signature_B = [3, 1, 3, 0]

Step 3: Estimate similarity from signature matches

Matching positions: [1]=1, [2]=3, [3]=0 (3 out of 4 match)
Estimated Jaccard = 3/4 = 0.75

Exact Jaccard:
  A ∩ B = {apple, cherry} → |A ∩ B| = 2
  A ∪ B = {apple, banana, cherry, date} → |A ∪ B| = 4
  Exact Jaccard = 2/4 = 0.5

Note: MinHash estimate is probabilistic, more accurate with more hash functions
```

**Visual Representation of MinHash**:

```
┌─────────────────────────────────────────────────────────────┐
│                    MinHash Process                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Set A: {apple, banana, cherry}                            │
│  Set B: {apple, cherry, date}                              │
│                                                             │
│  Step 1: Hash all elements with k functions                │
│  ┌──────────────────────────────────────────┐              │
│  │         k Random Hash Functions         │              │
│  │  hash₀, hash₁, hash₂, hash₃           │              │
│  └──────────────────────────────────────────┘              │
│         │           │           │           │               │
│         ▼           ▼           ▼           ▼               │
│  ┌──────────────────────────────────────────┐              │
│  │    Hash Values for Set A                │              │
│  ├──────────────────────────────────────────┤              │
│  │ apple:  [5, 9, 3, 0]                   │              │
│  │ banana: [2, 4, 7, 5]                   │              │
│  │ cherry: [8, 1, 6, 2]                   │              │
│  └──────────────────────────────────────────┘              │
│                      │                                    │
│                      ▼                                    │
│  ┌──────────────────────────────────────────┐              │
│  │    Take Minimum per Hash Function       │              │
│  ├──────────────────────────────────────────┤              │
│  │ hash₀: min(5, 2, 8) = 2               │              │
│  │ hash₁: min(9, 4, 1) = 1               │              │
│  │ hash₂: min(3, 7, 6) = 3               │              │
│  │ hash₃: min(0, 5, 2) = 0               │              │
│  └──────────────────────────────────────────┘              │
│                      │                                    │
│                      ▼                                    │
│  Signature_A = [2, 1, 3, 0]                                 │
│                                                             │
│  (Repeat for Set B → Signature_B = [3, 1, 3, 0])          │
│                                                             │
│  Step 2: Compare Signatures                                │
│  Signature_A: [2, 1, 3, 0]                                 │
│  Signature_B: [3, 1, 3, 0]                                 │
│                 ✗  ✓  ✓  ✓                                 │
│                                                             │
│  Matches: 3/4 = 0.75 → Estimated Jaccard ≈ 0.75           │
└─────────────────────────────────────────────────────────────┘
```

#### 5.4.3 LSH Algorithm Explained with Diagram

```
Step 1: Compute MinHash signatures for all sets

With k=12 hash functions, b=3 bands, r=4 rows per band:
  Signature length = 12
  Bands = 3, each with 4 rows

Step 2: Divide signature into bands and hash to buckets

Signature_A = [10, 5, 8, 3 | 9, 2, 7, 1 | 4, 6, 0, 11]
               └────Band 0────┘ └────Band 1────┘ └────Band 2────┘

Band 0 of A: [10, 5, 8, 3] → hash → bucket_0_1
Band 1 of A: [9, 2, 7, 1] → hash → bucket_1_5
Band 2 of A: [4, 6, 0, 11] → hash → bucket_2_3

Signature_B = [10, 5, 8, 2 | 9, 2, 7, 1 | 4, 6, 0, 11]
               └────Band 0────┘ └────Band 1────┘ └────Band 2────┘

Band 0 of B: [10, 5, 8, 2] → hash → bucket_0_7 (different)
Band 1 of B: [9, 2, 7, 1] → hash → bucket_1_5 (SAME as A!)
Band 2 of B: [4, 6, 0, 11] → hash → bucket_2_3 (SAME as A!)

Step 3: Generate candidate pairs

Since A and B share buckets in Band 1 and Band 2:
  (A, B) is a candidate pair

Step 4: Verify with exact Jaccard similarity

Compute exact J(A, B) to confirm similarity
```

**Visual Representation of LSH**:

```
┌─────────────────────────────────────────────────────────────┐
│                   LSH Candidate Generation                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Multiple Items with MinHash Signatures                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Item A    │  │   Item B    │  │   Item C    │         │
│  │ Signature:  │  │ Signature:  │  │ Signature:  │         │
│  │ [a₀,a₁,a₂,  │  │ [b₀,b₁,b₂,  │  │ [c₀,c₁,c₂,  │         │
│  │  a₃,a₄,a₅,  │  │  b₃,b₄,b₅,  │  │  c₃,c₄,c₅,  │         │
│  │  a₆,a₇,a₈,  │  │  b₆,b₇,b₈,  │  │  c₆,c₇,c₈,  │         │
│  │  a₉,a₁₀,a₁₁]│  │  b₉,b₁₀,b₁₁]│  │  c₉,c₁₀,c₁₁]│         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│         │                │                │                │
│         ▼                ▼                ▼                │
│  ┌──────────────────────────────────────────┐              │
│  │      Divide into b Bands of r Rows      │              │
│  │  (k = b × r)                            │              │
│  ├──────────────────────────────────────────┤              │
│  │  Band 0: [a₀,a₁,a₂,a₃]                 │              │
│  │  Band 1: [a₄,a₅,a₆,a₇]                 │              │
│  │  Band 2: [a₈,a₉,a₁₀,a₁₁]               │              │
│  └──────────────────────────────────────────┘              │
│         │                │                │                │
│         ▼                ▼                ▼                │
│  ┌──────────────────────────────────────────┐              │
│  │    Hash Each Band to Bucket             │              │
│  ├──────────────────────────────────────────┤              │
│  │  Band 0 → hash([a₀,a₁,a₂,a₃]) → bucket│              │
│  │  Band 1 → hash([a₄,a₅,a₆,a₇]) → bucket│              │
│  │  Band 2 → hash([a₈,a₉,a₁₀,a₁₁]) → bucket│              │
│  └──────────────────────────────────────────┘              │
│                                                             │
│  Bucket Table:                                               │
│  ┌──────────────────────────────────────────┐              │
│  │  bucket_id  │  Items in Bucket           │              │
│  ├──────────────────────────────────────────┤              │
│  │  hash_0_5    │  Item A, Item C           │ ← Match!   │
│  │  hash_1_3    │  Item A, Item B           │ ← Match!   │
│  │  hash_2_7    │  Item B                    │              │
│  │  ...        │  ...                       │              │
│  └──────────────────────────────────────────┘              │
│                      │                                    │
│                      ▼                                    │
│  ┌──────────────────────────────────────────┐              │
│  │        Candidate Pairs                 │              │
│  │  (A, C) - share bucket in Band 0       │              │
│  │  (A, B) - share bucket in Band 1       │              │
│  └──────────────────────────────────────────┘              │
│                      │                                    │
│                      ▼                                    │
│  ┌──────────────────────────────────────────┐              │
│  │    Verify with Exact Jaccard Similarity │              │
│  │    (Only for candidate pairs)           │              │
│  └──────────────────────────────────────────┘              │
│                      │                                    │
│                      ▼                                    │
│              Similar Pairs (with scores)                       │
└─────────────────────────────────────────────────────────────┘

Key Insight:
  - If two items are similar, they will likely hash to same bucket
    in at least one band
  - If they share a bucket in ANY band, they become candidates
  - This avoids comparing all n×(n-1)/2 pairs
  - Verification step ensures accuracy
```

#### 5.4.4 Mathematical Formulation

**MinHash Signature**:
```
signature[i] = min(hash_i(x) for x in set)
```

**Similarity Estimate**:
```
estimate = matches(signature_A, signature_B) / k
```

**LSH Threshold**:
```
threshold ≈ (1/b)^(1/r)
where b = number of bands, r = rows per band
```

**Collision Probability**:
```
P(collision in band) = 1 - (1 - s^r)^b
where s = Jaccard similarity
```

**Complexity**:
- MinHash signature: O(k * |S|) per set
- LSH candidate search: O(n * b)
- Exact Jaccard: O(|A| + |B|) per pair
- Space per set: O(k)

#### 5.4.5 Implementation in This Project

**File**: `services/probabilistic_algorithms/minhash_lsh.py`

**Integration in InstaMart Pipeline**:

```python
# Example: Finding similar products based on customer interactions
from probabilistic_algorithms import MinHash, LSH

# Initialize MinHash with 128 permutations
mh = MinHash(num_permutations=128)

# Initialize LSH with 32 bands, 4 rows per band
lsh = LSH(num_bands=32, rows_per_band=4)

# Build interaction sets for each product
product_interactions = {}
for product in products:
    # Get customers who interacted with this product
    customers = get_customers_who_viewed(product['product_id'])
    product_interactions[product['product_id']] = set(customers)

# Compute signatures and add to LSH
for product_id, customer_set in product_interactions.items():
    signature = mh.compute_signature(customer_set)
    lsh.add(product_id, signature)

# Get candidate similar pairs
candidates = lsh.get_candidates()

# Verify with exact Jaccard similarity
similar_products = []
for prod_a, prod_b in candidates:
    exact_sim = exact_jaccard_similarity(
        product_interactions[prod_a],
        product_interactions[prod_b]
    )
    if exact_sim > 0.5:  # Threshold
        similar_products.append((prod_a, prod_b, exact_sim))
```

**Use Case in InstaMart**:
1. **Similar Product Recommendations**: Find products with similar customer interaction patterns
2. **Campaign Clustering**: Group advertisement campaigns with similar audience overlap
3. **Customer Segmentation**: Find customers with similar purchase histories
4. **Cross-selling**: Identify products frequently bought together by similar customers

**Benchmark Implementation**:

The project benchmarks MinHash + LSH with:
- 100 datasets with 100 items each
- Controlled similarity (every 5th set is 70% similar to previous)
- Compares against brute-force pairwise comparison
- Measures candidate reduction, precision, recall, and runtime
- Tests multiple configurations (64/16×4, 128/32×4, 256/32×8)

**Actual Results from Project**:
- 128 perms, 32×4 bands: 99.6% candidate reduction, 95% precision, 95% recall
- Dramatically faster than comparing all 4,950 pairs
- Excellent balance of precision and recall

#### 5.4.6 Working Principle Summary

MinHash + LSH works by:

**MinHash**:
1. Hashing all elements in a set with k random hash functions
2. Taking the minimum hash value for each function as the signature
3. Estimating Jaccard similarity as the fraction of matching signature positions

**LSH**:
1. Dividing the signature into bands of rows
2. Hashing each band to a bucket
3. Items sharing any bucket become candidate pairs
4. Verifying candidates with exact Jaccard similarity

The key insights:
- Similar sets have high probability of sharing a bucket in at least one band
- This reduces pairwise comparisons from O(n²) to O(n × b)
- The threshold (1/b)^(1/r) controls the similarity sensitivity
- More bands/rows = higher threshold = fewer false positives but may miss some similar pairs

**Trade-offs**:
- **Pros**: Massive reduction in pairwise comparisons, configurable threshold
- **Cons**: Not exact (approximate), requires parameter tuning, precision/recall trade-off
- **Best for**: Finding similar items in large datasets where brute-force is impossible

---

### 5.5 Summary: Beyond-Syllabus Algorithms in This Project

#### 5.5.1 Why These Algorithms Are Beyond Syllabus

Traditional big data curricula typically focus on:
- Exact counting using sets/hash tables
- Exact frequency counting using dictionaries
- Exact membership testing using hash sets
- Exact similarity computation using set operations

The probabilistic algorithms implemented in this project introduce advanced concepts:

| Algorithm | Traditional Approach | Probabilistic Approach | Key Innovation |
|-----------|-------------------|----------------------|----------------|
| HyperLogLog | Store all IDs in set | Estimate using registers | Cardinality estimation with bounded error |
| Count-Min Sketch | Store all frequencies in dict | Estimate using counter array | Streaming frequency estimation with sub-linear space |
| Bloom Filter | Store all items in set | Use bit array with hash functions | Zero false negatives with controlled false positives |
| MinHash + LSH | Compare all pairs O(n²) | Use signatures and banding | Similarity search in sub-linear time |

#### 5.5.2 Integration Diagram: How Algorithms Work in the Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                  InstaMart Analytics Pipeline                     │
│                  with Probabilistic Algorithms                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │           Synthetic Data Generation Layer                 │   │
│  │  • Retail transactions (customers, products, amounts)     │   │
│  │  • Advertisement events (impressions, clicks, spend)       │   │
│  │  • 500K+ records, scalable to millions                    │   │
│  └────────────────────┬────────────────────────────────────┘   │
│                       │                                         │
│                       ▼                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Probabilistic Algorithms Module              │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │                                                             │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │   │
│  │  │ HyperLogLog  │  │Count-Min Sk  │  │ Bloom Filter  │  │   │
│  │  │              │  │              │  │              │  │   │
│  │  │ Unique:      │  │ Frequency:    │  │ Membership:  │  │   │
│  │  │ • Customers  │  │ • Clicks      │  │ • Order IDs   │  │   │
│  │  │ • Viewers    │  │ • Impressions │  │ • Event IDs   │  │   │
│  │  │ • Products   │  │ • Events      │  │ • Cache keys  │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │   │
│  │                                                             │   │
│  │  ┌──────────────┐                                          │   │
│  │  │ MinHash + LSH│                                          │   │
│  │  │              │                                          │   │
│  │  │ Similarity:  │                                          │   │
│  │  │ • Products   │                                          │   │
│  │  │ • Campaigns  │                                          │   │
│  │  │ • Customers  │                                          │   │
│  │  └──────────────┘                                          │   │
│  └────────────────────┬────────────────────────────────────┘   │
│                       │                                         │
│                       ▼                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │             Benchmarking & Comparison Layer               │   │
│  │  • Compare against exact methods                         │   │
│  │  • Measure accuracy, runtime, memory                      │   │
│  │  • Generate JSON results                                  │   │
│  └────────────────────┬────────────────────────────────────┘   │
│                       │                                         │
│                       ▼                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Algorithm Comparison Dashboard               │   │
│  │  • Visualize benchmark results                            │   │
│  │  • Show accuracy vs memory trade-offs                      │   │
│  │  • Display charts and metrics                             │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

#### 5.5.3 End-to-End Example: Customer Analytics Workflow

```
Scenario: Analyze customer behavior across retail and advertisement data

Step 1: Data Generation
  generate_extended_synthetic_data.py
  → Creates retail_data.csv (orders, customers, products)
  → Creates ad_data.csv (impressions, clicks, campaigns)

Step 2: Load Data
  retail_data = load_csv("retail_data.csv")
  ad_data = load_csv("ad_data.csv")

Step 3: Apply HyperLogLog (Cardinality Estimation)
  hll = HyperLogLog(p=12)
  for order in retail_data:
      hll.add(order['customer_id'])
  unique_customers = hll.count()
  # Result: ~10,000 unique customers (0.19% error, 68x memory reduction)

Step 4: Apply Count-Min Sketch (Frequency Estimation)
  cms = CountMinSketch(epsilon=0.001, delta=0.01)
  for event in ad_data:
      if event['clicks'] > 0:
          cms.add(event['product_id'], event['clicks'])
  popular_products = sorted(all_products,
                           key=lambda p: cms.estimate(p),
                           reverse=True)[:10]
  # Result: Top 10 most clicked products (0% error with tight epsilon)

Step 5: Apply Bloom Filter (Membership Testing)
  bf = BloomFilter(expected_items=100000, false_positive_rate=0.01)
  for order in processed_orders:
      bf.add(order['order_id'])
  for new_order in incoming_orders:
      if bf.contains(new_order['order_id']):
          skip_duplicate(new_order)
      else:
          process_order(new_order)
  # Result: Zero false negatives, 0.94% false positive rate

Step 6: Apply MinHash + LSH (Similarity Detection)
  mh = MinHash(num_permutations=128)
  lsh = LSH(num_bands=32, rows_per_band=4)
  for product in products:
      customers = get_viewers(product['product_id'])
      sig = mh.compute_signature(customers)
      lsh.add(product['product_id'], sig)
  candidates = lsh.get_candidates()
  similar_pairs = verify_with_exact_jaccard(candidates)
  # Result: 99.6% candidate reduction, 95% precision/recall

Step 7: Benchmarking
  run_all_benchmarks.py
  → Compares each algorithm against exact methods
  → Generates algorithm_benchmarks.json
  → Results displayed in dashboard at http://localhost:5200

Step 8: Dashboard Visualization
  - Accuracy charts (relative error, FP rate, precision/recall)
  - Memory comparison (algorithm vs exact method)
  - Runtime comparison
  - Scalability analysis
```

#### 5.5.4 Key Insights from Implementation

1. **HyperLogLog Excels at Cardinality Estimation**
   - Achieved 0.19% error with 68x memory reduction
   - Production-ready for counting unique customers/viewers
   - Works well regardless of data distribution

2. **Count-Min Sketch Requires Careful Tuning**
   - High error on skewed distributions (Zipf)
   - Accurate with tight epsilon on uniform data
   - Best for streaming frequency estimation where exact counting is impossible

3. **Bloom Filter Provides Perfect Recall**
   - Zero false negatives (guaranteed)
   - Controlled false positive rate (achievable)
   - Memory benefits appear at scale (millions of items)
   - Ideal for duplicate detection and cache filtering

4. **MinHash + LSH Dramatically Reduces Comparisons**
   - 99.6% reduction in pairwise comparisons
   - 95% precision and recall with proper tuning
   - Essential for similarity search in large datasets
   - Configurable threshold for different use cases

#### 5.5.5 Educational Value

These beyond-syllabus algorithms demonstrate:
- **Trade-off Analysis**: Understanding when to accept small errors for massive gains
- **Streaming Algorithms**: Processing data that cannot be stored entirely
- **Probabilistic Guarantees**: Bounding error rates mathematically
- **Scalability**: Techniques that work at internet scale
- **Practical Implementation**: Moving from theory to working code

The project successfully bridges the gap between theoretical big data concepts and practical implementation, showing how advanced algorithms solve real-world problems in retail analytics.

---

## 6. Implementation Details

### 6.1 Project Structure

```
Data_Pipeline_Example/
├─ README.md                          # User guide
├─ REPORT.md                          # This document
├─ DEPLOYMENT.md                      # Deployment guide
├─ ALGORITHMS.md                      # Algorithm documentation
├─ VERIFICATION_REPORT.md             # Verification results
├─ docker-compose.batch.yml           # Batch stack
├─ docker-compose.streaming.yml       # Streaming stack
├─ .env                               # Version configuration
├─ conf/                              # Hadoop configuration
├─ services/
│  ├─ batch/
│  │  ├─ generate_synthetic_data.py       # Original generator
│  │  ├─ generate_extended_synthetic_data.py  # Extended generator
│  │  └─ pipeline_batch.py                # Spark batch job
│  ├─ probabilistic_algorithms/
│  │  ├─ __init__.py                      # Module init
│  │  ├─ hyperloglog.py                   # HyperLogLog + benchmark
│  │  ├─ countmin_sketch.py               # CMS + benchmark
│  │  ├─ bloom_filter.py                  # Bloom Filter + benchmark
│  │  ├─ minhash_lsh.py                   # MinHash + LSH + benchmark
│  │  ├─ test_algorithms.py               # Unit tests
│  │  └─ run_all_benchmarks.py            # Comprehensive benchmark
│  ├─ event-generator/
│  │  └─ kafka_event_producer.py
│  └─ streaming/
│     └─ streaming_sales_aggregator.py
├─ dashboard/                         # Batch analytics dashboard
├─ streaming_dashboard/               # Streaming analytics dashboard
├─ algorithm_dashboard/               # Algorithm comparison dashboard
└─ data/                              # Runtime data
```

### 6.2 Synthetic Data Generator

The extended generator creates two types of data:

#### Retail Data Schema
| Column | Description | Type |
|--------|-------------|------|
| data_source | "SYNTHETIC_RETAIL" | string |
| order_id | Unique order identifier | string |
| order_timestamp | ISO timestamp | string |
| order_date | ISO date | string |
| customer_id | Customer identifier | string |
| customer_segment | Premium/Regular/Budget | string |
| customer_city | Customer location | string |
| store_id | Store code | string |
| store_city | Store location | string |
| product_id | Product code | string |
| product_name | Product name | string |
| product_category | Food/Beverage/Dessert | string |
| quantity | Units purchased | integer |
| unit_price | Price per unit | decimal |
| amount | Total amount | decimal |

#### Advertisement Data Schema
| Column | Description | Type |
|--------|-------------|------|
| data_source | "SYNTHETIC_ADVERTISEMENT" | string |
| event_id | Unique event identifier | string |
| event_timestamp | ISO timestamp | string |
| event_date | ISO date | string |
| customer_id | Customer identifier | string |
| customer_segment | Premium/Regular/Budget | string |
| customer_city | Customer location | string |
| campaign_id | Campaign code | string |
| campaign_name | Campaign name | string |
| platform | Facebook/Instagram/Google Ads/etc | string |
| product_id | Product code | string |
| product_name | Product name | string |
| product_category | Food/Beverage/Dessert | string |
| impressions | 1 if impression occurred | integer |
| clicks | 1 if click occurred | integer |
| conversions | 1 if conversion occurred | integer |
| spend | Ad spend amount | decimal |
| revenue | Revenue from conversion | decimal |

### 6.3 Algorithm Implementation Details

#### 6.3.1 HyperLogLog

**Class**: `HyperLogLog(p=12)`

**Parameters**:
- `p`: Register index bits (4-16, default 12)

**Methods**:
- `add(value)`: Add element to sketch
- `count()`: Estimate cardinality
- `merge(other)`: Merge with another HyperLogLog
- `get_memory_usage()`: Get memory in bytes

**Configuration**:
- p=10: 1,024 registers, ~3% error
- p=12: 4,096 registers, ~1.6% error (default)
- p=14: 16,384 registers, ~0.8% error

#### 6.3.2 Count-Min Sketch

**Class**: `CountMinSketch(epsilon=0.01, delta=0.01)`

**Parameters**:
- `epsilon`: Error parameter (default 0.01)
- `delta`: Failure probability (default 0.01)

**Methods**:
- `add(value, count=1)`: Add element with count
- `estimate(value)`: Estimate frequency
- `get_memory_usage()`: Get memory in bytes

**Configuration**:
- ε=0.01, δ=0.01: 272×5 counters, ~5% error
- ε=0.001, δ=0.01: 2,719×5 counters, ~0.5% error
- ε=0.0001, δ=0.01: 27,183×5 counters, ~0.05% error

#### 6.3.3 Bloom Filter

**Class**: `BloomFilter(expected_items, false_positive_rate)`

**Parameters**:
- `expected_items`: Number of items to insert
- `false_positive_rate`: Desired FP rate (e.g., 0.01 for 1%)

**Methods**:
- `add(value)`: Add element to filter
- `contains(value)`: Test membership
- `get_memory_usage()`: Get memory in bytes

**Configuration**:
- 100K items, FP=0.1: 479K bits, 4 hash functions
- 100K items, FP=0.01: 959K bits, 7 hash functions
- 100K items, FP=0.001: 1.4M bits, 10 hash functions

#### 6.3.4 MinHash + LSH

**Classes**:
- `MinHash(num_permutations=128)`
- `LSH(num_bands, rows_per_band)`

**Parameters**:
- `num_permutations`: Signature length (default 128)
- `num_bands`: Number of bands for LSH
- `rows_per_band`: Rows per band (k = bands × rows)

**Methods**:
- `compute_signature(input_set)`: Compute MinHash signature
- `estimate_similarity(sig1, sig2)`: Estimate Jaccard similarity
- `add(key, signature)`: Add signature to LSH
- `get_candidates()`: Get candidate similar pairs

**Configuration**:
- 64 perms, 16×4 bands: threshold ≈ 0.5
- 128 perms, 32×4 bands: threshold ≈ 0.42 (default)
- 256 perms, 32×8 bands: threshold ≈ 0.65

### 6.4 Testing

**Test Suite**: `services/probabilistic_algorithms/test_algorithms.py`

**Coverage**:
- Basic functionality tests
- Edge case handling (empty inputs, single items, large inputs)
- Accuracy validation
- Parameter variations
- Merge operations (HyperLogLog)
- Similarity estimation (MinHash)
- Candidate generation (LSH)

**Results**: 28/28 tests passing

### 6.5 Benchmarking

**Benchmark Runner**: `services/probabilistic_algorithms/run_all_benchmarks.py`

**Metrics Collected**:
- Accuracy: Relative error, false positive rate, precision, recall
- Performance: Insertion time, query time, total time
- Memory: Algorithm memory vs exact method memory
- Reduction: Memory reduction factor

**Output**: `data/output/algorithm_benchmarks.json`

---

## 7. Experimental Results

### 7.1 Test Data Configuration

All benchmarks use synthetic data with controlled properties:

| Algorithm | Data Size | Distribution | Purpose |
|-----------|-----------|--------------|---------|
| HyperLogLog | 150K elements | 100K unique + 50K duplicates | Cardinality estimation |
| Count-Min Sketch | 100K items | Zipf-skewed (1K unique) | Frequency estimation |
| Bloom Filter | 100K training, 10K test | 50% in set | Membership testing |
| MinHash + LSH | 100 datasets | 100 items each, controlled similarity | Similarity detection |

### 7.2 HyperLogLog Results

**Test Data**: 150K elements (100K unique + 50K duplicates)

| p | Registers | Estimate | Exact | Relative Error | Time | Memory | Reduction |
|---|-----------|----------|-------|---------------|------|--------|-----------|
| 10 | 1,024 | 99,940 | 100,000 | 0.06% | 0.21s | 36 KB | 273x |
| 12 | 4,096 | 99,815 | 100,000 | 0.19% | 0.21s | 144 KB | 68x |
| 14 | 16,384 | 99,820 | 100,000 | 0.18% | 0.22s | 576 KB | 17x |

**Analysis**:
- Excellent accuracy (<0.2% error)
- Significant memory reduction (17-273x)
- Runtime comparable to exact counting
- p=12 provides best balance (default configuration)

### 7.3 Count-Min Sketch Results

**Test Data**: 100K items with Zipf-skewed distribution (1K unique)

| ε | δ | Width | Depth | Max Rel Error | Mean Rel Error | Time | Memory | Reduction |
|---|---|-------|-------|--------------|---------------|------|--------|-----------|
| 0.01 | 0.01 | 272 | 5 | 635% | 163% | 0.65s | 48 KB | 2.5x |
| 0.001 | 0.01 | 2,719 | 5 | 0% | 0% | 0.64s | 442 KB | 0.3x |
| 0.0001 | 0.01 | 27,183 | 5 | 0% | 0% | 0.62s | 4.3 MB | 0.0x |

**Analysis**:
- High error on highly skewed distributions with loose epsilon
- Accurate with tight epsilon (ε=0.001, ε=0.0001)
- Memory benefit only for very large datasets
- Suitable for frequency estimation on uniform/near-uniform distributions

### 7.4 Bloom Filter Results

**Test Data**: 100K training items, 10K test items (50% in set)

| Target FP | Actual FP | Bits | Hash Fn | Recall | Time | Memory | Reduction |
|-----------|-----------|------|---------|--------|------|--------|-----------|
| 0.1 | 0.0984 | 479K | 4 | 1.00 | 0.58s | 16 MB | 0.6x |
| 0.01 | 0.0094 | 959K | 7 | 1.00 | 1.04s | 32 MB | 0.3x |
| 0.001 | 0.0004 | 1.4M | 10 | 1.00 | 1.45s | 48 MB | 0.2x |

**Analysis**:
- Zero false negatives (perfect recall)
- Actual FP close to target
- Memory reduction not significant for small datasets
- Would show significant benefits for millions of items

### 7.5 MinHash + LSH Results

**Test Data**: 100 datasets, 100 items each, 19 similar pairs (threshold=0.5)

| Perms | Bands | Rows | Threshold | Candidates | Reduction | Precision | Recall | Time |
|-------|-------|------|-----------|------------|-----------|-----------|--------|------|
| 64 | 16 | 4 | 0.50 | 18 | 99.64% | 0.82 | 0.74 | 0.74s |
| 128 | 32 | 4 | 0.42 | 20 | 99.60% | 0.95 | 0.95 | 1.43s |
| 256 | 32 | 8 | 0.65 | 7 | 99.86% | 1.00 | 0.32 | 2.96s |

**Analysis**:
- Excellent candidate reduction (99.6-99.9%)
- 128 perms, 32×4 bands provides best balance (95% precision, 95% recall)
- Higher thresholds improve precision but reduce recall
- Dramatically faster than brute-force pairwise comparison

### 7.6 Extended Data Generation Results

**Configuration**: 30 days, 1000 transactions/day, 2000 ad events/day, 10000 customers

**Output**:
- Total records: 90,000
- Retail transactions: 30,000
- Advertisement events: 60,000
- Unique customers: 10,000
- Date range: 2026-09-25 to 2026-10-24

**Scalability**: Configurable to millions by increasing `--transactions-per-day` and `--ad-events-per-day`

---

## 8. Performance Analysis

### 8.1 Accuracy Summary

| Algorithm | Metric | Result | Status |
|-----------|--------|--------|--------|
| HyperLogLog | Relative Error | 0.19% | Excellent |
| Count-Min Sketch | Max Relative Error | 0% (ε=0.001) | Good (depends on distribution) |
| Bloom Filter | False Positive Rate | 0.94% (target 1%) | Excellent |
| Bloom Filter | False Negative Rate | 0% | Perfect |
| MinHash + LSH | Precision | 95% | Excellent |
| MinHash + LSH | Recall | 95% | Excellent |

### 8.2 Memory Efficiency

| Algorithm | Memory Usage | Exact Method | Reduction | Benefit |
|-----------|--------------|--------------|-----------|---------|
| HyperLogLog | 144 KB | 9.8 MB | 68x | High |
| Count-Min Sketch | 442 KB | 119 KB | 0.3x | Low (for small datasets) |
| Bloom Filter | 32 MB | 9.8 MB | 0.3x | Low (for small datasets) |
| MinHash + LSH | 512 B/set | N/A | N/A | Candidate reduction: 99.6% |

**Note**: Bloom Filter and Count-Min Sketch show memory benefits primarily for large datasets (millions of items).

### 8.3 Runtime Performance

| Algorithm | Insertion Time | Query Time | Total Time | Comparison |
|-----------|----------------|------------|------------|------------|
| HyperLogLog | 0.21s | 0.00s | 0.21s | Comparable to exact |
| Count-Min Sketch | 0.64s | 0.00s | 0.64s | Comparable to exact |
| Bloom Filter | 1.04s | 0.00s | 1.04s | Slower than exact (for small data) |
| MinHash + LSH | 1.43s | 0.00s | 1.43s | Much faster than brute-force |

### 8.4 Trade-off Analysis

#### HyperLogLog
- **Strengths**: Excellent accuracy, high memory reduction, simple implementation
- **Weaknesses**: None significant
- **Best For**: Cardinality estimation at any scale

#### Count-Min Sketch
- **Strengths**: Bounded error guarantees, handles updates well
- **Weaknesses**: High error on skewed distributions, memory benefit only at scale
- **Best For**: Frequency estimation on uniform/near-uniform distributions

#### Bloom Filter
- **Strengths**: Zero false negatives, controlled false positives
- **Weaknesses**: No deletion, memory benefit only at scale
- **Best For**: Membership testing, duplicate detection (especially at scale)

#### MinHash + LSH
- **Strengths**: Massive candidate reduction, configurable threshold
- **Weaknesses**: Precision/recall trade-off, requires parameter tuning
- **Best For**: Similarity search in large datasets

---

## 9. Conclusion

### 9.1 Summary of Achievements

1. **Extended Data Generation**: Successfully implemented a configurable synthetic data generator capable of producing 500K+ retail and advertisement records with reproducible results.

2. **Algorithm Implementation**: Implemented four probabilistic algorithms with comprehensive benchmarking:
   - HyperLogLog: 0.19% error with 68x memory reduction
   - Count-Min Sketch: 0% error with tight epsilon configuration
   - Bloom Filter: 0.94% FP rate with zero false negatives
   - MinHash + LSH: 95% precision/recall with 99.6% candidate reduction

3. **Testing**: Created comprehensive test suite with 28 tests covering functionality, edge cases, and accuracy validation.

4. **Dashboard**: Developed interactive algorithm comparison dashboard for visualizing benchmark results.

5. **Documentation**: Provided extensive documentation including theoretical background, mathematical formulations, and deployment guides.

6. **Architecture Preservation**: Successfully integrated new components into existing Hadoop-Spark-Kafka pipeline without disrupting original functionality.

### 9.2 Key Insights

1. **HyperLogLog** is production-ready for cardinality estimation with excellent accuracy and memory efficiency.

2. **Count-Min Sketch** requires careful parameter tuning, especially for skewed distributions. Works best with uniform data.

3. **Bloom Filter** provides perfect recall (zero false negatives) with controlled false positives. Memory benefits become significant at scale.

4. **MinHash + LSH** dramatically reduces pairwise comparison workload (99.6% reduction) while maintaining high precision and recall.

5. **Probabilistic algorithms** offer significant benefits for big data analytics when:
   - Exact computation is prohibitively expensive
   - Small error rates are acceptable
   - Memory constraints exist
   - Real-time processing is required

### 9.3 Future Work

1. **Integration with Spark Jobs**: Use algorithms in actual Spark transformations for production workloads.

2. **Streaming Algorithms**: Implement streaming versions of algorithms for real-time analytics.

3. **Parameter Auto-tuning**: Develop mechanisms to automatically select optimal parameters based on data characteristics.

4. **Additional Algorithms**: Implement other probabilistic algorithms (e.g., T-Digest for quantile estimation).

5. **Performance Optimization**: Profile and optimize algorithm implementations for better performance.

### 9.4 Final Remarks

This project successfully demonstrates the practical application of probabilistic algorithms in big data analytics. The implementation shows that these algorithms can provide significant benefits in terms of memory efficiency and computational speed while maintaining acceptable accuracy levels. The comprehensive benchmarking and documentation provide a solid foundation for understanding and using these algorithms in real-world scenarios.

---

## 10. References

1. Flajolet, P., Fusy, É., Gandouet, O., & Meunier, F. (2007). "HyperLogLog: the analysis of a near-optimal cardinality estimation algorithm." *Proceedings of the 2007 International Conference on Analysis of Algorithms*.

2. Cormode, G., & Muthukrishnan, S. (2005). "An improved data stream summary: the count-min sketch and its applications." *Journal of Algorithms*, 55(1), 58-75.

3. Bloom, B. H. (1970). "Space/time trade-offs in hash coding with allowable errors." *Communications of the ACM*, 13(7), 422-426.

4. Broder, A. Z. (1997). "On the resemblance and containment of documents." *Proceedings of the Compression and Complexity of Sequences*.

5. Broder, A. Z., Charikar, M., Frieze, A. M., & Mitzenmacher, M. (2000). "Min-wise independent permutations." *Journal of Computer and System Sciences*, 60(3), 630-659.

6. Apache Spark. (2024). "Apache Spark Documentation." https://spark.apache.org/docs/latest/

7. Apache Kafka. (2024). "Apache Kafka Documentation." https://kafka.apache.org/documentation/

8. Apache Hadoop. (2024). "Apache Hadoop Documentation." https://hadoop.apache.org/docs/stable/
