@echo off
cd /d "%~dp0"

echo(
echo ========================================
echo   FarmaFacil Assistente - Git Push
echo ========================================
echo(

git add -A

echo Arquivos staged:
git status --short
echo(

set /p MSG="Mensagem do commit (Enter para usar data/hora): "
if "%MSG%"=="" (
    for /f "tokens=1-3 delims=/" %%a in ("%date%") do set DT=%%c-%%b-%%a
    for /f "tokens=1-2 delims=:" %%a in ("%time: =0%") do set TM=%%a%%b
    set MSG=update %DT% %TM%
)

git commit -m "%MSG%"
git push origin main

echo(
echo Push concluido!
pause
