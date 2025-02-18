import sqlite3

# Conectar ao banco de dados (ou criar se não existir)
conn = sqlite3.connect('c:/Users/user/Desktop/IA/chatbot/database/user.sqlite')

# Criar um cursor
cursor = conn.cursor()

# Criar a tabela de usuários
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
''')

# Adicionar alguns usuários iniciais
cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', ('admin', 'adminpass', 'admin'))
cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', ('user', 'userpass', 'user'))

# Salvar (commit) as alterações
conn.commit()

# Fechar a conexão
conn.close()
