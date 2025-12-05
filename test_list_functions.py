#!/usr/bin/env python3
"""
Comprehensive Test Suite for ECH0 List Functions
Tests all list-related functionality across the codebase
"""

import sys
import unittest
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from ech0_list_utilities import (
    ListManager, ListResponse, get_list_manager,
    paginate_list, search_list, deduplicate_list
)


class TestListUtilities(unittest.TestCase):
    """Test the list utilities library"""

    def setUp(self):
        """Set up test fixtures"""
        self.manager = ListManager()
        self.test_data = [
            {"id": 1, "name": "Alice", "age": 30, "city": "NYC"},
            {"id": 2, "name": "Bob", "age": 25, "city": "LA"},
            {"id": 3, "name": "Charlie", "age": 35, "city": "NYC"},
            {"id": 4, "name": "Diana", "age": 28, "city": "Chicago"},
            {"id": 5, "name": "Eve", "age": 32, "city": "LA"},
        ]

    def test_pagination_basic(self):
        """Test basic pagination"""
        result = self.manager.paginate(self.test_data, page=1, page_size=2)

        self.assertEqual(len(result.items), 2)
        self.assertEqual(result.total_count, 5)
        self.assertEqual(result.total_pages, 3)
        self.assertTrue(result.has_next)
        self.assertFalse(result.has_prev)

    def test_pagination_last_page(self):
        """Test pagination on last page"""
        result = self.manager.paginate(self.test_data, page=3, page_size=2)

        self.assertEqual(len(result.items), 1)
        self.assertFalse(result.has_next)
        self.assertTrue(result.has_prev)

    def test_pagination_invalid_page(self):
        """Test pagination with invalid page number"""
        result = self.manager.paginate(self.test_data, page=0, page_size=2)
        self.assertEqual(result.page, 1)

        result = self.manager.paginate(self.test_data, page=100, page_size=2)
        self.assertEqual(result.page, result.total_pages)

    def test_pagination_page_size_limits(self):
        """Test page size limits"""
        result = self.manager.paginate(self.test_data, page=1, page_size=0)
        self.assertEqual(result.page_size, 20)  # Default

        result = self.manager.paginate(self.test_data, page=1, page_size=2000)
        self.assertEqual(result.page_size, 1000)  # Max limit

    def test_filter_exact_match(self):
        """Test exact match filtering"""
        result = self.manager.paginate(
            self.test_data,
            filters={"city": "NYC"}
        )

        self.assertEqual(len(result.items), 2)
        self.assertTrue(all(item["city"] == "NYC" for item in result.items))

    def test_filter_contains(self):
        """Test substring filtering"""
        result = self.manager.paginate(
            self.test_data,
            filters={"name__contains": "a"}
        )

        # Should match Alice, Charlie, and Diana (case-insensitive)
        self.assertEqual(len(result.items), 3)

    def test_filter_comparison(self):
        """Test comparison filters"""
        # Greater than
        result = self.manager.paginate(
            self.test_data,
            filters={"age__gt": 30}
        )
        self.assertEqual(len(result.items), 2)

        # Less than
        result = self.manager.paginate(
            self.test_data,
            filters={"age__lt": 30}
        )
        self.assertEqual(len(result.items), 2)

        # Greater than or equal
        result = self.manager.paginate(
            self.test_data,
            filters={"age__gte": 30}
        )
        self.assertEqual(len(result.items), 3)

    def test_filter_in_list(self):
        """Test 'in' filter"""
        result = self.manager.paginate(
            self.test_data,
            filters={"city__in": ["NYC", "LA"]}
        )

        self.assertEqual(len(result.items), 4)

    def test_filter_not(self):
        """Test 'not' filter"""
        result = self.manager.paginate(
            self.test_data,
            filters={"city__not": "NYC"}
        )

        self.assertEqual(len(result.items), 3)

    def test_sort_ascending(self):
        """Test ascending sort"""
        result = self.manager.paginate(
            self.test_data,
            sort_by="age",
            sort_order="asc"
        )

        ages = [item["age"] for item in result.items]
        self.assertEqual(ages, sorted(ages))

    def test_sort_descending(self):
        """Test descending sort"""
        result = self.manager.paginate(
            self.test_data,
            sort_by="age",
            sort_order="desc"
        )

        ages = [item["age"] for item in result.items]
        self.assertEqual(ages, sorted(ages, reverse=True))

    def test_combined_filter_sort_page(self):
        """Test combined filtering, sorting, and pagination"""
        result = self.manager.paginate(
            self.test_data,
            page=1,
            page_size=2,
            filters={"age__gte": 28},
            sort_by="age",
            sort_order="desc"
        )

        self.assertEqual(len(result.items), 2)
        self.assertEqual(result.items[0]["name"], "Charlie")  # Age 35
        self.assertEqual(result.items[1]["name"], "Eve")      # Age 32

    def test_search_single_field(self):
        """Test search in single field"""
        results = self.manager.search(
            self.test_data,
            query="Bob",
            search_fields=["name"]
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Bob")

    def test_search_multiple_fields(self):
        """Test search across multiple fields"""
        results = self.manager.search(
            self.test_data,
            query="30",
            search_fields=["name", "age"]
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["age"], 30)

    def test_search_with_limit(self):
        """Test search with limit"""
        results = self.manager.search(
            self.test_data,
            query="a",  # Matches multiple names
            search_fields=["name", "city"],
            limit=2
        )

        self.assertEqual(len(results), 2)

    def test_search_empty_query(self):
        """Test search with empty query"""
        results = self.manager.search(
            self.test_data,
            query="",
            search_fields=["name"]
        )

        self.assertEqual(len(results), len(self.test_data))

    def test_deduplicate_with_key(self):
        """Test deduplication with key field"""
        duplicates = self.test_data + [self.test_data[0]]  # Add duplicate

        unique = self.manager.deduplicate(duplicates, key_field="id")

        self.assertEqual(len(unique), len(self.test_data))

    def test_deduplicate_without_key(self):
        """Test deduplication without key field"""
        duplicates = [1, 2, 3, 2, 1, 4]

        unique = self.manager.deduplicate(duplicates)

        self.assertEqual(unique, [1, 2, 3, 4])

    def test_group_by(self):
        """Test grouping by field"""
        groups = self.manager.group_by(self.test_data, "city")

        self.assertEqual(len(groups), 3)
        self.assertEqual(len(groups["NYC"]), 2)
        self.assertEqual(len(groups["LA"]), 2)
        self.assertEqual(len(groups["Chicago"]), 1)

    def test_aggregate_sum(self):
        """Test sum aggregation"""
        total = self.manager.aggregate(self.test_data, "age", "sum")
        self.assertEqual(total, 150)

    def test_aggregate_avg(self):
        """Test average aggregation"""
        avg = self.manager.aggregate(self.test_data, "age", "avg")
        self.assertEqual(avg, 30.0)

    def test_aggregate_min(self):
        """Test min aggregation"""
        min_age = self.manager.aggregate(self.test_data, "age", "min")
        self.assertEqual(min_age, 25)

    def test_aggregate_max(self):
        """Test max aggregation"""
        max_age = self.manager.aggregate(self.test_data, "age", "max")
        self.assertEqual(max_age, 35)

    def test_aggregate_count(self):
        """Test count aggregation"""
        count = self.manager.aggregate(self.test_data, "age", "count")
        self.assertEqual(count, 5)

    def test_cache_set_and_get(self):
        """Test caching functionality"""
        self.manager.cache_list("test_key", self.test_data, ttl_seconds=60)

        cached = self.manager.get_cached_list("test_key")
        self.assertEqual(cached, self.test_data)

    def test_cache_expiry(self):
        """Test cache expiry"""
        import time
        # Use very short TTL
        self.manager.cache_list("test_key", self.test_data, ttl_seconds=0.001)

        # Wait for expiry
        time.sleep(0.01)

        # Should be expired
        cached = self.manager.get_cached_list("test_key")
        self.assertIsNone(cached)

    def test_cache_clear(self):
        """Test cache clearing"""
        self.manager.cache_list("test_key", self.test_data)
        self.manager.clear_cache("test_key")

        cached = self.manager.get_cached_list("test_key")
        self.assertIsNone(cached)

    def test_batch_process(self):
        """Test batch processing"""
        processor = lambda x: x["age"] * 2

        results = self.manager.batch_process(
            self.test_data,
            processor,
            batch_size=2
        )

        self.assertEqual(len(results), 5)
        self.assertEqual(results[0], 60)  # 30 * 2

    def test_list_response_to_dict(self):
        """Test ListResponse to dict conversion"""
        result = self.manager.paginate(self.test_data, page=1, page_size=2)
        result_dict = result.to_dict()

        self.assertIsInstance(result_dict, dict)
        self.assertIn("items", result_dict)
        self.assertIn("total_count", result_dict)
        self.assertIn("page", result_dict)


class TestMemoryPalaceListFunctions(unittest.TestCase):
    """Test ech0_memory_palace.py list functions"""

    def setUp(self):
        """Set up test fixtures"""
        # Mock memory palace
        self.mock_memories = {
            "total_count": 3,
            "memories": [
                {
                    "id": "mem1",
                    "content": "Meeting with Alice about project",
                    "topics": ["work", "projects"],
                    "emotions": ["focused"],
                    "significance": 8,
                    "access_count": 0,
                    "last_accessed": None
                },
                {
                    "id": "mem2",
                    "content": "Coffee with Bob discussing ideas",
                    "topics": ["social", "ideas"],
                    "emotions": ["happy"],
                    "significance": 6,
                    "access_count": 0,
                    "last_accessed": None
                },
                {
                    "id": "mem3",
                    "content": "Working on project documentation",
                    "topics": ["work", "documentation"],
                    "emotions": ["focused", "productive"],
                    "significance": 7,
                    "access_count": 0,
                    "last_accessed": None
                }
            ]
        }

    def test_search_memories_no_duplicates(self):
        """Test that search_memories doesn't return duplicates"""
        # Import the fixed search function
        from ech0_memory_palace import MemoryPalace

        with patch.object(MemoryPalace, '__init__', lambda x: None):
            palace = MemoryPalace()
            palace.memories = self.mock_memories

            results = palace.search_memories("project")

            # Should find 2 memories with "project" but no duplicates
            self.assertEqual(len(results), 2)
            ids = [m["id"] for m in results]
            self.assertEqual(len(ids), len(set(ids)))  # No duplicate IDs

    def test_search_memories_empty_query(self):
        """Test search with empty query"""
        from ech0_memory_palace import MemoryPalace

        with patch.object(MemoryPalace, '__init__', lambda x: None):
            palace = MemoryPalace()
            palace.memories = self.mock_memories

            results = palace.search_memories("")
            self.assertEqual(len(results), 0)


class TestReloadListFunctions(unittest.TestCase):
    """Test ech0_reload.py list functions"""

    def test_list_backups_returns_data(self):
        """Test that list_backups returns structured data"""
        from ech0_reload import HotReloadSystem

        with patch('ech0_reload.BACKUP_DIR') as mock_backup_dir:
            # Mock backup files
            mock_backups = []
            reloader = HotReloadSystem()

            result = reloader.list_backups(display=False)

            self.assertIsInstance(result, list)


class TestMasterControlListFunctions(unittest.TestCase):
    """Test ech0_master_control.py list functions"""

    def test_list_all_systems_returns_data(self):
        """Test that list_all_systems returns structured data"""
        from ech0_master_control import MasterControl

        with patch.object(MasterControl, '__init__', lambda x: None):
            control = MasterControl()

            result = control.list_all_systems(display=False)

            self.assertIsInstance(result, dict)
            self.assertIn("meditation_inner_work", result)
            self.assertIn("communication", result)

            # Check structure
            for category, systems in result.items():
                self.assertIsInstance(systems, list)
                for system in systems:
                    self.assertIn("file", system)
                    self.assertIn("description", system)


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions"""

    def test_paginate_list_convenience(self):
        """Test paginate_list convenience function"""
        data = list(range(100))
        result = paginate_list(data, page=2, page_size=10)

        self.assertIsInstance(result, ListResponse)
        self.assertEqual(result.page, 2)
        self.assertEqual(len(result.items), 10)

    def test_search_list_convenience(self):
        """Test search_list convenience function"""
        data = [
            {"name": "Alice"},
            {"name": "Bob"},
            {"name": "Charlie"}
        ]

        results = search_list(data, "Bob", ["name"])
        self.assertEqual(len(results), 1)

    def test_deduplicate_list_convenience(self):
        """Test deduplicate_list convenience function"""
        data = [1, 2, 3, 2, 1, 4]
        unique = deduplicate_list(data)

        self.assertEqual(unique, [1, 2, 3, 4])


def run_tests():
    """Run all tests"""
    print("=" * 70)
    print("ECH0 List Functions - Comprehensive Test Suite")
    print("=" * 70)
    print()

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestListUtilities))
    suite.addTests(loader.loadTestsFromTestCase(TestMemoryPalaceListFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestReloadListFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestMasterControlListFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestConvenienceFunctions))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED!")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
