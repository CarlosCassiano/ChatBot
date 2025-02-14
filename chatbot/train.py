from config import get_chatbot, train_chatbot

if __name__ == '__main__':
    chatbot = get_chatbot()
    train_chatbot(chatbot)
    print("Chatbot treinado com sucesso!")
