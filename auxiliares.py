import math
import pandas as pd
import numpy as np
from typing import Callable
from individuo import *

def calcula_fitness_individuo(individuo:Individuo, df:pd.DataFrame):

    fitness = 0
    soma = 0

    resultados = df.apply(lambda linha: individuo.arvore.avalia_individuo(linha.to_dict()), axis=1).to_numpy()

    #("DF", df["y"].to_numpy())
    diferenca_quadrada = np.square(resultados - df["y"].to_numpy())
    soma = np.sum(diferenca_quadrada)
    fitness = math.sqrt(soma/len(df))

    individuo.arvore.fitness = fitness

    return fitness