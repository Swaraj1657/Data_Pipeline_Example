# Probabilistic Algorithms Documentation

This document provides detailed information about the probabilistic algorithms
implemented in this project, including theoretical background, implementation
details, parameter tuning, and benchmark methodology.

## Table of Contents

1. [HyperLogLog](#hyperloglog)
2. [Count-Min Sketch](#count-min-sketch)
3. [Bloom Filter](#bloom-filter)
4. [MinHash + LSH](#minhash--lsh)
5. [Benchmark Methodology](#benchmark-methodology)
6. [Integration with Pipeline](#integration-with-pipeline)

---

## HyperLogLog

### Theoretical Background

HyperLogLog is a probabilistic algorithm for estimating the cardinality (number
of distinct elements) of a multiset. It was introduced by Flajolet et al. in 2007
as an improvement over the LogLog algorithm.

**Key Insight**: The position of the leftmost 1-bit in a random hash value follows
a geometric distribution. By tracking the maximum position across many hash values,
we can estimate the number of distinct items.

### Algorithm Details

1. **Hashing**: Each element is hashed to a uniform random 64-bit value
2. **Register Selection**: First p bits determine which of m = 2^p registers to use
3. **Leading Zeros**: Count leading zeros (ρ) in the remaining bits
4. **Update**: Store the maximum ρ for each register
5. **Estimation**: Combine registers using harmonic mean

### Mathematical Formulation

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

**Corrections**:
- Small range (E ≤ 2.5m): Use linear counting
- Large range (E > 2^64/30): Apply large range correction

### Complexity Analysis

| Metric | Value |
|--------|-------|
| Time (insert) | O(1) |
| Time (estimate) | O(m) |
| Space | O(m) = O(2^p) |
| Relative Error | ≈ 1.04/√m |

### Parameter Tuning

| p | Registers (m) | Memory | Error | Use Case |
|---|---------------|--------|-------|----------|
| 10 | 1,024 | 8 KB | ~3% | Quick estimates |
| 12 | 4,096 | 32 KB | ~1.6% | **Default** |
| 14 | 16,384 | 128 KB | ~0.8% | High accuracy |
| 16 | 65,536 | 512 KB | ~0.4% | Very high accuracy |

### Implementation Notes

- Uses MD5 for 128-bit hashing (first 64 bits used)
- Supports merge operation for distributed computing
- Handles edge cases: empty set, single element, very large cardinalities

### Use Cases in Retail Analytics

1. **Unique Customer Count**: Count distinct customers without storing all IDs
2. **Unique Product Views**: Track how many different products were viewed
3. **Daily Active Users**: Estimate DAU/MAU with minimal memory
4. **Campaign Reach**: Measure unique ad viewers across campaigns

---

## Count-Min Sketch

### Theoretical Background

Count-Min Sketch is a probabilistic data structure for estimating frequency of
events in a data stream. It provides frequency estimates with bounded error and
was introduced by Cormode and Muthukrishnan in 2005.

**Key Insight**: By using multiple hash functions and taking the minimum counter
value, we can bound the estimation error while using sub-linear space.

### Algorithm Details

1. **Hash Functions**: Use d pairwise independent hash functions
2. **Counter Array**: Each hash function maps to a row of w counters
3. **Update**: Increment all d counters at hash positions
4. **Query**: Return minimum of d counters (upper bound on true frequency)

### Mathematical Formulation

**Dimensions**:
```
w = ceil(e / ε)     # Width
d = ceil(ln(1/δ))   # Depth
```

**Update**:
```
for i in 1..d:
    counter[i][hash_i(item)] += count
```

**Query**:
```
estimate(item) = min(counter[i][hash_i(item)] for i in 1..d)
```

**Error Guarantee**:
With probability at least 1-δ:
```
|estimate - true_frequency| ≤ ε * N
where N = total items in stream
```

### Complexity Analysis

| Metric | Value |
|--------|-------|
| Time (update) | O(d) |
| Time (query) | O(d) |
| Space | O(d * w) |
| Error | ε * N with probability 1-δ |

### Parameter Tuning

| ε | δ | Width (w) | Depth (d) | Counters | Memory | Use Case |
|---|---|-----------|----------|----------|--------|----------|
| 0.1 | 0.1 | 28 | 3 | 84 | 336 B | Rough estimates |
| 0.01 | 0.01 | 272 | 5 | 1,360 | 5.4 KB | **Default** |
| 0.001 | 0.001 | 2,719 | 7 | 19,033 | 76 KB | High accuracy |
| 0.0001 | 0.001 | 27,183 | 7 | 190,281 | 760 KB | Very high accuracy |

### Implementation Notes

- Uses double hashing with MD5 for pairwise independence
- Estimates are always upper bounds (never undercount)
- Handles skewed distributions well (Zipf-like)
- Supports count-weighted updates

### Use Cases in Retail Analytics

1. **Product Click Frequency**: Track how often each product is clicked
2. **Ad Impression Count**: Estimate advertisement impression counts
3. **Trending Items**: Find frequently viewed/added items
4. **Hotspot Detection**: Identify high-frequency events in streams

---

## Bloom Filter

### Theoretical Background

Bloom Filter is a space-efficient probabilistic data structure for testing set
membership. It was introduced by Burton Howard Bloom in 1970. The key property
is that it never produces false negatives, only false positives.

**Key Insight**: Multiple hash functions map each element to multiple bit positions.
Setting these bits to 1 allows membership testing with controlled false positive rate.

### Algorithm Details

1. **Bit Array**: Initialize m-bit array to all zeros
2. **Hash Functions**: Use k independent hash functions
3. **Add**: Compute k hash positions, set all bits to 1
4. **Test**: Check if all k bits are set
   - If any bit is 0: definitely not in set
   - If all bits are 1: probably in set (may be false positive)

### Mathematical Formulation

**Optimal Size**:
```
m = -n * ln(p) / (ln(2))²
```

**Optimal Hash Functions**:
```
k = (m/n) * ln(2)
```

**False Positive Rate**:
```
P(FP) = (1 - e^(-kn/m))^k
```

### Complexity Analysis

| Metric | Value |
|--------|-------|
| Time (add) | O(k) |
| Time (test) | O(k) |
| Space | O(m) bits |
| False Positive Rate | (1 - e^(-kn/m))^k |
| False Negative Rate | 0 |

### Parameter Tuning

| n (items) | p (FP rate) | m (bits) | k (hashes) | Memory | Use Case |
|-----------|-------------|-----------|------------|--------|----------|
| 10K | 0.1 | 48K | 3 | 6 KB | Loose filtering |
| 100K | 0.01 | 959K | 7 | 120 KB | **Default** |
| 1M | 0.001 | 19M | 10 | 2.4 MB | Strict filtering |
| 10M | 0.0001 | 239M | 13 | 30 MB | Very strict |

### Implementation Notes

- Uses MD5-based double hashing for k independent hash functions
- Memory-efficient: uses bit array (not byte array)
- Supports union operation (OR of bit arrays)
- No deletion operation (standard Bloom Filter)

### Use Cases in Retail Analytics

1. **Duplicate Detection**: Check if order ID already processed
2. **Cache Miss Filtering**: Avoid cache lookups for non-existent keys
3. **Spam/Event Filtering**: Block repeated fraudulent events
4. **Join Optimization**: Pre-filter before expensive joins

---

## MinHash + LSH

### Theoretical Background

MinHash is a technique for estimating Jaccard similarity between sets using
reduced signatures. Locality Sensitive Hashing (LSH) builds on MinHash to efficiently
find similar pairs without comparing all pairs.

**Jaccard Similarity**:
```
J(A, B) = |A ∩ B| / |A ∪ B|
```

**MinHash Property**: Probability that minhash values match equals Jaccard similarity.

### Algorithm Details

#### MinHash

1. **Hash Functions**: Generate k random hash functions
2. **Signature**: For each set, compute minimum hash value for each function
3. **Similarity**: Fraction of matching signature values ≈ Jaccard similarity

#### LSH

1. **Banding**: Divide signature into b bands of r rows each (k = b * r)
2. **Hash Bands**: Hash each band to a bucket
3. **Candidates**: Items in same bucket for any band are candidate pairs
4. **Verify**: Compute exact Jaccard similarity for candidates

### Mathematical Formulation

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
```

**Probability of Collision**:
```
P(collision in band) = 1 - (1 - s^r)^b
where s = Jaccard similarity
```

### Complexity Analysis

| Metric | Value |
|--------|-------|
| MinHash signature | O(k * \|S\|) per set |
| LSH candidate search | O(n * b) |
| Exact Jaccard | O(\|A\| + \|B\|) per pair |
| Space per set | O(k) |

### Parameter Tuning

| k | b | r | Threshold | Signature Size | Use Case |
|---|---|---|-----------|---------------|----------|
| 64 | 16 | 4 | 0.177 | 256 B | Low threshold |
| 128 | 20 | 6 | 0.415 | 512 B | **Default** |
| 256 | 32 | 8 | 0.595 | 1 KB | High threshold |
| 512 | 64 | 8 | 0.917 | 2 KB | Very high threshold |

**Trade-off**: Higher threshold = fewer false positives but may miss some similar pairs.

### Implementation Notes

- Uses MD5 for random hash function simulation
- Supports union of signatures (min of each position)
- LSH buckets use separate hash per band
- Configurable band/row combinations

### Use Cases in Retail Analytics

1. **Similar Products**: Find products with similar customer interaction patterns
2. **Campaign Clustering**: Group campaigns with similar audience overlap
3. **Customer Segmentation**: Find customers with similar purchase histories
4. **Recommendation**: Recommend items similar to user's preferences

---

## Benchmark Methodology

### Test Data Generation

All benchmarks use synthetic data with controlled properties:

1. **HyperLogLog**: 100K unique items + 50K duplicates
2. **Count-Min Sketch**: 100K items with Zipf distribution (α=1.5)
3. **Bloom Filter**: 100K training items, 10K test items (50% in set)
4. **MinHash + LSH**: 50 datasets with controlled similarity

### Metrics Collected

For each algorithm, we measure:

1. **Accuracy Metrics**:
   - Relative error (HyperLogLog, Count-Min Sketch)
   - False positive rate (Bloom Filter)
   - Precision/Recall (MinHash + LSH)

2. **Performance Metrics**:
   - Insertion time
   - Query time
   - Total time

3. **Memory Metrics**:
   - Algorithm memory usage
   - Exact method memory usage
   - Memory reduction factor

### Comparison Baselines

Each algorithm is compared against an exact method:

| Algorithm | Exact Method |
|-----------|--------------|
| HyperLogLog | Python set |
| Count-Min Sketch | Python dict |
| Bloom Filter | Python set |
| MinHash + LSH | Brute-force pairwise comparison |

### Reproducibility

- Fixed random seeds (seed=42)
- Deterministic hash functions
- Multiple parameter configurations tested
- Results saved to JSON for analysis

---

## Integration with Pipeline

### Running Benchmarks in Docker

The algorithm dashboard is integrated into the batch stack:

```bash
docker compose -f docker-compose.batch.yml up algorithm-dashboard
```

Access at: http://localhost:5200

### Standalone Execution

Run benchmarks locally without Docker:

```bash
# Individual algorithm demos
python services/probabilistic_algorithms/hyperloglog.py
python services/probabilistic_algorithms/countmin_sketch.py
python services/probabilistic_algorithms/bloom_filter.py
python services/probabilistic_algorithms/minhash_lsh.py

# Run all tests
python services/probabilistic_algorithms/test_algorithms.py
```

### Using Algorithms in Spark Jobs

The algorithms can be imported and used in Spark jobs:

```python
from services.probabilistic_algorithms import HyperLogLog

# In a Spark UDF
def count_unique(customers):
    hll = HyperLogLog(p=12)
    for customer in customers:
        hll.add(customer)
    return hll.count()

# Register UDF
spark.udf.register("count_unique", count_unique)
```

### Output Integration

Benchmark results are saved to:
```
data/output/algorithm_benchmarks.json
```

This file contains:
- Timestamp
- Algorithm-specific results
- Configuration parameters
- Metrics for comparison

The dashboard reads this file to display results.

---

## References

1. **HyperLogLog**: Flajolet, P., Fusy, É., Gandouet, O., & Meunier, F. (2007).
   "HyperLogLog: the analysis of a near-optimal cardinality estimation algorithm."

2. **Count-Min Sketch**: Cormode, G., & Muthukrishnan, S. (2005).
   "An improved data stream summary: the count-min sketch and its applications."

3. **Bloom Filter**: Bloom, B. H. (1970).
   "Space/time trade-offs in hash coding with allowable errors."

4. **MinHash**: Broder, A. Z. (1997).
   "On the resemblance and containment of documents."

5. **LSH**: Broder, A. Z., Charikar, M., Frieze, A. M., & Mitzenmacher, M. (2000).
   "Min-wise independent permutations."
