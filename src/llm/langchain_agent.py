from langchain_community.llms import Ollama
from langchain.agents import initialize_agent, Tool, AgentType
from llm.ollama_client import extrair_condominio_ollama

# Cria uma instância do LLM (Ollama)
llm = Ollama(model="llama3")  # Usar o modelo disponível no Ollama

# DICA: EM PRODUÇÃO
# -------------- Se estiver usando OpenAI, substitua por:
# from langchain_openai import ChatOpenAI
# llm = ChatOpenAI(
#     api_key="SUA_CHAVE_OPENAI",
#     model="gpt-4o"   # ou "gpt-3.5-turbo", etc.
# )
# -------------- Se estiver usando Bedrock, substitua por:
# from langchain_aws import BedrockLLM
# llm = BedrockLLM(
#     model="anthropic.claude-v2",
#     aws_access_key_id="...",
#     aws_secret_access_key="...",
#     region_name="us-east-1"
# )

# Exemplo de ferramenta customizada para o agente usar
def resumir_simples(text):
    "Resumo simples para exemplo."
    return text[:100] + "..."

# Define funções ("tools") que o agente pode usar
tools = [
    Tool(
        name="Método exemplo de resumo",
        func=resumir_simples,   # sua função Python
        description="Resumir um texto de forma simples, retornando os primeiros 100 caracteres."
    ),
    Tool(
        name="Extrair condomínio do texto",
        func=extrair_condominio_ollama,
        description="Extrai o nome do condomínio de uma descrição de imóvel. Retorna 'NÃO ENCONTRADO' se não houver nome."
    )
    # ,
    # Tool(
    #     name="Busca no Banco de Imóveis",
    #     func=buscar_imoveis_no_bd,   # sua função Python
    #     description="Busca imóveis por filtros variados"
    # ),
]

# Inicializa o agente LangChain
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

def run_agent(prompt):
    """
    Executa o agente com um prompt.
    """
    return agent.run(prompt)

# Exemplo de uso
if __name__ == "__main__":
    resultado = run_agent("Resuma o seguinte texto: Python é uma linguagem de programação...")
    print(resultado)
    

#   SOBRE O LANGCHAIN: Como o LangChain “descobre” qual tool usar?
#       O “pulo do gato” do AgentType.ZERO_SHOT_REACT_DESCRIPTION
#           Quando você usa o agente do tipo ZERO_SHOT_REACT_DESCRIPTION, o LLM recebe o prompt do usuário + a descrição das tools disponíveis.
#           O modelo então lê seu prompt (“Resuma: ...”, “Classifique: ...”) e, baseado na descrição de cada tool, decide sozinho qual ferramenta acionar — é uma inferência, não um mapeamento literal de texto para função.
#           Por isso, o texto do seu prompt não precisa ser igual ao nome da tool, mas quanto mais claro e próximo do “intuito” da ferramenta, melhor o resultado.
#       Como acontece “por dentro”?
#           O LangChain monta um prompt gigante assim:
#               Você tem as seguintes ferramentas:
#               1. CustomSummarizer: Resumir descrições de imóveis.
#               2. TextClassifier: Classificar tipos de anúncio.
#               Quando receber uma pergunta ou instrução, use a ferramenta apropriada para responder.
#               Usuário: Classifique: Apartamento com 3 dormitórios...
#           O LLM lê o prompt, entende (com base na descrição das ferramentas) que a instrução “Classifique” pede a tool “TextClassifier”.
#           O próprio modelo decide, usando linguagem natural, qual função acionar.
#           Ele faz isso com base em semântica, contexto e matching de intenção (e não por palavra-chave exata).