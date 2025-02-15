from config import get_chatbot

chatbot = get_chatbot()

import re

def detectar_intencao(pergunta):
    pergunta = pergunta.lower()
    if re.search(r'\bcadastrar\b.*\bcliente\b', pergunta):
        return "Como faço para cadastrar um cliente?"
    if re.search(r'\bgerar\b.*\bboleto\b', pergunta):
        return "Preciso gerar um boleto"
    if re.search(r'\bhorário\b.*\bfuncionamento\b', pergunta):
        return "Qual é o horário de funcionamento?"
    # Adicione mais padrões conforme necessário
    return None

def main():
    print("Bem-vindo ao Chatbot da Empresa! (Digite 'sair' para encerrar)")
    while True:
        pergunta = input("Você: ")
        if pergunta.lower() == 'sair':
            break
        intencao = detectar_intencao(pergunta)
        if intencao:
            resposta = chatbot.get_response(intencao)
        else:
            resposta = chatbot.get_response(pergunta)
        print("Chatbot:", resposta)

if __name__ == '__main__':
    main()
