import gurobipy as gp
import numpy as np
from itertools import product
import pandas as pd

class Modelo:
    def __init__(self):
        """Classe para modelar o problema de corte de bobinas"""

        self.modelo = gp.Model()
        self.x = None               # 
        self.objetivo = None        # 
        self.L = None               # Tamanho da bobina grande
        self.l = []                 # Comprimentos dos cortes
        self.Q = None               # Matriz com os padrões de cortes possiveis
        self.D = []                 # Demanda de cada corte
        self.n = None               # Quantidade dy comprimentos dos cortes
        self.m = None               # Quantidade máxima de padrões
        self.qtd_padrao = None      # Quantidade de padrões de corte
        self.qtd_cortes = None      # Quantidade dy comprimentos dos cortes
        self.perdas = None          # Lista com as perdas de cada padrão
        self._LIMITE = 0.9999999999 # Limite para considerar um padrão como utilizado

    def carregar_dados(self, L, l, D, n, m):
        """Carrega as variaveis que serão usadas no modelo
        Args:
            L (int): Tamanho da bobina grande
            l (list): Lista com os tamanhos dos cortes
            D (list): Lista com as demandas de cada corte
            n (int): Número de cortes distintos
            m (int): Número máximo de padrões"""
        
        self.L = L   # Tamanho da Bobina grande
        self.l = l   # Comprimento dos cortes
        self.D = D   # Demanda de cada corte
        self.Q, self.perdas = self.gerar_padroes(L,l)    # Quantidade de corte por padrão
        self.n = n
        self.m = m                     # Quantidade máxima de padrões
        self.qtd_padrao = len(self.Q)  # Quantidade de padrões de corte
        self.qtd_cortes = len(self.l)  # Quantidade dy comprimentos dos cortes


    def gerar_padroes(self, L, cortes):
        """Funçao para gerar todos os padrões de cortes possiveis
        Args:
            L (int) Tamanho da bobina grande
            cortes (list) Lista com os tamanhos dos cortes
        Retona:
            array: Matriz com os padrões de cortes possiveis junto com a perda"""
        
        menor_corte = min(cortes) # Obtem o tamanho do menor corte

        limites = [ # Gera uma lista com os limites de cada corte #| Exemplo. Para l = [50, 40, 30] e L =130  
            range((L // c) + 1) for c in cortes                   #| Divida (130/50)+1 = 3 | (130/40)+1 = 4 | (130/30)+1 = 5    
        ]                                                         #| Resultado: limites[range(0,3), range(0,4), range(0,5)]
        
        padroes = [] # lista para armazenar os padrões de corte possiveis
        perdas = []  # lista para armazenar as perdas dos padrões de corte possiveis

        for combinacao in product(*limites): # O product faz o plano cartesiano para cada RANGE em limites

            total = sum(qtd * tamanho for qtd, tamanho in zip(combinacao, cortes))  
            perda = L - total

            if 0 < total <= L and perda < menor_corte:
                padroes.append(list(combinacao))
                perdas.append(perda)

        return padroes, perdas

    def calcular_modelo(self):
        """Calcula o modelo de otimização"""
        
        # Criando um modelo
        modelo = gp.Model()

        # Variáveis de decisão
        self.x = modelo.addVars(self.qtd_padrao, lb = 0 ,vtype = gp.GRB.INTEGER)

        # Função Objetivo
        modelo.setObjective(
            sum(self.x[j] for j in range(self.qtd_padrao)),
            sense = gp.GRB.MINIMIZE
        )

        # Restrições
        r1 = modelo.addConstrs(
            sum(self.x[j] * self.Q[j][i] for j in range(self.qtd_padrao)) == self.D[i]
                                         for i in range(self.qtd_cortes)
        )

        print("Modelo de otimização criado com sucesso. Iniciando a resolução...")

        # Resolução
        modelo.setParam("OutputFlag", 0)
        modelo.optimize()

        if modelo.status == 2:
            lista_resultados = []
            for i in range(self.qtd_padrao):
                qtd = self.x[i].x

                if qtd > self._LIMITE:
                    lista_resultados.append({
                        "ID do Padrão": i + 1,
                        "Configuração de Corte": self.Q[i], 
                        "Quantidade Utilizada": int(qtd),
                        "Perda": self.perdas[i]
                    })
            
            resultados = pd.DataFrame(lista_resultados)

            if __name__ == "__main__": self.exibicao_debug(modelo)

            return modelo.status, resultados, f"{modelo.objVal:.2f}"
        
        else:
            print("Solução não encontrada")
            return modelo.status, pd.DataFrame(), "0"
        
    
    def padroes_usados(self):
        pass 

    def exibicao_debug(self, modelo):
        """Função de exibição de debug para mostrar os resultados do modelo"""

        print(f"\n\n\n{'*'*30} DEBUG {'*'*30}\n")
        print(f"Tamanho da Bobina Grande:  {self.L}")
        print(f"Maximo de Padroes:         {self.m}")
        print(f"Comprimento dos Cortes:    {self.l}")
        print(f"Demandas:                  {self.D}")
        print(f"Qtd. metidas de cortes:    {self.qtd_cortes}")
        print(f"Qtd. de PADRÕES de cortes: {self.qtd_padrao}")
        print(f"PADRÕES:                   {self.Q}")
        print("\n\n")
        print(f"Valor ótimo: {modelo.objVal:.2f}")
        print("")
        print(f"┌{'─'*37}┐")
        print(f"│{'ID'.center(4)}│{'Padrão'.center(10)}│{'Qtd Usada'.center(10)}│{'Perda'.center(10)}│")
        print(f"├{'─'*4}┼{'─'*10}┼{'─'*10}┼{'─'*10}┤")  

        for i in range(self.qtd_padrao):
            padrao = int(self.x[i].x)

            if padrao > 0.5:
                print(f"│{str(i + 1).center(4)}│{str(self.Q[i]).center(10)}│{str(int(self.x[i].x)).center(10)}│{str(self.L - sum(self.Q[i][j] * self.l[j] for j in range(self.qtd_cortes))).center(10)}│")
        
        print(f"└{'─'*4}┴{'─'*10}┴{'─'*10}┴{'─'*10}┘")


if __name__ == "__main__":
    modelo = Modelo()
    L = 130           # Tamanho da Bobina grande
    l = [50, 40, 30]  # Comprimento dos cortes

    D = [5,9,11]

    n = len(l)        # Quantidade dy comprimentos dos cortes
    m = 7             # Quantidade de padrões de corte

    modelo.carregar_dados(L, l, D, n, m)
    resultado = modelo.calcular_modelo()

    if L == 0:
        padroes, perda =modelo.gerar_padroes(130, [50, 40, 30])

        for i in range(len(padroes)):
            print(f"Padrão {i + 1} | {padroes[i]} | Perda: {perda[i]}")

