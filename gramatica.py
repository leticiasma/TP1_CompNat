import random
import numpy as np
from math import isclose

#MAIS OU MENOS!!!
EXPR = '<expr>' 
class Gramatica():
    def __init__(self, num_variaveis):
        self.regra_inicial = EXPR

        self.regras = {
            EXPR: [
                [EXPR, '<opbin>', EXPR],
                ['<opun>', EXPR],
                ['<var>'],
                ['<const>']],
            '<opbin>': [ #VER SE PRECISA MESMO DESSAS LISTAS COM 1 ELEMENTO SÓ
                '+',#['+'],
                '-',#['-'],
                '*',#['*'],
                '/'],#['/']],
            '<opun>': [
                'sen',#['sen'],
                'cos',#['cos'],
                'log'],#['log'],
            '<var>': 
                ['X'+str(i) for i in np.arange(0, num_variaveis)], #VER SE PRECISA MESMO DESSAS LISTAS COM 1 ELEMENTO SÓ
            '<const>': self.remove_zero([i for i in np.arange(-1, 1, 0.1)])
        }

        self.componentes = {
            'nao_terminais_bin': ['+', '-', '*', '/'], #AQUI NEM TEM LISTA, É SÓ AS STRINGS
            'nao_terminais_un': ['sen', 'cos', 'log', 'exp'],
            #ISSO AQUI TBM TÁ DIFERENTE DO DE CIMA
            'terminais' : ['X'+str(i) for i in range(0, num_variaveis)].extend(self.remove_zero([i for i in np.arange(-1, 1, 0.1)]))
        }

    def remove_zero(self, lista:list) -> list:
        return [e for e in lista if not isclose(e, 0, abs_tol=0.000000001)]

    def retorna_opcao_aleatoria_regra(self, regra:str) -> list:
        return random.choice(self.regras[regra])
    
    def retorna_regra_terminal_aleatoria(self):
        return random.choice(['<const>', '<var>']) #AQUI NAO É LISTA
    
    def eh_regra_que_produz_terminal(self, regra:str) -> bool: #AQUI É LISTA
        return regra in [['<var>'], ['<const>']]
    
    def eh_regra_que_produz_funcao(self, regra:str) -> bool: #CONFERIR
        return regra in [['<opbin>'], ['<opun>']]
    
    def eh_regra_que_produz_componente(self, regra:str) -> bool:
        return self.eh_regra_que_produz_funcao(regra) or self.eh_regra_que_produz_terminal(regra)
    
    def retorna_terminal_aleatorio(self):
        return random.choice(self.componentes['terminais'])