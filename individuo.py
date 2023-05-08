from gramatica import Gramatica
import math
import numpy as np
import random

#OK!!!
class No():
    def __init__(self, valor):
        self.valor = valor
        self.filhos:list[Individuo] = list() #Lista de nós
        self.altura = 0

    def add_filho(self, novo_no_filho:'No'):
        self.filhos.append(novo_no_filho)

    def del_filhos(self): #ACHO QUE NEM ESTOU USANDO
        self.filhos = list()

    def __repr__(self):
        str_filhos = ""
        for filho in self.filhos:
            str_filhos += filho.__repr__()
        
        return f' No(Altura: {self.altura}, Valor:{self.valor}, Filhos: {str_filhos} )'
    
    def avalia_valor(self, linha:dict): #PARA PASSAR SERIES_TODICT (???)
        raise NotImplementedError("Não implementado")
    
#MAIS OU MENOS!!!
class NoTerminal(No):
    def __init__(self, valor):
        super().__init__(valor)

    #CONFERIR
    def avalia_valor(self, linha:dict):
        if type(self.valor) == np.float64 or type(self.valor) == np.int64: #SEI LÁ
            return self.valor
        elif type(self.valor) == list: #ACHO QUE TÁ RUIM
            if self.valor[0][0] == "X":
                return linha[self.valor[0]]
        else:
            raise ValueError("Ue")

#MAIS OU MENOS!!!
class NoNaoTerminal(No):
    def __init__(self, valor):
        super().__init__(valor)

    #CONFERIR
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

                if not math.isclose(termo_dir, 0, abs_tol=0.000000001): #VER SE FUNCIONA MESMO
                    return termo_esq / termo_dir
                else:
                    return 0 #OU PENSAR EM ALGO MELHOR QUE ISSO
                
            else:
                raise ValueError("Ue")
            
        elif len (self.valor[0]) == 3:

            if self.valor[0] == 'sen':
                return np.sin(self.filhos[0].avalia_valor(linha)) #QUE PORRA EH ESSA?
            elif self.valor[0] == 'cos':
                return np.cos(self.filhos[0].avalia_valor(linha))
            elif self.valor[0] == 'log':
                return np.log(abs(self.filhos[0].avalia_valor(linha))) #VER SE DEIXA MESMO ESSE ABS
            elif self.valor[0] == 'exp':
                return np.exp(self.filhos[0].avalia_valor(linha))
            else:
                raise ValueError("Ue")
            
        else:
            raise ValueError("Ue")

#OK!!!
class Individuo():
    def __init__(self, altura_max_arvore):
        self.arvore = None
        self.altura_max_arvore = altura_max_arvore
    
    def __str__(self) -> str:
        return str(self.arvore)

#É a estrutura do indivíduo
#OK!!!
class Arvore():
    def __init__(self, no_raiz:No, altura_atual:int): #PQ "ALTURA_ATUAL?"
        self.raiz = no_raiz
        self.fitness = float('inf') #ACHO QUE NEM ESTOU USANDO
        self.altura = altura_atual
        self.nos = []

    def __repr__(self):
        return f'Arvore(Altura árvore: {self.altura}; Estrutura: **Raiz: {self.raiz}**)'

    def tem_so_terminal(self, lista_nos:list[No]):
        for no in lista_nos:
            if not isinstance(no, NoTerminal):
                return False
        
        return True

    #Talvez não precise se eu já atualizar a altura de início em geração de subárvores em mutacao e em crossover
    def atualiza_alturas(self):
        nos_nivel_atual = [self.raiz]
        altura_raiz = 0

        while self.tem_so_terminal(nos_nivel_atual) == False:
            pass
        #AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            

    #OK!!!
    def avalia_individuo(self, linha:dict):
        return self.raiz.avalia_valor(linha)

    def sorteia_no(self):
        print("NOS:", self.nos)
        return random.choice(self.nos)
    
    def add_nos(self, nos:list):
        self.nos.extend(nos) #VER SE TA TENDO CONFUSAO COM A RAIZ OU NAO

    def procura_no(self, tipo):
        nos_com_tipo_buscado = []

        for no in self.nos:
            if type(no) == tipo:
                nos_com_tipo_buscado.append(no)
            
        if len(nos_com_tipo_buscado) != 0:
            return random.choice(nos_com_tipo_buscado)
        else:
            return None

#PIOR PARTE, CONFERIR BEM
def gera_estrutura_arvore_grow(gramatica:Gramatica, expansao:list, t_max:int, nos:list, altura_atual):

    if t_max == 1:
        regra_terminal = gramatica.retorna_regra_terminal_aleatoria()
        no_criado = NoTerminal(gramatica.retorna_opcao_aleatoria_regra(regra_terminal))
        no_criado.altura = altura_atual
        nos.append(no_criado)
        
        return no_criado, 1
    
    if len(expansao) == 1:
        no_criado = NoTerminal(gramatica.retorna_opcao_aleatoria_regra(expansao[0]))
        no_criado.altura = altura_atual
        nos.append(no_criado)

        return no_criado, 1
    
    elif len(expansao) == 2:
        no_filho, altura_filho = gera_estrutura_arvore_grow(gramatica,
                                                    gramatica.retorna_opcao_aleatoria_regra(expansao[1]),
                                                    t_max-1, nos, altura_atual+1)
        
        no_criado = NoNaoTerminal(gramatica.retorna_opcao_aleatoria_regra(expansao[0]))
        no_criado.altura = altura_atual
        nos.append(no_criado)
        no_criado.add_filho(no_filho)

        return no_criado, altura_filho+1
    
    elif len(expansao) == 3:
        no_filho_esq, altura_filho_esq = gera_estrutura_arvore_grow(gramatica,
                                                    gramatica.retorna_opcao_aleatoria_regra(expansao[0]),
                                                    t_max-1, nos, altura_atual+1)
        
        no_filho_dir, altura_filho_dir = gera_estrutura_arvore_grow(gramatica,
                                                    gramatica.retorna_opcao_aleatoria_regra(expansao[2]),
                                                    t_max-1, nos, altura_atual+1)
        
        no_criado = NoNaoTerminal(gramatica.retorna_opcao_aleatoria_regra(expansao[1]))
        no_criado.add_filho(no_filho_esq)
        no_criado.add_filho(no_filho_dir)
        nos.append(no_criado)
    
        return no_criado, max([altura_filho_dir, altura_filho_esq])+1

#OK!!!       
def gera_arvore_grow(gramatica:Gramatica, altura_max_arvore:int)->'Arvore':
    nos = list()
    no_raiz, altura = gera_estrutura_arvore_grow(gramatica,
                                                gramatica.retorna_opcao_aleatoria_regra(gramatica.regra_inicial),
                                                altura_max_arvore,
                                                nos, 0
                                                )
    arvore = Arvore(no_raiz, altura)
    arvore.add_nos(nos)
    return arvore