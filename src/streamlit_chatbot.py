import streamlit as st
from llm.langchain_agent import run_agent
from llm.langchain_chatbot import ConsultorChatbot

st.title("Chatbot de Imóveis - Streamlit")

# Opção de modo
modo = st.selectbox("Escolha o modo do bot:", ["Agente LangChain (com tools)", "Chat com Memória Simples"])

if "historico" not in st.session_state:
    st.session_state["historico"] = []

# Instancia chatbot de memória (só 1 vez)
if "consultor_bot" not in st.session_state:
    st.session_state["consultor_bot"] = ConsultorChatbot(model="llama3")

user_input = st.text_input("Digite sua pergunta:")

if st.button("Enviar") and user_input:
    if modo == "Agente LangChain (com tools)":
        resposta = run_agent(user_input)
    else:
        resposta = st.session_state["consultor_bot"].chat(user_input)
    
    st.session_state["historico"].append(("Você", user_input))
    st.session_state["historico"].append(("Bot", resposta))
    st.experimental_rerun()  # Para mostrar o chat atualizado imediatamente

# Exibe o histórico em ordem
for autor, msg in st.session_state["historico"]:
    st.markdown(f"**{autor}:** {msg}")

# Limpar histórico
if st.button("Limpar conversa"):
    st.session_state["historico"] = []
    st.experimental_rerun()
