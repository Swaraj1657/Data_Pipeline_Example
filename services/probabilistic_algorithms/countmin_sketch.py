"""Count-Min Sketch implementation for frequency estimation.

Count-Min Sketch is a probabilistic data structure for estimating the frequency
of events in a data stream. It uses sub-linear space to provide approximate
frequency counts with bounded error.

Algorithm:
1. Use d pairwise independent hash functions
2. Each hash function maps to a row of w counters
3. For each item, increment all d counters at their hash positions
4. To estimate frequency, take the minimum of the d counters

Time Complexity: O(1) per update and query
Space Complexity: O(d * w) where d = depth, w = width
Error: With probability 1-δ, estimate is within ε*N of true frequency
Parameters: ε (epsilon) controls error, δ (delta) controls failure probability
Recommended: w = ceil(e/ε), d = ceil(ln(1/δ))
"""

import hashlib
import math
import time
import random
from typing import Dict, List, Tuple, Any
import sys


class CountMinSketch:
    """Count-Min Sketch frequency estimator."""

    def __init__(self, epsilon: float = 0.01, delta: float = 0.01):
        """
        Initialize Count-Min Sketch.

        Args:
            epsilon: Error parameter (smaller = more accurate but more memory)
            delta: Failure probability (smaller = more robust but more memory)
        """
        self.epsilon = epsilon
        self.delta = delta

        # Calculate dimensions
        self.w = math.ceil(math.e / epsilon)
        self.d = math.ceil(math.log(1.0 / delta))

        # Initialize counters
        self.counters = [[0] * self.w for _ in range(self.d)]

        # Generate hash seeds for each row
        self.seeds = [random.randint(0, 2**31 - 1) for _ in range(self.d)]

    def _hash(self, value: str, seed: int) -> int:
        """Hash a value to a counter index using double hashing."""
        hash_obj = hashlib.md5(f"{seed}{value}".encode('utf-8'))
        hash_int = int(hash_obj.hexdigest()[:8], 16)
        return hash_int % self.w

    def add(self, value: str, count: int = 1) -> None:
        """
        Add a value to the sketch.

        Args:
            value: The value to add
            count: The count to add (default 1)
        """
        for i in range(self.d):
            idx = self._hash(value, self.seeds[i])
            self.counters[i][idx] += count

    def estimate(self, value: str) -> int:
        """
        Estimate the frequency of a value.

        Args:
            value: The value to query

        Returns:
            Estimated frequency
        """
        min_count = float('inf')
        for i in range(self.d):
            idx = self._hash(value, self.seeds[i])
            min_count = min(min_count, self.counters[i][idx])
        return min_count

    def get_memory_usage(self) -> int:
        """Get memory usage in bytes."""
        return sys.getsizeof(self.counters) + sum(
            sys.getsizeof(row) + sum(sys.getsizeof(c) for c in row)
            for row in self.counters
        )


