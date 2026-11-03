import streamlit as slit


# Inicializa o estado da sessão se não existir
if 'tela_inicial' not in slit.session_state:
    slit.session_state.tela_inicial = True

if slit.session_state.tela_inicial:
    slit.title("Análise de Algoritmos")
    # Mostra a tela inicial apenas se não tiver escolhido uma opção
    option = slit.selectbox("Selecione o Módulo", ["1", "2"], index=0)
    
    print(slit.session_state)

    if slit.button("Iniciar Análise"):
        slit.session_state.tela_inicial = False
        slit.session_state.opcao_escolhida = option
        slit.rerun()  # Força a atualização do script
else:
    # Mostra o conteúdo da opção escolhida
    if slit.session_state.opcao_escolhida == "1":
        ans.run()
        slit.button("Voltar", on_click=lambda: setattr(slit.session_state, 'tela_inicial', True))
    elif slit.session_state.opcao_escolhida == "2":
        slit.markdown("""
        ### Sobre o Projeto
        Este projeto compara a performance de algoritmos de ordenação implementados em C
        e chamados via Python (ctypes).
        """)
        slit.button("Voltar", on_click=lambda: setattr(slit.session_state, 'tela_inicial', True))
