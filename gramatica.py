import random
import numpy as np
from math import isclose

EXPR = '<expr>' 
class Gramatica():
    def __init__(self, num_vars):
        self.regras = {
            EXPR: [
                [EXPR, '<opbin>', EXPR],
                ['<opun>', EXPR],
                ['<var>'],
                ['<const>']],
            '<opbin>': [
                ['+'],
                ['-'],
                ['*'],
                ['/']],
            '<opun>': [
                ['sen'],
                ['cos'],
                ['log'],
                ['exp']],
            '<var>': 
                [['X'+str(i)] for i in np.arange(1, num_vars+1)], #Pode ter 3 ou 9, depende da base de dados
            '<const>': self.remove_zero([i for i in np.arange(-1, 1, 0.1)])
        }

        self.componentes = {
            'nao_terminais_bin': ['+', '-', '*', '/'],
            'nao_terminais_un': ['sen', 'cos', 'log', 'exp'],
            'terminais' : ['X'+str(i) for i in range(1, num_vars+1)].extend(self.remove_zero([i for i in np.arange(-1, 1, 0.1)]))
        }

        self.regra_inicial = EXPR

    def remove_zero(self, lista:list) -> list:
        return [el for el in lista if not isclose(el, 0, abs_tol=0.0001)]

    def opcao_aleatoria(self, regra:str) -> list:
        return random.choice(self.regras[regra])
    
    def regra_terminal_aleatoria(self):
        return random.choice(['<const>', '<var>'])
    
    def eh_regra_que_produz_terminal(self, regra:str) -> bool:
        return regra in [['<var>'], ['<const>']]
    
    def eh_regra_que_produz_funcao(self, regra:str) -> bool:
        return regra in [['<opbin>'], ['<opun>']]
    
    def eh_regra_que_produz_componente(self, regra:str) -> bool:
        return self.eh_regra_que_produz_funcao(regra) or self.eh_regra_que_produz_terminal(regra)
    
    def terminal_aleatorio(self):
        return random.choice(self.componentes['terminais'])