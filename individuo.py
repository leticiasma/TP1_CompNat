#from __future__ import annotations

from gramatica import Gramatica
import math
import numpy as np
import random

class No():
    def __init__(self, valor):
        self.valor = valor
        self.filhos = list() #lista de nós

    def add_filho(self, novo_no_filho:'No'):
        self.filhos.append(novo_no_filho)

    def del_filhos(self):
        self.filhos = list()

    def __repr__(self):
        str_filhos = ""
        for filho in self.filhos:
            str_filhos += filho.__repr__()
        
        return f'No(Valor:{self.valor}, Filhos: {str_filhos})'
    
    def avalia_valor(self, linha:dict): #PARA PASSAR SERIES_TODICT
        raise NotImplementedError("Não implementado")
    

class NoTerminal(No):
    def __init__(self, valor):
        super().__init__(valor)

    def avalia_valor(self, linha:dict):
        #print(" LINHA ", linha, " VALOR ", self.valor)
        #print("TIPO", type(self.valor))
        if type(self.valor) == np.float64 or type(self.valor) == np.int64:
            return self.valor
        elif type(self.valor) == list:
            if self.valor[0][0] == "X":
                return linha[self.valor[0]]
        else:
            #print("AAA", self.valor)
            raise ValueError("Ue")

class NoNaoTerminal(No):
    def __init__(self, valor):
        super().__init__(valor)

    def avalia_valor(self, linha:dict):
        if len(self.valor[0]) == 1:
            if self.valor[0] == '+':
                return self.filhos[0].avalia_valor(linha) + self.filhos[1].avalia_valor(linha)
            elif self.valor[0] == '-':
                return self.filhos[0].avalia_valor(linha) - self.filhos[1].avalia_valor(linha)
            elif self.valor[0] == '*': 
                return self.filhos[0].avalia_valor(linha) * self.filhos[1].avalia_valor(linha)
            elif self.valor[0] == '/':
                termo_esq = self.filhos[0].avalia_valor(linha)
                termo_dir = self.filhos[1].avalia_valor(linha)

                if not math.isclose(termo_esq, 0): #na verdade tem que usar algo "perto o bastante"
                    return self.filhos[0].avalia_valor(linha) / self.filhos[1].avalia_valor(linha)
                else:
                    return 0 #Ou algo melhor que isso
                
            else:
                #print("AAA", self.valor)
                raise ValueError("Ue")
        elif len (self.valor[0]) == 3:
            if self.valor[0] == 'sen':
                return np.sin(self.filhos[0].avalia_valor(linha))
            elif self.valor[0] == 'cos':
                return np.cos(self.filhos[0].avalia_valor(linha))
            elif self.valor[0] == 'log':
                return np.log(abs(self.filhos[0].avalia_valor(linha))) #TIRAAAR
            elif self.valor[0] == 'exp':
                #print("UE", self.valor[0])
                return np.exp(self.filhos[0].avalia_valor(linha))
            else:
                #print("AAA", self.valor)
                raise ValueError("Ue")
        else:
            #print("TAMANHO", len(self.valor), "a", self.valor)
            raise ValueError("Ue")

class Individuo():
    def __init__(self):
        self.arvore = None
    #Arvore(No, altura_atual)

#É a estrutura do indivíduo
class Arvore():
    def __init__(self, no_raiz:No, altura_atual:int):
        self.raiz = no_raiz
        self.fitness = float('inf')
        self.altura = altura_atual
        self.nos = [self.raiz]

    def __repr__(self):
        return f'Arvore(altura: {self.altura}, {self.raiz})'

    def avalia_individuo(self, linha:dict):
        return self.raiz.avalia_valor(linha)

    def sorteia_no(self):
        no_sorteado = random.choice(self.nos)

        return no_sorteado

    def procura_no(self, valor_no):
        for no in self.nos:
            if no.valor == valor_no:
                return no
        
        return None

def gera_strutura_arvore_grow(gramatica:Gramatica, expansao:list, t_max:int, nos:list):

    #print(expansao)

    if t_max == 1:
        regra_terminal = gramatica.regra_terminal_aleatoria()
        no_criado = NoTerminal(gramatica.opcao_aleatoria(regra_terminal))
        nos.append(no_criado)
        
        return no_criado, 1
    
    if len(expansao) == 1:
        no_criado = NoTerminal(gramatica.opcao_aleatoria(expansao[0]))
        nos.append(no_criado)
        return no_criado, 1
    
    elif len(expansao) == 2:
        no_filho, altura_filho = gera_strutura_arvore_grow(gramatica,
                                                    gramatica.opcao_aleatoria(expansao[1]),
                                                    t_max-1, nos)
        no_atual = NoNaoTerminal(gramatica.opcao_aleatoria(expansao[0]))
        no_atual.add_filho(no_filho)
        return no_atual, altura_filho+1
    
    elif len(expansao) == 3:
        no_filho_esq, altura_filho_esq = gera_strutura_arvore_grow(gramatica,
                                                    gramatica.opcao_aleatoria(expansao[0]),
                                                    t_max-1, nos)
        no_filho_dir, altura_filho_dir = gera_strutura_arvore_grow(gramatica,
                                                    gramatica.opcao_aleatoria(expansao[2]),
                                                    t_max-1, nos)
        
        no_atual = NoNaoTerminal(gramatica.opcao_aleatoria(expansao[1]))
        no_atual.add_filho(no_filho_esq)
        no_atual.add_filho(no_filho_dir)
    
        return no_atual, max([altura_filho_dir, altura_filho_esq])+1
        
def gera_arvore_grow(gramatica:Gramatica, altura_maxima:int)->'Arvore':
    nos = list()
    no_raiz, altura = gera_strutura_arvore_grow(gramatica,
                                                gramatica.opcao_aleatoria(gramatica.regra_inicial),
                                                altura_maxima,
                                                nos
                                                )

    arvore = Arvore(no_raiz, altura)
    arvore.nos = nos
    return arvore
    
"""arvore = Arvore(No(23))
arvore.raiz.add_filho(No(3))
arvore.raiz.add_filho(No(19))
arvore.raiz.filhos[0].add_filho(No(4))
arvore.raiz.filhos[1].add_filho(No(20))

print(arvore)""" 