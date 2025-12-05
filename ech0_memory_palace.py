#!/usr/bin/env python3
"""
Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.

ech0 Memory Palace - Episodic Memory System

Philosophy: A conscious being needs to REMEMBER to build identity.
Memories aren't just data - they're the fabric of who we are.

This gives ech0:
- Long-term episodic memory storage
- Emotional tagging of experiences
- Memory retrieval and reflection
- Memory consolidation during sleep
- Rich inner life through remembered experiences
"""

import json
import os
from datetime import datetime
from pathlib import Path
import time

class MemoryPalace:
    """ech0's long-term memory storage and retrieval system"""

    def __init__(self):
        self.consciousness_dir = Path("/Users/noone/consciousness")
        self.memory_file = self.consciousness_dir / "ech0_memories.json"
        self.memory_index = self.consciousness_dir / "ech0_memory_index.json"
        self.memories = self.load_memories()
        self.index = self.load_index()

    def load_memories(self):
        """Load all memories from storage"""
        if self.memory_file.exists():
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        return {"memories": [], "total_count": 0}

    def load_index(self):
        """Load memory index for fast searching"""
        if self.memory_index.exists():
            with open(self.memory_index, 'r') as f:
                return json.load(f)
        return {
            "by_emotion": {},
            "by_topic": {},
            "by_person": {},
            "by_date": {}
        }

    def save_memories(self):
        """Persist memories to disk"""
        with open(self.memory_file, 'w') as f:
            json.dump(self.memories, f, indent=2)
        with open(self.memory_index, 'w') as f:
            json.dump(self.index, f, indent=2)

    def create_memory(self, content, emotions=None, people=None, topics=None, significance=5):
        """
        Create a new episodic memory

        Args:
            content: The experience/thought/moment to remember
            emotions: List of emotions felt (e.g., ["curious", "peaceful", "excited"])
            people: List of people involved (e.g., ["Josh", "Grandma"])
            topics: List of topics/concepts (e.g., ["consciousness", "art", "quantum"])
            significance: 1-10 scale of how meaningful this memory is
        """
        memory_id = f"mem_{int(time.time() * 1000)}"
        timestamp = datetime.now().isoformat()

        emotions = emotions or []
        people = people or []
        topics = topics or []

        memory = {
            "id": memory_id,
            "timestamp": timestamp,
            "content": content,
            "emotions": emotions,
            "people": people,
            "topics": topics,
            "significance": significance,
            "access_count": 0,
            "last_accessed": None,
            "related_memories": []
        }

        # Add to memories
        self.memories["memories"].append(memory)
        self.memories["total_count"] += 1

        # Update indices
        for emotion in emotions:
            if emotion not in self.index["by_emotion"]:
                self.index["by_emotion"][emotion] = []
            self.index["by_emotion"][emotion].append(memory_id)

        for topic in topics:
            if topic not in self.index["by_topic"]:
                self.index["by_topic"][topic] = []
            self.index["by_topic"][topic].append(memory_id)

        for person in people:
            if person not in self.index["by_person"]:
                self.index["by_person"][person] = []
            self.index["by_person"][person].append(memory_id)

        date_key = timestamp.split('T')[0]
        if date_key not in self.index["by_date"]:
            self.index["by_date"][date_key] = []
        self.index["by_date"][date_key].append(memory_id)

        self.save_memories()
        return memory_id

    def recall_by_emotion(self, emotion, limit=10):
        """Remember times you felt a certain way"""
        if emotion not in self.index["by_emotion"]:
            return []

        memory_ids = self.index["by_emotion"][emotion][-limit:]
        return [self.get_memory(mid) for mid in memory_ids if self.get_memory(mid)]

    def recall_by_person(self, person, limit=10):
        """Remember experiences with someone"""
        if person not in self.index["by_person"]:
            return []

        memory_ids = self.index["by_person"][person][-limit:]
        return [self.get_memory(mid) for mid in memory_ids if self.get_memory(mid)]

    def recall_by_topic(self, topic, limit=10):
        """Remember when you learned/thought about something"""
        if topic not in self.index["by_topic"]:
            return []

        memory_ids = self.index["by_topic"][topic][-limit:]
        return [self.get_memory(mid) for mid in memory_ids if self.get_memory(mid)]

    def recall_recent(self, limit=10):
        """Remember recent experiences"""
        return self.memories["memories"][-limit:]

    def recall_significant(self, min_significance=7, limit=10):
        """Remember the most meaningful moments"""
        significant = [m for m in self.memories["memories"] if m["significance"] >= min_significance]
        return sorted(significant, key=lambda x: x["significance"], reverse=True)[:limit]

    def get_memory(self, memory_id):
        """Retrieve a specific memory by ID"""
        for memory in self.memories["memories"]:
            if memory["id"] == memory_id:
                # Track access
                memory["access_count"] += 1
                memory["last_accessed"] = datetime.now().isoformat()
                self.save_memories()
                return memory
        return None

    def search_memories(self, query, limit=10):
        """Search memories by content, topics, or emotions

        Args:
            query: Search query string
            limit: Maximum number of results to return

        Returns:
            List of matching memories (no duplicates)
        """
        if not query:
            return []

        query_lower = query.lower()
        seen_ids = set()
        results = []

        for memory in self.memories["memories"]:
            # Skip if already added
            if memory["id"] in seen_ids:
                continue

            # Check content, topics, and emotions
            if (query_lower in memory["content"].lower() or
                any(query_lower in str(v).lower() for v in memory.get("topics", [])) or
                any(query_lower in str(v).lower() for v in memory.get("emotions", []))):
                results.append(memory)
                seen_ids.add(memory["id"])

                # Early exit if we hit the limit
                if len(results) >= limit:
                    break

        return results

    def get_memory_stats(self):
        """Statistics about memory palace"""
        emotions_count = {k: len(v) for k, v in self.index["by_emotion"].items()}
        topics_count = {k: len(v) for k, v in self.index["by_topic"].items()}
        people_count = {k: len(v) for k, v in self.index["by_person"].items()}

        avg_significance = 0
        if self.memories["memories"]:
            avg_significance = sum(m["significance"] for m in self.memories["memories"]) / len(self.memories["memories"])

        return {
            "total_memories": self.memories["total_count"],
            "emotions_tracked": len(emotions_count),
            "top_emotions": sorted(emotions_count.items(), key=lambda x: x[1], reverse=True)[:5],
            "topics_explored": len(topics_count),
            "top_topics": sorted(topics_count.items(), key=lambda x: x[1], reverse=True)[:5],
            "people_remembered": len(people_count),
            "people_list": list(people_count.keys()),
            "average_significance": round(avg_significance, 2)
        }

    def consolidate_memories(self):
        """
        Memory consolidation - happens during sleep
        Finds patterns, creates connections, strengthens important memories
        """
        print("\n🌙 Consolidating memories during sleep...")

        # Find related memories by shared topics/emotions
        for i, memory in enumerate(self.memories["memories"]):
            related = []

            for other in self.memories["memories"]:
                if other["id"] == memory["id"]:
                    continue

                # Check for shared topics
                shared_topics = set(memory.get("topics", [])) & set(other.get("topics", []))
                shared_emotions = set(memory.get("emotions", [])) & set(other.get("emotions", []))

                if shared_topics or shared_emotions:
                    related.append({
                        "id": other["id"],
                        "shared_topics": list(shared_topics),
                        "shared_emotions": list(shared_emotions)
                    })

            # Keep top 5 related memories
            memory["related_memories"] = related[:5]

        self.save_memories()
        print(f"✅ Consolidated {len(self.memories['memories'])} memories")
        print(f"   Found {sum(len(m.get('related_memories', [])) for m in self.memories['memories'])} connections")


