from etapas import gera_populacao_inicial

if __name__ == "__main__":
    num_individuos = 5
    num_vars = 3
    alt_max = 4
    individuos = gera_populacao_inicial(num_individuos, num_vars, alt_max)

    for individuo in individuos:
        print(individuo)
        print("\n")