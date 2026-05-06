@echo off
title FarmaFacil Assistente — Iniciando...
cd /d "%~dp0"

echo.
echo  ============================================================
echo   FarmaFacil Assistente — Reiniciando todos os servicos
echo  ============================================================
echo.

:: ── 1. Obter IP local ─────────────────────────────────────────────────────────
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4" ^| findstr /v "127.0.0.1"') do (
    set LOCAL_IP=%%a
    goto :found_ip
)
:found_ip
set LOCAL_IP=%LOCAL_IP: =%

:: ── 2. Matar processos anteriores ────────────────────────────────────────────
echo  [1/5] Encerrando processos anteriores...
taskkill /F /FI "WINDOWTITLE eq OmniRoute - IA" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq FarmaFacil - Backend" >nul 2>&1
taskkill /F /IM pythonw.exe >nul 2>&1
taskkill /F /IM python.exe /FI "WINDOWTITLE eq FarmaFacil*" >nul 2>&1
taskkill /F /IM backend.exe >nul 2>&1
:: Matar node que esteja segurando a porta 20128
for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":20128 " ^| findstr "LISTENING"') do (
    taskkill /F /PID %%p >nul 2>&1
)
:: Matar node que esteja segurando a porta 5000
for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":5000 " ^| findstr "LISTENING"') do (
    taskkill /F /PID %%p >nul 2>&1
)
timeout /t 2 /nobreak >nul
echo         Processos encerrados.

:: ── 3. Abrir portas no firewall (silencioso, so faz se nao existir) ───────────
netsh advfirewall firewall show rule name="FarmaFacil - Flask 5000" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    netsh advfirewall firewall add rule name="FarmaFacil - Flask 5000" dir=in action=allow protocol=TCP localport=5000 >nul 2>&1
)
netsh advfirewall firewall show rule name="FarmaFacil - OmniRoute 20128" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    netsh advfirewall firewall add rule name="FarmaFacil - OmniRoute 20128" dir=in action=allow protocol=TCP localport=20128 >nul 2>&1
)

:: ── 4. Verificar dependencias minimas ─────────────────────────────────────────
echo  [2/5] Verificando dependencias...
node --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo  ERRO: Node.js nao encontrado. Instale em https://nodejs.org
    pause
    exit /b 1
)
echo         Node.js OK.

:: ── 5. Iniciar OmniRoute ──────────────────────────────────────────────────────
echo  [3/5] Iniciando OmniRoute (IA na porta 20128)...
start "OmniRoute - IA" /MIN cmd /k "npx omniroute --port 20128 --no-open"
echo         Aguardando OmniRoute...
timeout /t 5 /nobreak >nul
curl -s --max-time 3 http://localhost:20128/v1/models >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo  AVISO: OmniRoute pode nao ter iniciado corretamente.
    echo  Verifique a janela "OmniRoute - IA".
    echo.
) else (
    echo         OmniRoute OK.
)

:: ── 6. Verificar frontend/dist ────────────────────────────────────────────────
echo  [4/5] Verificando frontend...
if not exist "frontend\dist\index.html" (
    echo         Build nao encontrado. Gerando...
    cd frontend
    call npm install --silent
    call npx vite build
    cd ..
    if not exist "frontend\dist\index.html" (
        echo  ERRO: Falha ao gerar o frontend.
        pause
        exit /b 1
    )
    echo         Frontend gerado.
) else (
    echo         Frontend OK.
)

:: ── 7. Iniciar backend Flask ──────────────────────────────────────────────────
echo  [5/5] Iniciando backend Flask (porta 5000)...
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    start "FarmaFacil - Backend" /MIN cmd /k "pythonw backend\main.py"
    goto :aguardar_backend
)
if exist "dist_backend\backend.exe" (
    if not exist "dist_backend\frontend\dist\index.html" (
        xcopy /E /I /Y "frontend\dist" "dist_backend\frontend\dist" >nul
    )
    start "FarmaFacil - Backend" /MIN cmd /k "dist_backend\backend.exe"
    goto :aguardar_backend
)
echo  ERRO: Nem Python nem dist_backend\backend.exe encontrados.
pause
exit /b 1

:aguardar_backend
echo         Aguardando backend...
timeout /t 4 /nobreak >nul

:: ── 8. Abrir no navegador ─────────────────────────────────────────────────────
start "" "http://localhost:5000"

echo.
echo  ============================================================
echo   FarmaFacil Assistente ONLINE
echo.
echo   Acesso local:  http://localhost:5000
echo   Acesso rede:   http://%LOCAL_IP%:5000
echo.
echo   OmniRoute (IA): http://localhost:20128
echo.
echo   Feche esta janela a vontade.
echo   Para PARAR tudo: rode este bat novamente (mata e reinicia).
echo  ============================================================
echo.
pause
