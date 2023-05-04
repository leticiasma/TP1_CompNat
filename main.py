from etapas import gera_populacao_inicial, calcula_fitness_individuos, selecao_por_roleta, selecao_por_torneio, realiza_crossovers, realiza_mutacoes

import random
import pandas as pd 
import numpy as n
import sys

def main():
    random.seed(0) #com 23 dá erro

    df = pd.read_csv(sys.argv[1])
    num_cols = len(df.columns)
    num_features_cols = num_cols-1
    nomes = [f'X{i}' for i in range(num_features_cols)]
    nomes.append('y')
    df.columns = nomes

    num_vars = len(nomes)-1 #Número de variáveis do dataset

    altura_max_individuo = int(sys.argv[2])
    num_individuos = int(sys.argv[3]) #Tamanho população
    num_geracoes = int(sys.argv[4])
    tipo_selecao = sys.argv[5]
    p_c = sys.argv[6] #Probabilidade crossover
    p_m = sys.argv[7] #Probabilidade mutação

    individuos_iniciais = gera_populacao_inicial(num_individuos, num_vars, altura_max_individuo)
    populacao_atual = individuos_iniciais

    for g in range(num_geracoes): #Critério de parada
        if tipo_selecao == 'r':
            individuos_selecionados = selecao_por_roleta(populacao_atual, num_individuos, df)
        elif tipo_selecao == 't':
            individuos_selecionados = selecao_por_torneio(populacao_atual, num_individuos, df)
            
        populacao_atual = individuos_selecionados

        realiza_crossovers(populacao_atual, p_c)
        realiza_mutacoes(populacao_atual, p_m)
    
    fitness_individuos_finais = calcula_fitness_individuos(populacao_atual, df)
    print(fitness_individuos_finais)
    #Retornar solução na posição da maior fitness 

    '''for individuo in individuos:
        print(individuo)
        print("\n")'''

if __name__ == "__main__":
    main()