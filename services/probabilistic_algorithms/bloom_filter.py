"""Bloom Filter implementation for membership testing.

Bloom Filter is a space-efficient probabilistic data structure for testing
set membership. It can tell you whether an element is definitely NOT in the set,
or PROBABLY in the set (with some false positive rate).

Algorithm:
1. Use k hash functions to map each element to k positions in a bit array
2. Set all k bits to 1 when adding an element
3. To test membership, check if all k bits are set
4. If any bit is 0, element is definitely not in the set
5. If all bits are 1, element is probably in the set (may be false positive)

Time Complexity: O(k) per operation
Space Complexity: O(m) where m = bit array size
False Positive Rate: (1 - e^(-kn/m))^k
Parameters: n = expected items, p = desired false positive rate
Recommended: m = -n*ln(p)/ln(2)^2, k = (m/n)*ln(2)
"""

import hashlib
import math
import time
import random
from typing import Set, List, Dict, Any
import sys


class BloomFilter:
    """Bloom Filter for membership testing."""

    def __init__(self, expected_items: int, false_positive_rate: float):
        """
        Initialize Bloom Filter.

        Args:
            expected_items: Expected number of items to be inserted
            false_positive_rate: Desired false positive rate (e.g., 0.01 for 1%)
        """
        self.n = expected_items
        self.p = false_positive_rate

        # Calculate optimal size and hash functions
        self.m = self._calculate_size(expected_items, false_positive_rate)
        self.k = self._calculate_hash_functions(self.m, expected_items)

        # Initialize bit array
        self.bit_array = [0] * self.m

        # Generate hash seeds
        self.seeds = [random.randint(0, 2**31 - 1) for _ in range(self.k)]

    def _calculate_size(self, n: int, p: float) -> int:
        """Calculate optimal bit array size."""
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(math.ceil(m))

    def _calculate_hash_functions(self, m: int, n: int) -> int:
        """Calculate optimal number of hash functions."""
        k = (m / n) * math.log(2)
        return int(math.ceil(k))

    def _hash(self, value: str, seed: int) -> int:
        """Hash a value to a bit index."""
        hash_obj = hashlib.md5(f"{seed}{value}".encode('utf-8'))
        hash_int = int(hash_obj.hexdigest()[:8], 16)
        return hash_int % self.m

    def add(self, value: str) -> None:
        """
        Add a value to the Bloom Filter.

        Args:
            value: The value to add
        """
        for i in range(self.k):
            idx = self._hash(value, self.seeds[i])
            self.bit_array[idx] = 1

    def contains(self, value: str) -> bool:
        """
        Test if a value is probably in the set.

        Args:
            value: The value to test

        Returns:
            True if probably in set, False if definitely not in set
        """
        for i in range(self.k):
            idx = self._hash(value, self.seeds[i])
            if self.bit_array[idx] == 0:
                return False
        return True

    def get_memory_usage(self) -> int:
        """Get memory usage in bytes."""
        return sys.getsizeof(self.bit_array) + sum(sys.getsizeof(b) for b in self.bit_array)


