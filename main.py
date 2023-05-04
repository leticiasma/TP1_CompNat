from etapas import gera_populacao_inicial, calcula_fitness_individuos

import random
import pandas as pd 
import numpy as n
import sys

def main():
    random.seed(2)

    df = pd.read_csv(sys.argv[1])
    num_cols = len(df.columns)
    num_features_cols = num_cols-1
    nomes = [f'X{i}' for i in range(num_features_cols)]
    nomes.append('y')
    df.columns = nomes

    num_individuos = int(sys.argv[2])
    num_vars = int(sys.argv[3])
    alt_max = int(sys.argv[4])
    individuos = gera_populacao_inicial(num_individuos, num_vars, alt_max)
    calcula_fitness_individuos(individuos, df)

    for individuo in individuos:
        print(individuo)
        print("\n")

if __name__ == "__main__":
    main()