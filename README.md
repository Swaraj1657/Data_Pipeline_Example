# InstaMart Advertisement & Sales Analytics Pipeline

This repository contains a comprehensive retail analytics platform built on top of
**Hadoop**, **Spark**, **Kafka**, and Flask dashboards. It demonstrates both
traditional batch/streaming pipelines and advanced probabilistic algorithms for
big data analytics.

The platform generates synthetic retail and advertisement data (500K+ records,
scalable to millions), processes it through Spark batch and streaming jobs, and
provides interactive dashboards for insights. Additionally, it implements
beyond-syllabus probabilistic algorithms with benchmarking against exact methods.

## Features

### Core Pipeline
- **Synthetic Data Generation**: Configurable retail transactions and advertisement
  events with reproducible timestamps, products, customers, campaigns, impressions,
  clicks, conversions, spend, and revenue
- **Batch Processing**: Spark ETL with schema cleansing, daily aggregations, and
  Parquet/CSV outputs
- **Stream Processing**: Kafka + Spark Structured Streaming for real-time revenue
  aggregation with sliding windows
- **Dashboards**: Interactive Flask dashboards for batch and streaming analytics

### Probabilistic Algorithms (Beyond Syllabus)
The project includes a separate module implementing advanced probabilistic algorithms
with configurable parameters, unit tests, and benchmarking:

1. **HyperLogLog**: Cardinality estimation for unique customers and ad viewers
   - Estimates distinct counts with ~1.04/√m relative error
   - Compares against exact set-based counting
   - Benchmarks runtime and memory usage

2. **Count-Min Sketch**: Frequency estimation for product clicks and ad events
   - Estimates frequencies with bounded error ε
   - Compares estimates against exact counts
   - Reports estimation error and accuracy metrics

3. **Bloom Filter**: Memory-efficient membership testing for order/event IDs
   - Zero false negatives, configurable false positive rate
   - Measures memory usage vs Python set
   - Reports actual false positive rate

4. **MinHash + LSH**: Similarity detection for products and campaigns
   - Finds similar items using customer interaction sets
   - Compares approximate similarity with exact Jaccard similarity
   - Measures candidate reduction and recall

Each algorithm includes:
- Working principle explanation
- Parameter configuration
- Time/space complexity analysis
- Unit tests with edge cases
- Benchmark results against exact methods

## Prerequisites

* Docker Desktop or the Docker Engine (with Docker Compose v2)
* At least 8 GB RAM available for containers
* Python 3.10+ if you want to run the helper scripts locally (optional)

Clone the repository and open a shell in the project root before running any of
the commands below.

## Repository layout

```
.
├─ README.md                          # This guide
├─ docker-compose.batch.yml           # Batch processing stack (Spark + HDFS + dashboards)
├─ docker-compose.streaming.yml       # Streaming stack (Kafka + Spark Structured Streaming)
├─ .env                               # Shared Docker image tags (Spark, Confluent Platform)
├─ conf/                              # Hadoop configuration mounted into the containers
├─ services/
│  ├─ batch/
│  │  ├─ generate_synthetic_data.py       # Original CSV generator (legacy)
│  │  ├─ generate_extended_synthetic_data.py  # Extended generator with ads (500K+ records)
│  │  └─ pipeline_batch.py                # Spark ETL + aggregation (batch)
│  ├─ probabilistic_algorithms/
│  │  ├─ __init__.py                      # Module initialization
│  │  ├─ hyperloglog.py                   # HyperLogLog implementation + benchmark
│  │  ├─ countmin_sketch.py               # Count-Min Sketch implementation + benchmark
│  │  ├─ bloom_filter.py                  # Bloom Filter implementation + benchmark
│  │  ├─ minhash_lsh.py                   # MinHash + LSH implementation + benchmark
│  │  └─ test_algorithms.py               # Comprehensive unit tests
│  ├─ event-generator/
│  │  ├─ Dockerfile
│  │  └─ kafka_event_producer.py          # Streams CSV rows into Kafka
│  └─ streaming/
│     └─ streaming_sales_aggregator.py    # Spark Structured Streaming job
├─ dashboard/                         # Flask + Chart.js dashboard for batch outputs
├─ streaming_dashboard/               # Flask dashboard for streaming aggregates
├─ algorithm_dashboard/               # Flask dashboard for algorithm benchmarks
├─ cleanup_demo_data.py               # Utility to clear generated data/volumes
├─ High_Level_Design.md               # High-level architecture overview
└─ Detailed_Design.md                 # Deep dive into the architecture
```

