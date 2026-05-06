@echo off
title Expor Claude Code na rede local
cd /d "%~dp0"

echo.
echo  ============================================================
echo   Expor Claude Code (porta 20128) para outras maquinas
echo  ============================================================
echo.
echo  Este script redireciona a porta 20128 do localhost
echo  para ficar acessivel em todas as interfaces de rede.
echo.
echo  ATENCAO: Execute como Administrador!
echo.

:: Verificar se e admin
net session >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo  ERRO: Este script precisa ser executado como Administrador.
    echo  Clique com botao direito no arquivo e selecione "Executar como administrador".
    pause
    exit /b 1
)

:: Obter IP local
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4" ^| findstr /v "127.0.0.1"') do (
    set LOCAL_IP=%%a
    goto :found_ip
)
:found_ip
set LOCAL_IP=%LOCAL_IP: =%

echo  IP desta maquina detectado: %LOCAL_IP%
echo.

:: Adicionar regra de portproxy
echo  [1/3] Configurando redirecionamento de porta...
netsh interface portproxy add v4tov4 listenport=20128 listenaddress=0.0.0.0 connectport=20128 connectaddress=127.0.0.1

if %ERRORLEVEL% NEQ 0 (
    echo  ERRO ao configurar portproxy.
    pause
    exit /b 1
)

:: Abrir no firewall
echo  [2/3] Abrindo porta no firewall do Windows...
netsh advfirewall firewall add rule name="Claude Code API - FarmaFacil Assistente" dir=in action=allow protocol=TCP localport=20128 >nul 2>&1

echo  [3/3] Verificando configuracao...
netsh interface portproxy show v4tov4

echo.
echo  ============================================================
echo   Pronto! Outras maquinas podem acessar via:
echo   http://%LOCAL_IP%:20128/v1
echo.
echo   No FarmaFacil Assistente das outras maquinas, informe:
echo   IP do servidor de IA: %LOCAL_IP%
echo  ============================================================
echo.

set /p REMOVER=Para REMOVER a regra depois, rode este script de novo (S/N):
if /i "%REMOVER%"=="S" goto :remover
goto :fim

:remover
echo  Removendo regras...
netsh interface portproxy delete v4tov4 listenport=20128 listenaddress=0.0.0.0 >nul 2>&1
netsh advfirewall firewall delete rule name="Claude Code API - FarmaFacil Assistente" >nul 2>&1
echo  Regras removidas.

:fim
pause
