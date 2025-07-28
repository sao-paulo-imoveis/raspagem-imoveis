from itemadapter import ItemAdapter
import re
from rapidfuzz import process, fuzz
from llm.ollama_client import extrair_condominio_ollama
from real_estate.transform.processar_dados import mapear_para_essenciais_fuzzy, parse_valor_periodo_fuzzy, extrair_padrao_condominio_fuzzy

class CleanRealStatePipeline:
    def process_item(self, item, spider=None):
        
        # 1. Aplica o fuzzy mapping nas características
        essenciais = mapear_para_essenciais_fuzzy(item.get('caracteristicas'))
        for nome, valor in essenciais.items():
            if "caracteristicas_essenciais" not in item:
                item["caracteristicas_essenciais"] = {}
            item["caracteristicas_essenciais"][nome] = valor
        
        # 2. Processa os valores de preço, iptu, condominio, etc.
        preco, _ = parse_valor_periodo_fuzzy(item.get('preco'))
        iptu, iptu_periodo = parse_valor_periodo_fuzzy(item.get('iptu'))
        condominio, condominio_periodo = parse_valor_periodo_fuzzy(item.get('condominio'))

        item['preco'] = int(preco)
        item['iptu'] = int(iptu)
        item['iptu_periodo'] = iptu_periodo
        item['condominio'] = int(condominio)
        item['condominio_periodo'] = condominio_periodo
        
        return item

class LLMCleanRealStatePipeline:
    def process_item(self, item, spider=None):
        # identificar se palavras chaves Condominio ou Predio constam na descrição
        temCondominio = extrair_padrao_condominio_fuzzy(item.get('descricao'))
        if temCondominio:
            # Se sim, extrai o nome do condomínio usando o modelo LLM
            item['condominio_nome'] = extrair_condominio_ollama(item.get('descricao'))
        else:
            item['condominio_nome'] = None
        item['condominio_nome'] = extrair_condominio_ollama(item.get('descricao'))
        return item
