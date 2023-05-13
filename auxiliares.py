import math
import pandas as pd
import numpy as np
from individuo import *

def calcula_fitness_individuo(individuo:Individuo, df:pd.DataFrame):

    fitness_individuo = 0
    soma = 0
    resultados = df.apply(lambda linha: individuo.arvore.avalia_individuo(linha.to_dict()), axis=1).to_numpy()

    diferenca_quadrada = np.square(resultados - df["y"].to_numpy())
    soma = np.sum(diferenca_quadrada)
    fitness_individuo = math.sqrt(soma/len(df))

    individuo.arvore.fitness = fitness_individuo

    return fitness_individuo

def calcula_fitness_individuo_linha(individuo:Individuo, linha:dict):

    resultado = individuo.arvore.avalia_individuo(linha)
    diferenca = resultado - linha["y"]

    return diferenca

def gera_estrutura_arvore_grow(gramatica:Gramatica, expansao:list, num_max_niveis_para_adicionar:int, nos:list, profundidade_atual:int):
    #VER SE A LOGICA DE num_max_niveis_para_adicionar-1 tá certa ou se tá fazendo inivíduos menores do que poderia
    if num_max_niveis_para_adicionar == 1: #Caso: Altura máxima da raiz chegando. Só pode adicionar mais um nível.
        regra_terminal = gramatica.retorna_regra_terminal_aleatoria()
        no_criado = NoTerminal(gramatica.retorna_opcao_aleatoria_regra(regra_terminal))
        no_criado.altura = 0 
        no_criado.profundidade = profundidade_atual
        nos.append(no_criado)
        
        return no_criado, 0, profundidade_atual
    
    if len(expansao) == 1: #Caso: sorteado um nó do tipo var ou const, mas isso aqui só valeria para expr... e os outros níveis?
        #Cria um NoTerminal, mas acho que não precisaria ser
        no_criado = NoTerminal(gramatica.retorna_opcao_aleatoria_regra(expansao[0]))
        no_criado.altura = 0
        no_criado.profundidade = profundidade_atual
        nos.append(no_criado)

        return no_criado, 0, profundidade_atual
    
    elif len(expansao) == 2:
        no_filho, altura_filho, profundidade_filho = gera_estrutura_arvore_grow(gramatica,
                                                    gramatica.retorna_opcao_aleatoria_regra(expansao[1]),
                                                    num_max_niveis_para_adicionar-1, nos, profundidade_atual+1)
        
        no_criado = NoNaoTerminal(gramatica.retorna_opcao_aleatoria_regra(expansao[0]))
        no_criado.altura = altura_filho+1
        no_criado.profundidade = profundidade_atual
        nos.append(no_criado)
        no_criado.add_filho(no_filho)
        no_filho.pai = no_criado

        return no_criado, altura_filho+1, profundidade_filho
    
    elif len(expansao) == 3:
        no_filho_esq, altura_filho_esq, profundidade_filho_esq = gera_estrutura_arvore_grow(gramatica,
                                                    gramatica.retorna_opcao_aleatoria_regra(expansao[0]),
                                                    num_max_niveis_para_adicionar-1, nos, profundidade_atual+1)
        
        no_filho_dir, altura_filho_dir, profundidade_filho_dir = gera_estrutura_arvore_grow(gramatica,
                                                    gramatica.retorna_opcao_aleatoria_regra(expansao[2]),
                                                    num_max_niveis_para_adicionar-1, nos, profundidade_atual+1)
        
        no_criado = NoNaoTerminal(gramatica.retorna_opcao_aleatoria_regra(expansao[1]))
        no_criado.altura = max(altura_filho_esq, altura_filho_dir)+1
        no_criado.profundidade = profundidade_atual
        no_criado.add_filho(no_filho_esq)
        no_filho_esq.pai = no_criado
        no_criado.add_filho(no_filho_dir)
        no_filho_dir.pai = no_criado
        nos.append(no_criado)
    
        return no_criado, no_criado.altura, max(profundidade_filho_esq, profundidade_filho_dir)
      
def gera_arvore_metodo_grow(num_variaveis:int, altura_max_arvore:int, profundidade_de_onde_iniciar=0)->Arvore:
    gramatica = Gramatica(num_variaveis)
    nos = list()

    no_raiz, altura_gerada, profundidade_gerada = gera_estrutura_arvore_grow(gramatica,
                                                gramatica.retorna_opcao_aleatoria_regra(gramatica.regra_inicial),
                                                altura_max_arvore,
                                                nos, profundidade_de_onde_iniciar)

    arvore = Arvore(no_raiz, altura_gerada, profundidade_gerada)
    arvore.add_nos(nos)
    
    return arvore