def benchmark_bloom_filter(
    training_data: List[str],
    test_data: List[str],
    test_labels: List[bool],
    fp_rates: List[float] = [0.1, 0.01, 0.001],
) -> Dict[str, Any]:
    """
    Benchmark Bloom Filter against Python set.

    Args:
        training_data: Data to insert into the filter
        test_data: Data to test membership
        test_labels: True if item is in training set, False otherwise
        fp_rates: List of false positive rates to test

    Returns:
        Dictionary with benchmark results
    """
    # Exact set
    start_time = time.time()
    exact_set = set(training_data)
    exact_time = time.time() - start_time
    exact_memory = sys.getsizeof(exact_set) + sum(sys.getsizeof(x) for x in exact_set)

    results = {
        "num_training": len(training_data),
        "num_test": len(test_data),
        "exact_time": exact_time,
        "exact_memory": exact_memory,
        "bloom_results": []
    }

    for fp_rate in fp_rates:
        bf = BloomFilter(len(training_data), fp_rate)

        # Insertion time
        start_time = time.time()
        for value in training_data:
            bf.add(value)
        insertion_time = time.time() - start_time

        # Query time
        start_time = time.time()
        predictions = [bf.contains(value) for value in test_data]
        query_time = time.time() - start_time

        # Calculate metrics
        false_positives = 0
        false_negatives = 0
        true_positives = 0
        true_negatives = 0

        for pred, actual in zip(predictions, test_labels):
            if pred and actual:
                true_positives += 1
            elif pred and not actual:
                false_positives += 1
            elif not pred and actual:
                false_negatives += 1
            else:
                true_negatives += 1

        actual_fp_rate = false_positives / (false_positives + true_negatives) if (false_positives + true_negatives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

        memory_usage = bf.get_memory_usage()

        results["bloom_results"].append({
            "target_fp_rate": fp_rate,
            "actual_fp_rate": actual_fp_rate,
            "bit_array_size": bf.m,
            "num_hash_functions": bf.k,
            "true_positives": true_positives,
            "false_positives": false_positives,
            "false_negatives": false_negatives,
            "true_negatives": true_negatives,
            "recall": recall,
            "insertion_time": insertion_time,
            "query_time": query_time,
            "total_time": insertion_time + query_time,
            "memory_usage": memory_usage,
            "memory_reduction": exact_memory / memory_usage if memory_usage > 0 else 0,
        })

    return results


def run_bloom_demo():
    """Run a demonstration of Bloom Filter."""
    print("=" * 80)
    print("Bloom Filter Membership Testing Demo")
    print("=" * 80)

    # Generate test data
    print("\nGenerating test data...")
    num_training = 100000
    num_test = 10000

    training_data = [f"item_{i}" for i in range(num_training)]
    test_in_set = [f"item_{random.randint(0, num_training - 1)}" for _ in range(num_test // 2)]
    test_not_in_set = [f"item_{num_training + i}" for i in range(num_test // 2)]

    test_data = test_in_set + test_not_in_set
    test_labels = [True] * len(test_in_set) + [False] * len(test_not_in_set)

    # Shuffle test data
    combined = list(zip(test_data, test_labels))
    random.shuffle(combined)
    test_data, test_labels = zip(*combined)

    print(f"Training items: {num_training:,}")
    print(f"Test items: {num_test:,}")
    print(f"  - In set: {len(test_in_set):,}")
    print(f"  - Not in set: {len(test_not_in_set):,}")

    # Run benchmark
    print("\n" + "-" * 80)
    print("Running benchmark...")
    print("-" * 80)

    results = benchmark_bloom_filter(training_data, test_data, test_labels, fp_rates=[0.1, 0.01, 0.001])

    print(f"\nPython Set:")
    print(f"  Items: {results['num_training']:,}")
    print(f"  Time: {results['exact_time']:.4f}s")
    print(f"  Memory: {results['exact_memory'] / 1024:.2f} KB")

    print(f"\nBloom Filter Results:")
    print(f"{'Target FP':<12} {'Actual FP':<12} {'Bits':<10} {'Hash Fn':<8} {'Recall':<10} "
          f"{'Time':<10} {'Memory':<12} {'Reduction':<10}")
    print("-" * 100)

    for r in results["bloom_results"]:
        print(f"{r['target_fp_rate']:<12.4f} {r['actual_fp_rate']:<12.4f} {r['bit_array_size']:<10} "
              f"{r['num_hash_functions']:<8} {r['recall']:<10.4f} {r['total_time']:<10.4f}s "
              f"{r['memory_usage']/1024:<12.2f}KB {r['memory_reduction']:<10.1f}x")

    print("\n" + "=" * 80)
    print("Bloom Filter Summary:")
    print("=" * 80)
    print("Bloom Filter provides memory-efficient membership testing with zero false negatives.")
    print(f"With target FP=0.01, we achieved actual FP of {results['bloom_results'][1]['actual_fp_rate']:.4f}")
    print(f"while using {results['bloom_results'][1]['memory_usage']/1024:.2f} KB vs {results['exact_memory']/1024:.2f} KB for exact set.")
    print("Memory reduction: {:.1f}x".format(results['bloom_results'][1]['memory_reduction']))
    print("\nKey insight: Bloom filters never produce false negatives, only false positives.")
    print("Trade-off: Lower false positive rate requires more memory.")
    print("=" * 80)


if __name__ == "__main__":
    run_bloom_demo()
