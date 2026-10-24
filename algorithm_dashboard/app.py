"""Algorithm comparison dashboard for probabilistic algorithms.

This Flask dashboard runs benchmarks on HyperLogLog, Count-Min Sketch,
Bloom Filter, and MinHash + LSH, and displays the results comparing
them against exact methods.
"""

import os
import sys
import json
import time
import random
from pathlib import Path
from flask import Flask, jsonify, send_from_directory, render_template_string, request

# Add services to path
sys.path.insert(0, "/opt/services")

# Try to import from Docker path, fallback to local path
try:
    from probabilistic_algorithms.hyperloglog import benchmark_hyperloglog
    from probabilistic_algorithms.countmin_sketch import benchmark_countmin_sketch
    from probabilistic_algorithms.bloom_filter import benchmark_bloom_filter
    from probabilistic_algorithms.minhash_lsh import benchmark_minhash_lsh
except ImportError:
    # Fallback for local development
    sys.path.insert(0, str(Path(__file__).parent.parent / "services"))
    from probabilistic_algorithms.hyperloglog import benchmark_hyperloglog
    from probabilistic_algorithms.countmin_sketch import benchmark_countmin_sketch
    from probabilistic_algorithms.bloom_filter import benchmark_bloom_filter
    from probabilistic_algorithms.minhash_lsh import benchmark_minhash_lsh

app = Flask(__name__, static_folder="static", static_url_path="/static")

OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "/opt/spark-data/output")
BENCHMARK_RESULTS_FILE = os.path.join(OUTPUT_DIR, "algorithm_benchmarks.json")


def generate_test_data():
    """Generate test data for benchmarks."""
    random.seed(42)

    # For HyperLogLog
    hll_data = [f"item_{i}" for i in range(100000)]
    hll_data.extend([f"item_{i % 100000}" for i in range(50000)])

    # For Count-Min Sketch (skewed distribution)
    cms_data = []
    for i in range(100000):
        idx = int(random.zipf(1.5)) % 1000
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
    print("Generating test data...")
    test_data = generate_test_data()

    results = {
        "timestamp": time.time(),
        "algorithms": {}
    }

    print("Running HyperLogLog benchmark...")
    try:
        hll_results = benchmark_hyperloglog(test_data["hll_data"], p_values=[10, 12, 14])
        results["algorithms"]["hyperloglog"] = hll_results
        print("HyperLogLog benchmark complete")
    except Exception as e:
        print(f"HyperLogLog benchmark failed: {e}")
        results["algorithms"]["hyperloglog"] = {"error": str(e)}

    print("Running Count-Min Sketch benchmark...")
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

    print("Running Bloom Filter benchmark...")
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

    print("Running MinHash + LSH benchmark...")
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
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(BENCHMARK_RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)

    return results


