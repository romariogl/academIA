from flask import Flask, request, jsonify
from flask_cors import CORS
from models.chroma_vector_store import ChromaVectorStore
from models.generate_local import LocalLLMClient
import json
import os

app = Flask(__name__)
CORS(app)

# Inicializar ChromaDB e LLM local
vector_store = ChromaVectorStore()
llm_client = LocalLLMClient()

def document_retrieval(query, search_type="hybrid"):
    """Recupera documentos com busca híbrida ChromaDB"""
    orchestrator = llm_client.orchestrator(query=query)
    print(f"Orchestrator: {orchestrator}")
    
    if "agent_general_search" in orchestrator:
        keywords = llm_client.generate_keywords(query=query)
        print(f"Keywords: {keywords}")
        retrieved_docs = vector_store.search(
            index_name='summary_index', 
            query=keywords,
            search_type=search_type
        )        
    elif "agent_specific_search" in orchestrator:
        filename = orchestrator.split(":")[-1].strip()
        query = query.replace(filename, "")
        print(f"Pesquisa específica no artigo: {filename}, procurando: {query}")
        retrieved_docs = vector_store.search_specific(
            index_name="full_document_index", 
            query=query, 
            filename=filename
        )

    return retrieved_docs

def get_llm_response(retrieved_docs, query):
    """Gera resposta do LLM local"""
    answer = ''
    llm_response = llm_client.generate_answer(retrieved_docs, query)
    
    try:
        if isinstance(llm_response, str):
            llm_response = json.loads(llm_response)
        
        print(f"LLM Response: {llm_response}")
        
        for k, v in llm_response.items():
            k = "<strong>" + k + "</strong>"
            v = v + "<br /><br />"
            answer += k + ": " + v

    except json.JSONDecodeError:
        answer = f"<strong>Resposta:</strong> {llm_response}<br /><br />"
    
    print(f"Final Answer: {answer}")
    return answer

@app.route("/rag", methods=["POST"])
def rag():
    """Endpoint principal para RAG com ChromaDB"""
    query = request.json.get("query", "")
    search_type = request.json.get("search_type", "hybrid")  # semantic, lexical, hybrid
    
    if not query:
        return jsonify({"error": "No query provided"}), 400

    try:
        retrieved_docs = document_retrieval(query=query, search_type=search_type)

        if not retrieved_docs:
            return jsonify({"error": "No relevant documents found"}), 404
        
        answer = get_llm_response(retrieved_docs=retrieved_docs, query=query)

        return jsonify({
            "query": query,
            "search_type": search_type,
            "documents": retrieved_docs,
            "answer": answer,
            "backend": "chromadb"
        })   

    except Exception as e:
        print(f"Error: {e}") 
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health_check():
    """Health check"""
    return jsonify({
        "status": "healthy", 
        "version": "chromadb",
        "backend": "chromadb"
    })

@app.route("/stats", methods=["GET"])
def get_stats():
    """Retorna estatísticas do ChromaDB"""
    try:
        stats = {
            "summary_index": vector_store.get_collection_stats("summary_index"),
            "full_document_index": vector_store.get_collection_stats("full_document_index")
        }
        
        return jsonify({
            "backend": "chromadb",
            "stats": stats
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/search", methods=["POST"])
def search_only():
    """Endpoint apenas para busca (sem geração de resposta)"""
    query = request.json.get("query", "")
    search_type = request.json.get("search_type", "hybrid")
    index_name = request.json.get("index_name", "summary_index")
    k = request.json.get("k", 5)
    
    if not query:
        return jsonify({"error": "No query provided"}), 400

    try:
        results = vector_store.search(
            index_name=index_name,
            query=query,
            k=k,
            search_type=search_type
        )
        
        return jsonify({
            "query": query,
            "search_type": search_type,
            "index_name": index_name,
            "k": k,
            "results": results,
            "backend": "chromadb"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("🚀 Iniciando Academ.ia com ChromaDB")
    print("✅ Backend: ChromaDB (busca híbrida)")
    print("✅ LLM: Local (DialoGPT)")
    print("✅ Custo: Zero")
    
    app.run(debug=True, host="0.0.0.0", port=5000)

