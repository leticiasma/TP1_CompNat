from individuo import Individuo, gera_arvore_grow 
from gramatica import Gramatica
from auxiliares import *
import random
from random import choices
import copy

#OK!!!
def gera_arvore_metodo_grow(num_variaveis:int, altura_max_arvore:int) -> Arvore:
    gramatica = Gramatica(num_variaveis)

    return gera_arvore_grow(gramatica, altura_max_arvore)

#OK!!!
def gera_populacao_inicial(tamanho_populacao:int, num_variaveis:int, altura_max_individuo:int) -> list: 
    individuos = []
    
    for _ in range(tamanho_populacao):
        individuo = Individuo(altura_max_individuo)
        individuo.arvore = gera_arvore_metodo_grow(num_variaveis, altura_max_individuo)
        individuos.append(individuo)

    return individuos

#OK!!!
def calcula_fitness_individuos(individuos:list, df):
    fitness_individuos = []

    for individuo in individuos:
        fitness = calcula_fitness_individuo(individuo, df)
        fitness_individuos.append(fitness)
    
    return fitness_individuos

######################################## TIPOS DE SELEÇÃO ########################################
def selecao_por_roleta(individuos:list, tamanho_populacao:int, df):
    fitness_individuos = calcula_fitness_individuos (individuos, df)
    soma_fitness = sum(fitness_individuos)

    pesos_selecao_individuos = [] #VER SE ISSO VAI ESTAR CERTO MESMO, SE AS PROB MAIORES BATEM COM AS MENORES FITNESS 
    for fitness_individuo in fitness_individuos:
        pesos_selecao_individuos.append(1 - (fitness_individuo/soma_fitness))

    individuos_selecionados = random.choices(individuos, pesos_selecao_individuos, k=tamanho_populacao)

    return individuos_selecionados

def selecao_por_torneio(individuos:list, tamanho_populacao:int, df):

    tamanho_torneio = 2
    individuos_selecionados = []

    for _ in range (tamanho_populacao):
        participantes_torneio = random.choices(population=individuos, k=tamanho_torneio)
        fitness_participantes_torneio = calcula_fitness_individuos(participantes_torneio, df)

        indice_fitness_vencedor_torneio = fitness_participantes_torneio.index(min(fitness_participantes_torneio))
        vencedor_torneio = participantes_torneio[indice_fitness_vencedor_torneio]

        individuos_selecionados.append(vencedor_torneio)

    return individuos_selecionados

def selecao_lexicase(individuos:list, tamanho_populacao:int, df:pd.DataFrame):

    for _ in range(tamanho_populacao):
        linhas_df_ordem_aleatoria = random.sample(df.values.tolist(), k=len(df))

        for linha in linhas_df_ordem_aleatoria:
            for individuo in individuos:
                resultado_avaliacao_individuo = individuo.arvore.avalia_individuo(linha) #VER SE DE FATO A LINHA JÁ É UM DICIONARIO PRINTANDO
        
    
    
    
    pass

######################################## OPERAÇÕES GENÉTICAS ########################################
def realiza_crossovers (individuos_selecionados, p_c):
    #Seleciona dois indivíduos aleatoriamente

    num_individuos = 2
    par_individuos:list[Individuo,Individuo] = random.choices(population=individuos_selecionados, k=num_individuos)
    numero_aleatorio = random.random()

    # print("Indivíduo 1 selecionado:", par_individuos[0])
    # print("Indivíduo 2 selecionado:", par_individuos[1], "\n\n")

    if numero_aleatorio < float(p_c):
        no_aleatorio_individuo_0 = par_individuos[0].arvore.sorteia_no()

        tipo_no_aleatorio_individuo_0 = type(no_aleatorio_individuo_0)
        #NÃO SEI SE VALE TROCANDO UM OPBIN POR UM OPUN POR EXEMPLO, MESMO AMBOS SENDO NAO TERMINAIS
        no_aleatorio_encontrado_com_mesmo_tipo = par_individuos[1].arvore.procura_no(tipo_no_aleatorio_individuo_0)

        if no_aleatorio_encontrado_com_mesmo_tipo == None:
            print("Não pôde realizar crossover, nós com tipos iguais não encontrados")
        else:
            # print("Vai fazer crossover. No a ser trocado indivíduo 1: ", no_aleatorio_individuo_0)
            # print("Vai fazer crossover. No a ser trocado indivíduo 2: ", no_aleatorio_encontrado_com_mesmo_tipo, "\n\n")
            #Crossover com termnais nao ta funcionando pq nao tem filhos
            subarvore_antiga_individuo_0 = no_aleatorio_individuo_0
            subarvore_antiga_individuo_0.pai.del_filho(no_aleatorio_individuo_0)
            subarvore_antiga_individuo_0.pai.add_filho(no_aleatorio_encontrado_com_mesmo_tipo)
            subarvore_antiga_individuo_1 = no_aleatorio_encontrado_com_mesmo_tipo
            subarvore_antiga_individuo_1.pai.del_filho(no_aleatorio_encontrado_com_mesmo_tipo)
            subarvore_antiga_individuo_1.pai.add_filho(subarvore_antiga_individuo_0)
            
            #no_aleatorio_individuo_0.filhos = no_aleatorio_encontrado_com_mesmo_tipo.filhos
            #no_aleatorio_encontrado_com_mesmo_tipo.filhos = subarvore_antiga_individuo_0
    else:
        print("NÃO FEZ O CROSSOVER por probabilidade.")       

    individuos_pos_crossover = par_individuos

    # print("Pos crossover indivíduo 1:", individuos_pos_crossover[0])
    # print("Pos crossover indivíduo 2:", individuos_pos_crossover[1])
    
    #Aplica ou não crossover
    #Troca os pais pelos filhos

def realiza_mutacoes (individuos, p_m, num_vars):
    #Seleciona um indivíduo aleatoriamente
    #Aplica ou não mutacao
    #Troca o "pai" pelo filho ou já diretao
    num_individuos = 1
    individuo_a_ser_mutado = random.choices(population=individuos, k=num_individuos)
    numero_aleatorio = random.random()

    print("\n\n\nIND ANTES MUTACAO: ", individuo_a_ser_mutado[0].arvore)

    if numero_aleatorio < float(p_m):
        no_aleatorio_individuo = individuo_a_ser_mutado[0].arvore.sorteia_no()

        print("NO A SER MUTADO: ", no_aleatorio_individuo)

        tamanho_max_subarvore = individuo_a_ser_mutado[0].altura_max_arvore - no_aleatorio_individuo.altura

        subarvore = gera_arvore_metodo_grow(num_vars, tamanho_max_subarvore)

        no_aleatorio_individuo.pai.del_filho(no_aleatorio_individuo)
        no_aleatorio_individuo.pai.add_filho(subarvore.raiz)
    
    print("IND DEPOIS MUTACAO: ", individuo_a_ser_mutado[0].arvore)

