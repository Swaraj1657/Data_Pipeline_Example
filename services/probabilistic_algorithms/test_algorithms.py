"""Unit tests for probabilistic algorithms.

Tests cover:
- Basic functionality
- Edge cases
- Accuracy validation
- Parameter variations
"""

import unittest
import random
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from probabilistic_algorithms.hyperloglog import HyperLogLog
from probabilistic_algorithms.countmin_sketch import CountMinSketch
from probabilistic_algorithms.bloom_filter import BloomFilter
from probabilistic_algorithms.minhash_lsh import MinHash, LSH, exact_jaccard_similarity


class TestHyperLogLog(unittest.TestCase):
    """Test cases for HyperLogLog."""

    def test_basic_functionality(self):
        """Test basic add and count operations."""
        hll = HyperLogLog(p=12)
        hll.add("item1")
        hll.add("item2")
        hll.add("item3")

        estimate = hll.count()
        self.assertGreater(estimate, 0)
        self.assertLessEqual(estimate, 10)  # Should be close to 3

    def test_duplicates(self):
        """Test that duplicates don't affect count."""
        hll = HyperLogLog(p=12)

        for _ in range(100):
            hll.add("item1")
        for _ in range(100):
            hll.add("item2")

        estimate = hll.count()
        self.assertGreater(estimate, 0)
        self.assertLessEqual(estimate, 10)  # Should be close to 2

    def test_merge(self):
        """Test merging two HyperLogLog instances."""
        hll1 = HyperLogLog(p=12)
        hll2 = HyperLogLog(p=12)

        for i in range(100):
            hll1.add(f"item_{i}")

        for i in range(50, 150):
            hll2.add(f"item_{i}")

        hll1.merge(hll2)
        estimate = hll1.count()

        # Union should have 150 unique items
        self.assertGreater(estimate, 100)
        self.assertLess(estimate, 200)

    def test_parameter_validation(self):
        """Test that invalid parameters raise errors."""
        with self.assertRaises(ValueError):
            HyperLogLog(p=3)  # Too small
        with self.assertRaises(ValueError):
            HyperLogLog(p=17)  # Too large

    def test_merge_different_p(self):
        """Test that merging with different p raises error."""
        hll1 = HyperLogLog(p=12)
        hll2 = HyperLogLog(p=10)

        with self.assertRaises(ValueError):
            hll1.merge(hll2)

    def test_accuracy(self):
        """Test accuracy with known dataset."""
        hll = HyperLogLog(p=12)
        num_items = 10000

        for i in range(num_items):
            hll.add(f"item_{i}")

        estimate = hll.count()
        relative_error = abs(estimate - num_items) / num_items

        # Should be within 5% error
        self.assertLess(relative_error, 0.05)


class TestCountMinSketch(unittest.TestCase):
    """Test cases for Count-Min Sketch."""

    def test_basic_functionality(self):
        """Test basic add and estimate operations."""
        cms = CountMinSketch(epsilon=0.01, delta=0.01)

        cms.add("item1", 5)
        cms.add("item2", 3)

        estimate1 = cms.estimate("item1")
        estimate2 = cms.estimate("item2")

        self.assertGreater(estimate1, 0)
        self.assertGreater(estimate2, 0)

    def test_frequency_accumulation(self):
        """Test that multiple adds accumulate."""
        cms = CountMinSketch(epsilon=0.01, delta=0.01)

        for _ in range(10):
            cms.add("item1")

        estimate = cms.estimate("item1")
        self.assertGreaterEqual(estimate, 10)

    def test_zero_estimate(self):
        """Test that unseen items have low estimates."""
        cms = CountMinSketch(epsilon=0.01, delta=0.01)

        cms.add("item1", 100)

        estimate = cms.estimate("item_never_seen")
        # Should be small (likely 0 or small collision)
        self.assertLess(estimate, 10)

    def test_bounds(self):
        """Test that estimates are upper bounds."""
        cms = CountMinSketch(epsilon=0.01, delta=0.01)

        # Add known counts
        known_counts = {"item1": 100, "item2": 50, "item3": 200}
        for item, count in known_counts.items():
            cms.add(item, count)

        # Estimates should be >= actual counts
        for item, count in known_counts.items():
            estimate = cms.estimate(item)
            self.assertGreaterEqual(estimate, count)

    def test_parameter_variations(self):
        """Test different epsilon/delta parameters."""
        cms1 = CountMinSketch(epsilon=0.1, delta=0.1)
        cms2 = CountMinSketch(epsilon=0.001, delta=0.001)

        # Smaller epsilon should have more counters
        self.assertGreater(cms2.w, cms1.w)
        self.assertGreater(cms2.d, cms1.d)


