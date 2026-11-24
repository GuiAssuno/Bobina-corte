import streamlit as st
import pandas as pd
import gurobipy as gp
from gurobipy import GRB
import arquivos as dados
import modelo as modelo
from modelo import Modelo
from planilha import excel

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
    #tam_bobina, max_padroes, compr_cortes, demandas, qtd_compr_cortes = dados.organiza_dados(arquivo_selecionado)
    
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
    
    if arquivo_selecionado == "Modelo Livre":
        if "modelo_livre" not in st.session_state:
            st.session_state["modelo_livre"] = 0

        with st.sidebar:
            col_deletar, col_adicionar = st.columns(2)

            if col_deletar.button("Excluir linha", disabled= (st.session_state["modelo_livre"] <= 0)):
                st.session_state["modelo_livre"] -= 1

            if col_adicionar.button("Adicionar linha"):
                st.session_state["modelo_livre"] += 1

        demandas = [] #* ultimo
        compr_cortes = [] #*ultimo 
            
        # Monta a lista com o as demandas e as suas quantidades os seus respectivos tamanhos de cortes
        for i in range(st.session_state["modelo_livre"]):
            coluna = st.sidebar.columns(2, gap="xxsmall")
            D = coluna[0].number_input(f"D{i+1} - Quantidade demandada (unid):",
                                min_value=0, 
                                max_value=10000, 
                                value=0, 
                                step=1)
                                
            l = coluna[1].number_input(f"l{i+1} - Comprimento do corte (cm):",
                                min_value=0, 
                                max_value=L, 
                                value=0, 
                                step=1)
            
            demandas.append(D)
            compr_cortes.append(l)

            print(st.session_state)

    else:
    
        # Monta a lista com o as demandas e as suas quantidades os seus respectivos tamanhos de cortes
        for i in range(qtd_compr_cortes): 
            coluna = st.sidebar.columns(2, gap="xxsmall")
            D = coluna[0].number_input(f"D{i + 1} - Quantidade demandada (unid):",
                                        min_value=0,
                                        max_value=10000,
                                        value=demandas[i],
                                        step=1)
            l = coluna[1].number_input(f"l{i + 1} - Comprimento do corte (cm):",
                                        min_value=0,
                                        max_value=L,
                                        value=compr_cortes[i],
                                        step=1)
            demandas[i] = D
            compr_cortes[i] = l

# Botão Executar 
if st.sidebar.button("Executar"):
    with st.spinner("Otimizando padrões no Gurobi..."): # Texto de Carregamento enquanto o Gurobi Carrega a solução Otima
            try:
                model = Modelo(L, compr_cortes, demandas, qtd_compr_cortes, m, alternativa)# alternativa adicionar aqui quando terminar o modelo com limite de padrões
                status_modelo, df_resultados, valor_objetivo, mts_total, perda = model.calcular_modelo() 
                print (f'Metros totais:{mts_total}')
                if status_modelo == 2:
                    planilha = excel(compr_cortes, model.Q, model.perdas, df_resultados)
                    planilha.salvar_arquivo(arquivo_selecionado)

                    st.session_state["Resultado"] = {
                        "df": df_resultados,
                        "objetivo": valor_objetivo,
                        "totais": mts_total,
                        "perda": perda,
                        "nome": f"{arquivo_selecionado}_padroes.xlsx",
                        "excel": planilha.buffer.getvalue()
                    }
    
                else:
                    st.warning("Solução ótima NÃO encontrada", title="Status do Modelo")

            except Exception as e:
                st.error(f"Erro ao executar o modelo: {e}")

if "Resultado" in st.session_state:
    resultado = st.session_state["Resultado"]
    st.success("Valor Ótimo encontrado", title="Status do Modelo")
                        
    col1, col2 = st.columns(2) # Cria Duas colunas na tela principal do 
    col1.metric(label="Valor da Função Objetivo", value=f"{float(resultado['objetivo']):.0f} bobinas")

    with col2:
        sub_col1, sub_col2 = st.columns(2)
        
        sub_col1.metric(label="Metros de bobinas utilizados", value=f"{resultado['totais']} mts")
        sub_col2.metric(label="Metros de bobinas perdidos", value=f"{resultado['perda']} mts")

    # Tabela final exibindo os padrões escolhidos
    st.subheader("Padrões Escolhidos")
    st.dataframe(resultado['df'], width='stretch', hide_index=True)

    # Salva o arquivo Excel
    st.download_button("Baixar Excel",
                        data = resultado['excel'],
                        file_name = resultado['nome'])


# Exibição do status da interface
if arquivo_selecionado and arquivo_selecionado != "--- Selecione um arquivo ---":
    st.write(f"**Instância selecionada para cálculo:** `{arquivo_selecionado}`")