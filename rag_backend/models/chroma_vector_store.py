import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import json
from collections import defaultdict
import os

class ChromaVectorStore:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChromaVectorStore, cls).__new__(cls)
            cls._instance.model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Configurar ChromaDB para persistência local
            cls._instance.client = chromadb.PersistentClient(
                path="./chroma_db",
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Criar ou obter coleções
            cls._instance.summary_collection = cls._instance.client.get_or_create_collection(
                name="summary_index",
                metadata={"hnsw:space": "cosine"}
            )
            cls._instance.full_collection = cls._instance.client.get_or_create_collection(
                name="full_document_index", 
                metadata={"hnsw:space": "cosine"}
            )
            
        return cls._instance

    def index(self, index_name, id, body):
        """Indexa um documento no ChromaDB"""
        content = body.get('content', '')
        article_name = body.get('article_name', 'Unknown')
        url = body.get('article_fulldoc_url', '')
        article_id = body.get('article_id', id)
        
        # Gerar embedding
        embedding = self.model.encode(content).tolist()
        
        # Preparar metadados
        metadata = {
            "article_name": article_name,
            "url": url,
            "article_id": article_id,
            "content_length": len(content)
        }
        
        # Escolher coleção baseada no índice
        collection = self.summary_collection if index_name == "summary_index" else self.full_collection
        
        # Adicionar documento
        collection.add(
            documents=[content],
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[id]
        )

    def search(self, index_name, query, k=5, search_type="hybrid"):
        """
        Busca híbrida: combina busca semântica (embedding) com busca léxica (texto)
        
        Args:
            index_name: Nome do índice
            query: Query de busca
            k: Número de resultados
            search_type: "semantic", "lexical", ou "hybrid"
        """
        collection = self.summary_collection if index_name == "summary_index" else self.full_collection
        
        if search_type == "semantic":
            # Busca apenas semântica
            results = collection.query(
                query_texts=[query],
                n_results=k,
                include=["documents", "metadatas", "distances"]
            )
        elif search_type == "lexical":
            # Busca apenas léxica (where clause)
            # ChromaDB não suporta $contains, então usamos busca semântica com filtro
            results = collection.query(
                query_texts=[query],
                n_results=k,
                include=["documents", "metadatas", "distances"]
            )
        else:  # hybrid
            # Busca híbrida: combina semântica + léxica
            semantic_results = collection.query(
                query_texts=[query],
                n_results=k,
                include=["documents", "metadatas", "distances"]
            )
            
            # Busca léxica adicional (sem filtro where devido a limitações do ChromaDB)
            lexical_results = collection.query(
                query_texts=[query],
                n_results=k//2,
                include=["documents", "metadatas", "distances"]
            )
            
            # Combinar resultados
            results = self._combine_results(semantic_results, lexical_results, k)
        
        return self._format_results(results)

    def search_specific(self, index_name, query, filename, k=20):
        """Busca específica em um documento"""
        collection = self.summary_collection if index_name == "summary_index" else self.full_collection
        
        # Busca semântica (filtro por nome será aplicado no pós-processamento)
        results = collection.query(
            query_texts=[query],
            n_results=k * 2,  # Buscar mais resultados para compensar a falta de filtro
            include=["documents", "metadatas", "distances"]
        )
        
        # Filtrar resultados por nome do arquivo no pós-processamento
        if results["documents"] and results["metadatas"]:
            filtered_results = {
                "documents": [],
                "metadatas": [],
                "distances": [],
                "ids": []
            }
            
            for i, metadata in enumerate(results["metadatas"][0]):
                article_name = metadata.get("article_name", "")
                if filename.lower() in article_name.lower():
                    filtered_results["documents"].append(results["documents"][0][i])
                    filtered_results["metadatas"].append(metadata)
                    filtered_results["distances"].append(results["distances"][0][i])
                    filtered_results["ids"].append(results["ids"][0][i])
            
            # Limitar a k resultados
            filtered_results["documents"] = filtered_results["documents"][:k]
            filtered_results["metadatas"] = filtered_results["metadatas"][:k]
            filtered_results["distances"] = filtered_results["distances"][:k]
            filtered_results["ids"] = filtered_results["ids"][:k]
            
            return self._format_results(filtered_results)
        
        return self._format_results(results)

    def search_with_filter(self, index_name, query, filter_field, filter_value, k=5):
        """
        Busca com filtro usando operadores suportados pelo ChromaDB
        """
        collection = self.summary_collection if index_name == "summary_index" else self.full_collection
        
        # Usar operador $eq para filtros exatos
        results = collection.query(
            query_texts=[query],
            n_results=k,
            where={filter_field: {"$eq": filter_value}},
            include=["documents", "metadatas", "distances"]
        )
        
        return self._format_results(results)

    def search_with_in_filter(self, index_name, query, filter_field, filter_values, k=5):
        """
        Busca com filtro IN usando operadores suportados pelo ChromaDB
        """
        collection = self.summary_collection if index_name == "summary_index" else self.full_collection
        
        # Usar operador $in para filtros de lista
        results = collection.query(
            query_texts=[query],
            n_results=k,
            where={filter_field: {"$in": filter_values}},
            include=["documents", "metadatas", "distances"]
        )
        
        return self._format_results(results)

    def _combine_results(self, semantic_results, lexical_results, k):
        """Combina resultados de busca semântica e léxica"""
        combined = {
            "documents": [],
            "metadatas": [],
            "distances": [],
            "ids": []
        }
        
        # Adicionar resultados semânticos
        if semantic_results["documents"]:
            combined["documents"].extend(semantic_results["documents"][0])
            combined["metadatas"].extend(semantic_results["metadatas"][0])
            combined["distances"].extend(semantic_results["distances"][0])
            combined["ids"].extend(semantic_results["ids"][0])
        
        # Adicionar resultados léxicos (evitando duplicatas)
        if lexical_results["documents"]:
            for i, doc_id in enumerate(lexical_results["ids"][0]):
                if doc_id not in combined["ids"]:
                    combined["documents"].append(lexical_results["documents"][0][i])
                    combined["metadatas"].append(lexical_results["metadatas"][0][i])
                    combined["distances"].append(lexical_results["distances"][0][i])
                    combined["ids"].append(doc_id)
        
        # Limitar a k resultados
        combined["documents"] = combined["documents"][:k]
        combined["metadatas"] = combined["metadatas"][:k]
        combined["distances"] = combined["distances"][:k]
        combined["ids"] = combined["ids"][:k]
        
        return combined

    def _format_results(self, results):
        """Formata resultados para compatibilidade com o sistema existente"""
        if not results["documents"]:
            return {}
        
        grouped_docs = defaultdict(str)
        
        for i, content in enumerate(results["documents"]):
            if i < len(results["metadatas"]):
                article_name = results["metadatas"][i].get("article_name", "Unknown Article")
                grouped_docs[article_name] += content + " "
        
        return dict(grouped_docs)

    def get_collection_stats(self, index_name):
        """Retorna estatísticas da coleção"""
        collection = self.summary_collection if index_name == "summary_index" else self.full_collection
        return collection.count()

    def delete_collection(self, index_name):
        """Deleta uma coleção"""
        try:
            self.client.delete_collection(index_name)
            print(f"Coleção {index_name} deletada com sucesso")
        except Exception as e:
            print(f"Erro ao deletar coleção {index_name}: {e}")

    def reset_collections(self):
        """Reseta todas as coleções"""
        try:
            self.client.reset()
            print("Todas as coleções foram resetadas")
        except Exception as e:
            print(f"Erro ao resetar coleções: {e}") 