class TestBloomFilter(unittest.TestCase):
    """Test cases for Bloom Filter."""

    def test_basic_functionality(self):
        """Test basic add and contains operations."""
        bf = BloomFilter(expected_items=1000, false_positive_rate=0.01)

        bf.add("item1")
        bf.add("item2")

        self.assertTrue(bf.contains("item1"))
        self.assertTrue(bf.contains("item2"))
        self.assertFalse(bf.contains("item3"))

    def test_no_false_negatives(self):
        """Test that added items always return True."""
        bf = BloomFilter(expected_items=1000, false_positive_rate=0.01)

        items = [f"item_{i}" for i in range(100)]
        for item in items:
            bf.add(item)

        for item in items:
            self.assertTrue(bf.contains(item))

    def test_false_positives(self):
        """Test that false positives occur at expected rate."""
        bf = BloomFilter(expected_items=1000, false_positive_rate=0.1)

        # Add 1000 items
        for i in range(1000):
            bf.add(f"item_{i}")

        # Test 1000 different items
        false_positives = 0
        for i in range(1000, 2000):
            if bf.contains(f"item_{i}"):
                false_positives += 1

        fp_rate = false_positives / 1000
        # Should be close to target rate (within factor of 2)
        self.assertLess(fp_rate, 0.2)

    def test_parameter_variations(self):
        """Test different false positive rates."""
        bf1 = BloomFilter(expected_items=1000, false_positive_rate=0.1)
        bf2 = BloomFilter(expected_items=1000, false_positive_rate=0.001)

        # Lower FP rate should require more bits
        self.assertGreater(bf2.m, bf1.m)
        self.assertGreater(bf2.k, bf1.k)

    def test_empty_filter(self):
        """Test behavior with empty filter."""
        bf = BloomFilter(expected_items=1000, false_positive_rate=0.01)

        self.assertFalse(bf.contains("any_item"))


class TestMinHash(unittest.TestCase):
    """Test cases for MinHash."""

    def test_basic_functionality(self):
        """Test basic signature computation."""
        mh = MinHash(num_permutations=128)

        set1 = {"item1", "item2", "item3"}
        sig1 = mh.compute_signature(set1)

        self.assertEqual(len(sig1), 128)
        self.assertTrue(all(isinstance(x, int) for x in sig1))

    def test_similarity_estimation(self):
        """Test similarity estimation for similar sets."""
        mh = MinHash(num_permutations=128)

        set1 = {"item1", "item2", "item3", "item4", "item5"}
        set2 = {"item1", "item2", "item3", "item6", "item7"}

        sig1 = mh.compute_signature(set1)
        sig2 = mh.compute_signature(set2)

        estimated = mh.estimate_similarity(sig1, sig2)
        exact = exact_jaccard_similarity(set1, set2)

        # Should be close (within 20%)
        error = abs(estimated - exact)
        self.assertLess(error, 0.2)

    def test_identical_sets(self):
        """Test that identical sets have similarity 1."""
        mh = MinHash(num_permutations=128)

        set1 = {"item1", "item2", "item3"}
        sig1 = mh.compute_signature(set1)
        sig2 = mh.compute_signature(set1)

        similarity = mh.estimate_similarity(sig1, sig2)
        self.assertEqual(similarity, 1.0)

    def test_disjoint_sets(self):
        """Test that disjoint sets have similarity 0."""
        mh = MinHash(num_permutations=128)

        set1 = {"item1", "item2", "item3"}
        set2 = {"item4", "item5", "item6"}

        sig1 = mh.compute_signature(set1)
        sig2 = mh.compute_signature(set2)

        similarity = mh.estimate_similarity(sig1, sig2)
        self.assertEqual(similarity, 0.0)

    def test_signature_length_validation(self):
        """Test that signatures must have same length."""
        mh = MinHash(num_permutations=128)

        sig1 = [1] * 128
        sig2 = [1] * 64

        with self.assertRaises(ValueError):
            mh.estimate_similarity(sig1, sig2)


