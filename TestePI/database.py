import sqlite3
import unicodedata

# Função para conectar ao banco de dados
def conectar_db():
    return sqlite3.connect('jogo_show_do_milhao.db')  # Cria ou abre o arquivo do banco de dados

def remover_acentos(texto):
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
                   
                   
def criar_tabelas():
    # Conectar ao banco de dados
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Criar a tabela de perguntas
    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS perguntas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- ID único para cada pergunta
        pergunta TEXT,  -- Texto da pergunta
        alternativa_1 TEXT,  -- Primeira alternativa
        alternativa_2 TEXT,  -- Segunda alternativa
        alternativa_3 TEXT,  -- Terceira alternativa
        alternativa_4 TEXT,  -- Quarta alternativa
        resposta_correta TEXT,  -- A resposta correta
        nivel TEXT  -- O nível da pergunta (fácil, médio, difícil, expert)
    )
    ''')

    # Criar a tabela de alunos e professores (usando o campo 'tipo' para diferenciar)
    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- ID único para cada aluno
        nome TEXT,  -- Nome do aluno
        email TEXT,  -- Email do aluno (opcional, mas pode ser útil)
        tipo TEXT DEFAULT 'aluno'  -- Tipo de usuário (aluno ou professor)
    )
    ''')

    # Criar a tabela de pontuações
    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS pontuacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- ID único para cada pontuação
        aluno_id INTEGER,  -- Relacionamento com o aluno
        pontos INTEGER,  -- A pontuação do aluno
        FOREIGN KEY (aluno_id) REFERENCES alunos(id)  -- Relacionamento com a tabela de alunos
    )
    ''')

    # Criar a tabela de respostas (rastrear quais respostas foram escolhidas por cada aluno)
    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS respostas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- ID único para cada resposta
        aluno_id INTEGER,  -- Relacionamento com o aluno
        pergunta_id INTEGER,  -- Relacionamento com a pergunta
        resposta_escolhida TEXT,  -- Resposta escolhida pelo aluno
        FOREIGN KEY (aluno_id) REFERENCES alunos(id),  -- Relacionamento com a tabela de alunos
        FOREIGN KEY (pergunta_id) REFERENCES perguntas(id)  -- Relacionamento com a tabela de perguntas
    )
    ''')

    # Confirmar as alterações e fechar a conexão com o banco de dados
    conn.commit()
    conn.close()
    
def adicionar_pergunta():
    pergunta = input("Digite a pergunta: ")
    pergunta = remover_acentos(pergunta)  # Remover acentos da pergunta
    
    alternativa_1 = input("Digite a alternativa A: ")
    alternativa_1 = remover_acentos(alternativa_1)  # Remover acentos da alternativa

    alternativa_2 = input("Digite a alternativa B: ")
    alternativa_2 = remover_acentos(alternativa_2)  # Remover acentos da alternativa

    alternativa_3 = input("Digite a alternativa C: ")
    alternativa_3 = remover_acentos(alternativa_3)  # Remover acentos da alternativa

    alternativa_4 = input("Digite a alternativa D: ")
    alternativa_4 = remover_acentos(alternativa_4)  # Remover acentos da alternativa

    resposta_correta = input("Digite a alternativa correta (A, B, C, D): ")
    
    nivel = input("Digite o nível da pergunta (fácil, médio, difícil): ")
    nivel = remover_acentos(nivel)  # Remover acentos do nível

    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO perguntas (pergunta, alternativa_1, alternativa_2, alternativa_3, alternativa_4, resposta_correta, nivel)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (pergunta, alternativa_1, alternativa_2, alternativa_3, alternativa_4, resposta_correta, nivel))

    conn.commit()
    conn.close()

    print("Pergunta adicionada com sucesso!")


def registrar_aluno(nome, email, tipo='aluno'):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO alunos (nome, email, tipo) 
    VALUES (?, ?, ?)
    ''', (nome, email, tipo))

    conn.commit()
    conn.close()

def registrar_pontuacao(aluno_id, pontos):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO pontuacoes (aluno_id, pontos) 
    VALUES (?, ?)
    ''', (aluno_id, pontos))

    conn.commit()
    conn.close()

def registrar_resposta(aluno_id, pergunta_id, resposta_escolhida):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO respostas (aluno_id, pergunta_id, resposta_escolhida) 
    VALUES (?, ?, ?)
    ''', (aluno_id, pergunta_id, resposta_escolhida))

    conn.commit()
    conn.close()

def obter_perguntas():
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM perguntas')
    perguntas = cursor.fetchall()

    conn.close()
    return perguntas

def obter_ranking():
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT alunos.nome, MAX(pontuacoes.pontos) as pontos
    FROM alunos
    JOIN pontuacoes ON alunos.id = pontuacoes.aluno_id
    GROUP BY alunos.id
    ORDER BY pontos DESC
    ''')
    ranking = cursor.fetchall()

    conn.close()
    return ranking

    
