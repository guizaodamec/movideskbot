@echo off
:: Sincroniza chamados do Movidesk e extrai conhecimento com IA
:: Agendar no Agendador de Tarefas do Windows para rodar à noite

cd /d "%~dp0"
echo [%date% %time%] Iniciando sincronizacao...
python sincronizar_chamados.py >> sincronizacao.log 2>&1
echo [%date% %time%] Concluido. Ver sincronizacao.log para detalhes.
