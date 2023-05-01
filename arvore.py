from __future__ import annotations

from gramatica import Gramatica

class No():
    def __init__(self, valor):
        self.valor = valor
        self.filhos = list() #lista de nós

    def add_filho(self, novo_no_filho:No):
        self.filhos.append(novo_no_filho)

    def del_filhos(self):
        self.filhos = list()

    def __repr__(self):
        str_filhos = ""
        for filho in self.filhos:
            str_filhos += filho.__repr__()
        
        return f'No(Valor:{self.valor}, Filhos: {str_filhos})'

class NoTerminal(No):
    def __init__(self, valor):
        super().__init__(valor)

class NoNaoTerminal(No):
    def __init__(self, valor):
        super().__init__(valor)

#É o indivíduo
class Arvore():
    def __init__(self, no_raiz:No, altura_atual:int):
        self.raiz = no_raiz
        self.fitness = float('inf')
        self.altura = altura_atual

    def __repr__(self):
        return f'Arvore(altura: {self.altura}, {self.raiz})'
    
    @staticmethod
    def gera_strutura_arvore_grow(gramatica:Gramatica, expansao:list, t_max:int)-> tuple(No, int):

        print(expansao)

        if t_max == 1:
            regra_terminal = gramatica.regra_terminal_aleatoria()
            return NoTerminal(gramatica.opcao_aleatoria(regra_terminal)), 1
        
        if len(expansao) == 1:
            return NoTerminal(gramatica.opcao_aleatoria(expansao[0])), 1
        
        elif len(expansao) == 2:
            no_filho, altura_filho = Arvore.gera_strutura_arvore_grow(gramatica,
                                                        gramatica.opcao_aleatoria(expansao[1]),
                                                        t_max-1)
            no_atual = NoNaoTerminal(gramatica.opcao_aleatoria(expansao[0]))
            no_atual.add_filho(no_filho)
            return no_atual, altura_filho+1
        
        elif len(expansao) == 3:
            no_filho_esq, altura_filho_esq = Arvore.gera_strutura_arvore_grow(gramatica,
                                                        gramatica.opcao_aleatoria(expansao[0]),
                                                        t_max-1)
            no_filho_dir, altura_filho_dir = Arvore.gera_strutura_arvore_grow(gramatica,
                                                        gramatica.opcao_aleatoria(expansao[2]),
                                                        t_max-1)
            
            no_atual = NoNaoTerminal(gramatica.opcao_aleatoria(expansao[1]))
            no_atual.add_filho(no_filho_esq)
            no_atual.add_filho(no_filho_dir)
        
            return no_atual, max([altura_filho_dir, altura_filho_esq])+1
    
    @staticmethod
    def gera_arvore_grow(gramatica:Gramatica, altura_maxima:int)->Arvore:
        no_raiz, altura = Arvore.gera_strutura_arvore_grow(gramatica,
                                                   gramatica.opcao_aleatoria(gramatica.regra_inicial),
                                                   altura_maxima
                                                   )

        return Arvore(no_raiz, altura)
    
"""arvore = Arvore(No(23))
arvore.raiz.add_filho(No(3))
arvore.raiz.add_filho(No(19))
arvore.raiz.filhos[0].add_filho(No(4))
arvore.raiz.filhos[1].add_filho(No(20))

print(arvore)""" 