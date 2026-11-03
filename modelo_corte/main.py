import streamlit as st
import pandas as pd
import gurobipy as gp
from gurobipy import GRB
import arquivos as dados
import modelo as modelo
from modelo import Modelo

# Configuração inicial da página
st.set_page_config(page_title="Otimização de Padronagem", layout="wide")
st.title("Trabalho de Programação Linear - Otimização de padrão de cortes")

# Lista das 16 instâncias
opcoes_arquivos = [ "--- Selecione um arquivo ---",
    "inst_100_4", "inst_100_5", "inst_100_6", "inst_100_7", 
    "inst_200_4", "inst_200_5", "inst_200_6", "inst_200_7", 
    "inst_250_4", "inst_250_5", "inst_250_6", "inst_250_7", 
    "inst_300_4", "inst_300_5", "inst_300_6", "inst_300_7",
"teste"]

# Barra lateral para seleção
st.sidebar.header("Configurações")
arquivo_selecionado = st.sidebar.selectbox("Escolha a instância de dados:", opcoes_arquivos, index=0)

if arquivo_selecionado and arquivo_selecionado != "--- Selecione um arquivo ---":

    tamanho_bobina, maximo_padroes, comprimento_cortes, demandas, quantidade_comprimentos_cortes =dados.organiza_dados(dados.carregar_dados(arquivo_selecionado))
    L = st.sidebar.slider("Tamanho da Bobina grande", 
                            min_value=100, 
                            max_value=1000, 
                            value=tamanho_bobina, 
                            step=1)
    
    m = st.sidebar.number_input("Máximo de Padrões", 
                                 min_value=1, 
                                 max_value=100,
                                 value=maximo_padroes, 
                                 step=1)
    for dem, comp in (zip(demandas, comprimento_cortes)):
        st.sidebar.write(f"Demanda de {dem}: de {comp} cm")

if st.sidebar.button("Executar"):
    with st.spinner("Otimizando padrões no Gurobi..."):
            try:
                model = Modelo()
                model.carregar_dados(L, comprimento_cortes, demandas, quantidade_comprimentos_cortes, m)
                status_modelo, df_resultados, valor_objetivo = model.calcular_modelo()
                
                if status_modelo == 2:
                    st.success("concluido com sucesso")
                    
                    col1, col2 = st.columns(2)
                    col1.metric(label="Status do Modelo", value="Ótimo")
                    col2.metric(label="Valor da Função Objetivo", value=valor_objetivo)
                    
                    # Tabela final exibindo os padrões escolhidos
                    st.subheader("Padrões Escolhidos")
                    st.dataframe(df_resultados, use_container_width=True, hide_index=True)
                else:
                    st.warning("Solução otima não encontrada")
                    
            except Exception as e:
                st.error(f"Erro ao executar o solver: {e}")

# Exibição do status da interface
if arquivo_selecionado and arquivo_selecionado != "--- Selecione um arquivo ---":
    st.write(f"**Instância selecionada para cálculo:** `{arquivo_selecionado}`")


    