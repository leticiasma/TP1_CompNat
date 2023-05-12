from individuo import Individuo, gera_arvore_grow 
from gramatica import Gramatica
from auxiliares import *
import random
from random import choices
import copy
import statistics

#OK!!!
def gera_arvore_metodo_grow(num_variaveis:int, altura_max_arvore:int) -> Arvore:
    gramatica = Gramatica(num_variaveis)

    #AQUI3
    arvore = gera_arvore_grow(gramatica, altura_max_arvore)
    #AQUI3

    return arvore

#OK!!!
def gera_populacao_inicial(tamanho_populacao:int, num_variaveis:int, altura_max_individuo:int) -> list: 
    individuos = []
    
    for _ in range(tamanho_populacao):
        individuo = Individuo(altura_max_individuo)

        #AQUI2
        individuo.arvore = gera_arvore_metodo_grow(num_variaveis, individuo.altura_max_arvore)
        #AQUI2

        individuos.append(individuo)

    #tinha que retornar individuos de fato e nao arvores
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
    individuos_selecionados_copias = [copy.deepcopy(individuo) for individuo in individuos_selecionados]

    return individuos_selecionados_copias

def selecao_por_torneio(individuos:list, tamanho_populacao:int, df):

    tamanho_torneio = 2
    individuos_selecionados = []

    for _ in range (tamanho_populacao):
        participantes_torneio = random.choices(population=individuos, k=tamanho_torneio)
        fitness_participantes_torneio = calcula_fitness_individuos(participantes_torneio, df)

        indice_fitness_vencedor_torneio = fitness_participantes_torneio.index(min(fitness_participantes_torneio))
        vencedor_torneio = participantes_torneio[indice_fitness_vencedor_torneio]

        individuos_selecionados.append(copy.deepcopy(vencedor_torneio))

    return individuos_selecionados

#Não tá passando por todas as linhas do DF.
def selecao_lexicase(individuos:list, tamanho_populacao:int, df:pd.DataFrame):

    individuos_finais_selecionados = []

    for _ in range(tamanho_populacao):
        #Cada loop do range é UMA seleção. Em cada loop vai excluindo até ficar apenas um selecionado.
        linhas_df_ordem_aleatoria = random.sample(df.to_dict('records'), k=len(df))
        individuos_selecionados = individuos

        for linha in linhas_df_ordem_aleatoria:
            print("A linha que esta vindo ", linha)
            fitness_individuos = []

            for individuo in individuos:
                #É o erro
                fitness_individuo = calcula_fitness_individuo_linha(individuo, linha)
                fitness_individuos.append(fitness_individuo)
            
            melhor_fitness = min(fitness_individuos)
            
            mediana_fitness_individuos = statistics.median(fitness_individuos)
            abs_diferenca_fitness_mediana = [abs(fitness - mediana_fitness_individuos) for fitness in fitness_individuos]
            MAD_linha = statistics.median(abs_diferenca_fitness_mediana)

            melhores_individuos = []

            for indice_individuo in range(len(individuos_selecionados)):
                fitness_individuo = fitness_individuos[indice_individuo]

                if fitness_individuo < melhor_fitness + MAD_linha:
                    melhores_individuos.append(individuos_selecionados[indice_individuo])
            
            individuos_selecionados = melhores_individuos

            if len(individuos_selecionados) == 1:
                break
        
        individuo_aleatorio = random.choice(individuos_selecionados) #Isso às vezes dá IndexError: list index out of range
        individuos_finais_selecionados.append(copy.deepcopy(individuo_aleatorio))
    
    return individuos_finais_selecionados

