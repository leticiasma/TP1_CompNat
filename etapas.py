from arvore import Arvore
from gramatica import Gramatica
from auxiliares import *
import random
from random import choices

#############################################

def gera_individuo_metodo_grow(num_vars:int, altura_maxima:int):
    gramatica = Gramatica(num_vars)

    individuo = Arvore.gera_arvore_grow(gramatica, altura_maxima)

    return individuo

def gera_populacao_inicial(num_individuos:int, num_vars:int, altura_maxima:int) -> list: 
    individuos = []
    
    for i in range(num_individuos):
        individuo = gera_individuo_metodo_grow(num_vars, altura_maxima)
        individuos.append(individuo)

    return individuos

def calcula_fitness_individuos(individuos:list, df):
    fitness_individuos = []

    for individuo in individuos:
        fitness = calcula_fitness_individuo(individuo, df)
        fitness_individuos.append(fitness)

    #print (fitness_individuos)
    
    return fitness_individuos

##########
def selecao_por_roleta(individuos:list, num_individuos:int, df):
    fitness_individuos = calcula_fitness_individuos (individuos, df)
    fitness_media_populacao = sum(fitness_individuos)/len(fitness_individuos)

    probabilidades_selecao_individuos = []
    for fitness in fitness_individuos:
        probabilidades_selecao_individuos.append(fitness/fitness_media_populacao)

    individuos_selecionados = choices(individuos, probabilidades_selecao_individuos, k=num_individuos)

    return individuos_selecionados

def selecao_por_torneio(individuos:list, num_individuos:int, df):
    tamanho_torneio = 2

    individuos_selecionados = []

    for t in range (num_individuos):
        participantes_torneio = random.SystemRandom().sample(individuos, tamanho_torneio)
        fitness_participantes_torneio = calcula_fitness_individuos(participantes_torneio, df)
        if fitness_participantes_torneio[0] >= fitness_participantes_torneio[1]:
            vencedor_torneio = participantes_torneio[0]
        else:
            vencedor_torneio = participantes_torneio[1]
        #vencedor_torneio = participantes_torneio.index(max(fitness_participantes_torneio))
        individuos_selecionados.append(vencedor_torneio)

    return individuos_selecionados