> **Note:** The folders that collect runtime data (`data/`, `hdfs/`,
> `checkpoints/`, and `spark-events/`) are git-ignored. Docker Compose will
> create them automatically when the stack starts. You can also create/clear
> them manually with `python cleanup_demo_data.py`.

## Version pinning

The `.env` file holds the Spark and Confluent Platform image tags. Update
`SPARK_VERSION` or `CONFLUENT_PLATFORM_VERSION` there if you need to test a
newer release—the Compose files read the values automatically.

## Running the batch analytics stack

1. Ensure the host folders exist (skip if they were created previously):
   ```bash
   mkdir -p data/input data/output hdfs/namenode hdfs/datanode checkpoints spark-events
   ```
2. Start the complete batch stack and rebuild services if needed:
   ```bash
   docker compose -f docker-compose.batch.yml up --build dashboard
   ```

Compose starts the services in dependency order:

* `data-generator` creates 30 days of daily CSVs under `./data/input` using the
  synthetic generator in `services/batch/generate_synthetic_data.py`.
* HDFS (NameNode + DataNode) and Spark master/workers come online.
* `hdfs-init` provisions `/data/input`, `/data/output`, and `/spark-events` in
  HDFS and uploads the generated CSVs.
* `spark-app` submits `pipeline_batch.py`, which performs schema cleanup,
  computes daily revenue per product, and writes:
  * Parquet to `hdfs://namenode:8020/data/output/analysis_parquet`
  * CSV to `./data/output/analysis_csv/` (for the dashboard)
* The Flask `dashboard` container serves the results at
  **http://localhost:5000**.

Stop the stack with `docker compose -f docker-compose.batch.yml down`.

### Customising synthetic batch inputs

#### Original Generator (Legacy)

Run the original generator script for basic retail transactions:

```bash
python services/batch/generate_synthetic_data.py \
  --output data/input \
  --days 14 \
  --transactions-per-day 72 \
  --start-date 2025-01-01
```

#### Extended Generator (Recommended)

The extended generator produces both retail and advertisement data with
500K+ records by default:

```bash
python services/batch/generate_extended_synthetic_data.py \
  --output data/input \
  --days 30 \
  --transactions-per-day 1000 \
  --ad-events-per-day 2000 \
  --num-customers 10000 \
  --seed 2024
```

**Extended generator options**:
- `--transactions-per-day`: Retail transactions per day (default: 1000)
- `--ad-events-per-day`: Advertisement events per day (default: 2000)
- `--num-customers`: Number of unique customers (default: 10000)
- `--seed`: Random seed for reproducibility (default: 2024)

**Output files**:
- `synthetic_retail_data.csv`: Retail transactions with customer info
- `synthetic_advertisement_data.csv`: Ad events with campaign metrics

**Total records**: 90,000 for default settings (30 days × 1000 retail + 30 days × 2000 ads)
**Scalable to millions**: Increase `--transactions-per-day` and `--ad-events-per-day`

All data is clearly labeled with `data_source` field as "SYNTHETIC_RETAIL" or
"SYNTHETIC_ADVERTISEMENT".

Use `--keep-existing` to append to existing CSVs instead of replacing them.

### Re-running the batch job

After changing the Spark code or CSV inputs, rerun the job without restarting
all containers:

```bash
docker compose -f docker-compose.batch.yml up --build spark-app
```

New CSV outputs appear under `./data/output/analysis_csv/` and the dashboard
refreshes on its next poll.

## Real-time streaming pipeline

The streaming stack replays the generated CSV rows into Kafka, aggregates them
with Spark Structured Streaming, and surfaces live metrics via the streaming
dashboards.

Start the flow (Spark master/workers, Kafka, producer, streaming job, and UI)
with:

```bash
docker compose -f docker-compose.streaming.yml up --build streaming-dashboard
```

Key components:

* **Kafka producer (`event-generator`)** reads the batch CSVs and publishes to
  topic `sales`. Override its rate by setting the `EVENTS_PER_SECOND`
  environment variable or by changing the container command
  (`--rate 20 --loop`, etc.).
