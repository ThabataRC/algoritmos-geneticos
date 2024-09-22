import random

# Função para criar um indivíduo aleatório
def criar_individuo(pesos_valores):
    return [random.randint(0, 1) for _ in range(len(pesos_valores))]

# Função de avaliação
def avaliar_individuo(individuo, pesos_valores, peso_maximo):
    peso_total = valor_total = 0
    for gene, (peso, valor) in zip(individuo, pesos_valores):
        if gene == 1:
            peso_total += peso
            valor_total += valor
        if peso_total > peso_maximo:
            return 0  # Penalização para soluções que excedem o peso máximo
    return valor_total

# Função de mutação
def mutacao(individuo, taxa_mutacao=0.01):
    for i in range(len(individuo)):
        if random.random() < taxa_mutacao:
            individuo[i] = 1 if individuo[i] == 0 else 0
    return individuo

# Função de crossover
def crossover(pai, mae):
    ponto_corte = random.randint(1, len(pai) - 1)
    filho = pai[:ponto_corte] + mae[ponto_corte:]
    return filho

# Função de seleção (torneio)
def selecao(populacao, fitness, torneio_tamanho=3):
    torneio = random.sample(list(zip(populacao, fitness)), torneio_tamanho)
    return max(torneio, key=lambda x: x[1])[0]

# Função principal para o algoritmo genético da mochila
def algoritmo_genetico_mochila(pesos_valores, peso_maximo, num_cromossomos, geracoes, taxa_mutacao=0.01):
    # Criar população inicial
    populacao = [criar_individuo(pesos_valores) for _ in range(num_cromossomos)]
    resultados = []

    for geracao in range(geracoes):
        fitness = [avaliar_individuo(ind, pesos_valores, peso_maximo) for ind in populacao]

        nova_populacao = []
        for _ in range(num_cromossomos // 2):
            pai = selecao(populacao, fitness)
            mae = selecao(populacao, fitness)
            filho1 = mutacao(crossover(pai, mae), taxa_mutacao)
            filho2 = mutacao(crossover(mae, pai), taxa_mutacao)
            nova_populacao.extend([filho1, filho2])

        populacao = nova_populacao

        # A cada geração, armazenar os 5 melhores indivíduos
        melhores_geracao = sorted(zip(fitness, populacao), key=lambda x: x[0], reverse=True)[:5]
        resultados_geracao = [[fitness, individuo] for fitness, individuo in melhores_geracao]
        resultados.append(resultados_geracao)

    # Selecionar os 5 melhores indivíduos após todas as gerações
    fitness_final = [avaliar_individuo(ind, pesos_valores, peso_maximo) for ind in populacao]
    melhores_finais = sorted(zip(fitness_final, populacao), key=lambda x: x[0], reverse=True)[:5]

    # Retornar a lista dos 5 melhores indivíduos e seus valores
    return [[fitness, individuo] for fitness, individuo in melhores_finais]

# Exemplo de uso
pesos_e_valores = [[2, 10], [4, 30], [6, 300], [8, 10], [8, 30], [8, 300], [12, 50], [25, 75], [50, 100], [100, 400]]
peso_maximo = 100
num_cromossomos = 150
geracoes = 50

resultado = algoritmo_genetico_mochila(pesos_e_valores, peso_maximo, num_cromossomos, geracoes)
print(f'Resultado final: {resultado}')
