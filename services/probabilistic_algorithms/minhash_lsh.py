"""MinHash + LSH implementation for similarity detection.

MinHash is a technique for estimating Jaccard similarity between sets using
a reduced representation (signature). Locality Sensitive Hashing (LSH) builds
on MinHash to efficiently find similar pairs without comparing all pairs.

MinHash Algorithm:
1. Generate k random hash functions
2. For each set, compute the minimum hash value for each function
3. The signature is the vector of these minimum values
4. Jaccard similarity ≈ fraction of matching signature values

LSH Algorithm:
1. Divide signature into b bands of r rows each
2. Hash each band to a bucket
3. Items in the same bucket for any band are candidate pairs
4. Verify candidates with exact Jaccard similarity

Time Complexity:
- MinHash signature: O(k * |S|) per set
- LSH candidate search: O(n * b) where n = number of items
- Exact Jaccard: O(|A| + |B|) per pair

Space Complexity:
- MinHash: O(k) per set
- LSH: O(n * b) for buckets

Parameters:
- k: Number of hash functions (signature length)
- b: Number of bands
- r: Rows per band (k = b * r)
- threshold: (1/b)^(1/r) is the approximate similarity threshold
"""

import hashlib
import math
import time
import random
from typing import Set, List, Dict, Tuple, Any
import sys


class MinHash:
    """MinHash signature for Jaccard similarity estimation."""

    def __init__(self, num_permutations: int = 128):
        """
        Initialize MinHash.

        Args:
            num_permutations: Number of hash functions (signature length)
        """
        self.num_permutations = num_permutations
        self.seeds = [random.randint(0, 2**31 - 1) for _ in range(num_permutations)]

    def _hash(self, value: str, seed: int) -> int:
        """Hash a value to a 32-bit integer."""
        hash_obj = hashlib.md5(f"{seed}{value}".encode('utf-8'))
        return int(hash_obj.hexdigest()[:8], 16)

    def compute_signature(self, input_set: Set[str]) -> List[int]:
        """
        Compute MinHash signature for a set.

        Args:
            input_set: Input set of strings

        Returns:
            MinHash signature (list of minimum hash values)
        """
        signature = [float('inf')] * self.num_permutations

        for item in input_set:
            for i, seed in enumerate(self.seeds):
                hash_val = self._hash(item, seed)
                if hash_val < signature[i]:
                    signature[i] = hash_val

        return signature

    def estimate_similarity(self, sig1: List[int], sig2: List[int]) -> float:
        """
        Estimate Jaccard similarity from signatures.

        Args:
            sig1: First signature
            sig2: Second signature

        Returns:
            Estimated Jaccard similarity
        """
        if len(sig1) != len(sig2):
            raise ValueError("Signatures must have same length")

        matches = sum(1 for a, b in zip(sig1, sig2) if a == b)
        return matches / len(sig1) if len(sig1) > 0 else 0.0


class LSH:
    """Locality Sensitive Hashing for candidate pair generation."""

    def __init__(self, num_bands: int, rows_per_band: int):
        """
        Initialize LSH.

        Args:
            num_bands: Number of bands
            rows_per_band: Rows per band
        """
        self.num_bands = num_bands
        self.rows_per_band = rows_per_band
        self.signature_length = num_bands * rows_per_band
        self.buckets: Dict[Tuple[int, int], List[str]] = {}

    def _hash_band(self, band: List[int]) -> int:
        """Hash a band to a bucket index."""
        band_str = ",".join(map(str, band))
        hash_obj = hashlib.md5(band_str.encode('utf-8'))
        return int(hash_obj.hexdigest()[:8], 16)

    def add(self, key: str, signature: List[int]) -> None:
        """
        Add a signature to LSH.

        Args:
            key: Identifier for the item
            signature: MinHash signature
        """
        if len(signature) != self.signature_length:
            raise ValueError(f"Signature length must be {self.signature_length}")

        for band_idx in range(self.num_bands):
            start = band_idx * self.rows_per_band
            end = start + self.rows_per_band
            band = signature[start:end]
            bucket_key = (band_idx, self._hash_band(band))

            if bucket_key not in self.buckets:
                self.buckets[bucket_key] = []
            self.buckets[bucket_key].append(key)

    def get_candidates(self) -> Set[Tuple[str, str]]:
        """
        Get candidate similar pairs.

        Returns:
            Set of candidate pairs (key1, key2) where key1 < key2
        """
        candidates = set()

        for bucket in self.buckets.values():
            if len(bucket) > 1:
                # All pairs in the same bucket are candidates
                for i in range(len(bucket)):
                    for j in range(i + 1, len(bucket)):
                        pair = tuple(sorted([bucket[i], bucket[j]]))
                        candidates.add(pair)

        return candidates


def exact_jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
    """Compute exact Jaccard similarity."""
    if not set1 and not set2:
        return 1.0
    if not set1 or not set2:
        return 0.0
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union


