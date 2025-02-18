import sys
import os
import json
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, Table
import sqlite3
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)

# Adicionar o diretório 'chatbot' ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar o módulo config
from config import get_chatbot

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Chave secreta para sessões
chatbot = get_chatbot()

# Configurar o mecanismo de banco de dados para o SQLAlchemy
engine = create_engine('sqlite:///c:/Users/user/Desktop/IA/chatbot/database/user.sqlite')
Session = sessionmaker(bind=engine)

def get_user(username):
    conn = sqlite3.connect('c:/Users/user/Desktop/IA/chatbot/database/user.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, password, role FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_users_by_query(query):
    conn = sqlite3.connect('c:/Users/user/Desktop/IA/chatbot/database/user.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, role FROM users WHERE username LIKE ?', (f'%{query}%',))
    users = cursor.fetchall()
    conn.close()
    return users

def create_user(username, password, role):
    conn = sqlite3.connect('c:/Users/user/Desktop/IA/chatbot/database/user.sqlite')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, password, role))
    conn.commit()
    conn.close()

def update_user_role(user_id, new_role):
    conn = sqlite3.connect('c:/Users/user/Desktop/IA/chatbot/database/user.sqlite')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET role = ? WHERE id = ?', (new_role, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = sqlite3.connect('c:/Users/user/Desktop/IA/chatbot/database/user.sqlite')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = get_user(username)
        if user and user[2] == password:
            session['username'] = username
            session['role'] = user[3]
            return jsonify({'success': True, 'redirect': url_for('index')})
        else:
            return jsonify({'success': False, 'message': 'Usuário ou senha inválidos.'})

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))

@app.route("/")
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("index.html", role=session.get('role'))

@app.route("/add")
def add():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('index'))
    return render_template("add_qna.html")

@app.route("/manage")
def manage():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('index'))
    return render_template("manage_qna.html")

@app.route("/manage_users")
def manage_users():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('index'))
    return render_template("manage_users.html")

@app.route("/add_qna", methods=["POST"])
def add_qna():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('index'))

    data = request.get_json()
    question = data['question']
    answer = data['answer']
    
    chatbot.storage.create(text=answer, in_response_to=question)
    
    return "Pergunta e Resposta adicionadas com sucesso!"

@app.route("/search_qna")
def search_qna():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('index'))

    query = request.args.get('query')
    logging.debug(f"Query received: {query}")
    
    session = Session()
    
    # Usar meta dados para acessar a tabela diretamente
    metadata = MetaData()
    statements = Table('statement', metadata, autoload_with=engine)
    
    results = session.query(statements).filter(
        or_(statements.c.text.like(f"%{query}%"), statements.c.in_response_to.like(f"%{query}%"))
    ).all()
    
    logging.debug(f"Results found: {results}")
    
    session.close()
    
    qna_list = []
    for result in results:
        logging.debug(f"Processing result: {result}")
        if result[4] is not None:  # Acessar o campo in_response_to corretamente
            qna_list.append({
                'id': result[7],  # Acessar o campo id corretamente
                'question': result[4],  # Acessar o campo in_response_to corretamente
                'answer': result[0]  # Acessar o campo text corretamente
            })
    
    logging.debug(f"Final QnA list: {qna_list}")
    return jsonify(qna_list)

@app.route("/edit_qna", methods=["POST"])
def edit_qna():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('index'))

    data = request.get_json()
    id = data['id']
    new_question = data['question']
    new_answer = data['answer']
    
    session = Session()
    
    # Usar meta dados para acessar a tabela diretamente
    metadata = MetaData()
    statements = Table('statement', metadata, autoload_with=engine)
    
    # Atualizar a entrada no banco de dados
    stmt = statements.update().where(statements.c.id == id).values(
        text=new_answer,
        in_response_to=new_question
    )
    session.execute(stmt)
    session.commit()
    session.close()
    
    return "Pergunta e Resposta editadas com sucesso!"

@app.route("/delete_qna", methods=["POST"])
def delete_qna():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('index'))

    data = request.get_json()
    id = data['id']
    
    session = Session()
    
    # Usar meta dados para acessar a tabela diretamente
    metadata = MetaData()
    statements = Table('statement', metadata, autoload_with=engine)
    
    # Deletar a entrada do banco de dados
    stmt = statements.delete().where(statements.c.id == id)
    session.execute(stmt)
    session.commit()
    session.close()
    
    return "Pergunta e Resposta excluídas com sucesso!"

@app.route("/add_user", methods=["POST"])
def add_user():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('index'))

    data = request.get_json()
    username = data['username']
    password = data['password']
    role = data['role']
    
    create_user(username, password, role)
    
    return "Usuário adicionado com sucesso!"

@app.route("/search_users")
def search_users():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('index'))

    query = request.args.get('query')
    logging.debug(f"Query received: {query}")
    
    users = get_users_by_query(query)
    logging.debug(f"Results found: {users}")
    
    user_list = []
    for user in users:
        user_list.append({
            'id': user[0],
            'username': user[1],
            'role': user[2]
        })
    
    logging.debug(f"Final user list: {user_list}")
    return jsonify(user_list)

@app.route("/edit_user", methods=["POST"])
def edit_user():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('index'))

    data = request.get_json()
    id = data['id']
    new_role = data['role']
    
    update_user_role(id, new_role)
    
    return "Permissão do usuário editada com sucesso!"

@app.route("/delete_user", methods=["POST"])
def delete_user():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('index'))

    data = request.get_json()
    id = data['id']
    
    delete_user(id)
    
    return "Usuário excluído com sucesso!"

@app.route("/get")
def get_bot_response():
    if 'username' not in session:
        return redirect(url_for('login'))

    userText = request.args.get('msg')
    resposta = chatbot.get_response(userText)
    return f"<pre>{str(resposta)}</pre>"

if __name__ == "__main__":
    app.run(debug=True)
