from etapas import gera_populacao_inicial, calcula_fitness_individuos, selecao_por_roleta, selecao_por_torneio, selecao_lexicase, realiza_crossovers, realiza_mutacoes

import random
import pandas as pd 
import sys
from individuo import *
import copy

seed = random.randrange(10000)
random.seed(seed)
print("Seed usada:", seed)
#random.seed(4438)
#seed boa: 327

#OK!!!
def main():

    df = pd.read_csv(sys.argv[1])
    num_variaveis = len(df.columns)-1 #Número de variáveis do dataset
    nomes_colunas = [f'X{i}' for i in range(num_variaveis)]
    nomes_colunas.append('y')
    df.columns = nomes_colunas

    num_geracoes = int(sys.argv[2]) #Num de iterações
    tamanho_populacao = int(sys.argv[3])
    altura_max_individuo = int(sys.argv[4]) #Altura máxima, sendo altura_raiz = 1
    tipo_selecao = str(sys.argv[5])
    p_c = float(sys.argv[6]) #Probabilidade crossover entre dois indivíduos
    p_m = float(sys.argv[7]) #Probabilidade mutação de um indivíduo
    elitismo = int(sys.argv[8]) #0 para não elitismo e 1 para elitismo

    #POR GERAÇÃO
    fitness_melhor_individuo = math.inf
    fitness_pior_individuo = math.inf
    fitness_media_populacao = math.inf
    num_individuos_repetidos_populacao = math.inf
    num_individuos_gerados_crossover_melhores_fitness_media_pais = math.inf
    num_individuos_gerados_crossover_piores_fitness_media_pais = math.inf

    #Gera a população inicial de indivíduos aleatoriamente seguindo regras da gramática
    
    #AQUI1
    individuos_iniciais = gera_populacao_inicial(tamanho_populacao, num_variaveis, altura_max_individuo)
    #AQUI1

    populacao_atual = individuos_iniciais

    #Por certo número de gerações ("critério de parada"), repetir o ciclo
    for g in range(num_geracoes):
        #Selecionar indivíduos
        if tipo_selecao == 'r':
            #Cálculo da fitness de toda a população calculada no início de "selecao_por_roleta"
            individuos_selecionados = selecao_por_roleta(populacao_atual, tamanho_populacao, df)
        elif tipo_selecao == 't':
            #A fitness é calculada para os participantes de cada torneio
            individuos_selecionados = selecao_por_torneio(populacao_atual, tamanho_populacao, df)
        elif tipo_selecao == 'l': #LEXICASE
            individuos_selecionados = selecao_lexicase(populacao_atual, tamanho_populacao, df)
        
        #Tentar aplicar operações genéticas cada uma n vezes, nessa ordem
        populacao_pos_crossover = realiza_crossovers(individuos_selecionados, p_c, tamanho_populacao//2) #VER SE MUDA DENTRO DA PROPRIA POP_ATUAL OU TERIA QUE CRIAR UMA NOVA
        
        tam_populacao_crossover = len(populacao_pos_crossover)
        num_mutacoes = tam_populacao_crossover

        if tam_populacao_crossover < tamanho_populacao:
            num_mutacoes += 1
        populacao_pos_crossovers_mutacoes = realiza_mutacoes(populacao_pos_crossover, p_m, num_variaveis, num_mutacoes)
    
        populacao_atual = copy.deepcopy(populacao_pos_crossovers_mutacoes) #Ver se isso precisaria mesmo ou não
    
    #Calcular a fitness para a última população gerada
    fitness_individuos_finais = calcula_fitness_individuos(populacao_atual, df)

    #Retornar solução na posição da maior fitness
    indice_melhor_fitness = fitness_individuos_finais.index(max(fitness_individuos_finais))
    melhor_individuo_solucao = populacao_atual[indice_melhor_fitness]

    print("\nMELHOR SOLUCAO: ", melhor_individuo_solucao.arvore)

if __name__ == "__main__":
    main()