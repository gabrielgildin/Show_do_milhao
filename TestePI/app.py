from database import registrar_aluno, obter_ranking
from jogo import iniciar_jogo

# Registrar novo aluno
nome = input("Digite seu nome: ")
email = input("Digite seu email: ")
registrar_aluno(nome, email, tipo="aluno")

# Iniciar jogo
aluno_id = 1  # Pegue o ID do aluno de alguma forma (exemplo simplificado)
iniciar_jogo(aluno_id)

# Exibir ranking
ranking = obter_ranking()
print("Ranking:")
for posicao, (nome, pontos) in enumerate(ranking, 1):
    print(f"{posicao}. {nome} - {pontos} pontos")