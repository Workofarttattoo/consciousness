#!/usr/bin/env python3
"""
ECH0 List Manager CLI - Interactive Command-Line Interface
Provides easy access to all list management functions
"""

import sys
import json
from pathlib import Path
from typing import List, Dict, Any
import argparse

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from ech0_list_utilities import get_list_manager, ListResponse
from ech0_memory_palace import MemoryPalace
from ech0_reload import HotReloadSystem
from ech0_master_control import MasterControl


class ListManagerCLI:
    """Interactive CLI for list management"""

    def __init__(self):
        self.manager = get_list_manager()

    def display_menu(self):
        """Display main menu"""
        print("\n" + "=" * 70)
        print("ECH0 LIST MANAGER - Interactive CLI")
        print("=" * 70)
        print("""
1.  Search Memories
2.  List Backups
3.  List All Systems
4.  List Materials
5.  List Quantum Circuits
6.  Hot Leads Detection
7.  Search Custom Data (JSON file)
8.  Paginate Custom Data (JSON file)
9.  Filter Custom Data (JSON file)
10. Deduplicate Custom Data (JSON file)
11. Group & Aggregate Data
12. Cache Management
13. Run All Tests
14. Help & Documentation
0.  Exit

        """)

    def search_memories(self):
        """Search memories interactively"""
        print("\n" + "=" * 70)
        print("SEARCH MEMORIES")
        print("=" * 70)

        query = input("Enter search query: ").strip()
        if not query:
            print("❌ Empty query")
            return

        try:
            limit = int(input("Max results (default 10): ") or "10")
        except ValueError:
            limit = 10

        try:
            palace = MemoryPalace()
            results = palace.search_memories(query, limit=limit)

            print(f"\n✅ Found {len(results)} memories:")
            for i, memory in enumerate(results, 1):
                print(f"\n{i}. [{memory['id']}] {memory['content']}")
                print(f"   Significance: {memory['significance']}/10")
                if memory.get('topics'):
                    print(f"   Topics: {', '.join(memory['topics'])}")

        except Exception as e:
            print(f"❌ Error: {e}")

    def list_backups(self):
        """List module backups"""
        print("\n" + "=" * 70)
        print("LIST MODULE BACKUPS")
        print("=" * 70)

        try:
            limit = int(input("Max backups to show (default 20): ") or "20")
        except ValueError:
            limit = 20

        try:
            reloader = HotReloadSystem()
            backups = reloader.list_backups(limit=limit, display=True)

            print(f"\n📊 Total backups: {len(backups)}")

        except Exception as e:
            print(f"❌ Error: {e}")

    def list_systems(self):
        """List all ECH0 systems"""
        print("\n" + "=" * 70)
        print("LIST ALL SYSTEMS")
        print("=" * 70)

        try:
            control = MasterControl()
            systems = control.list_all_systems(display=True)

            # Count systems
            total = sum(len(sys_list) for sys_list in systems.values())
            print(f"\n📊 Total systems: {total}")
            print(f"📦 Categories: {len(systems)}")

        except Exception as e:
            print(f"❌ Error: {e}")

    def search_json_file(self):
        """Search data in JSON file"""
        print("\n" + "=" * 70)
        print("SEARCH JSON FILE")
        print("=" * 70)

        file_path = input("Enter JSON file path: ").strip()
        if not file_path:
            print("❌ No file path provided")
            return

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            if not isinstance(data, list):
                print("❌ JSON file must contain a list")
                return

            print(f"✅ Loaded {len(data)} items")

            query = input("Enter search query: ").strip()
            fields = input("Enter fields to search (comma-separated): ").strip().split(',')
            fields = [f.strip() for f in fields if f.strip()]

            try:
                limit = int(input("Max results (default 10): ") or "10")
            except ValueError:
                limit = 10

            results = self.manager.search(data, query, fields, limit=limit)

            print(f"\n✅ Found {len(results)} results:")
            for i, item in enumerate(results, 1):
                print(f"{i}. {json.dumps(item, indent=2)}")

        except FileNotFoundError:
            print(f"❌ File not found: {file_path}")
        except json.JSONDecodeError:
            print("❌ Invalid JSON file")
        except Exception as e:
            print(f"❌ Error: {e}")

    def paginate_json_file(self):
        """Paginate data in JSON file"""
        print("\n" + "=" * 70)
        print("PAGINATE JSON FILE")
        print("=" * 70)

        file_path = input("Enter JSON file path: ").strip()
        if not file_path:
            print("❌ No file path provided")
            return

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            if not isinstance(data, list):
                print("❌ JSON file must contain a list")
                return

            print(f"✅ Loaded {len(data)} items")

            try:
                page = int(input("Page number (default 1): ") or "1")
                page_size = int(input("Page size (default 20): ") or "20")
            except ValueError:
                page, page_size = 1, 20

            # Optional sorting
            sort_by = input("Sort by field (optional): ").strip() or None
            sort_order = input("Sort order (asc/desc, default asc): ").strip() or "asc"

            result = self.manager.paginate(
                data,
                page=page,
                page_size=page_size,
                sort_by=sort_by,
                sort_order=sort_order
            )

            print(f"\n📄 Page {result.page}/{result.total_pages}")
            print(f"📊 Showing {len(result.items)} of {result.total_count} items")
            print(f"◀️  Previous: {result.has_prev}  |  Next: {result.has_next} ▶️")

            for i, item in enumerate(result.items, 1):
                print(f"\n{i}. {json.dumps(item, indent=2)}")

        except FileNotFoundError:
            print(f"❌ File not found: {file_path}")
        except json.JSONDecodeError:
            print("❌ Invalid JSON file")
        except Exception as e:
            print(f"❌ Error: {e}")

    def filter_json_file(self):
        """Filter data in JSON file"""
        print("\n" + "=" * 70)
        print("FILTER JSON FILE")
        print("=" * 70)

        file_path = input("Enter JSON file path: ").strip()
        if not file_path:
            print("❌ No file path provided")
            return

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            if not isinstance(data, list):
                print("❌ JSON file must contain a list")
                return

            print(f"✅ Loaded {len(data)} items")

            print("\nFilter options:")
            print("  field=value          (exact match)")
            print("  field__contains=val  (substring)")
            print("  field__gt=value      (greater than)")
            print("  field__lt=value      (less than)")
            print("  field__in=val1,val2  (in list)")

            filters = {}
            while True:
                filter_str = input("\nEnter filter (or press Enter to finish): ").strip()
                if not filter_str:
                    break

                if '=' in filter_str:
                    key, value = filter_str.split('=', 1)
                    # Handle __in operator
                    if '__in' in key:
                        value = [v.strip() for v in value.split(',')]
                    # Handle numeric values
                    elif '__gt' in key or '__lt' in key or '__gte' in key or '__lte' in key:
                        try:
                            value = float(value)
                        except ValueError:
                            pass
                    filters[key] = value

            if not filters:
                print("❌ No filters provided")
                return

            result = self.manager.paginate(data, filters=filters, page_size=1000)

            print(f"\n✅ Filtered to {result.total_count} items:")
            for i, item in enumerate(result.items[:10], 1):  # Show first 10
                print(f"{i}. {json.dumps(item, indent=2)}")

            if result.total_count > 10:
                print(f"\n... and {result.total_count - 10} more items")

        except FileNotFoundError:
            print(f"❌ File not found: {file_path}")
        except json.JSONDecodeError:
            print("❌ Invalid JSON file")
        except Exception as e:
            print(f"❌ Error: {e}")

    def deduplicate_json_file(self):
        """Deduplicate data in JSON file"""
        print("\n" + "=" * 70)
        print("DEDUPLICATE JSON FILE")
        print("=" * 70)

        file_path = input("Enter JSON file path: ").strip()
        if not file_path:
            print("❌ No file path provided")
            return

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            if not isinstance(data, list):
                print("❌ JSON file must contain a list")
                return

            print(f"✅ Loaded {len(data)} items")

            key_field = input("Unique key field (optional, press Enter for whole item): ").strip() or None

            unique = self.manager.deduplicate(data, key_field=key_field)

            print(f"\n✅ Deduplicated: {len(data)} → {len(unique)} items")
            print(f"🗑️  Removed {len(data) - len(unique)} duplicates")

            save = input("\nSave deduplicated data? (y/n): ").strip().lower()
            if save == 'y':
                output_path = input("Output file path: ").strip()
                with open(output_path, 'w') as f:
                    json.dump(unique, f, indent=2)
                print(f"✅ Saved to {output_path}")

        except FileNotFoundError:
            print(f"❌ File not found: {file_path}")
        except json.JSONDecodeError:
            print("❌ Invalid JSON file")
        except Exception as e:
            print(f"❌ Error: {e}")

    def group_and_aggregate(self):
        """Group and aggregate data"""
        print("\n" + "=" * 70)
        print("GROUP & AGGREGATE")
        print("=" * 70)

        file_path = input("Enter JSON file path: ").strip()
        if not file_path:
            print("❌ No file path provided")
            return

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            if not isinstance(data, list):
                print("❌ JSON file must contain a list")
                return

            print(f"✅ Loaded {len(data)} items")

            group_by_field = input("Group by field: ").strip()
            if not group_by_field:
                print("❌ No field provided")
                return

            groups = self.manager.group_by(data, group_by_field)

            print(f"\n📊 Grouped into {len(groups)} groups:")
            for key, items in groups.items():
                print(f"\n{key}: {len(items)} items")

            # Optional aggregation
            agg = input("\nAggregate a field? (y/n): ").strip().lower()
            if agg == 'y':
                agg_field = input("Field to aggregate: ").strip()
                operation = input("Operation (sum/avg/min/max/count): ").strip() or "sum"

                print(f"\n📈 Aggregation results:")
                for key, items in groups.items():
                    value = self.manager.aggregate(items, agg_field, operation)
                    print(f"  {key}: {value}")

        except FileNotFoundError:
            print(f"❌ File not found: {file_path}")
        except json.JSONDecodeError:
            print("❌ Invalid JSON file")
        except Exception as e:
            print(f"❌ Error: {e}")

    def cache_management(self):
        """Manage cache"""
        print("\n" + "=" * 70)
        print("CACHE MANAGEMENT")
        print("=" * 70)
        print("""
1. Clear specific cache key
2. Clear all caches
3. Back to main menu
        """)

        choice = input("Select option: ").strip()

        if choice == "1":
            key = input("Enter cache key: ").strip()
            self.manager.clear_cache(key)
            print(f"✅ Cleared cache for key: {key}")
        elif choice == "2":
            self.manager.clear_cache()
            print("✅ Cleared all caches")

    def run_tests(self):
        """Run comprehensive tests"""
        print("\n" + "=" * 70)
        print("RUNNING COMPREHENSIVE TESTS")
        print("=" * 70)

        import subprocess
        result = subprocess.run(
            [sys.executable, "test_list_functions.py"],
            cwd=Path(__file__).parent
        )

        if result.returncode == 0:
            print("\n✅ All tests passed!")
        else:
            print("\n❌ Some tests failed")

    def show_help(self):
        """Show help and documentation"""
        print("\n" + "=" * 70)
        print("HELP & DOCUMENTATION")
        print("=" * 70)
        print("""
ECH0 List Manager provides powerful tools for managing lists:

📋 FEATURES:
  • Pagination - Break large lists into pages
  • Filtering - Filter by exact match, contains, gt, lt, in, not
  • Sorting - Sort by any field (asc/desc)
  • Searching - Search across multiple fields
  • Deduplication - Remove duplicates by key field
  • Grouping - Group items by field value
  • Aggregation - Sum, avg, min, max, count
  • Caching - Cache expensive operations with TTL

🔧 FILTER OPERATORS:
  field=value          - Exact match
  field__contains=val  - Substring match (case-insensitive)
  field__gt=value      - Greater than
  field__lt=value      - Less than
  field__gte=value     - Greater than or equal
  field__lte=value     - Less than or equal
  field__in=val1,val2  - In list
  field__not=value     - Not equal

💡 TIPS:
  • JSON files must contain a list of objects
  • All operations are non-destructive unless you save
  • Use pagination for large datasets
  • Cache frequently accessed data
  • Combine filters for complex queries

📚 DOCUMENTATION:
  • See ech0_list_utilities.py for API reference
  • See test_list_functions.py for examples
  • All functions return structured data

        """)

    def run(self):
        """Main CLI loop"""
        while True:
            self.display_menu()
            choice = input("Select option: ").strip()

            if choice == "0":
                print("\n👋 Goodbye!")
                break
            elif choice == "1":
                self.search_memories()
            elif choice == "2":
                self.list_backups()
            elif choice == "3":
                self.list_systems()
            elif choice == "7":
                self.search_json_file()
            elif choice == "8":
                self.paginate_json_file()
            elif choice == "9":
                self.filter_json_file()
            elif choice == "10":
                self.deduplicate_json_file()
            elif choice == "11":
                self.group_and_aggregate()
            elif choice == "12":
                self.cache_management()
            elif choice == "13":
                self.run_tests()
            elif choice == "14":
                self.show_help()
            else:
                print("❌ Invalid option")

            input("\nPress Enter to continue...")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="ECH0 List Manager CLI - Interactive list management tool"
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run tests and exit'
    )

    args = parser.parse_args()

    if args.test:
        import subprocess
        sys.exit(subprocess.run([sys.executable, "test_list_functions.py"]).returncode)

    try:
        cli = ListManagerCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
