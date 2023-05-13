from gramatica import Gramatica
import math
import numpy as np
import random

#OK!!!
class No():
    def __init__(self, valor):
        if type(valor) != str:
            self.valor = round(valor, 5)
        else:
            self.valor = valor
        self.pai:No = None
        self.filhos:list[No] = list() #Lista de nós
        self.altura = 0
        self.profundidade = 0

    def add_filho(self, novo_no_filho:'No'):
        self.filhos.append(novo_no_filho)

    def del_filho(self, filho:'No'):
        self.filhos.remove(filho)

    def substitui_filho(self, filho_a_ser_substituido:'No', novo_filho:'No'):

        ##print("OS FILHOS SAO: ", self.filhos)
        ##print("FILHO A TROCAR: ", filho_a_ser_substituido)
        for indice_filho, filho in enumerate(self.filhos):
            if filho is filho_a_ser_substituido:
                self.filhos[indice_filho] = novo_filho
                return
        
        #raise ValueError("NÃO ENCONTROU O FILHO COM IS")
        # index_filho_a_ser_substituido = self.filhos.index(filho_a_ser_substituido)
        

    def __eq__(self, __other: object) -> bool:
        if not isinstance(__other, No):
            return False
        
        return self.valor == __other.valor and self.pai == __other.pai and self.filhos == __other.filhos and self.altura == __other.altura and self.profundidade == __other.profundidade

    def __repr__(self):
        str_filhos = ""
        for filho in self.filhos:
            str_filhos += str(filho)
        
        return f' No(Altura: {self.altura}, Profundidade: {self.profundidade}, Valor:{self.valor}, Filhos: {str_filhos} )'
    
    def avalia_valor(self, linha:dict): #PARA PASSAR SERIES_TODICT (???)
        raise NotImplementedError("Não implementado")
    
#MAIS OU MENOS!!!
class NoTerminal(No):
    def __init__(self, valor):
        super().__init__(valor)

    #CONFERIR
    def avalia_valor(self, linha:dict):
        ###print("A LINHA EH ", linha)
        if type(self.valor) == np.float64 or type(self.valor) == np.int64: #SEI LÁ
            ###print("eh um numero") #Isso ##printava muitas vezes ue
            return self.valor
        elif type(self.valor) == str: #ACHO QUE TÁ RUIM
            if self.valor[0] == "X":
                #return linha[self.valor[0]]
                #Isso às vezes dá KeyError: 1 ou 0
                return linha[self.valor] #do 1 até o final pq pode ser tipo, X23
        else:
            raise ValueError("Ue")

#MAIS OU MENOS!!!
class NoNaoTerminal(No):
    def __init__(self, valor):
        super().__init__(valor)

    #CONFERIR
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

                if not math.isclose(termo_dir, 0, abs_tol=0.000000001): #VER SE FUNCIONA MESMO
                    return termo_esq / termo_dir
                else:
                    return 0 #OU PENSAR EM ALGO MELHOR QUE ISSO
                
            else:
                raise ValueError("Ue")
            
        elif len (self.valor) == 3:

            if self.valor == 'sen':
                return np.sin(self.filhos[0].avalia_valor(linha)) #QUE PORRA EH ESSA?
            elif self.valor == 'cos':
                return np.cos(self.filhos[0].avalia_valor(linha))
            elif self.valor == 'log':

                termo = abs(self.filhos[0].avalia_valor(linha))

                if not math.isclose(termo, 0, abs_tol=0.000000001): #VER SE FUNCIONA MESMO
                    return np.log(termo)
                else:
                    return 0 #OU PENSAR EM ALGO MELHOR QUE ISSO
            else:
                raise ValueError("Ue")
            
        else:
            raise ValueError("Ue")

#OK!!!
class Individuo():
    def __init__(self, altura_max_arvore):
        self.arvore:Arvore = None
        self.altura_max_arvore = altura_max_arvore
        self.profundidade_max_arvore = altura_max_arvore
    
    def __str__(self) -> str:
        return str(self.arvore)

