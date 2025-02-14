from chatterbot import ChatBot

def get_chatbot():
    chatbot = ChatBot(
        'EmpresaBot',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri='sqlite:///c:/Users/user/Desktop/IA/chatbot/database/chatbot.sqlite',
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': 'Desculpe, não entendi.',
                'maximum_similarity_threshold': 0.90  # Ajustar o threshold para um valor mais permissivo
            }
        ],
        preprocessors=[
            'chatterbot.preprocessors.clean_whitespace'
        ],
        read_only=True  # Desativar a aprendizagem em tempo real
    )
    return chatbot
