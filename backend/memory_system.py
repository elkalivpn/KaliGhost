#!/usr/bin/env python3
"""
🐉 KaliGhost Memory System
Persistent long-term memory across sessions (DeerFlow-inspired)
Local SQLite storage, no external dependencies
"""

import json
import sqlite3
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging
import hashlib

logger = logging.getLogger(__name__)


@dataclass
class MemoryEntry:
    """Single memory entry"""
    id: str
    category: str  # "preference", "fact", "context", "learned_skill"
    content: str
    metadata: Dict[str, Any]
    created_at: str
    last_accessed: str
    access_count: int = 0
    relevance_score: float = 1.0


class KaliGhostMemorySystem:
    """
    Long-term memory management
    Stores preferences, learned patterns, user context, and capabilities
    """

    def __init__(self, memory_dir: Optional[Path] = None):
        if memory_dir is None:
            memory_dir = Path.home() / ".kalighost" / "memory"
        
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        self.db_path = self.memory_dir / "memory.db"
        self._init_database()

    def _init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                category TEXT NOT NULL,
                content TEXT NOT NULL,
                metadata TEXT,
                created_at TEXT,
                last_accessed TEXT,
                access_count INTEGER DEFAULT 0,
                relevance_score REAL DEFAULT 1.0
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_category ON memories(category)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_relevance ON memories(relevance_score DESC)
        """)
        
        conn.commit()
        conn.close()
        logger.info(f"✅ Memory database initialized at {self.db_path}")

    def add_memory(
        self,
        category: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Add a new memory entry"""
        memory_id = self._hash_content(content)
        
        # Check if duplicate
        if self.get_memory(memory_id):
            logger.info(f"⚠️  Memory already exists: {memory_id}")
            return memory_id
        
        entry = MemoryEntry(
            id=memory_id,
            category=category,
            content=content,
            metadata=metadata or {},
            created_at=datetime.now().isoformat(),
            last_accessed=datetime.now().isoformat()
        )
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO memories (id, category, content, metadata, created_at, last_accessed)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            entry.id,
            entry.category,
            entry.content,
            json.dumps(entry.metadata),
            entry.created_at,
            entry.last_accessed
        ))
        
        conn.commit()
        conn.close()
        
        logger.info(f"✅ Memory added: {category} - {memory_id[:8]}...")
        return entry.id

    def get_memory(self, memory_id: str) -> Optional[MemoryEntry]:
        """Retrieve a specific memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, category, content, metadata, created_at, last_accessed, access_count, relevance_score
            FROM memories WHERE id = ?
        """, (memory_id,))
        
        row = cursor.fetchone()
        
        if row:
            # Update access stats
            cursor.execute("""
                UPDATE memories SET access_count = access_count + 1, last_accessed = ?
                WHERE id = ?
            """, (datetime.now().isoformat(), memory_id))
            conn.commit()
        
        conn.close()
        
        if row:
            return MemoryEntry(
                id=row[0],
                category=row[1],
                content=row[2],
                metadata=json.loads(row[3]),
                created_at=row[4],
                last_accessed=row[5],
                access_count=row[6],
                relevance_score=row[7]
            )
        return None

    def search_memories(
        self,
        query: str,
        category: Optional[str] = None,
        limit: int = 10
    ) -> List[MemoryEntry]:
        """Search memories by content and category"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        sql = "SELECT id, category, content, metadata, created_at, last_accessed, access_count, relevance_score FROM memories WHERE 1=1"
        params = []
        
        if query:
            sql += " AND content LIKE ?"
            params.append(f"%{query}%")
        
        if category:
            sql += " AND category = ?"
            params.append(category)
        
        sql += " ORDER BY relevance_score DESC, last_accessed DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
        
        memories = [
            MemoryEntry(
                id=row[0],
                category=row[1],
                content=row[2],
                metadata=json.loads(row[3]),
                created_at=row[4],
                last_accessed=row[5],
                access_count=row[6],
                relevance_score=row[7]
            )
            for row in rows
        ]
        
        logger.info(f"🔍 Found {len(memories)} memories for query: {query}")
        return memories

    def get_by_category(self, category: str, limit: int = 20) -> List[MemoryEntry]:
        """Get all memories in a category"""
        return self.search_memories("", category=category, limit=limit)

    def update_relevance(self, memory_id: str, score: float):
        """Update memory relevance score (0.0-1.0)"""
        score = max(0.0, min(1.0, score))
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE memories SET relevance_score = ? WHERE id = ?
        """, (score, memory_id))
        
        conn.commit()
        conn.close()

    def delete_memory(self, memory_id: str) -> bool:
        """Delete a memory entry"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        
        if deleted:
            logger.info(f"🗑️  Memory deleted: {memory_id}")
        return deleted

    def get_user_profile(self) -> Dict[str, Any]:
        """Synthesize user profile from memories"""
        preferences = self.get_by_category("preference", limit=50)
        facts = self.get_by_category("fact", limit=50)
        learned_skills = self.get_by_category("learned_skill", limit=20)
        
        profile = {
            "preferences": [m.content for m in preferences],
            "facts": [m.content for m in facts],
            "learned_skills": [m.content for m in learned_skills],
            "memory_count": self._get_total_memory_count(),
            "last_updated": datetime.now().isoformat()
        }
        
        return profile

    def _get_total_memory_count(self) -> int:
        """Get total number of memories"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM memories")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def _hash_content(self, content: str) -> str:
        """Generate deterministic ID from content"""
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def cleanup_stale_memories(self, days: int = 90) -> int:
        """Remove memories not accessed in X days"""
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM memories 
            WHERE last_accessed < ? AND category NOT IN ('preference', 'fact')
        """, (cutoff_date,))
        
        conn.commit()
        deleted = cursor.rowcount
        conn.close()
        
        logger.info(f"🧹 Cleaned up {deleted} stale memories")
        return deleted

    def export_memories(self, output_path: Path) -> bool:
        """Export all memories to JSON"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM memories")
            rows = cursor.fetchall()
            conn.close()
            
            memories = [
                {
                    "id": row[0],
                    "category": row[1],
                    "content": row[2],
                    "metadata": json.loads(row[3]),
                    "created_at": row[4],
                    "last_accessed": row[5],
                    "access_count": row[6],
                    "relevance_score": row[7]
                }
                for row in rows
            ]
            
            with open(output_path, 'w') as f:
                json.dump(memories, f, indent=2)
            
            logger.info(f"✅ Memories exported to {output_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Export failed: {e}")
            return False

    def import_memories(self, input_path: Path) -> int:
        """Import memories from JSON"""
        try:
            with open(input_path, 'r') as f:
                memories = json.load(f)
            
            imported = 0
            for mem in memories:
                self.add_memory(
                    category=mem['category'],
                    content=mem['content'],
                    metadata=mem.get('metadata', {})
                )
                imported += 1
            
            logger.info(f"✅ Imported {imported} memories")
            return imported
        except Exception as e:
            logger.error(f"❌ Import failed: {e}")
            return 0


# Singleton instance
_memory_system: Optional[KaliGhostMemorySystem] = None


def get_memory_system(memory_dir: Optional[Path] = None) -> KaliGhostMemorySystem:
    """Get or create singleton memory system"""
    global _memory_system
    if _memory_system is None:
        _memory_system = KaliGhostMemorySystem(memory_dir)
    return _memory_system
