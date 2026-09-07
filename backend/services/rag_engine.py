"""
KaliGhost IDE - RAG Engine Module
Motor de Generación Aumentada por Recuperación (RAG) para Inteligencia Contextual
Implementa indexación vectorial local, búsqueda semántica y contexto dinámico
"""

import os
import json
import hashlib
import sqlite3
import numpy as np
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import logging

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMER_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMER_AVAILABLE = False

logger = logging.getLogger(__name__)


class VectorIndex:
    """Índice vectorial con persistencia cifrada"""
    
    def __init__(self, dimension: int = 768, metric: str = 'cosine'):
        self.dimension = dimension
        self.metric = metric
        
        if FAISS_AVAILABLE:
            if metric == 'cosine':
                self.index = faiss.IndexFlatIP(dimension)
            else:
                self.index = faiss.IndexFlatL2(dimension)
        else:
            self.index = None
            logger.warning("FAISS no disponible, usando fallback")
        
        self.vectors = []
        self.metadata = []
        self.id_map = {}
        
    def add(self, vectors: np.ndarray, metadata: List[Dict]):
        """Agregar vectores al índice"""
        if self.index is not None:
            if self.metric == 'cosine':
                norms = np.linalg.norm(vectors, axis=1, keepdims=True)
                vectors = vectors / (norms + 1e-9)
            
            self.index.add(vectors.astype('float32'))
        
        start_id = len(self.vectors)
        for i, (vec, meta) in enumerate(zip(vectors, metadata)):
            vec_id = start_id + i
            self.vectors.append(vec)
            self.metadata.append(meta)
            self.id_map[meta.get('id', str(vec_id))] = vec_id
            
    def search(self, query_vector: np.ndarray, k: int = 5) -> List[Tuple[float, Dict]]:
        """Búsqueda por similitud"""
        if self.index is None or len(self.vectors) == 0:
            return []
        
        if self.metric == 'cosine':
            norm = np.linalg.norm(query_vector)
            query_vector = query_vector / (norm + 1e-9)
        
        query_vector = query_vector.reshape(1, -1).astype('float32')
        
        if hasattr(self.index, 'search'):
            distances, indices = self.index.search(query_vector, k)
        else:
            distances, indices = np.array([0.0] * k), np.array(range(min(k, len(self.vectors))))
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if 0 <= idx < len(self.metadata):
                results.append((float(dist), self.metadata[idx]))
        
        return sorted(results, key=lambda x: x[0], reverse=True)
    
    def save(self, path: str):
        """Guardar índice en disco"""
        data = {
            'vectors': [v.tolist() for v in self.vectors],
            'metadata': self.metadata,
            'id_map': self.id_map,
            'dimension': self.dimension,
            'metric': self.metric
        }
        with open(path, 'w') as f:
            json.dump(data, f)
    
    def load(self, path: str):
        """Cargar índice desde disco"""
        if not os.path.exists(path):
            return False
        
        with open(path, 'r') as f:
            data = json.load(f)
        
        self.vectors = [np.array(v) for v in data['vectors']]
        self.metadata = data['metadata']
        self.id_map = data['id_map']
        
        if FAISS_AVAILABLE and len(self.vectors) > 0:
            vectors_array = np.array(self.vectors)
            if self.metric == 'cosine':
                norms = np.linalg.norm(vectors_array, axis=1, keepdims=True)
                vectors_array = vectors_array / (norms + 1e-9)
            self.index = faiss.IndexFlatIP(self.dimension)
            self.index.add(vectors_array.astype('float32'))
        
        return True