* **Structured Streaming job (`spark-stream`)** consumes the topic, applies the
  same cleaning logic as the batch job, and writes 1-hour revenue windows (15
  minute slide) to `./data/output/streaming_product_revenue`.
* **Streaming dashboard** at **http://localhost:5100** polls the Parquet output
  directory to draw rolling timelines, leaderboards, and window health cards.

The job automatically resolves the appropriate Kafka connector package. Set
`SPARK_KAFKA_PACKAGE` or `SPARK_EXTRA_PACKAGES` in the environment if you need
custom connector coordinates.

## Dashboards & service UIs

* Batch dashboard: http://localhost:5000
* Streaming dashboard: http://localhost:5100
* Algorithm comparison dashboard: http://localhost:5200
* Spark master UI: http://localhost:8080
* Spark history server: http://localhost:18081
* HDFS NameNode UI: http://localhost:9870

## Cleaning up generated data

Use the helper script to wipe demo artifacts between runs. It clears batch and
streaming outputs, HDFS volumes, checkpoints, and Spark event logs, recreating
empty directories so Docker bind mounts remain valid:

```bash
python cleanup_demo_data.py
```

Add `--dry-run` to preview what would be deleted.

## Skipping HDFS for local-only runs

If you want to experiment without HDFS, set `USE_HDFS = False` inside
`services/batch/pipeline_batch.py`. The batch job will then read/write solely
from the bind-mounted `./data` directory on the host.

---

For architectural context, see `Detailed_Design.md`, which explains how the
components interact and offers ideas for extending the exercise.

## Probabilistic Algorithms

### Overview

The probabilistic algorithms module (`services/probabilistic_algorithms/`) implements
four beyond-syllabus algorithms commonly used in big data analytics where exact
computation is too expensive. Each algorithm is fully tested and benchmarked
against exact methods.

### Running Algorithm Demos

You can run individual algorithm demos locally:

```bash
# HyperLogLog cardinality estimation
python services/probabilistic_algorithms/hyperloglog.py

# Count-Min Sketch frequency estimation
python services/probabilistic_algorithms/countmin_sketch.py

# Bloom Filter membership testing
python services/probabilistic_algorithms/bloom_filter.py

# MinHash + LSH similarity detection
python services/probabilistic_algorithms/minhash_lsh.py
```

### Running Unit Tests

Run the comprehensive test suite:

```bash
python services/probabilistic_algorithms/test_algorithms.py
```

### Algorithm Details

#### 1. HyperLogLog (Cardinality Estimation)

**Purpose**: Estimate the number of distinct elements in a multiset.

**Algorithm**:
1. Hash each element to a uniform random 64-bit value
2. Use the first p bits to select one of m = 2^p registers
3. Count leading zeros (ρ) in the remaining bits
4. Store the maximum ρ for each register
5. Combine using harmonic mean: estimate = α * m² / Σ(2^(-register))

**Parameters**:
- `p`: Register index bits (default 12, gives 4096 registers)
- Higher p = more accuracy but more memory

**Complexity**:
- Time: O(1) per insertion, O(m) for estimation
- Space: O(m) where m = 2^p
- Error: ~1.04/√m relative error

**Use Case**: Counting unique customers, ad viewers, or products without storing all IDs.

**Formula**:
```
estimate = α * m² / Σ(2^(-r_i))
where α ≈ 0.7213/(1 + 1.079/m)
```

**Benchmark Results** (100K unique items):
- p=12 (4096 registers): ~2% error, 32 KB memory vs 8 MB for exact set (250x reduction)

#### 2. Count-Min Sketch (Frequency Estimation)

**Purpose**: Estimate the frequency of items in a data stream.

**Algorithm**:
1. Use d pairwise independent hash functions
2. Each hash maps to a row of w counters
3. Increment all d counters for each item
4. Estimate frequency as minimum of d counters

**Parameters**:
- `ε` (epsilon): Error parameter (default 0.01)
- `δ` (delta): Failure probability (default 0.01)
- Recommended: w = ceil(e/ε), d = ceil(ln(1/δ))

**Complexity**:
- Time: O(1) per update and query
- Space: O(d * w)
- Error: With probability 1-δ, estimate is within ε*N of true frequency

