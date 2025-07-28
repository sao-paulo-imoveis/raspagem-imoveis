import json
import os
import pandas as pd
import re
from rapidfuzz import process, fuzz
import requests

ESSENCIAIS = [
    "academia", "piscina", "portaria 24h", "quadra poliesportiva", "churrasqueira",
    "salao de festas", "salao de jogos", "varanda gourmet", "elevador",
    "permite animais", "area de lazer", "mobiliado"
]

PERIODOS_ALVO = {
        "mensal": ["mensal", "mês", "mesal", "ao mês", "mensais", "por mês", "mes"],
        "anual": ["anual", "ano", "por ano", "anualmente", "ano."],
    }

PALAVRAS_CHAVE = ["condomínio", "condominio", "edifício", "edificio", "residencial", "empreendimento", "prédio", "predio"]

def mapear_para_essenciais_fuzzy(caracs, essenciais=ESSENCIAIS, threshold=80):
    resultado = {essencial: False for essencial in essenciais}
    for c in caracs:
        c_l = c.strip().lower()
        match, score, _ = process.extractOne(c_l, essenciais, scorer=fuzz.token_sort_ratio)
        if score >= threshold:
            resultado[match] = True
    return resultado

def parse_valor_periodo_fuzzy(campo):
    if not campo:
        return None, "indefinido"
    valor_match = re.search(r"R\$ ?([\d.,]+)", campo)
    valor = float(valor_match.group(1).replace('.', '').replace(',', '.')) if valor_match else None
    
    campo_lower = campo.lower()
    periodo = "indefinido"  # valor padrão
    for target, variations in PERIODOS_ALVO.items():
        match, score, _ = process.extractOne(campo_lower, variations, scorer=fuzz.partial_ratio)
        if score >= 80:
            periodo = target
            break
    return valor, periodo

# texto = descricao do imóvel
# threshold significa a porcentagem mínima de similaridade para considerar uma correspondência
def extrair_padrao_condominio_fuzzy(texto, threshold=80):
    palavras = texto.split()
    for i, palavra in enumerate(palavras):
        match, score, _ = process.extractOne(palavra.lower(), PALAVRAS_CHAVE, scorer=fuzz.partial_ratio)
        if score >= threshold and i < len(palavras)-1:
            nome = ' '.join(palavras[i:i+4])  # Pega a palavra-chave + possível nome
            return nome
    return None

def coletar_imoveis_processados(json_path):
    with open(json_path, encoding='utf-8') as f:
        imoveis = json.load(f)

    dados_imovel = []
    dados_endereco = []
    dados_caracteristicas = []

    for imovel in imoveis:
        dados_imovel.append({
            'codigo': imovel.get('codigo'),
            'imobiliaria': imovel.get('imobiliaria'),
            'url_detalhes': imovel.get('url_detalhes'),
            'url_img': imovel.get('url_img'),
            'preco': imovel.get('preco'),
            'tipo': imovel.get('tipo'),
            'dormitorios': imovel.get('dormitorios'),
            'metragem': imovel.get('metragem'),
            'vagas': imovel.get('vagas'),
            'data_captura': imovel.get('data_captura'),
            'descricao': imovel.get('descricao'),
            'condominio_nome': imovel.get('condominio_nome'),
            'iptu': imovel.get('iptu'),
            'iptu_periodo': imovel.get('iptu_periodo'),
            'condominio': imovel.get('condominio'),
            'condominio_periodo': imovel.get('condominio_periodo')
        })

        rua, bairro, cidade, estado = None, None, None, None
        endereco = imovel.get('endereco') or ''
        partes = [p.strip() for p in endereco.split(',')]
        if len(partes) >= 3:
            rua = partes[0]
            bairro = partes[1]
            cidade_estado = partes[2]
            if '/' in cidade_estado:
                cidade, estado = cidade_estado.split('/')
            else:
                cidade = cidade_estado
        dados_endereco.append({
            'codigo_imovel': imovel.get('codigo'),
            'rua': rua,
            'bairro': bairro,
            'cidade': cidade,
            'estado': estado
        })

        ess = {}
        for essencial in ESSENCIAIS:
            ess[essencial] = imovel.get(essencial, False)
        ess['codigo_imovel'] = imovel.get('codigo')
        dados_caracteristicas.append(ess)

    return (
        pd.DataFrame(dados_imovel),
        pd.DataFrame(dados_endereco),
        pd.DataFrame(dados_caracteristicas)
    )

def criar_pastas(date_YMD, date_HMS):
    base_path = f"../data/scraping/{date_YMD}"
    os.makedirs(f"{base_path}/raw/{date_HMS}", exist_ok=True)
    os.makedirs(f"{base_path}/processed/{date_HMS}", exist_ok=True)
    return base_path

def salvar_csvs(df_imovel, df_endereco, df_caracteristicas, date_YMD, date_HMS):
    processed_path = f'../data/scraping/{date_YMD}/processed/{date_HMS}'
    os.makedirs(processed_path, exist_ok=True)
    df_imovel.to_csv(f'{processed_path}/imoveis.csv', index=False)
    df_endereco.to_csv(f'{processed_path}/enderecos.csv', index=False)
    df_caracteristicas.to_csv(f'{processed_path}/caracteristicas.csv', index=False)

def salvar_parquets(df_imovel, df_endereco, df_caracteristicas, date_YMD, date_HMS):
    processed_path = f'../data/scraping/{date_YMD}/processed/{date_HMS}'
    os.makedirs(processed_path, exist_ok=True)
    df_imovel.to_parquet(f'{processed_path}/imoveis.parquet', index=False, engine='pyarrow')
    df_endereco.to_parquet(f'{processed_path}/enderecos.parquet', index=False, engine='pyarrow')
    df_caracteristicas.to_parquet(f'{processed_path}/caracteristicas.parquet', index=False, engine='pyarrow')