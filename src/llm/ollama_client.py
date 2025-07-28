import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def ask_ollama(prompt, model=MODEL, stream=False):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": stream  # Se quiser resposta em streaming [ humanização da escrita... ]
    }
    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    
    # Ollama pode retornar a resposta completa em 'response' ou 'message'
    data = response.json()
    return data.get('response') or data.get('message')

def extrair_condominio_ollama(texto_descricao, modelo="llama3"):
    prompt = f"""
    No texto a seguir, identifique e retorne APENAS o nome do condomínio, se houver.
    - Não escreva frases.
    - Não explique.
    - Não adicione pontuação extra.
    - NÃO coloque nada além do nome, uma única palavra ou expressão.
    - Se não encontrar, retorne apenas: NAO_ENCONTRADO

    Exemplo:
    Texto: 'Apartamento no condomínio Helbor Vivere, com lazer completo.'
    Resposta: Helbor Vivere

    Texto: 'Apartamento com lazer completo, próximo ao metrô.'
    Resposta: NAO_ENCONTRADO

    Texto: '''{texto_descricao}'''
    """
    resultado = ask_ollama(prompt, model=modelo)
    if "NÃO ENCONTRADO" in resultado.upper():
        return None
    return resultado