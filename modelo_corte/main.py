import streamlit as st
import pandas as pd
import gurobipy as gp
from gurobipy import GRB
import arquivos as dados
import modelo as modelo
from modelo import Modelo
import excel as caminho

# Configuração inicial da página
st.set_page_config(page_title="Otimização de Padronagem", layout="wide")
st.title("Trabalho de Programação Linear - Otimização de padrão de cortes")

# Lista das 16 instâncias
opcoes_arquivos = [ "--- Selecione um arquivo ---", 
    "Modelo Livre",
    "inst_100_4", "inst_100_5", "inst_100_6", "inst_100_7", 
    "inst_200_4", "inst_200_5", "inst_200_6", "inst_200_7", 
    "inst_250_4", "inst_250_5", "inst_250_6", "inst_250_7", 
    "inst_300_4", "inst_300_5", "inst_300_6", "inst_300_7",
    "teste"]

# Barra lateral para seleção
st.sidebar.header("Configurações")

# Variavel que armazena o arquivo selecionado na selectbox[ opcoes_arquivos ]
arquivo_selecionado = st.sidebar.selectbox("Escolha a instância de dados:", opcoes_arquivos, index=0)

alternativa = st.sidebar.toggle("Ativar Limite de Padrões", value=False) # altera entre versão do problema (a, b)

if arquivo_selecionado and arquivo_selecionado != "--- Selecione um arquivo ---":

    # Classe usada para descompactar os arquivos de instâncias escolhido em "arquivo_selecionado". 
    tam_bobina, max_padroes, compr_cortes, demandas, qtd_compr_cortes = dados.organiza_dados(arquivo_selecionado)
    
    # Barra deslizante para o tamanho da bobina
    L = st.sidebar.slider("Tamanho da Bobina grande",   
                            min_value=100,    # Valor minimo
                            max_value=1000,   # Valor maximo
                            value=tam_bobina, # Valor inicial 
                            step=1)           # Valor que altera (soma ou diminui)

    # Caixa de entrada de numeros que devine o maximo de padrões que pode utilizar
    m = st.sidebar.number_input("Máximo de Padrões",  
                                min_value=1, 
                                max_value=100,
                                value=max_padroes, 
                                step=1)
    
    # Monta a lista com o as demandas e as suas quantidades os seus respectivos tamanhos de cortes
    
    teste = 0

    if arquivo_selecionado == "Modelo Livre":
        st.sidebar.number_input("Número de linhas:",
                                min_value=0,
                                max_value=10,
                                value=teste,
                                step=1)
    else:
        teste = qtd_compr_cortes
    
    for i in range(teste): 
        coluna = st.sidebar.columns(2, gap="xxsmall")
        D = coluna[0].number_input("Quantidade demandada (unid):",
                                    min_value=0,
                                    max_value=10000,
                                    value=demandas[i],
                                    step=1)
        l = coluna[1].number_input("Comprimento do corte (cm):",
                                    min_value=0,
                                    max_value=L,
                                    value=compr_cortes[i],
                                    step=1)

# Botão Executar 
if st.sidebar.button("Executar"):
    with st.spinner("Otimizando padrões no Gurobi..."): # Texto de Carregamento enquanto o Gurobi Carrega a solução Otima
            try:
                model = Modelo(L, compr_cortes, demandas, qtd_compr_cortes, m, alternativa)# alternativa adicionar aqui quando terminar o modelo com limite de padrões
                status_modelo, df_resultados, valor_objetivo, mts_total, perda = model.calcular_modelo() 
                
                if status_modelo == 2:
                    st.success("Valor Ótimo encontrado", title="Status do Modelo")
                    
                    col1, col2 = st.columns(2) # Cria Duas colunas na tela principal do 
                    col1.metric(label="Valor da Função Objetivo", value=f"{valor_objetivo} cortes")

                    with col2:
                        sub_col1, sub_col2 = st.columns(2)
                        
                        sub_col1.metric(label="Metros de bobinas utilizados", value=f"{mts_total} mts")
                        sub_col2.metric(label="Metros de bobinas perdidos", value=f"{perda} mts")
                    
                    # Tabela final exibindo os padrões escolhidos
                    st.subheader("Padrões Escolhidos")
                    st.dataframe(df_resultados, width='stretch', hide_index=True)

                    # Salva o arquivo Excel
                    st.download_button("Baixar Excel",
                                       data=caminho.salvar_arquivo(arquivo_selecionado),
                                       file_name=f"{arquivo_selecionado}{caminho.tipos_excel}")
                else:
                    st.warning("Solução ótima NÃO encontrada", title="Status do Modelo")
                    
            except Exception as e:
                st.error(f"Erro ao executar o modelo: {e}")

# Exibição do status da interface
if arquivo_selecionado and arquivo_selecionado != "--- Selecione um arquivo ---":
    st.write(f"**Instância selecionada para cálculo:** `{arquivo_selecionado}`")