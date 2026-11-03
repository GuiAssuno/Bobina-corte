import gurobipy as gp
import numpy as np
from itertools import product
import pandas as pd

class Modelo:
    def __init__(self):
        self.modelo = gp.Model()
        self.x = None
        self.objetivo = None
        self.L = None 
        self.l = []
        self.Q = None
        self.D = []
        self.n = None
        self.m = None
        self.qtd_padrao = None
        self.qtd_cortes = None
        self.perdas = None

    def carregar_dados(self, L, l, D, n, m):
        """Carrega as variaveis que serão usadas no modelo
        Args:
            L (int): Tamanho da bobina grande
            l (list): Lista com os tamanhos dos cortes
            D (list): Lista com as demandas de cada corte
            n (int): Número de cortes distintos
            m (int): Número máximo de padrões"""
        
        self.L = L                          # Tamanho da Bobina grande
        self.l = l                          # Comprimento dos cortes
        self.D = D                          # Demanda de cada corte
        self.Q, self.perdas = self.gerar_padroes(L,l)    # Quantidade de corte por padrão
        self.n = n
        self.m = m
        self.qtd_padrao = len(self.Q[0])    # Quantidade de padrões de corte
        self.qtd_cortes = len(self.l)       # Quantidade dy comprimentos dos cortes


    def gerar_padroes(self, L, cortes):
        """Funçao para gerar todos os padrões de cortes possiveis
        Args:
            L (int) Tamanho da bobina grande
            cortes (list) Lista com os tamanhos dos cortes
        Retona:
            array: Matriz com os padrões de cortes possiveis junto com a perda"""
        
        menor_corte = min(cortes)
        limites = [range((L // c) + 1) for c in cortes]
        padroes = []
        perdas = []

        for combinacao in product(*limites):

            total = sum(qtd * tamanho for qtd, tamanho in zip(combinacao, cortes))
            perda = L - total

            if 0 < total <= L and perda < menor_corte:
                padroes.append(list(combinacao))
                perdas.append(perda)

        return padroes, perdas

    def calcular_modelo(self):
        """Calcula o modelo de otimização"""
        print("Iniciando a modelagem do problema de otimização...")
        print(f"""Tamanho da Bobina Grande: {self.L}
Maximo de Padroes: {self.m}
Comprimento dos Cortes: {self.l}
Demandas: {self.D}
Qauntidade de comprimentos de cortes: {self.qtd_cortes}
Qauntidade de padroes de cortes: {self.qtd_padrao}
padroes: {self.Q}""")
        
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
            sum(self.x[j] * self.Q[i][j] for j in range(self.qtd_padrao)) == self.D[i]
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

                if qtd > 0.5:
                    lista_resultados.append({
                        "ID do Padrão": i + 1,
                        "Configuração de Corte": self.Q[i].tolist(), 
                        "Quantidade Utilizada": int(qtd),
                        "Perda": self.perdas[i]
                    })
            
            resultados = pd.DataFrame(lista_resultados)

            return modelo.status, resultados, f"{modelo.objVal:.2f}"
        
        else:
            print("Solução não encontrada")
            return modelo.status, pd.DataFrame(), "0"
        
    
    def padroes_usados(self):
        pass 

    def resolucao(self):
        """Resolve o modelo"""
        self.modelo.setParam("OutputFlag", 0)
        self.modelo.optimize()

        if self.modelo.status == 2:
            print(f"Valor ótimo: {self.modelo.objVal:.2f}")
        for i in range(self.m):
            print(f"{self.x[i].x:.2f}")
        else:
            print("Solução não encontrada")


if __name__ == "__main__":
    modelo = Modelo()

    padroes, perda =modelo.gerar_padroes(130, [50, 40, 30])

    for i in range(len(padroes)):
        print(f"Padrão {i + 1} | {padroes[i]} | Perda: {perda[i]}")

