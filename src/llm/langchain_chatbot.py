from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_community.llms import Ollama

class ConsultorChatbot:
    def __init__(self, model="llama3"):
        self.llm = Ollama(model=model)
        self.memory = ConversationBufferMemory(k=10) # k=10 limita o histórico a 10 mensagens
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory
        )
        # O self.memory armazena o histórico da conversa,
        # permitindo que o chatbot mantenha contexto entre as mensagens.
        # O uso do ConversationBufferMemory padroniza o amazenamento de mensagens.

    def chat(self, message):
        """
        Envia uma mensagem ao chatbot e recebe a resposta.
        """
        resposta = self.conversation.predict(input=message)
        # O método predict executa a conversa com o LLM,
        # passando a mensagem do usuário e retornando a resposta gerada.
        # E todo o dialogo é armazenado na memória.
        # Isso permite que o chatbot lembre-se do contexto da conversa.
        return resposta

if __name__ == "__main__":
    bot = ConsultorChatbot()
    while True:
        user = input("Você: ")
        if user.lower() in {"sair", "exit", "quit"}:
            break
        resposta = bot.chat(user)
        print("Bot:", resposta)


# DICA: EM PRODUÇÃO
# from langchain_aws import BedrockLLM
# from langchain.memory import ConversationBufferMemory
# from langchain.chains import ConversationChain

# class SimpleChatbot:
#     def __init__(self, aws_access_key_id, aws_secret_access_key, region_name="us-east-1", model="anthropic.claude-v2"):
#         self.llm = BedrockLLM(
#             model=model,
#             aws_access_key_id=aws_access_key_id,
#             aws_secret_access_key=aws_secret_access_key,
#             region_name=region_name
#         )
#         self.memory = ConversationBufferMemory()
#         self.conversation = ConversationChain(
#             llm=self.llm,
#             memory=self.memory
#         )

#     def chat(self, message):
#         resposta = self.conversation.predict(input=message)
#         return resposta

# if __name__ == "__main__":
#     bot = SimpleChatbot(
#         aws_access_key_id="SUA_KEY_ID",
#         aws_secret_access_key="SUA_SECRET",
#         region_name="us-east-1"
#     ) ...