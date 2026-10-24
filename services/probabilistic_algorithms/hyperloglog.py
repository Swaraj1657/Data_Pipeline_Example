"""HyperLogLog implementation for cardinality estimation.

HyperLogLog is a probabilistic algorithm for estimating the number of distinct elements
in a multiset (cardinality). It uses significantly less memory than exact counting
while providing accurate estimates with bounded error.

Algorithm:
1. Hash each element to a uniform random value
2. Use the first p bits to determine one of m = 2^p registers
3. Count leading zeros in the remaining bits (rho)
4. Store the maximum rho for each register
5. Combine register values using harmonic mean to estimate cardinality

Time Complexity: O(1) per insertion, O(m) for estimation
Space Complexity: O(m) where m = 2^p (typically 12 bits = 4096 registers)
Error: ~1.04/sqrt(m) relative error
"""

import hashlib
import math
import time
from typing import Set, List, Tuple, Dict, Any
import sys


class HyperLogLog:
    """HyperLogLog cardinality estimator."""

    def __init__(self, p: int = 12):
        """
        Initialize HyperLogLog.

        Args:
            p: Number of bits for register indexing (default 12 gives 4096 registers)
                Higher p = more accuracy but more memory
        """
        if p < 4 or p > 16:
            raise ValueError("p must be between 4 and 16")

        self.p = p
        self.m = 1 << p  # Number of registers: 2^p
        self.registers = [0] * self.m
        self.alpha = self._get_alpha()

    def _get_alpha(self) -> float:
        """Get the alpha correction factor based on m."""
        if self.m == 16:
            return 0.673
        elif self.m == 32:
            return 0.697
        elif self.m == 64:
            return 0.709
        else:
            return 0.7213 / (1.0 + 1.079 / self.m)

    def _hash(self, value: str) -> int:
        """Hash a value to a 64-bit integer."""
        hash_obj = hashlib.md5(str(value).encode('utf-8'))
        hash_hex = hash_obj.hexdigest()
        return int(hash_hex[:16], 16)

    def add(self, value: str) -> None:
        """
        Add a value to the HyperLogLog structure.

        Args:
            value: The value to add (any hashable type converted to string)
        """
        x = self._hash(value)

        # Use first p bits for register index
        idx = x >> (64 - self.p)

        # Count leading zeros in remaining bits
        w = x << self.p
        rho = self._count_leading_zeros(w) + 1

        # Update register if this is the maximum rho seen
        if rho > self.registers[idx]:
            self.registers[idx] = rho

    def _count_leading_zeros(self, x: int) -> int:
        """Count leading zeros in a 64-bit integer."""
        if x == 0:
            return 64 - self.p
        count = 0
        while (x & (1 << 63)) == 0 and count < 64:
            x <<= 1
            count += 1
        return count

    def count(self) -> int:
        """
        Estimate the cardinality.

        Returns:
            Estimated number of distinct elements
        """
        # Calculate harmonic mean of 2^register
        sum_inverse = 0.0
        zeros = 0

        for r in self.registers:
            sum_inverse += 2.0 ** (-r)
            if r == 0:
                zeros += 1

        # Raw estimate
        estimate = self.alpha * (self.m ** 2) / sum_inverse

        # Apply corrections for small and large ranges
        if estimate <= 2.5 * self.m:
            # Linear counting for small estimates
            if zeros > 0:
                estimate = self.m * math.log(self.m / zeros)

        elif estimate > (1 << 64) / 30.0:
            # Large range correction
            estimate = -(1 << 64) * math.log(1.0 - estimate / (1 << 64))

        return int(round(estimate))

    def merge(self, other: 'HyperLogLog') -> None:
        """
        Merge another HyperLogLog into this one (union operation).

        Args:
            other: Another HyperLogLog instance
        """
        if self.p != other.p:
            raise ValueError("Cannot merge HyperLogLog instances with different p values")

        for i in range(self.m):
            self.registers[i] = max(self.registers[i], other.registers[i])

    def get_memory_usage(self) -> int:
        """Get memory usage in bytes."""
        return sys.getsizeof(self.registers) + sum(sys.getsizeof(r) for r in self.registers)


