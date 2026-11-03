@echo off
setlocal
 
REM Diretorio onde o .bat esta (Bobina-corte)
set "BASE_DIR=%~dp0"
set "VENV_DIR=%BASE_DIR%.venv"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"
set "APP_DIR=%BASE_DIR%modelo_corte"
 
REM Verificar o launcher do Python do Windows ----
where py >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Launcher "py" nao encontrado.
    echo Instale o Python em https://www.python.org/downloads/ e marque a opcao
    echo "Install launcher for all users / py launcher" durante a instalacao.
    pause
    exit /b 1
)
 
REM Remover .venv quebrado (ex: criado pelo Python do MSYS2) ----
if exist "%VENV_DIR%" (
    if not exist "%VENV_PY%" (
        echo [..] .venv invalido encontrado, removendo...
        rmdir /s /q "%VENV_DIR%"
    )
)
 
REM Criar .venv se nao existir ----
if exist "%VENV_PY%" (
    echo [OK] .venv ja existe.
) else (
    echo [..] Criando .venv...
    py -3 -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo [ERRO] Falha ao criar o .venv.
        pause
        exit /b 1
    )
)
 
REM Garantir que o pip existe no .venv ----
"%VENV_PY%" -m pip --version >nul 2>&1
if errorlevel 1 (
    echo Instalando pip no .venv...
    "%VENV_PY%" -m ensurepip --upgrade
)
 
REM Verificar/instalar dependencias ----
"%VENV_PY%" -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Instalando streamlit...
    "%VENV_PY%" -m pip install streamlit
    if errorlevel 1 (
        echo [ERRO] Falha ao instalar streamlit.
        pause
        exit /b 1
    )
) else (
    echo [OK] streamlit ja instalado.
)
 
"%VENV_PY%" -c "import gurobipy" >nul 2>&1
if errorlevel 1 (
    echo Instalando gurobipy...
    "%VENV_PY%" -m pip install gurobipy
    if errorlevel 1 (
        echo [ERRO] Falha ao instalar gurobipy.
        pause
        exit /b 1
    )
) else (
    echo [OK] gurobipy ja instalado.
)
 
REM Executar o app ----
echo Iniciando aplicacao...
cd /d "%APP_DIR%"
"%VENV_PY%" -m streamlit run main.py
 
pause
endlocal