@echo off
title FarmaFacil Assistente — Compilando...
cd /d "%~dp0"

echo.
echo  ============================================
echo   FarmaFacil Assistente — Build executavel
echo   Cliente: OpenAI SDK + Claude Code local
echo  ============================================
echo.

echo  [1/4] Encerrando processos anteriores...
taskkill /F /IM FarmaFacilAssistente.exe >nul 2>&1
taskkill /F /IM python.exe >nul 2>&1
timeout /t 1 /nobreak >nul

echo  [2/4] Verificando dependencias...
python -c "import openai" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo  Instalando dependencias...
    pip install -r requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo  ERRO: Falha ao instalar dependencias.
        pause
        exit /b 1
    )
)

python -c "import PyInstaller" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo  Instalando PyInstaller...
    pip install pyinstaller==4.10
)

echo  [3/4] Compilando FarmaFacilAssistente.exe...
python -m PyInstaller build.spec --noconfirm

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo  ERRO: Falha na compilacao.
    pause
    exit /b 1
)

if not exist "dist\FarmaFacilAssistente.exe" (
    echo.
    echo  ERRO: FarmaFacilAssistente.exe nao foi gerado.
    pause
    exit /b 1
)

echo  [4/4] Copiando arquivos necessarios para dist\...
if exist "farmafacil_knowledge.md" copy /Y "farmafacil_knowledge.md" "dist\" >nul
if exist "users.json"              copy /Y "users.json"              "dist\" >nul

echo.
echo  ============================================
echo   Build concluido com sucesso!
echo.
echo   Executavel: dist\FarmaFacilAssistente.exe
echo.
echo   ATENCAO: o Claude Code deve estar rodando
echo   em 192.168.0.118:20128 para a IA funcionar.
echo  ============================================
echo.

set /p ABRIR=Abrir a pasta dist\ agora? (S/N):
if /i "%ABRIR%"=="S" (
    explorer dist
)

pause
