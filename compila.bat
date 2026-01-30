@echo off
TITLE PyPong Builder (Env Copel)
COLOR 0A

REM --- Configuracao do Caminho do Ambiente Virtual ---
REM Ajustado para o seu caminho especifico
SET "ENV_PATH=D:\Software\Python\Copel"

CLS
ECHO.
ECHO ======================================================
ECHO    PYPONG - COMPILACAO PROFISSIONAL
ECHO    Ambiente: %ENV_PATH%
ECHO ======================================================
ECHO.

REM 1. Verifica e Ativa o Ambiente Virtual
IF NOT EXIST "%ENV_PATH%\Scripts\activate.bat" (
    COLOR 0C
    ECHO [ERRO] Ambiente virtual nao encontrado em:
    ECHO %ENV_PATH%
    ECHO Verifique se o caminho esta correto.
    PAUSE
    EXIT /B
)

ECHO [1/4] Ativando ambiente virtual...
CALL "%ENV_PATH%\Scripts\activate.bat"

REM 2. Instalação de Dependências
ECHO.
ECHO [2/4] Verificando dependencias (pygame, cx_Freeze)...
ECHO ------------------------------------------
pip install pygame cx_Freeze --upgrade
IF %errorlevel% neq 0 (
    COLOR 0C
    ECHO [ERRO] Falha ao instalar bibliotecas.
    PAUSE
    EXIT /B
)

REM 3. Limpeza
ECHO.
ECHO [3/4] Limpando builds antigas...
ECHO ------------------------------------------
IF EXIST build (
    rmdir /s /q build
    ECHO Pasta 'build' limpa.
) ELSE (
    ECHO Nenhuma build anterior.
)

REM 4. Compilação
ECHO.
ECHO [4/4] Gerando executavel (PyPong Neo Edition)...
ECHO ------------------------------------------
python setup.py build
IF %errorlevel% neq 0 (
    COLOR 0C
    ECHO.
    ECHO [ERRO] Falha no cx_Freeze. Verifique o setup.py.
    PAUSE
    EXIT /B
)

ECHO.
ECHO ==========================================
ECHO      SUCESSO! JOGO PRONTO.
ECHO ==========================================
ECHO.
ECHO O executavel esta na pasta 'build'.
ECHO Pode fechar e jogar!
ECHO.
PAUSE