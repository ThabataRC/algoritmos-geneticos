import random
import math

class AlgoritmoGenetico():
    def __init__(self, x_min, x_max, tam_populacao=10, taxa_mutacao=0.01, taxa_crossover=0.7, num_geracoes=100, elitismo=True, percent_elitismo=0.1, pontos_corte=1):
        """
        Inicializa os parâmetros do algoritmo genético
        """
        self.x_min = x_min
        self.x_max = x_max
        self.tam_populacao = tam_populacao
        self.taxa_mutacao = taxa_mutacao
        self.taxa_crossover = taxa_crossover
        self.num_geracoes = num_geracoes
        self.elitismo = elitismo
        self.percent_elitismo = percent_elitismo
        self.pontos_corte = pontos_corte
        self.num_bits = self._calcular_num_bits()
        self.populacao = self._gerar_populacao_inicial()

    def _calcular_num_bits(self):
        """
        Calcula o número de bits necessário para representar x como um vetor binário
        """
        precisao = 1000  # Precisão para mapear número real no intervalo binário
        return math.ceil(math.log2((self.x_max - self.x_min) * precisao))

    def _gerar_populacao_inicial(self):
        """
        Gera a população inicial com indivíduos representados por vetores binários
        """
        populacao = []
        for _ in range(self.tam_populacao):
            individuo = [random.randint(0, 1) for _ in range(self.num_bits)]
            populacao.append(individuo)
        return populacao

    def _binario_para_decimal(self, individuo):
        """
        Converte um vetor binário para um valor decimal real dentro da faixa [x_min, x_max]
        """
        precisao = 1000
        decimal = int("".join(map(str, individuo)), 2)
        x = self.x_min + (self.x_max - self.x_min) * decimal / (2**self.num_bits - 1)
        return x

    def _funcao_objetivo(self, x):
        """
        Avalia a função objetivo f(x) = x³ - 6x + 14
        """
        return x**3 - 6*x + 14

    def avaliar_populacao(self):
        """
        Avalia toda a população e retorna a lista de fitness (valores da função objetivo)
        """
        fitness = []
        for individuo in self.populacao:
            x = self._binario_para_decimal(individuo)
            fitness.append(self._funcao_objetivo(x))
        return fitness

    def selecionar_por_torneio(self, fitness):
        """
        Seleciona um indivíduo usando o método do torneio
        """
        torneio_size = 3
        selecionados = random.sample(range(self.tam_populacao), torneio_size)
        melhor_indice = min(selecionados, key=lambda i: fitness[i])
        return self.populacao[melhor_indice]

    def crossover(self, pai, mae):
        """
        Realiza o crossover entre dois indivíduos (pai e mãe) com 1 ou 2 pontos de corte
        """
        if random.random() < self.taxa_crossover:
            if self.pontos_corte == 1:
                ponto = random.randint(1, self.num_bits - 1)
                filho1 = pai[:ponto] + mae[ponto:]
                filho2 = mae[:ponto] + pai[ponto:]
            elif self.pontos_corte == 2:
                ponto1 = random.randint(1, self.num_bits - 2)
                ponto2 = random.randint(ponto1, self.num_bits - 1)
                filho1 = pai[:ponto1] + mae[ponto1:ponto2] + pai[ponto2:]
                filho2 = mae[:ponto1] + pai[ponto1:ponto2] + mae[ponto2:]
            return filho1, filho2
        return pai[:], mae[:]

    def mutacao(self, individuo):
        """
        Aplica mutação em um indivíduo com a taxa de mutação configurada
        """
        for i in range(len(individuo)):
            if random.random() < self.taxa_mutacao:
                individuo[i] = 1 if individuo[i] == 0 else 0

    def executar(self):
        """
        Executa o algoritmo genético para encontrar o valor de x que minimiza a função f(x)
        """
        for geracao in range(self.num_geracoes):
            fitness = self.avaliar_populacao()

            nova_populacao = []
            if self.elitismo:
                num_elites = math.ceil(self.percent_elitismo * self.tam_populacao)
                elite_indices = sorted(range(len(fitness)), key=lambda i: fitness[i])[:num_elites]
                elites = [self.populacao[i] for i in elite_indices]
                nova_populacao.extend(elites)

            while len(nova_populacao) < self.tam_populacao:
                pai = self.selecionar_por_torneio(fitness)
                mae = self.selecionar_por_torneio(fitness)
                filho1, filho2 = self.crossover(pai, mae)
                self.mutacao(filho1)
                self.mutacao(filho2)
                nova_populacao.append(filho1)
                if len(nova_populacao) < self.tam_populacao:
                    nova_populacao.append(filho2)

            self.populacao = nova_populacao

            # Imprime o melhor indivíduo de cada geração
            melhor_individuo = min(self.populacao, key=lambda ind: self._funcao_objetivo(self._binario_para_decimal(ind)))
            melhor_x = self._binario_para_decimal(melhor_individuo)
            print(f'Geração {geracao + 1}: Melhor x = {melhor_x}, f(x) = {self._funcao_objetivo(melhor_x)}')

        # Retorna o melhor indivíduo final
        fitness = self.avaliar_populacao()
        melhor_indice = min(range(len(fitness)), key=lambda i: fitness[i])
        melhor_individuo = self.populacao[melhor_indice]
        melhor_x = self._binario_para_decimal(melhor_individuo)
        return melhor_x, self._funcao_objetivo(melhor_x)

# Função principal para rodar o algoritmo genético
if __name__ == "__main__":
    ag = AlgoritmoGenetico(x_min=-10, x_max=10, tam_populacao=10, taxa_mutacao=0.01, taxa_crossover=0.7, num_geracoes=100, elitismo=True, percent_elitismo=0.1, pontos_corte=2)
    melhor_x, melhor_fitness = ag.executar()
    print(f'\nMelhor solução: x = {melhor_x}, f(x) = {melhor_fitness}')
