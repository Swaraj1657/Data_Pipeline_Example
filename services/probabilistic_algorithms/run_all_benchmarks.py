"""Run all algorithm benchmarks and save results to JSON.

This script runs benchmarks for all probabilistic algorithms and saves
the results to a JSON file for analysis or dashboard display.
"""

import sys
import json
import time
import random
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from probabilistic_algorithms.hyperloglog import benchmark_hyperloglog
from probabilistic_algorithms.countmin_sketch import benchmark_countmin_sketch
from probabilistic_algorithms.bloom_filter import benchmark_bloom_filter
from probabilistic_algorithms.minhash_lsh import benchmark_minhash_lsh


def generate_test_data():
    """Generate test data for benchmarks."""
    random.seed(42)

    # For HyperLogLog
    hll_data = [f"item_{i}" for i in range(100000)]
    hll_data.extend([f"item_{i % 100000}" for i in range(50000)])

    # For Count-Min Sketch (skewed distribution)
    cms_data = []
    for i in range(100000):
        u = random.random()
        idx = int((1000 * (1 - u) ** (-1 / 0.5))) % 1000
        cms_data.append(f"item_{idx}")

    # For Bloom Filter
    bf_training = [f"item_{i}" for i in range(100000)]
    bf_test_in = [f"item_{random.randint(0, 99999)}" for _ in range(5000)]
    bf_test_out = [f"item_{100000 + i}" for i in range(5000)]
    bf_test = bf_test_in + bf_test_out
    bf_labels = [True] * 5000 + [False] * 5000

    # For MinHash + LSH
    base_items = [f"item_{i}" for i in range(1000)]
    minhash_datasets = {}
    for i in range(50):
        dataset = set(random.sample(base_items, 100))
        if i > 0 and i % 5 == 0:
            similar_to = minhash_datasets[f"set_{i-1}"]
            overlap = int(0.7 * len(similar_to))
            dataset = set(random.sample(base_items, 100 - overlap))
            dataset.update(random.sample(list(similar_to), overlap))
        minhash_datasets[f"set_{i}"] = dataset

    return {
        "hll_data": hll_data,
        "cms_data": cms_data,
        "bf_training": bf_training,
        "bf_test": bf_test,
        "bf_labels": bf_labels,
        "minhash_datasets": minhash_datasets,
    }


def run_all_benchmarks():
    """Run all algorithm benchmarks."""
    print("=" * 80)
    print("Running All Algorithm Benchmarks")
    print("=" * 80)

    print("\nGenerating test data...")
    test_data = generate_test_data()

    results = {
        "timestamp": time.time(),
        "algorithms": {}
    }

    print("\n" + "-" * 80)
    print("1. Running HyperLogLog benchmark...")
    print("-" * 80)
    try:
        hll_results = benchmark_hyperloglog(test_data["hll_data"], p_values=[10, 12, 14])
        results["algorithms"]["hyperloglog"] = hll_results
        print("HyperLogLog benchmark complete")
    except Exception as e:
        print(f"HyperLogLog benchmark failed: {e}")
        results["algorithms"]["hyperloglog"] = {"error": str(e)}

    print("\n" + "-" * 80)
    print("2. Running Count-Min Sketch benchmark...")
    print("-" * 80)
    try:
        cms_results = benchmark_countmin_sketch(
            test_data["cms_data"],
            epsilon_values=[0.01, 0.001, 0.0001]
        )
        results["algorithms"]["countmin_sketch"] = cms_results
        print("Count-Min Sketch benchmark complete")
    except Exception as e:
        print(f"Count-Min Sketch benchmark failed: {e}")
        results["algorithms"]["countmin_sketch"] = {"error": str(e)}

    print("\n" + "-" * 80)
    print("3. Running Bloom Filter benchmark...")
    print("-" * 80)
    try:
        bf_results = benchmark_bloom_filter(
            test_data["bf_training"],
            test_data["bf_test"],
            test_data["bf_labels"],
            fp_rates=[0.1, 0.01, 0.001]
        )
        results["algorithms"]["bloom_filter"] = bf_results
        print("Bloom Filter benchmark complete")
    except Exception as e:
        print(f"Bloom Filter benchmark failed: {e}")
        results["algorithms"]["bloom_filter"] = {"error": str(e)}

    print("\n" + "-" * 80)
    print("4. Running MinHash + LSH benchmark...")
    print("-" * 80)
    try:
        mh_results = benchmark_minhash_lsh(
            test_data["minhash_datasets"],
            num_permutations_values=[64, 128, 256],
            band_configs=[(16, 4), (20, 6), (32, 4)]
        )
        results["algorithms"]["minhash_lsh"] = mh_results
        print("MinHash + LSH benchmark complete")
    except Exception as e:
        print(f"MinHash + LSH benchmark failed: {e}")
        results["algorithms"]["minhash_lsh"] = {"error": str(e)}

    # Save results
    output_dir = Path("data/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "algorithm_benchmarks.json"

    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 80)
    print("All Benchmarks Complete")
    print("=" * 80)
    print(f"Results saved to: {output_file}")

    # Print summary
    print("\nSummary:")
    for algo_name, algo_results in results["algorithms"].items():
        if "error" in algo_results:
            print(f"  {algo_name}: FAILED - {algo_results['error']}")
        else:
            print(f"  {algo_name}: SUCCESS")

    return results


if __name__ == "__main__":
    run_all_benchmarks()
