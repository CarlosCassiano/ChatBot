import sys
import os
from flask import Flask, render_template, request

# Adicionar o diretório pai ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import get_chatbot

app = Flask(__name__)
chatbot = get_chatbot()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    resposta = chatbot.get_response(userText)
    return str(resposta)

if __name__ == "__main__":
    app.run()
