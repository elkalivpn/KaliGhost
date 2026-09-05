"""
KaliGhost IDE - RAG-based CVE Intelligence Module
Implements Retrieval-Augmented Generation for local CVE database queries.
Provides real-time vulnerability intelligence to the AI agent.
"""

import os
import json
import sqlite3
import hashlib
import requests
import threading
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class CVEEntry:
    """Represents a CVE entry with full metadata."""
    cve_id: str
    description: str
    severity: str
    cvss_score: float
    published_date: str
    modified_date: str
    affected_products: List[str]
    references: List[str]
    exploit_available: bool
    patch_available: bool
    embedding: Optional[List[float]] = None


class CVEDatabase:
    """
    Local SQLite database for CVE storage with vector embeddings.
    Supports semantic search and fast lookups.
    """
    
    def __init__(self, db_path: str = "/tmp/kalighost_cve.db"):
        self.db_path = db_path
        self.conn = None
        self.lock = threading.Lock()
        self._init_db()
    
    def _init_db(self):
        """Initialize the database schema."""
        with self.lock:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            cursor = self.conn.cursor()
            
            # Main CVE table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cves (
                    cve_id TEXT PRIMARY KEY,
                    description TEXT,
                    severity TEXT,
                    cvss_score REAL,
                    published_date TEXT,
                    modified_date TEXT,
                    affected_products TEXT,
                    references TEXT,
                    exploit_available BOOLEAN,
                    patch_available BOOLEAN,
                    embedding BLOB,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Indexes for fast lookup
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_severity ON cves(severity)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_cvss ON cves(cvss_score)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_published ON cves(published_date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_exploit ON cves(exploit_available)')
            
            # Products table for many-to-many relationship
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_name TEXT UNIQUE
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cve_products (
                    cve_id TEXT,
                    product_id INTEGER,
                    FOREIGN KEY (cve_id) REFERENCES cves(cve_id),
                    FOREIGN KEY (product_id) REFERENCES products(id),
                    PRIMARY KEY (cve_id, product_id)
                )
            ''')
            
            self.conn.commit()
    
    def insert_cve(self, cve: CVEEntry) -> bool:
        """Insert or update a CVE entry."""
        try:
            with self.lock:
                cursor = self.conn.cursor()
                
                # Serialize lists
                affected_products = json.dumps(cve.affected_products)
                references = json.dumps(cve.references)
                embedding = json.dumps(cve.embedding).encode() if cve.embedding else None
                
                cursor.execute('''
                    INSERT OR REPLACE INTO cves 
                    (cve_id, description, severity, cvss_score, published_date, 
                     modified_date, affected_products, references, 
                     exploit_available, patch_available, embedding)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    cve.cve_id, cve.description, cve.severity, cve.cvss_score,
                    cve.published_date, cve.modified_date, affected_products,
                    references, cve.exploit_available, cve.patch_available, embedding
                ))
                
                self.conn.commit()
                return True
                
        except Exception as e:
            print(f"Error inserting CVE: {e}")
            return False
    
    def get_cve(self, cve_id: str) -> Optional[CVEEntry]:
        """Retrieve a specific CVE by ID."""
        try:
            with self.lock:
                cursor = self.conn.cursor()
                cursor.execute('SELECT * FROM cves WHERE cve_id = ?', (cve_id,))
                row = cursor.fetchone()
                
                if not row:
                    return None
                
                return CVEEntry(
                    cve_id=row[0],
                    description=row[1],
                    severity=row[2],
                    cvss_score=row[3],
                    published_date=row[4],
                    modified_date=row[5],
                    affected_products=json.loads(row[6]),
                    references=json.loads(row[7]),
                    exploit_available=bool(row[8]),
                    patch_available=bool(row[9]),
                    embedding=json.loads(row[10]) if row[10] else None
                )
                
        except Exception as e:
            print(f"Error retrieving CVE: {e}")
            return None
    
    def search_by_severity(self, severity: str, limit: int = 100) -> List[CVEEntry]:
        """Search CVEs by severity level."""
        return self._query_cves('severity = ?', (severity,), limit)
    
    def search_high_cvss(self, min_score: float = 9.0, limit: int = 100) -> List[CVEEntry]:
        """Search CVEs with high CVSS scores."""
        return self._query_cves('cvss_score >= ?', (min_score,), limit)
    
    def search_with_exploits(self, limit: int = 100) -> List[CVEEntry]:
        """Search CVEs that have known exploits."""
        return self._query_cves('exploit_available = 1', (), limit)
    
    def search_by_product(self, product_name: str, limit: int = 100) -> List[CVEEntry]:
        """Search CVEs affecting a specific product."""
        try:
            with self.lock:
                cursor = self.conn.cursor()
                cursor.execute('''
                    SELECT c.* FROM cves c
                    JOIN cve_products cp ON c.cve_id = cp.cve_id
                    JOIN products p ON cp.product_id = p.id
                    WHERE p.product_name LIKE ?
                    LIMIT ?
                ''', (f'%{product_name}%', limit))
                
                rows = cursor.fetchall()
                return [self._row_to_cve(row) for row in rows]
                
        except Exception as e:
            print(f"Error searching by product: {e}")
            return []
    
    def semantic_search(self, query_embedding: List[float], 
                       limit: int = 20) -> List[Tuple[CVEEntry, float]]:
        """
        Perform semantic search using vector similarity.
        Returns CVEs with similarity scores.
        """
        try:
            with self.lock:
                cursor = self.conn.cursor()
                cursor.execute('SELECT * FROM cves WHERE embedding IS NOT NULL')
                rows = cursor.fetchall()
                
                results = []
                for row in rows:
                    cve = self._row_to_cve(row)
                    if cve and cve.embedding:
                        similarity = self._cosine_similarity(query_embedding, cve.embedding)
                        results.append((cve, similarity))
                
                # Sort by similarity descending
                results.sort(key=lambda x: x[1], reverse=True)
                return results[:limit]
                
        except Exception as e:
            print(f"Error in semantic search: {e}")
            return []
    
    def _query_cves(self, where_clause: str, params: tuple, limit: int) -> List[CVEEntry]:
        """Generic CVE query method."""
        try:
            with self.lock:
                cursor = self.conn.cursor()
                query = f'SELECT * FROM cves WHERE {where_clause} ORDER BY cvss_score DESC LIMIT ?'
                cursor.execute(query, params + (limit,))
                rows = cursor.fetchall()
                return [self._row_to_cve(row) for row in rows]
                
        except Exception as e:
            print(f"Error querying CVEs: {e}")
            return []
    
    def _row_to_cve(self, row) -> Optional[CVEEntry]:
        """Convert database row to CVEEntry object."""
        try:
            return CVEEntry(
                cve_id=row[0],
                description=row[1],
                severity=row[2],
                cvss_score=row[3],
                published_date=row[4],
                modified_date=row[5],
                affected_products=json.loads(row[6]),
                references=json.loads(row[7]),
                exploit_available=bool(row[8]),
                patch_available=bool(row[9]),
                embedding=json.loads(row[10]) if row[10] else None
            )
        except:
            return None
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        if len(vec1) != len(vec2) or not vec1:
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a * a for a in vec1) ** 0.5
        norm2 = sum(b * b for b in vec2) ** 0.5
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        try:
            with self.lock:
                cursor = self.conn.cursor()
                
                stats = {}
                
                # Total CVEs
                cursor.execute('SELECT COUNT(*) FROM cves')
                stats['total_cves'] = cursor.fetchone()[0]
                
                # By severity
                cursor.execute('SELECT severity, COUNT(*) FROM cves GROUP BY severity')
                stats['by_severity'] = dict(cursor.fetchall())
                
                # With exploits
                cursor.execute('SELECT COUNT(*) FROM cves WHERE exploit_available = 1')
                stats['with_exploits'] = cursor.fetchone()[0]
                
                # High CVSS
                cursor.execute('SELECT COUNT(*) FROM cves WHERE cvss_score >= 9.0')
                stats['high_cvss'] = cursor.fetchone()[0]
                
                return stats
                
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {}
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()


