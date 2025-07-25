import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from sentence_transformers import SentenceTransformer
import json
import re

class LocalLLMClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LocalLLMClient, cls).__new__(cls)
            # Usando modelo gratuito e leve
            cls._instance.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
            cls._instance.model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
            
            # Configurar para usar CPU se GPU não estiver disponível
            cls._instance.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            cls._instance.model.to(cls._instance.device)
            
        return cls._instance

    def generate_response(self, prompt, max_new_tokens=150):
        """Gera resposta usando modelo local"""
        try:
            # Configurar tokenizer para evitar warnings
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Codificar com attention mask
            inputs = self.tokenizer(
                prompt, 
                return_tensors="pt", 
                padding=True, 
                truncation=True,
                max_length=512  # Limitar entrada para evitar problemas
            ).to(self.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    input_ids=inputs['input_ids'],
                    attention_mask=inputs['attention_mask'],
                    max_new_tokens=max_new_tokens,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response[len(prompt):].strip()
            
        except Exception as e:
            print(f"Erro na geração: {e}")
            return "Desculpe, não consegui gerar uma resposta adequada."

    def orchestrator(self, query):
        """Determina o tipo de busca baseado na query"""
        # Lógica simples baseada em palavras-chave
        query_lower = query.lower()
        
        # Palavras que indicam busca específica
        specific_indicators = ["no artigo", "do artigo", "no documento", "do documento", "no texto", "do texto"]
        
        for indicator in specific_indicators:
            if indicator in query_lower:
                # Extrair nome do documento
                match = re.search(r'["\']([^"\']+)["\']', query)
                if match:
                    return f"agent_specific_search: {match.group(1)}"
                else:
                    # Tentar extrair após "no artigo" ou similar
                    for indicator in specific_indicators:
                        if indicator in query_lower:
                            parts = query_lower.split(indicator)
                            if len(parts) > 1:
                                filename = parts[1].strip().split()[0]
                                return f"agent_specific_search: {filename}"
        
        return "agent_general_search"

    def generate_keywords(self, query):
        """Extrai palavras-chave da query"""
        # Lógica simples de extração de palavras-chave
        stop_words = {"quais", "são", "os", "as", "um", "uma", "sobre", "de", "da", "do", "em", "com", "para", "por", "que", "qual", "como", "quando", "onde", "quem"}
        
        words = query.lower().split()
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        return " ".join(keywords[:5])  # Retorna até 5 palavras-chave

    def generate_answer(self, retrieved_docs, query):
        """Gera resposta baseada nos documentos recuperados"""
        if not retrieved_docs:
            return json.dumps({"Erro": "Nenhum documento encontrado"})
        
        # Construir contexto (limitando tamanho para evitar problemas)
        context_parts = []
        for doc_name, content in retrieved_docs.items():
            # Limitar conteúdo de cada documento
            limited_content = content[:300] + "..." if len(content) > 300 else content
            context_parts.append(f"{doc_name}: {limited_content}")
        
        context = "\n\n".join(context_parts)
        
        # Prompt para o modelo local (limitando tamanho total)
        prompt = f"""
        Com base nos seguintes documentos, responda à pergunta do usuário.
        
        Documentos:
        {context}
        
        Pergunta: {query}
        
        Resposta:"""
        
        # Verificar se o prompt não é muito longo
        if len(prompt) > 1000:
            # Se for muito longo, simplificar
            prompt = f"""
            Pergunta: {query}
            
            Documentos encontrados: {', '.join(retrieved_docs.keys())}
            
            Resposta:"""
        
        try:
            # Gerar resposta
            response = self.generate_response(prompt, max_new_tokens=300)
            
            # Verificar se a resposta é válida
            if not response or response == "Desculpe, não consegui gerar uma resposta adequada.":
                # Retornar resposta baseada nos documentos encontrados
                formatted_response = {}
                for doc_name, content in retrieved_docs.items():
                    formatted_response[doc_name] = f"Documento encontrado: {doc_name}. Conteúdo relevante: {content[:200]}..."
                return json.dumps(formatted_response, ensure_ascii=False)
            
            # Formatar como JSON
            formatted_response = {}
            for doc_name in retrieved_docs.keys():
                # Extrair parte da resposta relacionada ao documento
                if doc_name.lower() in response.lower():
                    formatted_response[doc_name] = response
                else:
                    formatted_response[doc_name] = response[:200] + "..."
            
            return json.dumps(formatted_response, ensure_ascii=False)
            
        except Exception as e:
            print(f"Erro na geração de resposta: {e}")
            # Em caso de erro, retornar resposta simples
            error_response = {}
            for doc_name, content in retrieved_docs.items():
                error_response[doc_name] = f"Conteúdo do documento: {content[:300]}..."
            return json.dumps(error_response, ensure_ascii=False) 