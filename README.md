
# Academ.ia - CAPES Periodicals Portal with AI

<div align="center">
  <img src="capes.png" alt="CAPES Logo" width="200" style="margin: 20px;">
  <img src="academia.png" alt="Academ.ia AI Assistant" width="200" style="margin: 20px;">
</div>

<div align="center">
  <h3>🤖 Sistema Inteligente de Busca para o Portal de Periódicos da CAPES</h3>
  <p><strong>Integrando IA Generativa com Busca Semântica em Documentos Acadêmicos</strong></p>
  
  [![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
  [![React](https://img.shields.io/badge/React-18.3.1-blue.svg)](https://reactjs.org/)
  [![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
  [![ChromaDB](https://img.shields.io/badge/ChromaDB-Latest-orange.svg)](https://www.trychroma.com/)
  [![AI](https://img.shields.io/badge/AI-DialoGPT-purple.svg)](https://huggingface.co/microsoft/DialoGPT-medium)
</div>

---

## 🚀 Features

- **🌐 Interface Web**: Design baseado no Portal de Periódicos da CAPES
- **🤖 Chat com IA**: Assistente virtual para pesquisa acadêmica
- **🧠 Busca Semântica**: Usa ChromaDB para busca inteligente
- **🔍 RAG (Retrieval-Augmented Generation)**: Combina busca de documentos com geração de respostas
- **🏠 Modelo Local**: Usa DialoGPT para geração de respostas

## 🏗️ Architecture

### 📁 File Structure
```
academIA/
├── rag_backend/           # Flask Backend + ChromaDB
│   ├── app.py            # Flask API
│   ├── models/           # AI and vector models
│   │   ├── chroma_vector_store.py
│   │   └── generate_local.py
│   └── requirements.txt  # Python dependencies
├── rag_frontend/         # React Frontend
│   ├── src/
│   │   ├── App.js        # Main interface
│   │   └── App.css       # CAPES-based styles
│   └── package.json      # Node.js dependencies
└── ingestion_module/     # Data ingestion scripts
    └── ingest.py         # ChromaDB ingestion
```

### 🔄 Architecture Diagram
For a detailed view of the system architecture, see the [**Architecture Diagram**](./ARCHITECTURE.md).

**Main Components:**
- **React Frontend**: Interface based on the CAPES Periodicals Portal
- **Flask API**: Backend with search orchestration
- **ChromaDB**: Vector database for semantic search
- **DialoGPT**: Local AI model for response generation
- **Ingestion**: Data processing and indexing system

## 🛠️ Technologies

### Backend
- **Flask**: REST API
- **ChromaDB**: Vector database
- **Sentence Transformers**: Embeddings for semantic search
- **DialoGPT**: Local language model
- **Transformers**: AI models library

### Frontend
- **React**: User interface
- **Bootstrap**: CSS framework
- **Font Awesome**: Icons
- **Axios**: HTTP client

## 📦 Installation

### 1. Backend

```bash
cd rag_backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 2. Frontend

```bash
cd rag_frontend
npm install
```

## 🚀 Execution

### 1. Start Backend

```bash
cd rag_backend
python app.py
```

The backend will be available at: `http://127.0.0.1:5000`

### 2. Start Frontend

```bash
cd rag_frontend
npm start
```

The frontend will be available at: `http://localhost:3000`

### 3. Ingest Data (Optional)

```bash
python ingestion_module/ingest.py
```

## 🎯 How to Use

1. **Access the interface**: Open `http://localhost:3000`
2. **Click the AI button**: "For a better search experience, use our AI!"
3. **Ask questions**: 
   - General questions: "What are the articles about Artificial Intelligence?"
   - Specific questions: "In article X, what are the main conclusions?"

## 🔧 Configuration

### Environment Variables

```bash
# Backend
BACKEND_URL=http://127.0.0.1:5000

# ChromaDB
CHROMA_DB_PATH=./chroma_db
```

### AI Models

The system uses:
- **Sentence Transformers**: `all-MiniLM-L6-v2` (for embeddings)
- **DialoGPT**: `microsoft/DialoGPT-medium` (for generation)

## 📊 AI Features

### Search Types
- **Semantic Search**: Finds similar documents
- **Hybrid Search**: Combines semantic + lexical
- **Specific Search**: Focuses on a specific document

### Capabilities
- ✅ Search in academic articles
- ✅ Context-based responses
- ✅ Familiar CAPES interface
- ✅ Interactive chat
- ✅ Keyword search

## 🎨 Interface

<div align="center">
  <h4>🖥️ Interface Principal - Portal de Periódicos da CAPES</h4>
  <p><em>Design oficial do Portal de Periódicos da CAPES com integração da IA</em></p>
</div>

- **Government Header**: Standard gov.br bar
- **CAPES Logo**: Official visual identity
- **Institutional Colors**: Blue (#1c1c5c) and orange (#f16421)
- **Responsive Layout**: Works on desktop and mobile
- **AI Chat Modal**: Integrated AI interface

## 🔍 Usage Examples

### General Questions
```
"Quais artigos falam sobre machine learning?"
"Mostre artigos sobre inteligência artificial na educação"
"Quais são as tendências em IA?"
```

### Specific Questions
```
"No artigo 'Inteligência Artificial na Educação', quais são as principais conclusões?"
"Quais metodologias são mencionadas no artigo sobre machine learning?"
```

## 🔄 Data Flow

### 1. **User Query**
```
User → React Frontend → Flask API
```

### 2. **Orchestration**
```
API → Orchestrator → Search Type (General/Specific)
```

### 3. **Document Search**
```
Orchestrator → ChromaDB → Relevant Results
```

### 4. **Response Generation**
```
Results → DialoGPT → Contextualized Response
```

### 5. **Return**
```
Response → API → Frontend → User
```

## 🐛 Troubleshooting

### Backend Connection Error
- Check if Flask is running on port 5000
- Confirm CORS is enabled

### ChromaDB Error
- Check if the `chroma_db` directory exists
- Run the ingestion script again

### AI Model Error
- Check if dependencies are installed
- Confirm there's enough disk space

## 📝 License

This project is an educational prototype based on the CAPES Periodicals Portal.

## 🤝 Contribution

1. Fork the project
2. Create a branch for your feature
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

**Developed with ❤️ for the Brazilian academic community** 