#É a estrutura do indivíduo
#OK!!!
class Arvore():
    def __init__(self, no_raiz:No, altura_atual:int, profundidade_atual:int): #PQ "ALTURA_ATUAL?"
        self.raiz = no_raiz
        #self.fitness = float('inf') #ACHO QUE NEM ESTOU USANDO
        self.altura_atual = altura_atual #acho q a altura da arvore em si preciso atualizar tbm pra eu saber quantos pode add a mais
        self.profundidade_atual = profundidade_atual
        self.nos:list[No] = [] #VER SE A RAIZ ESTA SENDO COLOCADA

    def __repr__(self):
        return f'Arvore(Altura árvore: {self.altura_atual}; Profundidade árvore: {self.profundidade_atual}; Estrutura: **Raiz: {self.raiz}**)'

    # def tem_so_terminal(self, lista_nos:list[No]):
    #     for no in lista_nos:
    #         if not isinstance(no, NoTerminal):
    #             return False
        
    #     return True

    #Talvez não precise se eu já atualizar a altura de início em geração de subárvores em mutacao. Mas cross sim
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

    #OK!!!
    def avalia_individuo(self, linha:dict):
        return self.raiz.avalia_valor(linha)

    def sorteia_no(self) -> No:
        return random.choice(self.nos)
    
    #Lembrar que depois de mutação e crossover a lista de nós precisa estar atualizada! Tanto deletando quanto adicionando
    def add_nos(self, nos:list):
        self.nos.extend(nos) #VER SE TA TENDO CONFUSAO COM A RAIZ OU NAO

    #talvez apagar
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
def gera_estrutura_arvore_grow(gramatica:Gramatica, expansao:list, num_max_niveis_para_adicionar:int, nos:list, profundidade_atual:int):
    #VER SE A LOGICA DE num_max_niveis_para_adicionar-1 tá certa ou se tá fazendo inivíduos menores do que poderia
    if num_max_niveis_para_adicionar == 1: #Caso: Altura máxima da raiz chegando. Só pode adicionar mais um nível.
        ##print("Altura máxima sendo atingida. Vai adicionar um terminal.")
        regra_terminal = gramatica.retorna_regra_terminal_aleatoria()
        no_criado = NoTerminal(gramatica.retorna_opcao_aleatoria_regra(regra_terminal))
        no_criado.altura = 0 #VERIFICAR
        no_criado.profundidade = profundidade_atual
        ###print("O no criado foi: ", no_criado)
        nos.append(no_criado)
        
        return no_criado, 0, profundidade_atual #Altura e depois profundidade
    
    if len(expansao) == 1: #Caso: sorteado um nó do tipo var ou const, mas isso aqui só valeria para expr... e os outros níveis?
        ###print("A expansao foi const ou var")
        #Cria um NoTerminal, mas acho que não precisaria ser
        no_criado = NoTerminal(gramatica.retorna_opcao_aleatoria_regra(expansao[0]))
        no_criado.altura = 0 #VERIFICAR
        no_criado.profundidade = profundidade_atual
        nos.append(no_criado)

        return no_criado, 0, profundidade_atual
    
    elif len(expansao) == 2:
        ###print("A expansao foi opun expr")
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
        ###print("A expansão foi expr opbin expr")
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

#OK!!!       
def gera_arvore_grow(gramatica:Gramatica, altura_max_arvore:int, profundidade_de_onde_iniciar)->Arvore: #mudei aqui de 'Arvore' para Arvore
    nos = list()

    #AQUI4
    no_raiz, altura_gerada, profundidade_gerada = gera_estrutura_arvore_grow(gramatica,
                                                gramatica.retorna_opcao_aleatoria_regra(gramatica.regra_inicial),
                                                altura_max_arvore,
                                                nos, profundidade_de_onde_iniciar)
    ###print("ALTURA GERADA ARVORE", altura_gerada)
    #AQUI4

    arvore = Arvore(no_raiz, altura_gerada, profundidade_gerada)
    ##print("A ARVORE GERADA: ", arvore)
    ###print("Altura raiz: ", arvore.raiz.altura)
    arvore.add_nos(nos)
    return arvore