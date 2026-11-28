"""Executa todos os arquivos. para isso precisa da licença do gurobi"""
import pandas as pd
import arquivos 
from modelo import Modelo
import time

opcoes_arquivos = [
    "inst_100_4", "inst_100_5", "inst_100_6", "inst_100_7", 
    "inst_200_4", "inst_200_5", "inst_200_6", "inst_200_7", 
    "inst_250_4", "inst_250_5", "inst_250_6", "inst_250_7", 
    "inst_300_4", "inst_300_5", "inst_300_6", "inst_300_7",
    ]

for x in [1,2,3,4,5]:
    resultados = []

    for a in [False, True]:
        for arquivo_selecionado in opcoes_arquivos:
            tam_bobina, max_padroes, compr_cortes, demandas, qtd_compr_cortes = arquivos.organiza_dados(arquivo_selecionado)

            inicio_total = time.perf_counter()
            model = Modelo(tam_bobina, compr_cortes, demandas, qtd_compr_cortes, max_padroes, a)
            status_modelo, df_resultados, valor_objetivo, mts_total, perda = model.calcular_modelo()
            tempo_total = time.perf_counter() - inicio_total

            resultados.append({
                "Instancia": arquivo_selecionado,
                "Etapa": "B" if a else "A",
                # "Tempo Total (s)": round(tempo_total, 4),
                # "Gerar Padrões (s)": round(model.tempo_padroes, 4),
                # "Executar Modelo (s)": round(model.tempo_modelo, 4),
                "Qtd Padrões": model.qtd_padrao,
                "Padrões Utilizados": len(df_resultados[('', 'ID')]),
                "Valor Objetivo": valor_objetivo,
                "Perda": perda,
            })

    df = pd.DataFrame(resultados)

    df = df.sort_values(by=["Instancia", "Etapa"]).reset_index(drop=True)

    df.to_excel(f"resultados{x}.xlsx", index=False)
    print(df.to_string(index=False))

# if __name__ == "__main__":
#     model = modelo.Modelo()        