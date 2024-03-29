from etapas import gera_populacao_inicial, calcula_fitness_individuos, calcula_fitness_individuo, selecao_por_roleta, selecao_por_torneio, selecao_lexicase, realiza_crossovers, realiza_mutacoes
import random
import pandas as pd 
import sys
from individuo import *
import copy
import csv
from tqdm import tqdm

#print("Seed usada:", seed)
#random.seed(4438)
#seed boa: 327

def main():
    num_csv = 0

    df_treino = pd.read_csv(sys.argv[1])
    df_teste = pd.read_csv(sys.argv[2])
    num_variaveis = len(df_treino.columns)-1 #Número de variáveis do dataset
    nomes_colunas = [f'X{i}' for i in range(num_variaveis)]
    nomes_colunas.append('y')
    df_treino.columns = nomes_colunas
    df_teste.columns = nomes_colunas

    num_geracoes = int(sys.argv[3]) #Num de iterações
    tamanho_populacao = int(sys.argv[4])
    altura_max_individuo = int(sys.argv[5]) 
    tipo_selecao = str(sys.argv[6])
    p_c = float(sys.argv[7]) #Probabilidade crossover entre dois indivíduos
    p_m = float(sys.argv[8]) #Probabilidade mutação de um indivíduo
    elitismo = int(sys.argv[9]) #0 para não elitismo e 1 para elitismo

    tamanho_populacao_original = copy.deepcopy(tamanho_populacao)

    if elitismo == 1:
        tamanho_populacao -= 1

    with open('melhor_fitness_treino_vs_teste.csv', 'w', encoding='UTF8', newline='') as f:
        titulos_colunas_f = ['fit_melhor_indiv_da_iteracao_base_treino', 'fit_melhor_indiv_da_iteracao_base_teste']
        writerf = csv.writer(f)
        writerf.writerow(titulos_colunas_f)

        for _ in tqdm(range(30)):
            
            seed = random.randrange(100000)
            random.seed(seed)

            nome_arquivo_estatisticas = 'estatisticas'+str(num_csv)+'_ger'+str(num_geracoes)+'_pop'+str(tamanho_populacao_original)+'_selecao_'+tipo_selecao+'_pc'+str(p_c)+'_pm'+str(p_m)+'.csv'
            with open(nome_arquivo_estatisticas, 'w', encoding='UTF8', newline='') as g:
                titulos_colunas_g = ['seed_aleatoria_usada', 'fit_melhor_indiv', 'fit_pior_indiv', 'fit_media_pop', 'indiv_repetidos_pop', 'indiv_cross_melhores_que_pais', 'indiv_cross_piores_que_pais']
                writerg = csv.writer(g)
                writerg.writerow(titulos_colunas_g)

                #ESTATÍSTICAS QUE SERÃO COLETADAS POR GERAÇÃO
                fitness_melhor_individuo = math.inf
                fitness_pior_individuo = math.inf
                fitness_media_populacao = math.inf
                num_individuos_repetidos_populacao = math.inf
                num_individuos_gerados_crossover_melhores_fitness_media_pais = 0
                num_individuos_gerados_crossover_piores_fitness_media_pais = 0
                
                #Gera a população inicial de indivíduos aleatoriamente seguindo regras da gramática
                individuos_iniciais = gera_populacao_inicial(tamanho_populacao, num_variaveis, altura_max_individuo)

                populacao_atual = individuos_iniciais

                #Por certo número de gerações ("critério de parada"), repetir o ciclo
                for _ in range(num_geracoes):

                    #Selecionar indivíduos
                    if tipo_selecao == 'r':
                        #Cálculo da fitness de toda a população calculada no início de "selecao_por_roleta"
                        individuos_selecionados = selecao_por_roleta(populacao_atual, tamanho_populacao, df_treino)
                    elif tipo_selecao == 't':
                        #A fitness é calculada para os participantes de cada torneio
                        individuos_selecionados = selecao_por_torneio(populacao_atual, tamanho_populacao, df_treino)
                    elif tipo_selecao == 'l': #LEXICASE
                        individuos_selecionados = selecao_lexicase(populacao_atual, tamanho_populacao, df_treino)
                    
                    #Tentar aplicar operações genéticas cada uma um certo número de vezes, na ordem: crossovers, mutações
                    populacao_pos_crossover, num_individuos_gerados_crossover_melhores_fitness_media_pais, num_individuos_gerados_crossover_piores_fitness_media_pais = realiza_crossovers(df_treino, individuos_selecionados, p_c, tamanho_populacao//2) #VER SE MUDA DENTRO DA PROPRIA POP_ATUAL OU TERIA QUE CRIAR UMA NOVA
                    
                    tam_populacao_crossover = len(populacao_pos_crossover)
                    num_mutacoes = tam_populacao_crossover

                    if tam_populacao_crossover < tamanho_populacao:
                        num_mutacoes += 1
                    populacao_pos_crossovers_mutacoes = realiza_mutacoes(populacao_pos_crossover, p_m, num_variaveis, num_mutacoes)

                    if elitismo == 1:
                        #Salva o melhor indivíduo da população atual
                        fitness_individuos_populacao_atual = calcula_fitness_individuos(populacao_atual, df_treino)
                        indice_individuo_melhor_fitness_populacao_atual = np.argmin(fitness_individuos_populacao_atual)
                        indivivuo_melhor_fitness_populacao_atual = populacao_atual[indice_individuo_melhor_fitness_populacao_atual]
                    
                    populacao_atual = copy.deepcopy(populacao_pos_crossovers_mutacoes)

                    #Se elitismo, adiciona o melhor salvo na população atual
                    if elitismo == 1:
                        populacao_atual.append(indivivuo_melhor_fitness_populacao_atual)

                    #-----ESTATISTICAS-----
                    fitnesses_da_geracao = calcula_fitness_individuos(populacao_atual, df_treino)
                    fitness_melhor_individuo = np.min(fitnesses_da_geracao)
                    fitness_pior_individuo = np.max(fitnesses_da_geracao)
                    fitness_media_populacao = np.mean(fitnesses_da_geracao)

                    num_individuos_repetidos_populacao = len(fitnesses_da_geracao) - len(set(fitnesses_da_geracao))

                    linha_estatisticas = [seed, fitness_melhor_individuo, fitness_pior_individuo, fitness_media_populacao, num_individuos_repetidos_populacao, num_individuos_gerados_crossover_melhores_fitness_media_pais, num_individuos_gerados_crossover_piores_fitness_media_pais]
                    writerg.writerow(linha_estatisticas)       
                
                #Calcular a fitness para a última população gerada
                fitnesses_individuos_finais = calcula_fitness_individuos(populacao_atual, df_treino)

                #Retornar solução na posição da maior fitness
                indice_melhor_fitness = np.argmin(fitnesses_individuos_finais)
                melhor_individuo_solucao_base_treino = populacao_atual[indice_melhor_fitness]

                fitness_melhor_individuo_solucao_base_treino = np.min(fitnesses_individuos_finais)

                melhor_individuo_solucao_base_treino.cache_fitness_dataset = None
                resultado_avaliacao_base_teste = calcula_fitness_individuo(melhor_individuo_solucao_base_treino, df_teste)

                linha_melhor_individuo = [fitness_melhor_individuo_solucao_base_treino, resultado_avaliacao_base_teste]
                writerf.writerow(linha_melhor_individuo)

            num_csv += 1

if __name__ == "__main__":
    main()