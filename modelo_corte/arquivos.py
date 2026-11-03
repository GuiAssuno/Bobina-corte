import os


def carregar_dados(nome_arquivo):
    """Carrega os dados dos arquivos"""

    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho = os.path.join(diretorio_atual, "data", f"{nome_arquivo}.txt")
    print (caminho)
    with open(caminho, 'r') as arquivo:
        linhas = arquivo.read()
    return linhas

def organiza_dados(linhas):
    """pega o conteudo das linhas e organiza nas variaveis"""

    tamanho_bobina = 0       # Tamanho da Bobina grande
    maximo_padroes = 0       # Maximo de padroes
    comprimento_cortes = []  # Comprimento dos cortes
    demandas = []

    for n, linha in enumerate(linhas.splitlines()):
        if n == 0: 
            tamanho_bobina = int (linha.strip())
            continue
        if n == 1:
            maximo_padroes = int (linha.strip())
            continue
        comp, dem = linha.strip().split()
        comprimento_cortes.append(int(comp))
        demandas.append(int(dem))

    quantidade_comprimentos_cortes = len(comprimento_cortes) # Quantidade dy comprimentos dos cortes

    return tamanho_bobina, maximo_padroes, comprimento_cortes, demandas, quantidade_comprimentos_cortes


if __name__ == "__main__":
    linhas = carregar_dados("inst_100_4")
    L, m, l, D, n = organiza_dados(linhas)

    print(f"""Tamanho da Bobina Grande: {L}
Maximo de Padroes: {m}
Comprimento dos Cortes: {l}
Demandas: {D}
Qauntidade de comprimentos de cortes: {n}""")