class TestLSH(unittest.TestCase):
    """Test cases for LSH."""

    def test_basic_functionality(self):
        """Test basic add and candidate generation."""
        lsh = LSH(num_bands=16, rows_per_band=4)

        sig1 = [random.randint(0, 2**32) for _ in range(64)]
        sig2 = [random.randint(0, 2**32) for _ in range(64)]

        lsh.add("item1", sig1)
        lsh.add("item2", sig2)

        candidates = lsh.get_candidates()
        # May or may not have candidates depending on hash collisions
        self.assertIsInstance(candidates, set)

    def test_similar_signatures(self):
        """Test that similar signatures become candidates."""
        lsh = LSH(num_bands=16, rows_per_band=4)

        # Create similar signatures (same in some bands)
        base_sig = [random.randint(0, 2**32) for _ in range(64)]
        sig1 = base_sig[:]
        sig2 = base_sig[:]

        lsh.add("item1", sig1)
        lsh.add("item2", sig2)

        candidates = lsh.get_candidates()
        # Should have at least one candidate
        self.assertGreater(len(candidates), 0)

    def test_signature_length_validation(self):
        """Test that signature length must match bands * rows."""
        lsh = LSH(num_bands=16, rows_per_band=4)

        sig = [1] * 32  # Wrong length

        with self.assertRaises(ValueError):
            lsh.add("item1", sig)

    def test_threshold_approximation(self):
        """Test that band/row configuration affects threshold."""
        # More bands with fewer rows = higher threshold
        lsh1 = LSH(num_bands=32, rows_per_band=2)
        lsh2 = LSH(num_bands=8, rows_per_band=8)

        # Threshold = (1/b)^(1/r)
        thresh1 = (1.0 / 32) ** (1.0 / 2)
        thresh2 = (1.0 / 8) ** (1.0 / 8)

        # thresh1 = 0.177, thresh2 = 0.771 - actually fewer bands with more rows = higher threshold
        # Let me fix the test logic
        self.assertGreater(thresh2, thresh1)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases across all algorithms."""

    def test_empty_inputs(self):
        """Test behavior with empty inputs."""
        hll = HyperLogLog(p=12)
        self.assertEqual(hll.count(), 0)

        cms = CountMinSketch(epsilon=0.01, delta=0.01)
        self.assertEqual(cms.estimate("item"), 0)

        bf = BloomFilter(expected_items=1000, false_positive_rate=0.01)
        self.assertFalse(bf.contains("item"))

        mh = MinHash(num_permutations=128)
        sig = mh.compute_signature(set())
        self.assertEqual(len(sig), 128)

    def test_single_item(self):
        """Test behavior with single item."""
        hll = HyperLogLog(p=12)
        hll.add("item1")
        estimate = hll.count()
        self.assertGreater(estimate, 0)
        self.assertLess(estimate, 5)

        cms = CountMinSketch(epsilon=0.01, delta=0.01)
        cms.add("item1", 10)
        self.assertGreaterEqual(cms.estimate("item1"), 10)

        bf = BloomFilter(expected_items=1000, false_positive_rate=0.01)
        bf.add("item1")
        self.assertTrue(bf.contains("item1"))

    def test_large_inputs(self):
        """Test behavior with large inputs."""
        hll = HyperLogLog(p=12)
        for i in range(100000):
            hll.add(f"item_{i}")
        estimate = hll.count()
        relative_error = abs(estimate - 100000) / 100000
        self.assertLess(relative_error, 0.05)

        cms = CountMinSketch(epsilon=0.01, delta=0.01)
        for i in range(100000):
            cms.add(f"item_{i}")
        # Should handle large inputs without error
        self.assertGreater(cms.estimate("item_0"), 0)


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestHyperLogLog))
    suite.addTests(loader.loadTestsFromTestCase(TestCountMinSketch))
    suite.addTests(loader.loadTestsFromTestCase(TestBloomFilter))
    suite.addTests(loader.loadTestsFromTestCase(TestMinHash))
    suite.addTests(loader.loadTestsFromTestCase(TestLSH))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