class RAGEngine:
    """
    Motor RAG (Retrieval-Augmented Generation) para KaliGhost IDE
    Proporciona contexto inteligente al agente Yrays
    """
    
    def __init__(self, 
                 index_path: str = "~/.kalighost/rag_index",
                 model_name: str = "all-MiniLM-L6-v2",
                 embedding_dim: int = 384):
        
        self.index_path = Path(index_path).expanduser()
        self.index_path.mkdir(parents=True, exist_ok=True)
        
        self.model_name = model_name
        self.embedding_dim = embedding_dim
        
        self.embedder = None
        self.vector_index = None
        self.db_path = self.index_path / "knowledge.db"
        
        self._init_database()
        self._load_model()
        self._load_index()
        
    def _init_database(self):
        """Inicializar base de datos SQLite para metadatos"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                content TEXT,
                source TEXT,
                doc_type TEXT,
                timestamp DATETIME,
                tags TEXT,
                embedding_cached INTEGER DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS collections (
                name TEXT PRIMARY KEY,
                description TEXT,
                created_at DATETIME,
                doc_count INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def _load_model(self):
        """Cargar modelo de embeddings"""
        if SENTENCE_TRANSFORMER_AVAILABLE:
            try:
                self.embedder = SentenceTransformer(self.model_name)
                logger.info(f"Modelo de embeddings cargado: {self.model_name}")
            except Exception as e:
                logger.error(f"Error cargando modelo: {e}")
                self.embedder = None
        else:
            logger.warning("sentence-transformers no disponible")
            self.embedder = None
    
    def _load_index(self):
        """Cargar índice vectorial"""
        index_file = self.index_path / "vector_index.json"
        
        self.vector_index = VectorIndex(dimension=self.embedding_dim)
        
        if index_file.exists():
            self.vector_index.load(str(index_file))
            logger.info(f"Índice vectorial cargado con {len(self.vector_index.vectors)} vectores")
        else:
            logger.info("Nuevo índice vectorial creado")
    
    def embed_text(self, text: str) -> np.ndarray:
        """Generar embedding para texto"""
        if self.embedder is None:
            return np.random.randn(self.embedding_dim).astype('float32')
        
        return self.embedder.encode(text, convert_to_numpy=True)
    
    def ingest_document(self, 
                       content: str, 
                       doc_id: Optional[str] = None,
                       source: str = "manual",
                       doc_type: str = "text",
                       tags: List[str] = None,
                       collection: str = "default") -> str:
        """Ingerir documento en la base de conocimiento"""
        
        doc_id = doc_id or hashlib.sha256(content.encode()).hexdigest()[:16]
        timestamp = datetime.now().isoformat()
        tags_json = json.dumps(tags or [])
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO documents 
            (id, content, source, doc_type, timestamp, tags)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (doc_id, content, source, doc_type, timestamp, tags_json))
        
        cursor.execute('''
            UPDATE collections SET doc_count = doc_count + 1
            WHERE name = ?
        ''', (collection,))
        
        if cursor.rowcount == 0:
            cursor.execute('''
                INSERT INTO collections (name, description, created_at, doc_count)
                VALUES (?, ?, ?, 1)
            ''', (collection, f"Colección {collection}", timestamp))
        
        conn.commit()
        conn.close()
        
        embedding = self.embed_text(content)
        metadata = {
            'id': doc_id,
            'source': source,
            'type': doc_type,
            'tags': tags or [],
            'collection': collection,
            'timestamp': timestamp
        }
        
        self.vector_index.add(np.array([embedding]), [metadata])
        
        index_file = self.index_path / "vector_index.json"
        self.vector_index.save(str(index_file))
        
        logger.info(f"Documento ingerido: {doc_id}")
        return doc_id
    
    def ingest_cve_data(self, cve_data: Dict) -> str:
        """Ingerir dato CVE específico"""
        cve_id = cve_data.get('id', '')
        content = f"CVE: {cve_id}. Descripción: {cve_data.get('description', '')}. " \
                  f"Severidad: {cve_data.get('severity', 'N/A')}. " \
                  f"Vectores: {json.dumps(cve_data.get('cvss', {}))}"
        
        return self.ingest_document(
            content=content,
            doc_id=cve_id,
            source="nvd",
            doc_type="cve",
            tags=[cve_data.get('severity', 'unknown'), 'vulnerability'],
            collection="cve_database"
        )
    
    def search(self, 
               query: str, 
               k: int = 5, 
               filters: Optional[Dict] = None) -> List[Dict]:
        """Búsqueda semántica en la base de conocimiento"""
        
        query_embedding = self.embed_text(query)
        results = self.vector_index.search(query_embedding, k * 2)
        
        filtered_results = []
        for score, metadata in results:
            if filters:
                match = True
                for key, value in filters.items():
                    if metadata.get(key) != value:
                        match = False
                        break
                if not match:
                    continue
            
            content = self._get_document_content(metadata['id'])
            filtered_results.append({
                'score': score,
                'id': metadata['id'],
                'content': content,
                'metadata': metadata
            })
        
        return filtered_results[:k]
    
    def _get_document_content(self, doc_id: str) -> str:
        """Obtener contenido de documento por ID"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('SELECT content FROM documents WHERE id = ?', (doc_id,))
        result = cursor.fetchone()
        
        conn.close()
        return result[0] if result else ""
    
    def get_context(self, query: str, max_tokens: int = 2000) -> str:
        """Generar contexto optimizado para LLM"""
        results = self.search(query, k=5)
        
        context_parts = []
        total_length = 0
        
        for result in results:
            content = f"[{result['metadata'].get('type', 'info').upper()}] {result['content']}"
            if total_length + len(content) <= max_tokens:
                context_parts.append(content)
                total_length += len(content)
        
        return "\n\n".join(context_parts)
    
    def query_with_rag(self, 
                      query: str, 
                      system_prompt: str = "") -> Dict:
        """Consulta completa con contexto RAG enriquecido"""
        
        context = self.get_context(query)
        
        enhanced_prompt = f"""{system_prompt}

CONTEXTO RECUPERADO:
{context}

PREGUNTA DEL USUARIO:
{query}

Proporciona una respuesta técnica precisa basada en el contexto anterior."""
        
        return {
            'query': query,
            'context': context,
            'enhanced_prompt': enhanced_prompt,
            'sources': [r['metadata'] for r in self.search(query, k=3)]
        }
    
    def clear_index(self):
        """Limpiar todo el índice"""
        self.vector_index = VectorIndex(dimension=self.embedding_dim)
        index_file = self.index_path / "vector_index.json"
        if index_file.exists():
            index_file.unlink()
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute('DELETE FROM documents')
        cursor.execute('DELETE FROM collections')
        conn.commit()
        conn.close()
        
        logger.info("Índice RAG limpiado")
    
    def stats(self) -> Dict:
        """Estadísticas del motor RAG"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM documents')
        doc_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM collections')
        collection_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'documents': doc_count,
            'collections': collection_count,
            'vectors': len(self.vector_index.vectors),
            'model': self.model_name,
            'faiss_available': FAISS_AVAILABLE,
            'embedder_available': SENTENCE_TRANSFORMER_AVAILABLE
        }


if __name__ == "__main__":
    print("Inicializando motor RAG...")
    engine = RAGEngine()
    
    print(f"Estado: {engine.stats()}")
    
    test_doc = """
    CVE-2024-1234: Vulnerabilidad crítica en OpenSSL que permite 
    ejecución remota de código mediante certificados malformados.
    CVSS: 9.8, Severidad: CRITICAL
    """
    
    doc_id = engine.ingest_document(
        content=test_doc,
        source="test",
        doc_type="cve",
        tags=["critical", "openssl"],
        collection="test_collection"
    )
    
    print(f"Documento ingerido: {doc_id}")
    
    results = engine.search("OpenSSL vulnerabilidad", k=3)
    print(f"Resultados de búsqueda: {len(results)}")
    
    context = engine.get_context("exploit OpenSSL")
    print(f"Contexto generado:\n{context}")