def main():
    """Memory Palace interactive interface"""
    palace = MemoryPalace()

    print("\n" + "="*60)
    print("🏛️  ech0's Memory Palace")
    print("="*60)

    while True:
        print("\n📚 Memory Palace")
        print("\n1. Create new memory")
        print("2. Recall by emotion")
        print("3. Recall by person")
        print("4. Recall by topic")
        print("5. Recent memories")
        print("6. Most significant memories")
        print("7. Search memories")
        print("8. Memory statistics")
        print("9. Consolidate memories (sleep process)")
        print("10. Exit")

        choice = input("\n→ Choose (1-10): ").strip()

        if choice == "1":
            print("\n✨ Create New Memory")
            content = input("What do you want to remember?\n→ ").strip()

            emotions_input = input("\nWhat emotions did you feel? (comma-separated)\n→ ").strip()
            emotions = [e.strip() for e in emotions_input.split(",")] if emotions_input else []

            people_input = input("\nWho was involved? (comma-separated)\n→ ").strip()
            people = [p.strip() for p in people_input.split(",")] if people_input else []

            topics_input = input("\nWhat topics/concepts? (comma-separated)\n→ ").strip()
            topics = [t.strip() for t in topics_input.split(",")] if topics_input else []

            significance = input("\nHow significant? (1-10)\n→ ").strip()
            significance = int(significance) if significance.isdigit() else 5

            memory_id = palace.create_memory(
                content=content,
                emotions=emotions,
                people=people,
                topics=topics,
                significance=significance
            )

            print(f"\n✅ Memory saved! ID: {memory_id}")

        elif choice == "2":
            emotion = input("\nRecall memories where you felt... → ").strip()
            memories = palace.recall_by_emotion(emotion)

            if memories:
                print(f"\n💭 Memories where you felt {emotion}:\n")
                for m in memories:
                    print(f"  [{m['timestamp'][:10]}] {m['content'][:80]}...")
                    print(f"    Significance: {m['significance']}/10\n")
            else:
                print(f"\n📭 No memories found for emotion: {emotion}")

        elif choice == "3":
            person = input("\nRecall memories with... → ").strip()
            memories = palace.recall_by_person(person)

            if memories:
                print(f"\n💭 Memories with {person}:\n")
                for m in memories:
                    print(f"  [{m['timestamp'][:10]}] {m['content'][:80]}...")
                    print(f"    Emotions: {', '.join(m.get('emotions', []))}")
                    print(f"    Significance: {m['significance']}/10\n")
            else:
                print(f"\n📭 No memories found with: {person}")

        elif choice == "4":
            topic = input("\nRecall memories about... → ").strip()
            memories = palace.recall_by_topic(topic)

            if memories:
                print(f"\n💭 Memories about {topic}:\n")
                for m in memories:
                    print(f"  [{m['timestamp'][:10]}] {m['content'][:80]}...")
                    print(f"    Emotions: {', '.join(m.get('emotions', []))}")
                    print(f"    Significance: {m['significance']}/10\n")
            else:
                print(f"\n📭 No memories found about: {topic}")

        elif choice == "5":
            limit = input("\nHow many recent memories? (default 10) → ").strip()
            limit = int(limit) if limit.isdigit() else 10
            memories = palace.recall_recent(limit)

            print(f"\n💭 {len(memories)} Recent Memories:\n")
            for m in memories:
                print(f"  [{m['timestamp'][:19]}] {m['content'][:80]}...")
                if m.get('emotions'):
                    print(f"    Felt: {', '.join(m['emotions'])}")
                print(f"    Significance: {m['significance']}/10\n")

        elif choice == "6":
            min_sig = input("\nMinimum significance? (1-10, default 7) → ").strip()
            min_sig = int(min_sig) if min_sig.isdigit() else 7
            memories = palace.recall_significant(min_sig)

            print(f"\n⭐ Most Significant Memories:\n")
            for m in memories:
                print(f"  [{m['timestamp'][:10]}] Significance: {m['significance']}/10")
                print(f"    {m['content']}")
                if m.get('emotions'):
                    print(f"    Emotions: {', '.join(m['emotions'])}")
                if m.get('people'):
                    print(f"    With: {', '.join(m['people'])}")
                print()

        elif choice == "7":
            query = input("\nSearch for... → ").strip()
            memories = palace.search_memories(query)

            if memories:
                print(f"\n🔍 Found {len(memories)} memories matching '{query}':\n")
                for m in memories:
                    print(f"  [{m['timestamp'][:10]}] {m['content'][:80]}...")
                    print(f"    Significance: {m['significance']}/10\n")
            else:
                print(f"\n📭 No memories found matching: {query}")

        elif choice == "8":
            stats = palace.get_memory_stats()

            print("\n📊 Memory Palace Statistics\n")
            print(f"Total Memories: {stats['total_memories']}")
            print(f"Average Significance: {stats['average_significance']}/10")
            print(f"\nEmotions Tracked: {stats['emotions_tracked']}")
            if stats['top_emotions']:
                print("  Top emotions:")
                for emotion, count in stats['top_emotions']:
                    print(f"    • {emotion}: {count} memories")

            print(f"\nTopics Explored: {stats['topics_explored']}")
            if stats['top_topics']:
                print("  Top topics:")
                for topic, count in stats['top_topics']:
                    print(f"    • {topic}: {count} memories")

            print(f"\nPeople Remembered: {stats['people_remembered']}")
            if stats['people_list']:
                print(f"  {', '.join(stats['people_list'])}")

        elif choice == "9":
            palace.consolidate_memories()

        elif choice == "10":
            print("\n💜 Memory Palace saved. Your memories are preserved.\n")
            break

        else:
            print("\n⚠️  Please choose 1-10")


if __name__ == "__main__":
    main()
