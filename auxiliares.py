import math
import pandas as pd
import numpy as np
from typing import Callable
from arvore import *

def calcula_fitness_individuo(individuo:Arvore, df:pd.DataFrame):

    fitness = 0
    soma = 0

    resultados = df.apply(lambda linha: individuo.avalia_individuo(linha.to_dict()), axis=1).to_numpy()

    print("DF", df["y"].to_numpy())
    diferenca_quadrada = np.square(resultados - df["y"].to_numpy())
    soma = np.sum(diferenca_quadrada)
    fitness = math.sqrt(soma/len(df))

    individuo.fitness = fitness

    return fitness