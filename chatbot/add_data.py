from config import get_chatbot

chatbot = get_chatbot()

# Dados de treinamento
custom_training_data = [
    ("Bom dia", "Bom dia! Como posso ajudar você hoje?"),
    ("Como faço para cadastrar um cliente?", "Para cadastrar um cliente, acesse o sistema de cadastro e preencha todas as informações necessárias."),
    ("Preciso gerar um boleto", "Para gerar um boleto, vá até a seção de finanças e clique em 'Gerar Boleto'."),
    ("Qual é o horário de funcionamento?", "Nosso horário de funcionamento é das 9h às 18h, de segunda a sexta-feira."),
    ("Qual é o número de telefone do suporte?", "Você pode entrar em contato com o suporte pelo número (XX) XXXX-XXXX."),
    ("Como faço para acessar o portal do cliente?", "Para acessar o portal do cliente, clique em 'Portal do Cliente' no site e faça login com suas credenciais."),
    ("Quais são os produtos disponíveis?", "Você pode ver a lista completa de produtos disponíveis no nosso catálogo online."),
    ("Posso obter um desconto na minha compra?", "Você pode verificar as promoções e descontos disponíveis na seção de ofertas do nosso site."),
]

# Adiciona ao banco de dados do ChatterBot
for pergunta, resposta in custom_training_data:
    chatbot.storage.create(text=pergunta, in_response_to=None)
    chatbot.storage.create(text=resposta, in_response_to=pergunta)

print("Dados adicionados com sucesso!")