def listar_perguntas():
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, pergunta, nivel FROM perguntas")
    perguntas = cursor.fetchall()

    conn.close()

    if perguntas:
        print("\nPerguntas cadastradas:")
        for pergunta in perguntas:
            print(f"ID: {pergunta[0]} | Pergunta: {pergunta[1]} | Nível: {pergunta[2]}")
    else:
        print("\nNenhuma pergunta cadastrada ainda.")

def editar_pergunta(id_pergunta, nova_pergunta, nova_alt1, nova_alt2, nova_alt3, nova_alt4, nova_resposta, novo_nivel):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE perguntas
        SET pergunta = ?, alternativa_1 = ?, alternativa_2 = ?, alternativa_3 = ?, alternativa_4 = ?, resposta_correta = ?, nivel = ?
        WHERE id = ?
    ''', (nova_pergunta, nova_alt1, nova_alt2, nova_alt3, nova_alt4, nova_resposta, novo_nivel, id_pergunta))

    conn.commit()
    conn.close()
    print(f"\nPergunta ID {id_pergunta} atualizada com sucesso!")
    
    
def excluir_pergunta(id_pergunta):
    conn = conectar_db()
    cursor = conn.cursor()

    # Verifica se a pergunta existe antes de excluir
    cursor.execute("SELECT id FROM perguntas WHERE id = ?", (id_pergunta,))
    pergunta = cursor.fetchone()

    if pergunta:
        # Se a pergunta existe, exclui ela
        cursor.execute("DELETE FROM perguntas WHERE id = ?", (id_pergunta,))
        conn.commit()
        print(f"\nPergunta ID {id_pergunta} excluída com sucesso!")
    else:
        # Se a pergunta não existe, exibe uma mensagem de erro
        print(f"\nPergunta ID {id_pergunta} não encontrada.")

    conn.close()
    
    
def cadastrar_professor(nome, email):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO alunos (nome, email, tipo) 
        VALUES (?, ?, 'professor')
    ''', (nome, email))

    conn.commit()
    conn.close()
    print(f"\nProfessor {nome} cadastrado com sucesso!")
    
def listar_professores():
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome, email FROM alunos WHERE tipo = 'professor'")
    professores = cursor.fetchall()

    conn.close()

    print("\nProfessores cadastrados:")
    for professor in professores:
        print(f"ID: {professor[0]} | Nome: {professor[1]} | Email: {professor[2]}")
    
    
def login(nome, email):
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Verificando se o usuário é professor ou aluno
    cursor.execute('SELECT * FROM alunos WHERE nome=? AND email=?', (nome, email))
    usuario = cursor.fetchone()
    
    if usuario:
        if usuario[3] == 'professor':  # A coluna 3 é o tipo (professor/aluno)
            return 'professor'
        else:
            return 'aluno'
    else:
        return None
    

def jogar_jogo(usuario):
    conn = conectar_db()
    cursor = conn.cursor()

    # Obter 15 perguntas aleatórias do banco de dados
    cursor.execute('SELECT * FROM perguntas ORDER BY RANDOM() LIMIT 15')
    perguntas = cursor.fetchall()

    print("\nIniciando o Jogo...\n")
    
    pontos = 0
    for pergunta in perguntas:
        print(f"Pergunta: {pergunta[1]}")
        print(f"A) {pergunta[2]}")
        print(f"B) {pergunta[3]}")
        print(f"C) {pergunta[4]}")
        print(f"D) {pergunta[5]}")
        
        resposta = input("\nEscolha sua resposta (A/B/C/D): ").upper()
        
        if resposta == pergunta[6].upper():
            print("Resposta correta!")
            pontos += 10
        else:
            print("Resposta errada.")
            print(f"O jogo acabou! Você fez {pontos} pontos.")
            break

    print(f"\nFim do jogo! Você fez {pontos} pontos.")
    
    # Registrar a pontuação no banco de dados
    cursor.execute('INSERT INTO pontuacoes (aluno_id, pontos) VALUES (?, ?)', (usuario[0], pontos))
    conn.commit()

    conn.close()

    print("\nObrigado por jogar!")
    
    
def listar_perguntas_por_nivel(nivel):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, pergunta, nivel FROM perguntas WHERE nivel = ?", (nivel,))
    perguntas = cursor.fetchall()

    conn.close()

    if perguntas:
        print(f"\nPerguntas de nível {nivel}:")
        for pergunta in perguntas:
            print(f"ID: {pergunta[0]} | Pergunta: {pergunta[1]} | Nível: {pergunta[2]}")
    else:
        print(f"\nNenhuma pergunta de nível {nivel} cadastrada ainda.")
        
if __name__ == "__main__":
    criar_tabelas()
    print("Tabelas criadas com sucesso!")
    
            

def verificar_estrutura_tabela():
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute('PRAGMA table_info(perguntas);')  # Consulta para verificar a estrutura da tabela
    colunas = cursor.fetchall()

    if not colunas:
        print("Tabela 'perguntas' não encontrada.")
    else:
        for coluna in colunas:
            print(coluna)  # Exibe as colunas da tabela

    conn.close()

# Chamar a função para verificar a estrutura da tabela
verificar_estrutura_tabela()
           
# Teste: Listar professores cadastrados
listar_professores()

# Listar novamente para ver as mudanças
listar_perguntas()




