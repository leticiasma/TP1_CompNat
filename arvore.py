from __future__ import annotations

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

class Arvore():
    def __init__(self, no_raiz:No):
        self.raiz = no_raiz

    def __repr__(self):
        return f'Arvore({self.raiz})'
    
arvore = Arvore(No(23))
arvore.raiz.add_filho(No(3))
arvore.raiz.add_filho(No(19))
arvore.raiz.filhos[0].add_filho(No(4))
arvore.raiz.filhos[1].add_filho(No(20))

print(arvore)