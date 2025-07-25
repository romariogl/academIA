import sys
import os

# Adiciona o diretório raiz do projeto ao PATH
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from rag_backend.models.chroma_vector_store import ChromaVectorStore
from bs4 import BeautifulSoup
import requests
from langchain_community.document_loaders import WebBaseLoader
from sentence_transformers import SentenceTransformer 

# Configurações do ChromaDB
vector_store = ChromaVectorStore()

# Função para indexar um chunk no ChromaDB
def index_chunk(index_name, chunk, article_name, article_id, url):
    body = {
        "article_name": article_name,
        "content": chunk,
        "article_fulldoc_url": url,
        "article_id": article_id
    }
    vector_store.index(index_name=index_name, id=article_id, body=body)

# Função para extrair o título do artigo da tag meta
def extract_article_title_text_and_fulldocurl(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Erro ao acessar a URL: {url}")    
    soup = BeautifulSoup(response.text, "html.parser")
    
    meta_tag = soup.find("meta", attrs={"name": "title"})
    if not meta_tag or not meta_tag.get("content"):
        raise ValueError("Não foi possível encontrar a meta tag com o título do artigo.")    
    title = meta_tag.get("content")
    print(f"Título: {title}")

    meta_tag = soup.find("meta", attrs={"name": "description"})
    if not meta_tag or not meta_tag.get("content"):
        raise ValueError("Não foi possível encontrar a meta tag com a descrição do artigo.")    
    description = meta_tag.get("content")
    print(f"Descrição: {description}")

    button = soup.find("a", id="item-acessar")
    if button and button.has_attr("href"):
        href = button["href"]
        print(f"Link 'Acessar' encontrado: {href}")
    else:
        print("Botão/link 'Acessar' não encontrado.")
        href = url  # Fallback para a URL original

    return title, description, href

# Carrega os dados do website e processa os chunks
def fetch_and_process_website_summary(url):
    # 1. Extrair o título do artigo
    article_title, description, fulldoc_url = extract_article_title_text_and_fulldocurl(url)
    print(f"Título do artigo extraído: {article_title}")

    # 2. Dividir o conteúdo em chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    document = Document(page_content=description, metadata={"title": article_title, "article_fulldoc_url": fulldoc_url})
    chunks = text_splitter.split_documents([document])
    print(f"Dividiu os documentos em {len(chunks)} chunks.")

    # 3. Ingerir os chunks no ChromaDB
    for i, chunk in enumerate(chunks):
        chunk_id = f"{article_title}_summary_chunk_{i}"
        index_chunk(index_name="summary_index", chunk=chunk.page_content, article_id=chunk_id, article_name=article_title, url=fulldoc_url)
        print(f"Indexou chunk de resumo com ID: {chunk_id}")

    # 4. Processar documento completo
    fetch_and_process_website_full(url=fulldoc_url, article_title=article_title)    

# Carrega os dados do website e processa os chunks
def fetch_and_process_website_full(url, article_title):
    try:
        loader = WebBaseLoader(url)
        documents = loader.load()
        
        # Dividir o conteúdo em chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = text_splitter.split_documents(documents)
        print(f"Dividiu os documentos completos em {len(chunks)} chunks.")

        # Ingerir os chunks no ChromaDB
        for i, chunk in enumerate(chunks):
            chunk_id = f"{article_title}_full_chunk_{i}"
            index_chunk(index_name="full_document_index", chunk=chunk.page_content, article_id=chunk_id, article_name=article_title, url=url)
            print(f"Indexou chunk completo com ID: {chunk_id}")

        print(f"Todos os chunks foram ingeridos no ChromaDB.")
        
    except Exception as e:
        print(f"Erro ao processar documento completo: {e}")

def extract_website_urls():
    capes_ia_search_url = "https://www.periodicos.capes.gov.br/index.php/acervo/buscador.html?q=intelig%C3%AAncia+artificial&source=&publishyear_min%5B%5D=1943&publishyear_max%5B%5D=2025&page="
    capes_ia_articles_urls = []
    
    # Limitar a 2 páginas para teste (pode ser aumentado)
    for i in range(2):
        try:
            response = requests.get(capes_ia_search_url + str(i))
            if response.status_code != 200:
                print(f"Erro ao acessar página {i}")
                continue
                
            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all('a', class_='titulo-busca')

            for link in links:
                url = "https://www.periodicos.capes.gov.br" + link.get('href')
                capes_ia_articles_urls.append(url)
                
        except Exception as e:
            print(f"Erro ao processar página {i}: {e}")
    
    return capes_ia_articles_urls

# Função para carregar dados de exemplo (para teste sem internet)
def load_sample_data():
    """Carrega dados de exemplo para teste"""
    sample_docs = [
        {
            "title": "Inteligência Artificial na Educação",
            "content": "A inteligência artificial está revolucionando a educação através de sistemas adaptativos e personalização do aprendizado. Os algoritmos de machine learning permitem identificar padrões de aprendizado individuais e adaptar o conteúdo educacional de acordo com as necessidades específicas de cada aluno.",
            "url": "https://exemplo.com/ia-educacao"
        },
        {
            "title": "Machine Learning em Medicina",
            "content": "O machine learning tem aplicações importantes na medicina, incluindo diagnóstico precoce e análise de imagens médicas. Algoritmos de deep learning são capazes de detectar anomalias em radiografias e tomografias com precisão superior à humana em muitos casos.",
            "url": "https://exemplo.com/ml-medicina"
        },
        {
            "title": "Chatbots e Processamento de Linguagem Natural",
            "content": "Chatbots modernos utilizam técnicas avançadas de processamento de linguagem natural para melhorar a interação com usuários. Modelos como GPT e BERT revolucionaram a capacidade de compreensão e geração de texto natural.",
            "url": "https://exemplo.com/chatbots-nlp"
        },
        {
            "title": "Ética em Inteligência Artificial",
            "content": "A ética em inteligência artificial é fundamental para garantir que os sistemas de IA sejam desenvolvidos e utilizados de forma responsável. Questões como viés algorítmico, privacidade e transparência são cruciais para o futuro da tecnologia.",
            "url": "https://exemplo.com/etica-ia"
        },
        {
            "title": "Redes Neurais e Deep Learning",
            "content": "Redes neurais profundas são a base do deep learning moderno. Essas arquiteturas complexas permitem que máquinas aprendam representações hierárquicas de dados, desde características simples até conceitos abstratos complexos.",
            "url": "https://exemplo.com/redes-neurais"
        }
    ]
    
    for i, doc in enumerate(sample_docs):
        # Indexar resumo
        chunk_id = f"{doc['title']}_sample_summary_{i}"
        index_chunk(
            index_name="summary_index", 
            chunk=doc['content'], 
            article_id=chunk_id, 
            article_name=doc['title'], 
            url=doc['url']
        )
        
        # Indexar documento completo (simular documento mais longo)
        chunk_id = f"{doc['title']}_sample_full_{i}"
        index_chunk(
            index_name="full_document_index", 
            chunk=doc['content'] * 3,  # Simular documento mais longo
            article_id=chunk_id, 
            article_name=doc['title'], 
            url=doc['url']
        )
    
    print("Dados de exemplo carregados com sucesso no ChromaDB!")

# Executa o processamento e ingestão
if __name__ == "__main__":
    print("🚀 Iniciando ingestão de dados no ChromaDB...")
    
    # Opção 1: Carregar dados de exemplo (para teste rápido)
    load_sample_data()
    
    # Opção 2: Extrair dados reais do CAPES (descomente se quiser usar)
    # website_urls = extract_website_urls()
    # print(f"Encontradas {len(website_urls)} URLs")
    # 
    # for url in website_urls:
    #     try:
    #         fetch_and_process_website_summary(url)
    #     except Exception as e:
    #         print(f"Erro ao processar {url}: {e}")
    
    print("✅ Ingestão concluída no ChromaDB!")