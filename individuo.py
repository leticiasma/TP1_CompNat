from gramatica import Gramatica
import math
import numpy as np
import random

class No():
    def __init__(self, valor):
        if type(valor) != str:
            self.valor = round(valor, 5)
        else:
            self.valor = valor
        self.pai:No = None
        self.filhos:list[No] = list()
        self.altura = 0
        self.profundidade = 0

    def add_filho(self, novo_no_filho:'No'):
        self.filhos.append(novo_no_filho)

    def substitui_filho(self, filho_a_ser_substituido:'No', novo_filho:'No'):
        for indice_filho, filho in enumerate(self.filhos):
            if filho is filho_a_ser_substituido:
                self.filhos[indice_filho] = novo_filho
                return        

    def __repr__(self):
        str_filhos = ""
        for filho in self.filhos:
            str_filhos += str(filho)
        
        return f' No(Altura: {self.altura}, Profundidade: {self.profundidade}, Valor:{self.valor}, Filhos: {str_filhos} )'
    
    def avalia_valor(self, linha:dict):
        raise NotImplementedError("Não implementado")
    
class NoTerminal(No):
    def __init__(self, valor):
        super().__init__(valor)

    def avalia_valor(self, linha:dict):
        if type(self.valor) != str:
            return self.valor
        else:
            if self.valor[0] == "X":
                #Isso às vezes dá KeyError: 1 ou 0
                return linha[self.valor]

class NoNaoTerminal(No):
    def __init__(self, valor):
        super().__init__(valor)

    def avalia_valor(self, linha:dict):
        if len(self.valor) == 1:
            if self.valor == '+':
                return self.filhos[0].avalia_valor(linha) + self.filhos[1].avalia_valor(linha)
            elif self.valor == '-':
                return self.filhos[0].avalia_valor(linha) - self.filhos[1].avalia_valor(linha)
            elif self.valor == '*': 
                return self.filhos[0].avalia_valor(linha) * self.filhos[1].avalia_valor(linha)
            elif self.valor == '/':
                termo_esq = self.filhos[0].avalia_valor(linha)
                termo_dir = self.filhos[1].avalia_valor(linha)

                if not math.isclose(termo_dir, 0, abs_tol=0.000000001):
                    return termo_esq / termo_dir
                else:
                    return 0
            
        elif len (self.valor) == 3:
            if self.valor == 'sen':
                return np.sin(self.filhos[0].avalia_valor(linha))
            elif self.valor == 'cos':
                return np.cos(self.filhos[0].avalia_valor(linha))
            elif self.valor == 'log':

                termo = abs(self.filhos[0].avalia_valor(linha))

                if not math.isclose(termo, 0, abs_tol=0.000000001):
                    return np.log(termo)
                else:
                    return 0

class Individuo():
    def __init__(self, altura_max_arvore):
        self.arvore:Arvore = None
        self.altura_max_arvore = altura_max_arvore
        self.profundidade_max_arvore = altura_max_arvore
        self.cache_fitness_dataset = None
    
    def __str__(self) -> str:
        return str(self.arvore)

#É a estrutura do indivíduo
class Arvore():
    def __init__(self, no_raiz:No, altura_atual:int, profundidade_atual:int):
        self.raiz = no_raiz
        self.altura_atual = altura_atual
        self.profundidade_atual = profundidade_atual
        self.nos:list[No] = []

    def __repr__(self):
        return f'Arvore(Altura árvore: {self.altura_atual}; Profundidade árvore: {self.profundidade_atual}; Estrutura: **Raiz: {self.raiz}**)'

    def atualiza_alturas_e_retorna(self, no:No):
        if type(no) is NoTerminal:
            no.altura = 0
            return 0
        
        alturas_filhos = []
        for filho in no.filhos:
            alturas_filhos.append(self.atualiza_alturas_e_retorna(filho))
            
        no.altura = max(alturas_filhos)+1
        return no.altura

    def atualiza_profundidades(self, no:No, profundidade:int):
        no.profundidade = profundidade
        for filho in no.filhos:
            self.atualiza_profundidades(filho, profundidade+1)     

    def atualiza_lista_nos(self, no:No, nos_a_serem_adicionados):
        nos_a_serem_adicionados.append(no)

        for filho in no.filhos:
            self.atualiza_lista_nos(filho, nos_a_serem_adicionados)
        
        return nos_a_serem_adicionados

    def avalia_individuo(self, linha:dict):
        return self.raiz.avalia_valor(linha)

    def sorteia_no(self) -> No:
        return random.choice(self.nos)
    
    def add_nos(self, nos:list):
        self.nos.extend(nos)