def benchmark_minhash_lsh(
    datasets: Dict[str, Set[str]],
    num_permutations_values: List[int] = [64, 128, 256],
    band_configs: List[Tuple[int, int]] = [(16, 4), (20, 6), (32, 4)],
) -> Dict[str, Any]:
    """
    Benchmark MinHash + LSH against exact similarity computation.

    Args:
        datasets: Dictionary of {key: set} to compare
        num_permutations_values: List of signature lengths to test
        band_configs: List of (bands, rows_per_band) configurations

    Returns:
        Dictionary with benchmark results
    """
    keys = list(datasets.keys())
    num_items = len(keys)

    # Compute all exact similarities
    print("Computing exact similarities...")
    start_time = time.time()
    exact_similarities = {}
    for i in range(num_items):
        for j in range(i + 1, num_items):
            sim = exact_jaccard_similarity(datasets[keys[i]], datasets[keys[j]])
            exact_similarities[(keys[i], keys[j])] = sim
    exact_time = time.time() - start_time

    # Find true similar pairs (threshold = 0.5)
    threshold = 0.5
    true_similar_pairs = {pair for pair, sim in exact_similarities.items() if sim >= threshold}

    results = {
        "num_items": num_items,
        "num_pairs": len(exact_similarities),
        "true_similar_pairs": len(true_similar_pairs),
        "exact_time": exact_time,
        "lsh_results": []
    }

    for num_perm in num_permutations_values:
        for bands, rows in band_configs:
            if bands * rows != num_perm:
                continue

            minhash = MinHash(num_perm)
            lsh = LSH(bands, rows)

            # Compute signatures and add to LSH
            start_time = time.time()
            signatures = {}
            for key, dataset in datasets.items():
                sig = minhash.compute_signature(dataset)
                signatures[key] = sig
                lsh.add(key, sig)
            signature_time = time.time() - start_time

            # Get candidates
            start_time = time.time()
            candidates = lsh.get_candidates()
            candidate_time = time.time() - start_time

            # Verify candidates
            start_time = time.time()
            true_positives = 0
            false_positives = 0
            false_negatives = 0

            for pair in exact_similarities.keys():
                in_candidates = pair in candidates
                is_similar = exact_similarities[pair] >= threshold

                if in_candidates and is_similar:
                    true_positives += 1
                elif in_candidates and not is_similar:
                    false_positives += 1
                elif not in_candidates and is_similar:
                    false_negatives += 1

            verification_time = time.time() - start_time

            precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
            recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
            candidate_reduction = 1 - (len(candidates) / len(exact_similarities)) if len(exact_similarities) > 0 else 0

            results["lsh_results"].append({
                "num_permutations": num_perm,
                "bands": bands,
                "rows_per_band": rows,
                "threshold_approx": (1.0 / bands) ** (1.0 / rows),
                "signature_time": signature_time,
                "candidate_time": candidate_time,
                "verification_time": verification_time,
                "total_time": signature_time + candidate_time + verification_time,
                "num_candidates": len(candidates),
                "candidate_reduction": candidate_reduction,
                "true_positives": true_positives,
                "false_positives": false_positives,
                "false_negatives": false_negatives,
                "precision": precision,
                "recall": recall,
            })

    return results


def run_minhash_lsh_demo():
    """Run a demonstration of MinHash + LSH."""
    print("=" * 80)
    print("MinHash + LSH Similarity Detection Demo")
    print("=" * 80)

    # Generate test datasets with controlled similarity
    print("\nGenerating test datasets with controlled similarity...")
    num_items = 100
    base_items = [f"item_{i}" for i in range(1000)]

    datasets = {}
    for i in range(num_items):
        # Each set has 100 items
        dataset = set(random.sample(base_items, 100))

        # Add similar items to create correlated sets
        if i > 0 and i % 5 == 0:
            # Make this set similar to previous one
            similar_to = datasets[f"set_{i-1}"]
            overlap = int(0.7 * len(similar_to))  # 70% overlap
            dataset = set(random.sample(base_items, 100 - overlap))
            dataset.update(random.sample(list(similar_to), overlap))

        datasets[f"set_{i}"] = dataset

    print(f"Number of datasets: {num_items}")
    print(f"Items per dataset: 100")
    print(f"Total possible pairs: {num_items * (num_items - 1) // 2:,}")

    # Run benchmark
    print("\n" + "-" * 80)
    print("Running benchmark...")
    print("-" * 80)

    results = benchmark_minhash_lsh(
        datasets,
        num_permutations_values=[64, 128, 256],
        band_configs=[(16, 4), (20, 6), (32, 4), (32, 8)]
    )

    print(f"\nExact Similarity Computation:")
    print(f"  Pairs compared: {results['num_pairs']:,}")
    print(f"  Time: {results['exact_time']:.4f}s")
    print(f"  Similar pairs (threshold=0.5): {results['true_similar_pairs']}")

    print(f"\nMinHash + LSH Results:")
    print(f"{'Perm':<6} {'Bands':<6} {'Rows':<6} {'Thresh':<8} {'Candidates':<12} "
          f"{'Reduction':<12} {'Precision':<10} {'Recall':<10} {'Time':<10}")
    print("-" * 100)

    for r in results["lsh_results"]:
        print(f"{r['num_permutations']:<6} {r['bands']:<6} {r['rows_per_band']:<6} "
              f"{r['threshold_approx']:<8.3f} {r['num_candidates']:<12} "
              f"{r['candidate_reduction']:<12.2%} {r['precision']:<10.4f} "
              f"{r['recall']:<10.4f} {r['total_time']:<10.4f}s")

    print("\n" + "=" * 80)
    print("MinHash + LSH Summary:")
    print("=" * 80)
    print("MinHash + LSH efficiently finds similar pairs without comparing all pairs.")
    print(f"Reduction in candidate pairs: up to {max(r['candidate_reduction'] for r in results['lsh_results']):.2%}")
    print("\nKey insights:")
    print("- More permutations = better accuracy but slower")
    print("- Bands and rows control the similarity threshold")
    print("- Threshold approx (1/bands)^(1/rows)")
    print("- LSH dramatically reduces the number of pairs to verify")
    print("=" * 80)


if __name__ == "__main__":
    run_minhash_lsh_demo()