def benchmark_hyperloglog(
    data: List[str],
    p_values: List[int] = [10, 12, 14],
) -> Dict[str, Any]:
    """
    Benchmark HyperLogLog against exact counting.

    Args:
        data: List of values to count
        p_values: List of p values to test

    Returns:
        Dictionary with benchmark results
    """
    # Exact counting
    start_time = time.time()
    exact_set = set(data)
    exact_count = len(exact_set)
    exact_time = time.time() - start_time
    exact_memory = sys.getsizeof(exact_set) + sum(sys.getsizeof(x) for x in exact_set)

    results = {
        "exact_count": exact_count,
        "exact_time": exact_time,
        "exact_memory": exact_memory,
        "hll_results": []
    }

    for p in p_values:
        hll = HyperLogLog(p)

        # Insertion time
        start_time = time.time()
        for value in data:
            hll.add(value)
        insertion_time = time.time() - start_time

        # Estimation time
        start_time = time.time()
        estimated_count = hll.count()
        estimation_time = time.time() - start_time

        # Metrics
        relative_error = abs(estimated_count - exact_count) / exact_count if exact_count > 0 else 0
        memory_usage = hll.get_memory_usage()

        results["hll_results"].append({
            "p": p,
            "registers": hll.m,
            "estimated_count": estimated_count,
            "relative_error": relative_error,
            "insertion_time": insertion_time,
            "estimation_time": estimation_time,
            "total_time": insertion_time + estimation_time,
            "memory_usage": memory_usage,
            "memory_reduction": exact_memory / memory_usage if memory_usage > 0 else 0,
        })

    return results


def run_hll_demo():
    """Run a demonstration of HyperLogLog."""
    print("=" * 80)
    print("HyperLogLog Cardinality Estimation Demo")
    print("=" * 80)

    # Generate test data
    print("\nGenerating test data...")
    num_unique = 100000
    num_duplicates = 50000
    data = [f"item_{i}" for i in range(num_unique)]
    data.extend([f"item_{i % num_unique}" for i in range(num_duplicates)])

    print(f"Total elements: {len(data):,}")
    print(f"Unique elements: {num_unique:,}")
    print(f"Duplicates: {num_duplicates:,}")

    # Run benchmark
    print("\n" + "-" * 80)
    print("Running benchmark...")
    print("-" * 80)

    results = benchmark_hyperloglog(data, p_values=[10, 12, 14])

    print(f"\nExact Counting:")
    print(f"  Count: {results['exact_count']:,}")
    print(f"  Time: {results['exact_time']:.4f}s")
    print(f"  Memory: {results['exact_memory'] / 1024:.2f} KB")

    print(f"\nHyperLogLog Results:")
    print(f"{'p':<4} {'Registers':<10} {'Estimate':<12} {'Rel Error':<10} {'Time':<10} {'Memory':<12} {'Reduction':<10}")
    print("-" * 80)

    for r in results["hll_results"]:
        print(f"{r['p']:<4} {r['registers']:<10} {r['estimated_count']:<12,} "
              f"{r['relative_error']:<10.4%} {r['total_time']:<10.4f}s "
              f"{r['memory_usage']/1024:<12.2f}KB {r['memory_reduction']:<10.1f}x")

    print("\n" + "=" * 80)
    print("HyperLogLog Summary:")
    print("=" * 80)
    print("HyperLogLog provides accurate cardinality estimates with minimal memory.")
    print(f"With p=12 (4096 registers), we achieved ~{results['hll_results'][1]['relative_error']:.2%} error")
    print(f"while using {results['hll_results'][1]['memory_usage']/1024:.2f} KB vs {results['exact_memory']/1024:.2f} KB for exact counting.")
    print("Memory reduction: {:.1f}x".format(results['hll_results'][1]['memory_reduction']))
    print("=" * 80)


if __name__ == "__main__":
    run_hll_demo()
