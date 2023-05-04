from etapas import gera_populacao_inicial, calcula_fitness_individuos, selecao_por_roleta, selecao_por_torneio

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
    p_c = int(sys.argv[5]) #Probabilidade crossover
    p_m = int(sys.argv[6]) #Probabilidade mutação

    individuos_iniciais = gera_populacao_inicial(num_individuos, num_vars, altura_max_individuo)
    fitness_individuos_iniciais = calcula_fitness_individuos(individuos_iniciais, df)

    individuos_selecionados = selecao_por_roleta(individuos_iniciais, num_individuos, df)
    novas_fitness = calcula_fitness_individuos(individuos_selecionados, df)

    individuos_selecionados = selecao_por_torneio(individuos_iniciais, num_individuos, df)
    novas_fitness_2 = calcula_fitness_individuos(individuos_selecionados, df)

    print(fitness_individuos_iniciais)
    print(novas_fitness)
    print(novas_fitness_2)

    '''for individuo in individuos:
        print(individuo)
        print("\n")'''

if __name__ == "__main__":
    main()