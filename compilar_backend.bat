@echo off
title Compilando Backend...
cd /d "%~dp0"
echo.
echo  Compilando backend (backend.exe)...
echo.
python -m PyInstaller build_backend.spec --distpath dist_backend --noconfirm
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo  ERRO na compilacao.
    pause
    exit /b 1
)
echo.
echo  Pronto! dist_backend\backend.exe atualizado.
echo.
pause
