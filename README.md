# 🏘️ crawler-real-estate-template

Template estruturado para scraping de imóveis com foco em extração limpa, anização modular e pronto para uso em Data Science, integração com LLMs e ortação em CSV/Parquet.

---

## 🚀 Objetivo

Este repositório serve como **modelo base** para projetos de scraping do cado imobiliário. A estrutura foi pensada para:

- Separar a coleta (`scrapy` + `playwright`) da transformação dos dados.
- Exportar dados diretamente para análises.
- Enriquecer os resultados com técnicas de **fuzzy matching** e **modelos **.

---

## ⚙️ Requisitos

### 📦 Dependências (requirements.txt)

```txt
# WebScraping
scrapy
playwright
scrapy-playwright

# Data Science + Utils
pandas
rapidfuzz
requests
streamlit
pyarrow

# LLM
llama-index
llama-index-llms-ollama
langchain
langchain-community
```

---

## 📥 Instalação

> Recomendado: ambiente virtual (venv ou conda)

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/crawler-real-estate-template.git
cd crawler-real-estate-template

# Instale as dependências
pip install -r requirements.txt

# Instale o Playwright
playwright install
```

---

## ▶️ Execução

O pipeline completo é iniciado via `main.py`, que:

1. Executa o spider Scrapy com Playwright.
2. Processa e organiza os dados coletados.
3. Salva arquivos CSV e Parquet em pastas nomeadas por data/hora.

```bash
python main.py
```

Exemplo de saída no terminal:

```
Iniciando o pipeline de scraping para EvidenceImoveis - 2025_07_28 14_03_10
Pipeline finalizado!
```

---

## 📂 Onde os dados são salvos?

Ao rodar o `main.py`, a seguinte estrutura será criada automaticamente:

```
/data/YYYY_MM_DD/
├── raw/
│   └── HH_MM_SS/
│       └── EvidenceImoveis.json
├── processed/
│   ├── imovel.csv
│   ├── endereco.csv
│   ├── caracteristicas.csv
│   ├── imovel.parquet
│   └── ...
```

![Exemplo de Extração](https://raw.githubusercontent.com/PardoMarques/crawler-real-estate-template/refs/heads/main/extracao.png)

---

## 🧠 Integração com LLM

O pipeline `LLMCleanRealStatePipeline` detecta nomes de condomínios em crições usando LLMs locais (via Ollama).

⚙️ Verifique o funcionamento do Ollama e o modelo LLM instalado no script:

```python
from llm.ollama_client import extrair_condominio_ollama
```

---

## 📌 Exemplo de Spider

A pasta `spiders/` contém exemplos reais, como o `EvidenceImoveis.py` ou o `VisaoGlobalImoveis.py`, que cadastram imóveis em São Paulo com critérios definidos.  
A estrutura pode ser adaptada para qualquer outro portal, MAS seguindo majoritariamente a classe definida em Items, para que toda integração de análise dos dados possam futuramente obter sucesso.

---

## CONTRIBUIÇÃO:

## Pull Requests serão bem-vindos!

## MAS neste momento ainda estou organizando a base principal

---

## 🧭 Roadmap Futuro (próximas versões)

- [ ] Dashboard com Streamlit
- [ ] Arquitetura LLM -> Boas Práticas + Prompt Engineering
- [ ] Disponibilizar curso gratuíto para utilização do template

---

## 📄 Licença

MIT License.

---

## 👨‍💻 Autor

Projeto iniciado por [Caio Marques](https://github.com/pardomarques), com o intuito de promover scraping ético e padronizado no mercado imobiliário brasileiro.