class CVEIntelligenceEngine:
    """
    Main engine for CVE intelligence gathering and analysis.
    Integrates with NVD API and provides RAG capabilities.
    """
    
    def __init__(self, nvd_api_key: Optional[str] = None):
        self.db = CVEDatabase()
        self.nvd_api_key = nvd_api_key
        self.nvd_base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        self.last_update = None
        self.update_lock = threading.Lock()
    
    def fetch_latest_cves(self, days_back: int = 7) -> int:
        """
        Fetch latest CVEs from NVD API.
        Returns number of CVEs fetched.
        """
        try:
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days_back)
            
            headers = {}
            if self.nvd_api_key:
                headers['apiKey'] = self.nvd_api_key
            
            all_cves = []
            
            # Paginate through results
            start_index = 0
            results_per_page = 2000
            
            while True:
                params = {
                    'lastModStartDate': start_date.isoformat(),
                    'lastModEndDate': end_date.isoformat(),
                    'startIndex': start_index,
                    'resultsPerPage': results_per_page
                }
                
                response = requests.get(self.nvd_base_url, headers=headers, params=params, timeout=30)
                
                if response.status_code != 200:
                    print(f"NVD API error: {response.status_code}")
                    break
                
                data = response.json()
                cves = data.get('vulnerabilities', [])
                
                if not cves:
                    break
                
                all_cves.extend(cves)
                
                if start_index + results_per_page >= data.get('totalCount', 0):
                    break
                
                start_index += results_per_page
                time.sleep(0.5)  # Rate limiting
            
            # Process and store CVEs
            count = 0
            for vuln in all_cves:
                cve_data = vuln.get('cve', {})
                
                # Extract metrics
                metrics = cve_data.get('metrics', {})
                cvss_data = metrics.get('cvssMetricV31', [{}])[0]
                cvss_score = cvss_data.get('cvssData', {}).get('baseScore', 0.0)
                severity = cvss_data.get('cvssData', {}).get('baseSeverity', 'UNKNOWN')
                
                # Extract affected products
                configurations = cve_data.get('configurations', [])
                affected_products = []
                for config in configurations:
                    for node in config.get('nodes', []):
                        for cpe_match in node.get('cpeMatch', []):
                            affected_products.append(cpe_match.get('criteria', ''))
                
                # Create CVE entry
                cve = CVEEntry(
                    cve_id=cve_data.get('id', ''),
                    description=cve_data.get('descriptions', [{}])[0].get('value', ''),
                    severity=severity,
                    cvss_score=cvss_score,
                    published_date=cve_data.get('published', ''),
                    modified_date=cve_data.get('lastModified', ''),
                    affected_products=affected_products,
                    references=[ref.get('url', '') for ref in cve_data.get('references', [])],
                    exploit_available=self._check_exploit_availability(cve_data.get('id', '')),
                    patch_available=self._check_patch_availability(cve_data)
                )
                
                if self.db.insert_cve(cve):
                    count += 1
            
            self.last_update = datetime.utcnow()
            return count
            
        except Exception as e:
            print(f"Error fetching CVEs: {e}")
            return 0
    
    def query_cve(self, cve_id: str) -> Optional[CVEEntry]:
        """Query a specific CVE from local database."""
        return self.db.get_cve(cve_id)
    
    def search_vulnerabilities(self, query: str, product: Optional[str] = None,
                              min_cvss: float = 0.0, 
                              has_exploit: bool = False) -> List[CVEEntry]:
        """
        Search vulnerabilities with multiple filters.
        
        Args:
            query: Search query (product name, keyword, etc.)
            product: Specific product to filter
            min_cvss: Minimum CVSS score
            has_exploit: Filter for CVEs with exploits
            
        Returns:
            List of matching CVE entries
        """
        results = []
        
        # Start with product search if specified
        if product:
            results = self.db.search_by_product(product)
        elif has_exploit:
            results = self.db.search_with_exploits()
        elif min_cvss > 0:
            results = self.db.search_high_cvss(min_cvss)
        else:
            # Default to recent high-severity CVEs
            results = self.db.search_by_severity('HIGH')
        
        # Apply additional filters
        filtered = []
        for cve in results:
            if cve.cvss_score < min_cvss:
                continue
            if has_exploit and not cve.exploit_available:
                continue
            if query and query.lower() not in cve.description.lower():
                continue
            filtered.append(cve)
        
        return filtered
    
    def get_exploit_ready_cves(self, product_filter: Optional[str] = None) -> List[CVEEntry]:
        """Get CVEs that are ready for exploitation (exploit available, no patch)."""
        all_exploits = self.db.search_with_exploits()
        
        if not product_filter:
            return [cve for cve in all_exploits if not cve.patch_available]
        
        return [
            cve for cve in all_exploits 
            if not cve.patch_available and 
            any(product_filter.lower() in p.lower() for p in cve.affected_products)
        ]
    
    def generate_rag_context(self, query: str, context_size: int = 5) -> str:
        """
        Generate RAG context for AI agent queries.
        Returns formatted context string with relevant CVE information.
        """
        # Simple keyword-based retrieval (can be enhanced with embeddings)
        results = self.search_vulnerabilities(query, min_cvss=7.0)
        
        if not results:
            return "No relevant CVE information found."
        
        context_parts = []
        for i, cve in enumerate(results[:context_size], 1):
            context_parts.append(f"""
CVE-{i}: {cve.cve_id}
Severity: {cve.severity} (CVSS: {cve.cvss_score})
Description: {cve.description[:200]}...
Affected: {', '.join(cve.affected_products[:3])}
Exploit Available: {'Yes' if cve.exploit_available else 'No'}
Patch Available: {'Yes' if cve.patch_available else 'No'}
""")
        
        return "\n".join(context_parts)
    
    def _check_exploit_availability(self, cve_id: str) -> bool:
        """Check if exploit is available for CVE (simplified check)."""
        # In production, this would check ExploitDB, GitHub, etc.
        # For now, random simulation
        import random
        return random.random() < 0.15  # 15% chance
    
    def _check_patch_availability(self, cve_data: Dict) -> bool:
        """Check if patch is available for CVE."""
        # Check for vendor solutions in the data
        solutions = cve_data.get('solverOutput', {})
        return bool(solutions)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive CVE statistics."""
        stats = self.db.get_stats()
        stats['last_update'] = str(self.last_update) if self.last_update else 'Never'
        return stats
    
    def close(self):
        """Cleanup resources."""
        self.db.close()


# Singleton instance
_cve_engine: Optional[CVEIntelligenceEngine] = None


def get_cve_engine(nvd_api_key: Optional[str] = None) -> CVEIntelligenceEngine:
    """Get or create CVE intelligence engine singleton."""
    global _cve_engine
    if _cve_engine is None:
        _cve_engine = CVEIntelligenceEngine(nvd_api_key)
    return _cve_engine


if __name__ == "__main__":
    print("KaliGhost CVE Intelligence Module")
    
    engine = get_cve_engine()
    
    # Get statistics
    stats = engine.get_statistics()
    print(f"\nDatabase Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Example search
    print("\nSearching for high-CVSS vulnerabilities...")
    results = engine.search_vulnerabilities("", min_cvss=9.5, has_exploit=True)
    for cve in results[:5]:
        print(f"  {cve.cve_id}: {cve.severity} ({cve.cvss_score})")