@app.route("/")
def index():
    """Serve the dashboard HTML."""
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>Probabilistic Algorithms Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1400px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        h1 { color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px; }
        h2 { color: #555; margin-top: 30px; }
        .card { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #007bff; }
        .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 15px 0; }
        .metric { background: white; padding: 15px; border-radius: 5px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .metric-value { font-size: 24px; font-weight: bold; color: #007bff; }
        .metric-label { font-size: 14px; color: #666; }
        button { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 16px; }
        button:hover { background: #0056b3; }
        .chart-container { position: relative; height: 300px; margin: 20px 0; }
        table { width: 100%; border-collapse: collapse; margin: 15px 0; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #007bff; color: white; }
        tr:hover { background: #f5f5f5; }
        .error { color: #dc3545; padding: 10px; background: #f8d7da; border-radius: 5px; }
        .success { color: #155724; padding: 10px; background: #d4edda; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Probabilistic Algorithms Dashboard</h1>
        <p>This dashboard benchmarks probabilistic algorithms against exact methods for big data analytics.</p>

        <div class="card">
            <button onclick="runBenchmarks()">Run Benchmarks</button>
            <span id="status" style="margin-left: 20px;"></span>
        </div>

        <div id="results"></div>
    </div>

    <script>
        function runBenchmarks() {
            const status = document.getElementById('status');
            const results = document.getElementById('results');
            status.textContent = 'Running benchmarks... (this may take 1-2 minutes)';
            results.innerHTML = '';

            fetch('/api/benchmarks', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    status.textContent = 'Benchmarks complete!';
                    displayResults(data);
                })
                .catch(error => {
                    status.textContent = 'Error: ' + error.message;
                });
        }

        function displayResults(data) {
            const results = document.getElementById('results');

            // HyperLogLog
            if (data.algorithms.hyperloglog && !data.algorithms.hyperloglog.error) {
                const hll = data.algorithms.hyperloglog;
                results.innerHTML += `
                    <h2>HyperLogLog (Cardinality Estimation)</h2>
                    <div class="card">
                        <p><strong>Exact Count:</strong> ${hll.exact_count.toLocaleString()}</p>
                        <p><strong>Exact Time:</strong> ${hll.exact_time.toFixed(4)}s</p>
                        <p><strong>Exact Memory:</strong> ${(hll.exact_memory / 1024).toFixed(2)} KB</p>
                    </div>
                    <div class="metrics">
                        ${hll.hll_results.map(r => `
                            <div class="metric">
                                <div class="metric-value">${r.relative_error.toFixed(2%)}</div>
                                <div class="metric-label">Rel Error (p=${r.p})</div>
                            </div>
                            <div class="metric">
                                <div class="metric-value">${r.memory_reduction.toFixed(1)}x</div>
                                <div class="metric-label">Memory Reduction</div>
                            </div>
                        `).join('')}
                    </div>
                    <div class="chart-container">
                        <canvas id="hllChart"></canvas>
                    </div>
                `;
                renderHLLChart(hll);
            }

            // Count-Min Sketch
            if (data.algorithms.countmin_sketch && !data.algorithms.countmin_sketch.error) {
                const cms = data.algorithms.countmin_sketch;
                results.innerHTML += `
                    <h2>Count-Min Sketch (Frequency Estimation)</h2>
                    <div class="card">
                        <p><strong>Unique Items:</strong> ${cms.num_unique.toLocaleString()}</p>
                        <p><strong>Exact Time:</strong> ${cms.exact_time.toFixed(4)}s</p>
                        <p><strong>Exact Memory:</strong> ${(cms.exact_memory / 1024).toFixed(2)} KB</p>
                    </div>
                    <div class="metrics">
                        ${cms.cms_results.map(r => `
                            <div class="metric">
                                <div class="metric-value">${r.max_relative_error.toFixed(2%)}</div>
                                <div class="metric-label">Max Rel Error (ε=${r.epsilon})</div>
                            </div>
                            <div class="metric">
                                <div class="metric-value">${r.memory_reduction.toFixed(1)}x</div>
                                <div class="metric-label">Memory Reduction</div>
                            </div>
                        `).join('')}
                    </div>
                    <div class="chart-container">
                        <canvas id="cmsChart"></canvas>
                    </div>
                `;
                renderCMSChart(cms);
            }

            // Bloom Filter
            if (data.algorithms.bloom_filter && !data.algorithms.bloom_filter.error) {
                const bf = data.algorithms.bloom_filter;
                results.innerHTML += `
                    <h2>Bloom Filter (Membership Testing)</h2>
                    <div class="card">
                        <p><strong>Training Items:</strong> ${bf.num_training.toLocaleString()}</p>
                        <p><strong>Test Items:</strong> ${bf.num_test.toLocaleString()}</p>
                        <p><strong>Exact Memory:</strong> ${(bf.exact_memory / 1024).toFixed(2)} KB</p>
                    </div>
                    <div class="metrics">
                        ${bf.bloom_results.map(r => `
                            <div class="metric">
                                <div class="metric-value">${r.actual_fp_rate.toFixed(4)}</div>
                                <div class="metric-label">Actual FP Rate</div>
                            </div>
                            <div class="metric">
                                <div class="metric-value">${r.recall.toFixed(2)}</div>
                                <div class="metric-label">Recall</div>
                            </div>
                            <div class="metric">
                                <div class="metric-value">${r.memory_reduction.toFixed(1)}x</div>
                                <div class="metric-label">Memory Reduction</div>
                            </div>
                        `).join('')}
                    </div>
                    <div class="chart-container">
                        <canvas id="bfChart"></canvas>
                    </div>
                `;
                renderBFChart(bf);
            }

            // MinHash + LSH
            if (data.algorithms.minhash_lsh && !data.algorithms.minhash_lsh.error) {
                const mh = data.algorithms.minhash_lsh;
                results.innerHTML += `
                    <h2>MinHash + LSH (Similarity Detection)</h2>
                    <div class="card">
                        <p><strong>Number of Items:</strong> ${mh.num_items}</p>
                        <p><strong>Total Pairs:</strong> ${mh.num_pairs.toLocaleString()}</p>
                        <p><strong>True Similar Pairs:</strong> ${mh.true_similar_pairs}</p>
                        <p><strong>Exact Time:</strong> ${mh.exact_time.toFixed(4)}s</p>
                    </div>
                    <div class="metrics">
                        ${mh.lsh_results.map(r => `
                            <div class="metric">
                                <div class="metric-value">${r.candidate_reduction.toFixed(1%)}</div>
                                <div class="metric-label">Candidate Reduction</div>
                            </div>
                            <div class="metric">
                                <div class="metric-value">${r.precision.toFixed(2)}</div>
                                <div class="metric-label">Precision</div>
                            </div>
                            <div class="metric">
                                <div class="metric-value">${r.recall.toFixed(2)}</div>
                                <div class="metric-label">Recall</div>
                            </div>
                        `).join('')}
                    </div>
                    <div class="chart-container">
                        <canvas id="mhChart"></canvas>
                    </div>
                `;
                renderMHChart(mh);
            }
        }

        function renderHLLChart(data) {
            const ctx = document.getElementById('hllChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.hll_results.map(r => `p=${r.p}`),
                    datasets: [{
                        label: 'Relative Error',
                        data: data.hll_results.map(r => r.relative_error),
                        backgroundColor: 'rgba(0, 123, 255, 0.6)'
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false }
            });
        }

        function renderCMSChart(data) {
            const ctx = document.getElementById('cmsChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.cms_results.map(r => `ε=${r.epsilon}`),
                    datasets: [{
                        label: 'Max Relative Error',
                        data: data.cms_results.map(r => r.max_relative_error),
                        backgroundColor: 'rgba(0, 123, 255, 0.6)'
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false }
            });
        }

        function renderBFChart(data) {
            const ctx = document.getElementById('bfChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.bloom_results.map(r => `Target FP=${r.target_fp_rate}`),
                    datasets: [{
                        label: 'Actual FP Rate',
                        data: data.bloom_results.map(r => r.actual_fp_rate),
                        backgroundColor: 'rgba(0, 123, 255, 0.6)'
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false }
            });
        }

        function renderMHChart(data) {
            const ctx = document.getElementById('mhChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.lsh_results.map(r => `${r.bands}x${r.rows_per_band}`),
                    datasets: [{
                        label: 'Candidate Reduction',
                        data: data.lsh_results.map(r => r.candidate_reduction),
                        backgroundColor: 'rgba(0, 123, 255, 0.6)'
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false }
            });
        }

        // Load existing results on page load
        window.onload = function() {
            fetch('/api/benchmarks')
                .then(response => response.json())
                .then(data => {
                    if (data.algorithms && Object.keys(data.algorithms).length > 0) {
                        displayResults(data);
                    }
                })
                .catch(error => console.log('No cached results'));
        };
    </script>
</body>
</html>
    """
    return html


@app.route("/api/benchmarks", methods=["GET", "POST"])
def api_benchmarks():
    """Get or run benchmarks."""
    if request.method == "POST":
        results = run_all_benchmarks()
        return jsonify(results)
    else:
        if os.path.exists(BENCHMARK_RESULTS_FILE):
            with open(BENCHMARK_RESULTS_FILE, "r") as f:
                return jsonify(json.load(f))
        else:
            return jsonify({"algorithms": {}})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5200, debug=False)
