from individuo import Individuo
from gramatica import Gramatica
from auxiliares import *
import random
from random import choices
from typing import List
import copy
import statistics

def gera_populacao_inicial(tamanho_populacao:int, num_variaveis:int, altura_max_individuo:int) -> list: 
    individuos = []
    
    for _ in range(tamanho_populacao):
        individuo = Individuo(altura_max_individuo)

        individuo.arvore = gera_arvore_metodo_grow(num_variaveis, individuo.altura_max_arvore)

        individuos.append(individuo)

    return individuos

def calcula_fitness_individuos(individuos:list, df) -> np.ndarray:
    fitness_individuos = np.zeros(len(individuos))

    for ind_idx, individuo in enumerate(individuos):
        fitness_individuos[ind_idx] = calcula_fitness_individuo(individuo, df)
    
    return fitness_individuos

######################################## TIPOS DE SELEÇÃO ########################################
def selecao_por_roleta(individuos:list, tamanho_populacao:int, df):
    fitness_individuos = calcula_fitness_individuos(individuos, df)
    soma_fitness = np.sum(fitness_individuos)

    pesos_selecao_individuos:np.ndarray = (1 - (fitness_individuos/soma_fitness))

    individuos_selecionados = choices(individuos, pesos_selecao_individuos, k=tamanho_populacao)
    individuos_selecionados_copias = [copy.deepcopy(individuo) for individuo in individuos_selecionados]

    return individuos_selecionados_copias

def selecao_por_torneio(individuos:list, tamanho_populacao:int, df):

    tamanho_torneio = 2
    individuos_selecionados = []

    for _ in range (tamanho_populacao):
        participantes_torneio = choices(population=individuos, k=tamanho_torneio)
        fitness_participantes_torneio = calcula_fitness_individuos(participantes_torneio, df)

        indice_fitness_vencedor_torneio = np.argmin(fitness_participantes_torneio)
        vencedor_torneio = participantes_torneio[indice_fitness_vencedor_torneio]

        individuos_selecionados.append(copy.deepcopy(vencedor_torneio))

    return individuos_selecionados

#Não tá passando por todas as linhas do DF.
def selecao_lexicase(individuos:list, tamanho_populacao:int, df:pd.DataFrame):

    df_para_dict = df.to_dict('records')

    individuos_finais_selecionados = []

    for _ in range(tamanho_populacao):
        #Cada loop do range é UMA seleção. Em cada loop vai excluindo até ficar apenas um selecionado.
        linhas_df_ordem_aleatoria = random.sample(df_para_dict, k=len(df))
        individuos_selecionados_copia = copy.deepcopy(individuos)

        for linha in linhas_df_ordem_aleatoria:
            fitness_individuos = []

            for individuo in individuos_selecionados_copia:
                #É o erro
                fitness_individuo = calcula_fitness_individuo_linha(individuo, linha)
                fitness_individuos.append(fitness_individuo)
            
            melhor_fitness = min(fitness_individuos)
            print("MELHOR FITNESS ", melhor_fitness)
            
            mediana_fitness_individuos = statistics.median(fitness_individuos)
            abs_diferenca_fitness_mediana = [abs(fitness - mediana_fitness_individuos) for fitness in fitness_individuos]
            MAD_linha = statistics.median(abs_diferenca_fitness_mediana)
            print("MAD_LINHA ", MAD_linha)

            melhores_individuos = []

            for indice_individuo in range(len(individuos_selecionados_copia)):
                fitness_individuo = fitness_individuos[indice_individuo]
                print("FITNESS INDIVIDUO ", fitness_individuo)

                if fitness_individuo <= melhor_fitness + MAD_linha:
                    print("É DOS MELHORES.")
                    melhores_individuos.append(copy.deepcopy(individuos_selecionados_copia[indice_individuo]))
                else:
                    print("NAO ENTROU")
            
            individuos_selecionados_copia = melhores_individuos

            if len(individuos_selecionados_copia) == 1:
                break
        
        print("LEN INDIV SELEC ", len(individuos_selecionados_copia))
        individuo_aleatorio = random.choice(individuos_selecionados_copia) #Isso às vezes dá IndexError: list index out of range
        individuos_finais_selecionados.append(copy.deepcopy(individuo_aleatorio))
    
    return individuos_finais_selecionados

