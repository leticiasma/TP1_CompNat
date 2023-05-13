import random
import numpy as np
from math import isclose

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
            '<opbin>': [
                '+',
                '-',
                '*',
                '/'],
            '<opun>': [
                'sen',
                'cos',
                'log'],
            '<var>': 
                ['X'+str(i) for i in np.arange(0, num_variaveis)],
            '<const>': self.remove_zero([i for i in np.arange(-1, 1, 0.1)])
        }

    def remove_zero(self, lista:list) -> list:
        return [e for e in lista if not isclose(e, 0, abs_tol=0.000000001)]

    def retorna_opcao_aleatoria_regra(self, regra:str) -> list:
        return random.choice(self.regras[regra])
    
    def retorna_regra_terminal_aleatoria(self):
        return random.choice(['<const>', '<var>'])