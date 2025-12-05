#!/usr/bin/env python3
"""
ECH0 List Utilities - Unified List Management
Provides pagination, filtering, sorting, and caching for all list operations
"""

from typing import List, Dict, Any, Callable, Optional, Union
from dataclasses import dataclass
from functools import lru_cache
import json
from datetime import datetime, timedelta


@dataclass
class ListResponse:
    """Standardized list response format"""
    items: List[Any]
    total_count: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool
    filters_applied: Dict[str, Any]
    sort_by: Optional[str] = None
    sort_order: str = "asc"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "items": self.items,
            "total_count": self.total_count,
            "page": self.page,
            "page_size": self.page_size,
            "total_pages": self.total_pages,
            "has_next": self.has_next,
            "has_prev": self.has_prev,
            "filters_applied": self.filters_applied,
            "sort_by": self.sort_by,
            "sort_order": self.sort_order
        }


class ListManager:
    """Advanced list management with pagination, filtering, and caching"""

    def __init__(self, cache_ttl_seconds: int = 300):
        """
        Initialize list manager

        Args:
            cache_ttl_seconds: Time to live for cache entries (default 5 minutes)
        """
        self.cache_ttl = timedelta(seconds=cache_ttl_seconds)
        self._cache = {}

    def paginate(
        self,
        items: List[Any],
        page: int = 1,
        page_size: int = 20,
        filters: Optional[Dict[str, Any]] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc"
    ) -> ListResponse:
        """
        Paginate a list with optional filtering and sorting

        Args:
            items: List of items to paginate
            page: Page number (1-indexed)
            page_size: Number of items per page
            filters: Dictionary of filters to apply
            sort_by: Field name to sort by (for dicts/objects)
            sort_order: "asc" or "desc"

        Returns:
            ListResponse with paginated data
        """
        # Validate inputs
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 20
        if page_size > 1000:
            page_size = 1000  # Max page size for safety

        # Apply filters
        filtered_items = items
        filters_applied = filters or {}

        if filters:
            filtered_items = self._apply_filters(items, filters)

        # Apply sorting
        if sort_by:
            filtered_items = self._sort_items(filtered_items, sort_by, sort_order)

        # Calculate pagination
        total_count = len(filtered_items)
        total_pages = max(1, (total_count + page_size - 1) // page_size)

        # Ensure page is within bounds
        if page > total_pages:
            page = total_pages

        # Get page slice
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        page_items = filtered_items[start_idx:end_idx]

        return ListResponse(
            items=page_items,
            total_count=total_count,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_prev=page > 1,
            filters_applied=filters_applied,
            sort_by=sort_by,
            sort_order=sort_order
        )

    def _apply_filters(self, items: List[Any], filters: Dict[str, Any]) -> List[Any]:
        """
        Apply filters to a list of items

        Filters can be:
        - field_name: value (exact match)
        - field_name__contains: value (substring match)
        - field_name__gt: value (greater than)
        - field_name__lt: value (less than)
        - field_name__in: [values] (in list)
        """
        filtered = items

        for filter_key, filter_value in filters.items():
            if "__" in filter_key:
                field, operator = filter_key.rsplit("__", 1)
            else:
                field, operator = filter_key, "eq"

            if operator == "eq":
                filtered = [item for item in filtered if self._get_field(item, field) == filter_value]
            elif operator == "contains":
                filtered = [
                    item for item in filtered
                    if filter_value.lower() in str(self._get_field(item, field)).lower()
                ]
            elif operator == "gt":
                filtered = [item for item in filtered if self._get_field(item, field) > filter_value]
            elif operator == "lt":
                filtered = [item for item in filtered if self._get_field(item, field) < filter_value]
            elif operator == "gte":
                filtered = [item for item in filtered if self._get_field(item, field) >= filter_value]
            elif operator == "lte":
                filtered = [item for item in filtered if self._get_field(item, field) <= filter_value]
            elif operator == "in":
                filtered = [item for item in filtered if self._get_field(item, field) in filter_value]
            elif operator == "not":
                filtered = [item for item in filtered if self._get_field(item, field) != filter_value]

        return filtered

    def _sort_items(self, items: List[Any], sort_by: str, sort_order: str = "asc") -> List[Any]:
        """Sort items by a field"""
        reverse = sort_order.lower() == "desc"

        try:
            return sorted(items, key=lambda x: self._get_field(x, sort_by), reverse=reverse)
        except (TypeError, KeyError):
            # If sorting fails, return unsorted
            return items

    def _get_field(self, item: Any, field: str) -> Any:
        """Get field value from dict or object"""
        if isinstance(item, dict):
            return item.get(field)
        else:
            return getattr(item, field, None)

    def search(
        self,
        items: List[Any],
        query: str,
        search_fields: List[str],
        limit: Optional[int] = None
    ) -> List[Any]:
        """
        Search items across multiple fields

        Args:
            items: List of items to search
            query: Search query string
            search_fields: List of field names to search in
            limit: Maximum results to return

        Returns:
            List of matching items
        """
        if not query:
            return items[:limit] if limit else items

        query_lower = query.lower()
        results = []
        seen_ids = set()

        for item in items:
            # Get unique ID if available
            item_id = self._get_field(item, "id")

            if item_id and item_id in seen_ids:
                continue

            # Check each search field
            for field in search_fields:
                field_value = self._get_field(item, field)
                if field_value and query_lower in str(field_value).lower():
                    results.append(item)
                    if item_id:
                        seen_ids.add(item_id)
                    break

            # Early exit if limit reached
            if limit and len(results) >= limit:
                break

        return results

    def cache_list(self, key: str, items: List[Any], ttl_seconds: Optional[int] = None):
        """Cache a list with TTL"""
        ttl = timedelta(seconds=ttl_seconds) if ttl_seconds else self.cache_ttl
        expiry = datetime.now() + ttl

        self._cache[key] = {
            "items": items,
            "expiry": expiry
        }

    def get_cached_list(self, key: str) -> Optional[List[Any]]:
        """Get cached list if not expired"""
        if key not in self._cache:
            return None

        cached = self._cache[key]
        if datetime.now() >= cached["expiry"]:
            del self._cache[key]
            return None

        return cached["items"]

    def clear_cache(self, key: Optional[str] = None):
        """Clear cache (specific key or all)"""
        if key:
            self._cache.pop(key, None)
        else:
            self._cache.clear()

    def batch_process(
        self,
        items: List[Any],
        processor: Callable[[Any], Any],
        batch_size: int = 100
    ) -> List[Any]:
        """
        Process items in batches

        Args:
            items: Items to process
            processor: Function to apply to each item
            batch_size: Number of items per batch

        Returns:
            List of processed items
        """
        results = []

        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            results.extend([processor(item) for item in batch])

        return results

    def deduplicate(
        self,
        items: List[Any],
        key_field: Optional[str] = None
    ) -> List[Any]:
        """
        Remove duplicates from list

        Args:
            items: List to deduplicate
            key_field: Field to use for uniqueness (None = whole item)

        Returns:
            Deduplicated list
        """
        if not items:
            return []

        if key_field:
            seen = set()
            unique = []
            for item in items:
                key = self._get_field(item, key_field)
                if key not in seen:
                    seen.add(key)
                    unique.append(item)
            return unique
        else:
            # For hashable items
            try:
                return list(dict.fromkeys(items))
            except TypeError:
                # For unhashable items, use str representation
                seen = set()
                unique = []
                for item in items:
                    item_str = str(item)
                    if item_str not in seen:
                        seen.add(item_str)
                        unique.append(item)
                return unique

    def group_by(self, items: List[Any], field: str) -> Dict[Any, List[Any]]:
        """
        Group items by field value

        Args:
            items: List to group
            field: Field to group by

        Returns:
            Dict mapping field values to lists of items
        """
        groups = {}

        for item in items:
            key = self._get_field(item, field)
            if key not in groups:
                groups[key] = []
            groups[key].append(item)

        return groups

    def aggregate(
        self,
        items: List[Any],
        field: str,
        operation: str = "sum"
    ) -> Union[int, float, Any]:
        """
        Aggregate numeric field

        Args:
            items: List to aggregate
            field: Field to aggregate
            operation: "sum", "avg", "min", "max", "count"

        Returns:
            Aggregated value
        """
        values = [self._get_field(item, field) for item in items]
        values = [v for v in values if v is not None]

        if not values:
            return 0

        if operation == "sum":
            return sum(values)
        elif operation == "avg":
            return sum(values) / len(values)
        elif operation == "min":
            return min(values)
        elif operation == "max":
            return max(values)
        elif operation == "count":
            return len(values)
        else:
            raise ValueError(f"Unknown operation: {operation}")


# Singleton instance
_list_manager = None


def get_list_manager() -> ListManager:
    """Get singleton list manager instance"""
    global _list_manager
    if _list_manager is None:
        _list_manager = ListManager()
    return _list_manager


# Convenience functions

def paginate_list(
    items: List[Any],
    page: int = 1,
    page_size: int = 20,
    **kwargs
) -> ListResponse:
    """Convenience function for pagination"""
    return get_list_manager().paginate(items, page, page_size, **kwargs)


def search_list(
    items: List[Any],
    query: str,
    search_fields: List[str],
    limit: Optional[int] = None
) -> List[Any]:
    """Convenience function for searching"""
    return get_list_manager().search(items, query, search_fields, limit)


def deduplicate_list(items: List[Any], key_field: Optional[str] = None) -> List[Any]:
    """Convenience function for deduplication"""
    return get_list_manager().deduplicate(items, key_field)


if __name__ == "__main__":
    # Example usage
    print("ECH0 List Utilities - Test Suite")
    print("=" * 70)

    # Test data
    test_items = [
        {"id": 1, "name": "Alpha", "score": 85, "category": "A"},
        {"id": 2, "name": "Beta", "score": 92, "category": "B"},
        {"id": 3, "name": "Gamma", "score": 78, "category": "A"},
        {"id": 4, "name": "Delta", "score": 95, "category": "C"},
        {"id": 5, "name": "Epsilon", "score": 88, "category": "B"},
        {"id": 6, "name": "Zeta", "score": 91, "category": "A"},
    ]

    manager = get_list_manager()

    # Test pagination
    print("\n1. Pagination (page 1, size 3):")
    result = manager.paginate(test_items, page=1, page_size=3)
    print(f"   Items: {[item['name'] for item in result.items]}")
    print(f"   Total: {result.total_count}, Pages: {result.total_pages}")

    # Test filtering
    print("\n2. Filter (category = A):")
    result = manager.paginate(test_items, filters={"category": "A"})
    print(f"   Items: {[item['name'] for item in result.items]}")

    # Test sorting
    print("\n3. Sort by score (desc):")
    result = manager.paginate(test_items, sort_by="score", sort_order="desc", page_size=3)
    print(f"   Items: {[(item['name'], item['score']) for item in result.items]}")

    # Test search
    print("\n4. Search (query = 'ta'):")
    results = manager.search(test_items, "ta", ["name"])
    print(f"   Items: {[item['name'] for item in results]}")

    # Test grouping
    print("\n5. Group by category:")
    groups = manager.group_by(test_items, "category")
    for category, items in groups.items():
        print(f"   {category}: {[item['name'] for item in items]}")

    # Test aggregation
    print("\n6. Aggregate scores:")
    print(f"   Sum: {manager.aggregate(test_items, 'score', 'sum')}")
    print(f"   Avg: {manager.aggregate(test_items, 'score', 'avg'):.2f}")
    print(f"   Max: {manager.aggregate(test_items, 'score', 'max')}")

    print("\n✅ All tests completed!")