######################################## OPERAÇÕES GENÉTICAS ########################################
def realiza_crossovers (individuos_selecionados, p_c:float, num_tentativas): #FALTA ATUALIZAR ALTURA, PROFUNDIDADE E LISTA DE NOS

    individuos_pos_crossover = []

    for _ in range(num_tentativas):
        #Seleciona dois indivíduos aleatoriamente
        num_individuos = 2
        par_individuos_copia:list[Individuo,Individuo] = copy.deepcopy(random.choices(population=individuos_selecionados, k=num_individuos))

        # print("Indivíduo 1 selecionado:", par_individuos[0])
        # print("Indivíduo 2 selecionado:", par_individuos[1], "\n\n")

        numero_aleatorio = random.random()

        if numero_aleatorio < p_c:
            no_aleatorio_individuo_0 = par_individuos_copia[0].arvore.sorteia_no()
            no_aleatorio_individuo_1 = par_individuos_copia[1].arvore.sorteia_no()

            # print("Vai fazer crossover. No a ser trocado indivíduo 1: ", no_aleatorio_individuo_0)
            # print("Vai fazer crossover. No a ser trocado indivíduo 2: ", no_aleatorio_encontrado_com_mesmo_tipo, "\n\n")
            
            #Verificar essa lógica e ver se precisa e hard copy para o return
            subarvore_antiga_individuo_0 = no_aleatorio_individuo_0
            subarvore_antiga_individuo_1 = no_aleatorio_individuo_1

            if no_aleatorio_individuo_0.pai == None and no_aleatorio_individuo_1.pai == None:
                print("Ambos são raiz. Continuar com os pais.")
                pass
            
            else:
                if no_aleatorio_individuo_0.pai == None:
                    #Acho que isso atribui a raiz
                    par_individuos_copia[0].arvore.raiz = subarvore_antiga_individuo_1
                    subarvore_antiga_individuo_1.pai.substitui_filho(subarvore_antiga_individuo_1, subarvore_antiga_individuo_0)

                elif subarvore_antiga_individuo_1.pai == None:
                    par_individuos_copia[1].arvore.raiz = subarvore_antiga_individuo_0
                    subarvore_antiga_individuo_0.pai.substitui_filho(subarvore_antiga_individuo_0, subarvore_antiga_individuo_1)

                else:
                #Crossover com termnais nao ta funcionando pq nao tem filhos
                    subarvore_antiga_individuo_0.pai.substitui_filho(subarvore_antiga_individuo_0, subarvore_antiga_individuo_1)
                    subarvore_antiga_individuo_1.pai.substitui_filho(subarvore_antiga_individuo_1, subarvore_antiga_individuo_0)

                subarvore_antiga_individuo_1.pai, subarvore_antiga_individuo_0.pai = subarvore_antiga_individuo_0.pai, subarvore_antiga_individuo_1.pai  

        individuos_pos_crossover.extend(par_individuos_copia) #Confirmar que estou mexendo no par_individuos_copia

    return individuos_pos_crossover

        # print("Pos crossover indivíduo 1:", individuos_pos_crossover[0])
        # print("Pos crossover indivíduo 2:", individuos_pos_crossover[1])
        
        #Aplica ou não crossover
        #Troca os pais pelos filhos

def realiza_mutacoes (individuos_pos_crossover, p_m:float, num_vars, num_tentativas): #FALTA ATUALIZAR ALTURA, PROFUNDIDADE E LISTA DE NOS
    #Seleciona um indivíduo aleatoriamente
    #Aplica ou não mutacao
    #Troca o "pai" pelo filho ou já diretao

    individuos_pos_mutacao = []

    for _ in range(num_tentativas):
        individuo_a_ser_mutado_copia = copy.deepcopy(random.choice(individuos_pos_crossover)) #Ver se compensa fazer 1 random choices com k = n e depois percorrer a lista

        #print("\n\n\nIND ANTES MUTACAO: ", individuo_a_ser_mutado[0].arvore)

        numero_aleatorio = random.random()

        if numero_aleatorio < p_m:
            no_aleatorio_individuo = individuo_a_ser_mutado_copia.arvore.sorteia_no()

            #print("NO A SER MUTADO: ", no_aleatorio_individuo)

            tamanho_max_subarvore = individuo_a_ser_mutado_copia.profundidade_max_arvore - no_aleatorio_individuo.profundidade + 1

            subarvore = gera_arvore_metodo_grow(num_vars, tamanho_max_subarvore)

            if no_aleatorio_individuo.pai == None:
                individuo_a_ser_mutado_copia.arvore.raiz = subarvore.raiz
            else:
                no_aleatorio_individuo.pai.substitui_filho(no_aleatorio_individuo, subarvore.raiz)
                subarvore.raiz.pai = no_aleatorio_individuo
        
        #print("IND DEPOIS MUTACAO: ", individuo_a_ser_mutado[0].arvore)

        individuos_pos_mutacao.append(individuo_a_ser_mutado_copia) #Confirmar que estou mexendo no par_individuos_copia

    return individuos_pos_mutacao

