
# Academ.ia - Portal de Periódicos da CAPES com IA

Sistema de busca inteligente para o Portal de Periódicos da CAPES, integrando IA generativa com busca semântica em documentos acadêmicos.

## 🚀 Funcionalidades

- **Interface Web**: Design baseado no Portal de Periódicos da CAPES
- **Chat com IA**: Assistente virtual para pesquisa acadêmica
- **Busca Semântica**: Utiliza ChromaDB para busca inteligente
- **RAG (Retrieval-Augmented Generation)**: Combina busca de documentos com geração de respostas
- **Modelo Local**: Usa DialoGPT para geração de respostas

## 🏗️ Arquitetura

### 📁 Estrutura de Arquivos
```
academIA/
├── rag_backend/           # Backend Flask + ChromaDB
│   ├── app.py            # API Flask
│   ├── models/           # Modelos de IA e vetores
│   │   ├── chroma_vector_store.py
│   │   └── generate_local.py
│   └── requirements.txt  # Dependências Python
├── rag_frontend/         # Frontend React
│   ├── src/
│   │   ├── App.js        # Interface principal
│   │   └── App.css       # Estilos baseados no CAPES
│   └── package.json      # Dependências Node.js
└── ingestion_module/     # Scripts de ingestão de dados
    └── ingest.py         # Ingestão no ChromaDB
```

### 🔄 Diagrama de Arquitetura
Para uma visualização detalhada da arquitetura do sistema, consulte o [**Diagrama de Arquitetura**](./ARCHITECTURE.md).

**Componentes Principais:**
- **Frontend React**: Interface baseada no Portal de Periódicos da CAPES
- **API Flask**: Backend com orquestração de busca
- **ChromaDB**: Banco de dados vetorial para busca semântica
- **DialoGPT**: Modelo local de IA para geração de respostas
- **Ingestão**: Sistema de processamento e indexação de dados

## 🛠️ Tecnologias

### Backend
- **Flask**: API REST
- **ChromaDB**: Banco de dados vetorial
- **Sentence Transformers**: Embeddings para busca semântica
- **DialoGPT**: Modelo de linguagem local
- **Transformers**: Biblioteca para modelos de IA

### Frontend
- **React**: Interface de usuário
- **Bootstrap**: Framework CSS
- **Font Awesome**: Ícones
- **Axios**: Cliente HTTP

## 📦 Instalação

### 1. Backend

```bash
cd rag_backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 2. Frontend

```bash
cd rag_frontend
npm install
```

## 🚀 Execução

### 1. Iniciar Backend

```bash
cd rag_backend
python app.py
```

O backend estará disponível em: `http://127.0.0.1:5000`

### 2. Iniciar Frontend

```bash
cd rag_frontend
npm start
```

O frontend estará disponível em: `http://localhost:3000`

### 3. Ingerir Dados (Opcional)

```bash
python ingestion_module/ingest.py
```

## 🎯 Como Usar

1. **Acesse a interface**: Abra `http://localhost:3000`
2. **Clique no botão da IA**: "Para uma melhor experiência de busca, utilize a nossa IA!"
3. **Faça perguntas**: 
   - Perguntas gerais: "Quais são os artigos sobre Inteligência Artificial?"
   - Perguntas específicas: "No artigo X, quais são as principais conclusões?"

## 🔧 Configuração

### Variáveis de Ambiente

```bash
# Backend
BACKEND_URL=http://127.0.0.1:5000

# ChromaDB
CHROMA_DB_PATH=./chroma_db
```

### Modelos de IA

O sistema usa:
- **Sentence Transformers**: `all-MiniLM-L6-v2` (para embeddings)
- **DialoGPT**: `microsoft/DialoGPT-medium` (para geração)

## 📊 Funcionalidades da IA

### Tipos de Busca
- **Busca Semântica**: Encontra documentos similares
- **Busca Híbrida**: Combina semântica + léxica
- **Busca Específica**: Foca em um documento específico

### Capacidades
- ✅ Busca em artigos acadêmicos
- ✅ Respostas baseadas em contexto
- ✅ Interface familiar do CAPES
- ✅ Chat interativo
- ✅ Busca por palavras-chave

## 🔄 Fluxo de Dados

### 1. **Consulta do Usuário**
```
Usuário → Frontend React → API Flask
```

### 2. **Orquestração**
```
API → Orchestrator → Tipo de Busca (Geral/Específica)
```

### 3. **Busca de Documentos**
```
Orchestrator → ChromaDB → Resultados Relevantes
```

### 4. **Geração de Resposta**
```
Resultados → DialoGPT → Resposta Contextualizada
```

### 5. **Retorno**
```
Resposta → API → Frontend → Usuário
```

## 🎨 Interface

A interface foi baseada no design oficial do Portal de Periódicos da CAPES, incluindo:

- **Header do Governo**: Barra padrão do gov.br
- **Logo da CAPES**: Identidade visual oficial
- **Cores Institucionais**: Azul (#1c1c5c) e laranja (#f16421)
- **Layout Responsivo**: Funciona em desktop e mobile
- **Chat Modal**: Interface de IA integrada

## 🔍 Exemplos de Uso

### Perguntas Gerais
```
"Quais artigos falam sobre machine learning?"
"Mostre artigos sobre inteligência artificial na educação"
"Quais são as tendências em IA?"
```

### Perguntas Específicas
```
"No artigo 'Inteligência Artificial na Educação', quais são as principais conclusões?"
"Quais metodologias são mencionadas no artigo sobre machine learning?"
```

## 🐛 Solução de Problemas

### Erro de Conexão com Backend
- Verifique se o Flask está rodando na porta 5000
- Confirme se o CORS está habilitado

### Erro de ChromaDB
- Verifique se o diretório `chroma_db` existe
- Execute novamente o script de ingestão

### Erro de Modelo de IA
- Verifique se as dependências estão instaladas
- Confirme se há espaço suficiente em disco

## 📝 Licença

Este projeto é um protótipo educacional baseado no Portal de Periódicos da CAPES.

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

---

**Desenvolvido com ❤️ para a comunidade acadêmica brasileira** 
