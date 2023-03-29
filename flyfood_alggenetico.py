from random import sample, random, choice
import random
import operator

'''Formulação do Problema:'''

tamanho_pop = 8
taxa_mut = 0.5

def lendo_matriz(arquivo):
    pontos = {}
    i, j = map(int, arquivo.readline().split(' '))
    for l in range(i):
        linha = arquivo.readline().strip().split(' ')
        for c in range(len(linha)):
            if linha[c] != '0':
                pontos[linha[c]] = (l, c)
    return pontos

'''Populaçao inicial e função fitness:'''

def populacao_inicial(pontos):
    cromossomo = [item for item in pontos if item != 'R']
    pop_inicial = []
    while len(pop_inicial) < tamanho_pop:
        permutation = sample(cromossomo, len(cromossomo))
        if permutation not in pop_inicial:
            pop_inicial.append(permutation)
    return pop_inicial


def rotas(rota):
    rota = 'R' + "".join(rota) + 'R'
    custo = 0
    for pos in range(len(rota) - 1):
        ponto1 = pontos.get(rota[pos])
        ponto2 = pontos.get(rota[pos + 1])
        distancia1 = abs(ponto1[0] - ponto2[0])
        distancia2 = abs(ponto1[1] - ponto2[1])
        custo += distancia1 + distancia2
    return custo


def fitnessFunction(pop):
    fitness = {}
    for custo in range(len(pop)):
        fitness[custo] = 1 / rotas(pop[custo])
    return fitness


'''Algoritmo genético: seleção -> crossover -> mutação -> implementação'''

def ranking(fitness, pop):
    global solucao
    rota = max(fitness.items(), key=operator.itemgetter(1))
    if solucao == None:
        solucao = [pop[rota[0]], rota[1]]
    else:
        if rota[1] > solucao[1]:
            solucao = [pop[rota[0]], rota[1]]


def selecao(fitness):
    pais = sorted(fitness.items(), key=operator.itemgetter(1), reverse=True)
    return pais


def selecao_pais(fitness):
    global tamanho_pop
    rotas_apt = []
    pais = sorted(fitness.items(), key=operator.itemgetter(1), reverse=False)
    rank_sum = tamanho_pop * (tamanho_pop + 1) / 2
    for iterator in range(tamanho_pop):
        prob = (float(iterator + 1) / rank_sum) * 100
        for i in range(int(prob)):
            rotas_apt.append(pais[iterator])
    return rotas_apt


def crossover(pai1, pai2):
    filho1 = []
    filho2 = []
    aux = len(pai1) // 2
    for i in range(0, aux):
        filho1.append(pai1[i])
    filho2 = [item for item in pai2 if item not in filho1]
    return filho1 + filho2


def mutacao(rota):
    global taxa_mut
    for ponto_entrega in range(len(rota)):
        if (random.random() < taxa_mut):
            mudar_rota = int(random.random() * len(rota))
            ponto1 = rota[ponto_entrega]
            ponto2 = rota[mudar_rota]

            rota[mudar_rota] = ponto1
            rota[ponto_entrega] = ponto2
    return rota


def mutacao_pop(nova_geracao):
    filho_mutado = []
    for iterator in range(0, len(nova_geracao)):
        mutacao_feita = mutacao(nova_geracao[iterator])
        filho_mutado.append(mutacao_feita)
    return filho_mutado


arquivo = open('arquivo.txt', 'r')
pontos = lendo_matriz(arquivo)

pop = populacao_inicial(pontos)

solucao = None
parada = 10

for i in range(parada):
    fitness = (fitnessFunction(pop))
    ranking(fitness, pop)
    tam_novageracao = 0
    nova_geracao = []
    selecao_ranking = selecao_pais(fitness)
    while tam_novageracao < tamanho_pop:
        pai1, pai2 = (pop[choice(selecao_ranking)[0]], pop[choice(selecao_ranking)[0]])
        filho1 = crossover(pai1, pai2)
        filho2 = crossover(pai2, pai1)

        nova_geracao.append(filho1)
        nova_geracao.append(filho2)

        tam_novageracao += 2

    pop = mutacao_pop(nova_geracao)

print("".join(solucao[0]))