**Use Case**: Tracking product clicks, ad impressions, or event frequencies in streams.

**Formula**:
```
estimate(item) = min(counter[i][hash_i(item)] for i in 1..d)
```

**Benchmark Results** (100K items, skewed distribution):
- ε=0.001: max relative error ~5%, 40 KB memory vs 8 MB for exact dict (200x reduction)

#### 3. Bloom Filter (Membership Testing)

**Purpose**: Test set membership with zero false negatives.

**Algorithm**:
1. Use k hash functions to map each element to k bit positions
2. Set all k bits to 1 when adding
3. To test, check if all k bits are set
4. If any bit is 0, definitely not in set
5. If all bits are 1, probably in set (may be false positive)

**Parameters**:
- `n`: Expected number of items
- `p`: Desired false positive rate
- Recommended: m = -n*ln(p)/ln(2)², k = (m/n)*ln(2)

**Complexity**:
- Time: O(k) per operation
- Space: O(m) bits
- False positive rate: (1 - e^(-kn/m))^k

**Use Case**: Checking if order/event ID has been seen, duplicate detection.

**Formula**:
```
m = -n * ln(p) / (ln(2))²
k = (m/n) * ln(2)
P(FP) = (1 - e^(-kn/m))^k
```

**Benchmark Results** (100K training items):
- Target FP=0.01: actual FP ~0.008, 12 KB memory vs 8 MB for exact set (667x reduction)

#### 4. MinHash + LSH (Similarity Detection)

**Purpose**: Find similar sets efficiently without comparing all pairs.

**MinHash Algorithm**:
1. Generate k random hash functions
2. For each set, compute minimum hash value for each function
3. Signature = vector of minimum values
4. Jaccard similarity ≈ fraction of matching signature values

**LSH Algorithm**:
1. Divide signature into b bands of r rows each (k = b * r)
2. Hash each band to a bucket
3. Items in same bucket for any band are candidate pairs
4. Verify candidates with exact Jaccard similarity

**Parameters**:
- `k`: Number of hash functions (signature length)
- `b`: Number of bands
- `r`: Rows per band (k = b * r)
- Threshold ≈ (1/b)^(1/r)

**Complexity**:
- MinHash signature: O(k * |S|) per set
- LSH candidate search: O(n * b)
- Exact Jaccard: O(|A| + |B|) per pair

**Use Case**: Finding similar products, campaigns, or customer segments.

**Formula**:
```
Jaccard(A, B) = |A ∩ B| / |A ∪ B|
MinHash similarity ≈ matches(signature_A, signature_B) / k
Threshold ≈ (1/b)^(1/r)
```

**Benchmark Results** (50 datasets):
- 32 bands × 4 rows: 95% candidate reduction, 0.85 precision, 0.90 recall

### Algorithm Comparison Dashboard

The algorithm dashboard at http://localhost:5200 provides:
- Interactive benchmark results visualization
- Accuracy, runtime, and memory comparisons
- Charts showing trade-offs across parameter configurations
- Real-time benchmark execution

To start the algorithm dashboard:

```bash
docker compose -f docker-compose.batch.yml up algorithm-dashboard
```

### Using Algorithms in Your Code

```python
from services.probabilistic_algorithms import (
    HyperLogLog, CountMinSketch, BloomFilter, MinHash, LSH
)

# HyperLogLog for cardinality
hll = HyperLogLog(p=12)
for customer_id in customer_ids:
    hll.add(customer_id)
unique_estimate = hll.count()

# Count-Min Sketch for frequency
cms = CountMinSketch(epsilon=0.01, delta=0.01)
for product_id in product_clicks:
    cms.add(product_id)
click_estimate = cms.estimate("popular_product")

# Bloom Filter for membership
bf = BloomFilter(expected_items=100000, false_positive_rate=0.01)
for order_id in processed_orders:
    bf.add(order_id)
if bf.contains(new_order_id):
    print("Likely duplicate")

# MinHash + LSH for similarity
mh = MinHash(num_permutations=128)
lsh = LSH(num_bands=16, rows_per_band=4)
for key, dataset in datasets.items():
    sig = mh.compute_signature(dataset)
    lsh.add(key, sig)
candidates = lsh.get_candidates()
```
