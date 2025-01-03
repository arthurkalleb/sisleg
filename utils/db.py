import sqlite3

def init_db():
    """
    Inicializa o banco de dados e cria as tabelas de usuários e vereadores, se elas não existirem.
    Insere usuários de teste apenas se a tabela estiver vazia.
    """
    conn = sqlite3.connect('votacao.db')
    c = conn.cursor()
    
    # Criar a tabela de usuários, se não existir
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, role TEXT)''')
    
    # Criar a tabela de vereadores, se não existir
    c.execute('''CREATE TABLE IF NOT EXISTS vereadores
                 (id INTEGER PRIMARY KEY, nome TEXT UNIQUE, classificacao TEXT, senha TEXT, foto TEXT)''')
    
    # Verificar se a tabela de usuários já contém dados
    c.execute("SELECT COUNT(*) FROM usuarios")
    count = c.fetchone()[0]
    
    # Inserir usuários de teste apenas se a tabela estiver vazia
    if count == 0:
        usuarios_teste = [
            ("vereador1", "123", "Vereador"),
            ("presidente1", "123", "Presidente"),
            ("admin1", "123", "Administrador"),
        ]
        c.executemany("INSERT INTO usuarios (username, password, role) VALUES (?, ?, ?)", usuarios_teste)
        print("Usuários de teste inseridos.")
    else:
        print("Usuários de teste já existem. Nenhum dado foi inserido.")
    
    conn.commit()
    conn.close()

def verify_login(username, password, role):
    """
    Verifica se o usuário existe no banco de dados com o nome de usuário, senha e categoria fornecidos.
    Retorna os dados do usuário se encontrado, ou None caso contrário.
    """
    conn = sqlite3.connect('votacao.db')
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios WHERE username = ? AND password = ? AND role = ?", (username, password, role))
    user = c.fetchone()
    conn.close()
    if user:
        return {"id": user[0], "username": user[1], "role": user[3]}
    return None

def get_roles():
    """
    Retorna uma lista de categorias (roles) disponíveis no banco de dados.
    """
    conn = sqlite3.connect('votacao.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT role FROM usuarios")
    roles = [row[0] for row in c.fetchall()]
    conn.close()
    return roles

def add_vereador(nome, classificacao, senha, foto=None):
    """
    Adiciona um novo vereador ao banco de dados e cria as credenciais de acesso.
    """
    conn = sqlite3.connect('votacao.db')
    c = conn.cursor()

    # Adiciona o vereador à tabela `vereadores`
    c.execute("INSERT INTO vereadores (nome, classificacao, senha, foto) VALUES (?, ?, ?, ?)", (nome, classificacao, senha, foto))

    # Adiciona as credenciais de acesso à tabela `usuarios`
    c.execute("INSERT INTO usuarios (username, password, role) VALUES (?, ?, ?)", (nome, senha, classificacao))

    conn.commit()
    conn.close()

def get_vereadores():
    """
    Retorna uma lista de vereadores.
    """
    conn = sqlite3.connect('votacao.db')
    c = conn.cursor()
    c.execute("SELECT * FROM vereadores")
    vereadores = [{"id": row[0], "nome": row[1], "classificacao": row[2], "senha": row[3], "foto": row[4]} for row in c.fetchall()]
    conn.close()
    return vereadores

def get_vereadores_com_status():
    """
    Retorna uma lista de vereadores com o status de login.
    """
    conn = sqlite3.connect('votacao.db')
    c = conn.cursor()

    # Obtém os vereadores e verifica se estão logados
    c.execute('''
        SELECT v.id, v.nome, v.foto, u.username IS NOT NULL AS logado
        FROM vereadores v
        LEFT JOIN usuarios u ON v.nome = u.username AND u.role = 'Vereador'
    ''')
    vereadores = [
        {
            "id": row[0],
            "nome": row[1],
            "foto": row[2],
            "logado": bool(row[3]),
        }
        for row in c.fetchall()
    ]

    conn.close()
    return vereadores

def update_vereador(id, nome, classificacao, senha, foto=None):
    """
    Atualiza os dados de um vereador no banco de dados e suas credenciais de acesso.
    """
    conn = sqlite3.connect('votacao.db')
    c = conn.cursor()

    # Atualiza o vereador na tabela `vereadores`
    c.execute("UPDATE vereadores SET nome = ?, classificacao = ?, senha = ?, foto = ? WHERE id = ?", (nome, classificacao, senha, foto, id))

    # Atualiza as credenciais de acesso na tabela `usuarios`
    c.execute("UPDATE usuarios SET username = ?, password = ?, role = ? WHERE username = (SELECT nome FROM vereadores WHERE id = ?)", (nome, senha, classificacao, id))

    conn.commit()
    conn.close()

def remove_vereador(id):
    """
    Remove um vereador do banco de dados e suas credenciais de acesso.
    """
    conn = sqlite3.connect('votacao.db')
    c = conn.cursor()

    # Obtém o nome do vereador antes de removê-lo
    c.execute("SELECT nome FROM vereadores WHERE id = ?", (id,))
    nome = c.fetchone()[0]

    # Remove o vereador da tabela `vereadores`
    c.execute("DELETE FROM vereadores WHERE id = ?", (id,))

    # Remove as credenciais de acesso da tabela `usuarios`
    c.execute("DELETE FROM usuarios WHERE username = ?", (nome,))

    conn.commit()
    conn.close()