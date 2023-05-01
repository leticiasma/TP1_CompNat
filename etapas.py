from arvore import Arvore
from gramatica import Gramatica

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