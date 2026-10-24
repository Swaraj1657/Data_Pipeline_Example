"""Probabilistic Algorithms Module for InstaMart Analytics.

This module implements beyond-syllabus probabilistic algorithms for big data analytics:
- HyperLogLog: Cardinality estimation
- Count-Min Sketch: Frequency estimation
- Bloom Filter: Membership testing
- MinHash + LSH: Similarity detection

Each algorithm includes benchmarking against exact methods to demonstrate
accuracy, runtime, and memory trade-offs.
"""

from .hyperloglog import HyperLogLog, benchmark_hyperloglog
from .countmin_sketch import CountMinSketch, benchmark_countmin_sketch
from .bloom_filter import BloomFilter, benchmark_bloom_filter
from .minhash_lsh import MinHash, LSH, benchmark_minhash_lsh

__all__ = [
    'HyperLogLog',
    'CountMinSketch',
    'BloomFilter',
    'MinHash',
    'LSH',
    'benchmark_hyperloglog',
    'benchmark_countmin_sketch',
    'benchmark_bloom_filter',
    'benchmark_minhash_lsh',
]
