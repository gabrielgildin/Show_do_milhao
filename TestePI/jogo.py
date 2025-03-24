import sqlite3
import random
from database import conectar_db, login , adicionar_pergunta, editar_pergunta, excluir_pergunta, jogar_jogo, obter_ranking # Aqui estamos importando as funções do database.py


def editar_pergunta_menu():
    try:
        # Solicita o ID da pergunta que será editada
        id_pergunta = int(input("Digite o ID da pergunta que deseja editar: "))
        
        # Solicita os novos dados da pergunta
        nova_pergunta = input("Digite a nova pergunta: ")
        nova_alt1 = input("Digite a nova primeira alternativa: ")
        nova_alt2 = input("Digite a nova segunda alternativa: ")
        nova_alt3 = input("Digite a nova terceira alternativa: ")
        nova_alt4 = input("Digite a nova quarta alternativa: ")
        nova_resposta = input("Digite a nova resposta correta (A/B/C/D): ").upper()
        while nova_resposta not in ['A', 'B', 'C', 'D']:
            print("Resposta inválida! Digite A, B, C ou D.")
            nova_resposta = input("Digite a nova resposta correta (A/B/C/D): ").upper()
        novo_nivel = input("Digite o novo nível da pergunta (fácil, médio, difícil): ")

        # Chama a função editar_pergunta do database.py com os parâmetros corretos
        from database import editar_pergunta
        editar_pergunta(id_pergunta, nova_pergunta, nova_alt1, nova_alt2, nova_alt3, nova_alt4, nova_resposta, novo_nivel)
    except ValueError:
        print("ID inválido! Digite um número.")

def excluir_pergunta_menu():
    try:
        # Solicita o ID da pergunta que será excluída
        id_pergunta = int(input("Digite o ID da pergunta que deseja excluir: "))

        # Chama a função excluir_pergunta do database.py
        from database import excluir_pergunta
        excluir_pergunta(id_pergunta)
    except ValueError:
        print("ID inválido! Digite um número.")
        
        
# Função para exibir o menu de opções do professor
def exibir_menu_professor():
    print("\nMenu de opções:")
    print("1. Adicionar pergunta")
    print("2. Editar pergunta")
    print("3. Excluir pergunta")
    print("4. Sair")

# Função para exibir o menu de opções do aluno (apenas jogar o jogo)
def exibir_menu_aluno():
    print("\nMenu de opções:")
    print("1. Jogar o jogo")
    print("2. Ver ranking")
    print("3. Sair")

# Função para o menu de interação com o professor
def menu_professor():
    while True:
        exibir_menu_professor()  # Exibe o menu do professor
        opcao = input("Digite o número da opção desejada: ")

        if opcao == '1':
            adicionar_pergunta()
        elif opcao == '2':
            editar_pergunta_menu()  # Chama a função editar_pergunta_menu do mainn.py
        elif opcao == '3':
            excluir_pergunta_menu()
        elif opcao == '4':
            print("\nSaindo...")
            break
        else:
            print("\nOpção inválida! Tente novamente.")

# Função para o menu do aluno
def menu_aluno(usuario):
    while True:
        exibir_menu_aluno()  # Exibe o menu do aluno
        opcao = input("Digite o número da opção desejada: ")

        if opcao == '1':
            jogar_jogo(usuario)  # Passa o objeto usuario para a função jogar_jogo
        elif opcao == '3':
            print("\nSaindo...")
            break  # Saímos do loop e terminamos o programa
        elif opcao == '2':
            obter_ranking()
        else:
            print("\nOpção inválida! Tente novamente.")

# Função de login
def realizar_login():
    nome = input("Digite seu nome: ")
    email = input("Digite seu email: ")
    
    # Valida o login, retornando o tipo de usuário (professor ou aluno)
    tipo_usuario = login(nome, email)
    
    if tipo_usuario == 'professor':
        print(f"\nLogin bem-sucedido! Bem-vindo(a), {nome} (professor)")
        menu_professor()  # Chama o menu de professor
    elif tipo_usuario == 'aluno':
        print(f"\nLogin bem-sucedido! Bem-vindo(a), {nome} (aluno)")
        usuario = (nome, email)  # Cria um objeto usuario com nome e email
        menu_aluno(usuario)  # Chama o menu de aluno passando o objeto usuario
    else:
        print("\nLogin falhou. Tente novamente.")

# Função principal
def main():
    print("Iniciando o Jogo...")
    realizar_login()  # Chama a função de login

num = 1
# Chama a função principal para iniciar o jogo
if num == 1:
    main()


    
