@echo off
title Compilando Frontend...
cd /d "%~dp0"
echo.
echo  Compilando frontend (FarmaFacilAssistente.exe)...
echo.
cd frontend
call npm run build
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo  ERRO na compilacao.
    pause
    exit /b 1
)
echo.
echo  Pronto! frontend\dist-electron\FarmaFacilAssistente-1.0.0.exe atualizado.
echo.
pause
