from etapas import gera_populacao_inicial, calcula_fitness_individuos, selecao_por_roleta, selecao_por_torneio, realiza_crossovers, realiza_mutacoes

import random
import pandas as pd 
import sys
from individuo import *

#seed = random.randrange(10000)
random.seed(22)
#print("Seed usada:", seed)

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

    #Gera a população inicial de indivíduos aleatoriamente seguindo regras da gramática
    #individuos_iniciais = gera_populacao_inicial(tamanho_populacao, num_variaveis, altura_max_individuo)

    #Indivíduo 1
    individuo1 = Individuo(5)
    individuo1.altura_max_arvore = 5
    nos_nivel_0 = [NoNaoTerminal('sen')]
    nos_nivel_1 = [NoNaoTerminal('+')]
    nos_nivel_0[0].filhos = nos_nivel_1
    nos_nivel_1[0].pai = nos_nivel_0[0]
    nos_nivel_2 = [NoTerminal(1), NoNaoTerminal('*')]
    nos_nivel_1[0].filhos = nos_nivel_2
    nos_nivel_2[0].pai = nos_nivel_1[0]
    nos_nivel_2[1].pai = nos_nivel_1[0]
    nos_nivel_3 = [NoTerminal(2), NoNaoTerminal('-')]
    nos_nivel_3[0].pai = nos_nivel_2[1]
    nos_nivel_3[1].pai = nos_nivel_2[1]
    nos_nivel_2[1].filhos = nos_nivel_3
    nos_nivel_4 = [NoNaoTerminal('*'), NoTerminal(3)]
    nos_nivel_4[0].pai = nos_nivel_3[1]
    nos_nivel_4[1].pai = nos_nivel_3[1] 
    nos_nivel_3[1].filhos = nos_nivel_4
    nos_nivel_5 = [NoTerminal(4), NoTerminal(5)]
    nos_nivel_5[0].pai = nos_nivel_4[0]
    nos_nivel_5[1].pai = nos_nivel_4[0]
    nos_nivel_4[0].filhos = nos_nivel_5

    individuo1.arvore = Arvore(nos_nivel_0, 5)
    individuo1.arvore.nos.extend(nos_nivel_0+nos_nivel_1+nos_nivel_2+nos_nivel_3+nos_nivel_4+nos_nivel_5)

    #Indivíduo 2
    individuo2 = Individuo(4)
    individuo2.altura_max_arvore = 5
    nos_nivel_0_2 = [NoNaoTerminal('cos')]
    nos_nivel_1_2 = [NoNaoTerminal('*')]
    nos_nivel_1_2[0].pai = nos_nivel_0_2[0]
    nos_nivel_0_2[0].filhos = nos_nivel_1_2
    nos_nivel_2_2 = [NoTerminal(6), NoNaoTerminal('+')]
    nos_nivel_2_2[0].pai = nos_nivel_1_2[0]
    nos_nivel_2_2[1].pai = nos_nivel_1_2[0]
    nos_nivel_1_2[0].filhos = nos_nivel_2_2
    nos_nivel_3_2 = [NoTerminal(7), NoNaoTerminal('log')]
    nos_nivel_3_2[0].pai = nos_nivel_2_2[1]
    nos_nivel_3_2[1].pai = nos_nivel_2_2[1]
    nos_nivel_2_2[1].filhos = nos_nivel_3_2
    nos_nivel_4_2 = [NoTerminal(8)]
    nos_nivel_4_2[0].pai = nos_nivel_3_2[1]
    nos_nivel_3_2[1].filhos = nos_nivel_4_2

    individuo2.arvore = Arvore(nos_nivel_0_2, 5) 
    individuo2.arvore.nos.extend(nos_nivel_0_2+nos_nivel_1_2+nos_nivel_2_2+nos_nivel_3_2+nos_nivel_4_2)  

    individuos_iniciais = [individuo1, individuo2]

    realiza_crossovers(individuos_iniciais, p_c)
    realiza_mutacoes(individuos_iniciais, p_m, 2)

    # populacao_atual = individuos_iniciais

    # #Por certo número de gerações ("critério de parada"), repetir o ciclo
    # for g in range(num_geracoes):
    #     #Selecionar indivíduos
    #     if tipo_selecao == 'r':
    #         #Cálculo da fitness de toda a população calculada no início de "selecao_por_roleta"
    #         individuos_selecionados = selecao_por_roleta(populacao_atual, tamanho_populacao, df)
    #     elif tipo_selecao == 't':
    #         #A fitness é calculada para os participantes de cada torneio
    #         individuos_selecionados = selecao_por_torneio(populacao_atual, tamanho_populacao, df)
    #     elif tipo_selecao == 'l': #LEXICASE
    #         individuos_selecionados = selecao_lexicase(populacao_atual, tamanho_populacao, df
            
    #     populacao_atual = individuos_selecionados

    #     #Aplicar operações genéticas
    #     realiza_crossovers(populacao_atual, p_c) #VER SE MUDA DENTRO DA PROPRIA POP_ATUAL OU TERIA QUE CRIAR UMA NOVA
    #     realiza_mutacoes(populacao_atual, p_m, num_variaveis)
    
    # #Calcular a fitness para a última população gerada
    # fitness_individuos_finais = calcula_fitness_individuos(populacao_atual, df)

    # #Retornar solução na posição da maior fitness
    # indice_melhor_fitness = fitness_individuos_finais.index(max(fitness_individuos_finais))
    # melhor_individuo_solucao = populacao_atual[indice_melhor_fitness]

    # print("\nMELHOR SOLUCAO: ", melhor_individuo_solucao.arvore)

if __name__ == "__main__":
    main()