######################################## OPERAÇÕES GENÉTICAS ########################################
def realiza_crossovers (df, individuos_selecionados, p_c:float, num_tentativas):

    num_individuos_gerados_crossover_melhores_fitness_media_pais = 0
    num_individuos_gerados_crossover_piores_fitness_media_pais = 0
    individuos_pos_crossover = []

    for _ in range(num_tentativas):
        num_individuos = 2
        par_individuos = choices(population=individuos_selecionados, k=num_individuos)
        par_individuos_copia:list[Individuo,Individuo] = copy.deepcopy(par_individuos)

        numero_aleatorio = random.random()

        if numero_aleatorio < p_c:
            alturas_da_para_trocar = False

            while not alturas_da_para_trocar:
                no_aleatorio_individuo_0:No = par_individuos_copia[0].arvore.sorteia_no()
                no_aleatorio_individuo_1:No = par_individuos_copia[1].arvore.sorteia_no()

                if no_aleatorio_individuo_0.profundidade + no_aleatorio_individuo_1.altura <= par_individuos_copia[0].altura_max_arvore:
                    if no_aleatorio_individuo_1.profundidade + no_aleatorio_individuo_0.altura <= par_individuos_copia[0].altura_max_arvore:
                        alturas_da_para_trocar = True

            if no_aleatorio_individuo_0.pai == None and no_aleatorio_individuo_1.pai == None:
                pass
            
            else:
                if no_aleatorio_individuo_0.pai == None:
                    par_individuos_copia[0].arvore.raiz = no_aleatorio_individuo_1
                    no_aleatorio_individuo_1.pai.substitui_filho(no_aleatorio_individuo_1, no_aleatorio_individuo_0)

                elif no_aleatorio_individuo_1.pai == None:
                    par_individuos_copia[1].arvore.raiz = no_aleatorio_individuo_0
                    no_aleatorio_individuo_0.pai.substitui_filho(no_aleatorio_individuo_0, no_aleatorio_individuo_1)

                else:
                    no_aleatorio_individuo_1:No = no_aleatorio_individuo_1
                    #Crossover com termnais nao ta funcionando pq nao tem filhos
                    no_aleatorio_individuo_0.pai.substitui_filho(no_aleatorio_individuo_0, no_aleatorio_individuo_1)
                    no_aleatorio_individuo_1.pai.substitui_filho(no_aleatorio_individuo_1, no_aleatorio_individuo_0)

                no_aleatorio_individuo_1.pai, no_aleatorio_individuo_0.pai = no_aleatorio_individuo_0.pai, no_aleatorio_individuo_1.pai  

                for individuo in par_individuos_copia:
                    individuo.cache_fitness_dataset = None

        for individuo in par_individuos_copia:
            
            individuo.arvore.nos = []
            lista_nos_a_serem_adicionados = []
            _ = individuo.arvore.atualiza_lista_nos(individuo.arvore.raiz, lista_nos_a_serem_adicionados)
            individuo.arvore.add_nos(lista_nos_a_serem_adicionados)

            nova_altura_raiz = individuo.arvore.atualiza_alturas_e_retorna(individuo.arvore.raiz)
            individuo.arvore.altura_atual = nova_altura_raiz
            individuo.arvore.atualiza_profundidades(individuo.arvore.raiz, 0)
            individuo.arvore.profundidade_atual = individuo.arvore.raiz.profundidade

        individuos_pos_crossover.extend(par_individuos_copia)

        fitnesses_pais = calcula_fitness_individuos(par_individuos, df)
        fitnesses_filhos = calcula_fitness_individuos(par_individuos_copia, df)

        fitness_media_pais = np.mean(fitnesses_pais)
        num_individuos_gerados_crossover_melhores_fitness_media_pais += np.sum(fitnesses_filhos > fitness_media_pais)
        num_individuos_gerados_crossover_piores_fitness_media_pais += np.sum(fitnesses_filhos <= fitness_media_pais)

    return individuos_pos_crossover, num_individuos_gerados_crossover_melhores_fitness_media_pais, num_individuos_gerados_crossover_piores_fitness_media_pais

def realiza_mutacoes (individuos_pos_crossover, p_m:float, num_vars, num_tentativas) -> List[Individuo]:
    individuos_pos_mutacao = []

    for _ in range(num_tentativas):
        individuo_a_ser_mutado_copia:Individuo = copy.deepcopy(random.choice(individuos_pos_crossover)) #Ver se compensa fazer 1 random choices com k = n e depois percorrer a lista

        numero_aleatorio = random.random()

        if numero_aleatorio < p_m:
            no_aleatorio_individuo = individuo_a_ser_mutado_copia.arvore.sorteia_no()

            tamanho_max_subarvore = individuo_a_ser_mutado_copia.profundidade_max_arvore - no_aleatorio_individuo.profundidade + 1

            subarvore = gera_arvore_metodo_grow(num_vars, tamanho_max_subarvore, no_aleatorio_individuo.profundidade)

            if no_aleatorio_individuo.pai == None:
                individuo_a_ser_mutado_copia.arvore.raiz = subarvore.raiz
            else:
                no_aleatorio_individuo.pai.substitui_filho(no_aleatorio_individuo, subarvore.raiz)
                subarvore.raiz.pai = no_aleatorio_individuo.pai
        
            individuo_a_ser_mutado_copia.arvore.nos = []
            lista_nos_a_serem_adicionados = []
            _ = individuo_a_ser_mutado_copia.arvore.atualiza_lista_nos(individuo_a_ser_mutado_copia.arvore.raiz, lista_nos_a_serem_adicionados)
            individuo_a_ser_mutado_copia.arvore.add_nos(lista_nos_a_serem_adicionados)

            individuo_a_ser_mutado_copia.cache_fitness_dataset = None

            nova_altura_raiz = individuo_a_ser_mutado_copia.arvore.atualiza_alturas_e_retorna(individuo_a_ser_mutado_copia.arvore.raiz)
            individuo_a_ser_mutado_copia.arvore.altura_atual = nova_altura_raiz
            individuo_a_ser_mutado_copia.arvore.atualiza_profundidades(individuo_a_ser_mutado_copia.arvore.raiz, 0)
            individuo_a_ser_mutado_copia.arvore.profundidade_atual = individuo_a_ser_mutado_copia.arvore.raiz.profundidade

        individuos_pos_mutacao.append(individuo_a_ser_mutado_copia)

    return individuos_pos_mutacao

