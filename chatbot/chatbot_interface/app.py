import sys
import os
from flask import Flask, render_template, request

# Adicionar o diretório 'chatbot' ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar o módulo config
from config import get_chatbot

app = Flask(__name__)
chatbot = get_chatbot()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add")
def add():
    return render_template("add_qna.html")

@app.route("/add_qna", methods=["POST"])
def add_qna():
    data = request.get_json()
    question = data['question']
    answer = data['answer']
    
    chatbot.storage.create(text=question, in_response_to=None)
    chatbot.storage.create(text=answer, in_response_to=question)
    
    return "Pergunta e Resposta adicionadas com sucesso!"

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    resposta = chatbot.get_response(userText)
    return f"<pre>{str(resposta)}</pre>"  # Usar a tag <pre> para preservar a formatação

if __name__ == "__main__":
    app.run()
