from config import get_chatbot

chatbot = get_chatbot()

def main():
    print("Bem-vindo ao Chatbot da Empresa! (Digite 'sair' para encerrar)")
    while True:
        pergunta = input("Você: ")
        if pergunta.lower() == 'sair':
            break
        resposta = chatbot.get_response(pergunta)
        print("Chatbot:", resposta)

if __name__ == '__main__':
    main()
