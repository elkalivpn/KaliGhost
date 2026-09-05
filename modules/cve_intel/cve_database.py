"""
CVE Intelligence Engine - Base de datos CVE con RAG y búsqueda semántica
"""
import sqlite3
import json
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
import numpy as np

class CVEIntelligenceEngine:
    """Motor de inteligencia CVE con búsqueda semántica"""
    
    def __init__(self, db_path: str = "data/cve_db/cve_database.sqlite"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    def _init_database(self) -> None:
        """Inicializa base de datos SQLite"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cves (
                cve_id TEXT PRIMARY KEY,
                description TEXT,
                severity TEXT,
                cvss_score REAL,
                published_date TEXT,
                modified_date TEXT,
                affected_products TEXT,
                references_json TEXT,
                embedding_vector BLOB
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_severity ON cves(severity)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_cvss ON cves(cvss_score)
        ''')
        
        conn.commit()
        conn.close()
    
    def add_cve(self, cve_data: Dict[str, Any]) -> bool:
        """Añade CVE a la base de datos"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Generar embedding simple (placeholder para modelo real)
            embedding = self._generate_embedding(cve_data.get("description", ""))
            
            cursor.execute('''
                INSERT OR REPLACE INTO cves 
                (cve_id, description, severity, cvss_score, published_date, 
                 modified_date, affected_products, references_json, embedding_vector)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                cve_data.get("id"),
                cve_data.get("description"),
                cve_data.get("severity", "UNKNOWN"),
                cve_data.get("cvss_score", 0.0),
                cve_data.get("published_date"),
                cve_data.get("modified_date"),
                json.dumps(cve_data.get("affected_products", [])),
                json.dumps(cve_data.get("references", [])),
                embedding.tobytes() if embedding is not None else None
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error añadiendo CVE: {e}")
            return False
    
    def search_by_id(self, cve_id: str) -> Optional[Dict[str, Any]]:
        """Busca CVE por ID"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM cves WHERE cve_id = ?', (cve_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def search_by_severity(self, severity: str) -> List[Dict[str, Any]]:
        """Busca CVEs por severidad"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM cves WHERE severity = ? ORDER BY cvss_score DESC', (severity,))
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def search_semantic(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Búsqueda semántica por similitud de embeddings"""
        query_embedding = self._generate_embedding(query)
        
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT cve_id, description, severity, cvss_score, embedding_vector FROM cves')
        rows = cursor.fetchall()
        conn.close()
        
        results = []
        for row in rows:
            if row['embedding_vector']:
                stored_embedding = np.frombuffer(row['embedding_vector'], dtype=np.float32)
                similarity = self._cosine_similarity(query_embedding, stored_embedding)
                results.append({
                    **dict(row),
                    "similarity": float(similarity)
                })
        
        # Ordenar por similitud
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]
    
    def get_critical_cves(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Obtiene CVEs críticos ordenados por CVSS"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM cves 
            WHERE severity IN ('CRITICAL', 'HIGH') 
            ORDER BY cvss_score DESC 
            LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de la base de datos"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM cves')
        total = cursor.fetchone()[0]
        
        cursor.execute('SELECT severity, COUNT(*) FROM cves GROUP BY severity')
        by_severity = dict(cursor.fetchall())
        
        cursor.execute('SELECT AVG(cvss_score) FROM cves')
        avg_cvss = cursor.fetchone()[0] or 0.0
        
        conn.close()
        
        return {
            "total_cves": total,
            "by_severity": by_severity,
            "average_cvss": round(avg_cvss, 2),
            "last_updated": datetime.now().isoformat()
        }
    
    def _generate_embedding(self, text: str, dimensions: int = 128) -> Optional[np.ndarray]:
        """Genera embedding vectorial simple (placeholder)"""
        if not text:
            return None
        
        # Hash simple como embedding (en producción usar modelo ML real)
        hash_val = hash(text)
        np.random.seed(hash_val % (2**32))
        embedding = np.random.randn(dimensions).astype(np.float32)
        
        # Normalizar
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        
        return embedding
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calcula similitud coseno entre dos vectores"""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return float(dot_product / (norm1 * norm2))
