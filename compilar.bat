@echo off
title ERP Assistant — Compilando...
cd /d "%~dp0"

echo.
echo  ============================================
echo   ERP Assistant — Build completo
echo  ============================================
echo.

echo  [1/3] Fechando processos em execucao...
taskkill /F /IM "ERP Assistant.exe" >nul 2>&1
taskkill /F /IM electron.exe >nul 2>&1
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM backend.exe >nul 2>&1
timeout /t 2 /nobreak >nul

echo  [2/3] Compilando backend Python (PyInstaller)...
python -m PyInstaller build_backend.spec --noconfirm --distpath dist_backend

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo  ERRO: Falha ao compilar o backend.
    echo  Verifique se pyinstaller esta instalado: pip install pyinstaller
    pause
    exit /b 1
)

if not exist "dist_backend\backend.exe" (
    echo.
    echo  ERRO: backend.exe nao foi gerado.
    pause
    exit /b 1
)

echo  [3/3] Compilando frontend Electron...
cd frontend
call npm run build

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo  ERRO: Falha ao compilar o frontend.
    pause
    exit /b 1
)

echo.
echo  ============================================
echo   Build concluido com sucesso!
echo.
echo   Executavel: frontend\dist-electron\ERPAssistant-1.0.0-x64.exe
echo   (portavel — funciona em qualquer Windows sem Python)
echo  ============================================
echo.

set /p INICIAR=Deseja iniciar o sistema agora? (S/N):
if /i "%INICIAR%"=="S" (
    start "" python backend\main.py
    echo  Backend iniciado. Acesse: http://localhost:5000
)

pause