def benchmark_countmin_sketch(
    data: List[str],
    epsilon_values: List[float] = [0.01, 0.001, 0.0001],
    delta: float = 0.01,
) -> Dict[str, Any]:
    """
    Benchmark Count-Min Sketch against exact counting.

    Args:
        data: List of values to count
        epsilon_values: List of epsilon values to test
        delta: Failure probability parameter

    Returns:
        Dictionary with benchmark results
    """
    # Exact counting
    start_time = time.time()
    exact_counts: Dict[str, int] = {}
    for value in data:
        exact_counts[value] = exact_counts.get(value, 0) + 1
    exact_time = time.time() - start_time
    exact_memory = sys.getsizeof(exact_counts) + sum(
        sys.getsizeof(k) + sys.getsizeof(v) for k, v in exact_counts.items()
    )

    results = {
        "num_items": len(data),
        "num_unique": len(exact_counts),
        "exact_time": exact_time,
        "exact_memory": exact_memory,
        "cms_results": []
    }

    for epsilon in epsilon_values:
        cms = CountMinSketch(epsilon=epsilon, delta=delta)

        # Insertion time
        start_time = time.time()
        for value in data:
            cms.add(value)
        insertion_time = time.time() - start_time

        # Query time for all unique items
        start_time = time.time()
        estimates = {value: cms.estimate(value) for value in exact_counts.keys()}
        query_time = time.time() - start_time

        # Calculate error metrics
        absolute_errors = []
        relative_errors = []

        for value, exact_count in exact_counts.items():
            estimated = estimates[value]
            abs_error = abs(estimated - exact_count)
            rel_error = abs_error / exact_count if exact_count > 0 else 0
            absolute_errors.append(abs_error)
            relative_errors.append(rel_error)

        max_absolute_error = max(absolute_errors)
        mean_absolute_error = sum(absolute_errors) / len(absolute_errors)
        max_relative_error = max(relative_errors)
        mean_relative_error = sum(relative_errors) / len(relative_errors)

        memory_usage = cms.get_memory_usage()

        results["cms_results"].append({
            "epsilon": epsilon,
            "delta": delta,
            "width": cms.w,
            "depth": cms.d,
            "num_counters": cms.w * cms.d,
            "max_absolute_error": max_absolute_error,
            "mean_absolute_error": mean_absolute_error,
            "max_relative_error": max_relative_error,
            "mean_relative_error": mean_relative_error,
            "insertion_time": insertion_time,
            "query_time": query_time,
            "total_time": insertion_time + query_time,
            "memory_usage": memory_usage,
            "memory_reduction": exact_memory / memory_usage if memory_usage > 0 else 0,
        })

    return results


def run_cms_demo():
    """Run a demonstration of Count-Min Sketch."""
    print("=" * 80)
    print("Count-Min Sketch Frequency Estimation Demo")
    print("=" * 80)

    # Generate test data with skewed distribution (Zipf-like)
    print("\nGenerating test data with skewed distribution...")
    num_items = 100000
    num_unique = 1000

    # Generate with Zipf-like distribution (few items very frequent)
    data = []
    for i in range(num_items):
        # Zipf-like distribution: probability ~ 1/(rank^alpha)
        zipf_param = 1.5
        # Generate Zipf-distributed index
        u = random.random()
        idx = int((num_unique * (1 - u) ** (-1 / (zipf_param - 1)))) % num_unique
        data.append(f"item_{idx}")

    print(f"Total items: {num_items:,}")
    print(f"Unique items: {num_unique:,}")

    # Run benchmark
    print("\n" + "-" * 80)
    print("Running benchmark...")
    print("-" * 80)

    results = benchmark_countmin_sketch(data, epsilon_values=[0.01, 0.001, 0.0001])

    print(f"\nExact Counting:")
    print(f"  Unique items: {results['num_unique']:,}")
    print(f"  Time: {results['exact_time']:.4f}s")
    print(f"  Memory: {results['exact_memory'] / 1024:.2f} KB")

    print(f"\nCount-Min Sketch Results:")
    print(f"{'Eps':<8} {'Delta':<8} {'Width':<8} {'Depth':<6} {'Max Rel Err':<12} {'Mean Rel Err':<12} "
          f"{'Time':<10} {'Memory':<12} {'Reduction':<10}")
    print("-" * 100)

    for r in results["cms_results"]:
        print(f"{r['epsilon']:<8.4f} {r['delta']:<8.4f} {r['width']:<8} {r['depth']:<6} "
              f"{r['max_relative_error']:<12.4%} {r['mean_relative_error']:<12.4%} "
              f"{r['total_time']:<10.4f}s {r['memory_usage']/1024:<12.2f}KB "
              f"{r['memory_reduction']:<10.1f}x")

    print("\n" + "=" * 80)
    print("Count-Min Sketch Summary:")
    print("=" * 80)
    print("Count-Min Sketch provides frequency estimates with bounded error.")
    print(f"With epsilon=0.001, we achieved max relative error of {results['cms_results'][1]['max_relative_error']:.2%}")
    print(f"while using {results['cms_results'][1]['memory_usage']/1024:.2f} KB vs {results['exact_memory']/1024:.2f} KB for exact counting.")
    print("Memory reduction: {:.1f}x".format(results['cms_results'][1]['memory_reduction']))
    print("\nKey insight: epsilon controls accuracy vs memory trade-off. Smaller epsilon = more accurate but more memory.")
    print("=" * 80)


if __name__ == "__main__":
    run_cms_demo()
