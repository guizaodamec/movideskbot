"""
Script de sincronização noturna dos chamados do Movidesk.
Executar diretamente: python sincronizar_chamados.py
Ou agendar no Agendador de Tarefas do Windows.

Estratégia de sync em 3 etapas:
  1. Sync últimos 90 dias em batches mensais — garante que passo 2 (resolvidos) sempre rode
  2. Sync histórico via /tickets/past para chamados criados há 91-120 dias
  3. Extração de problema+solução com IA para chamados ainda não processados
"""
import sys
import os
from datetime import datetime, timedelta

# Garante que o diretório do projeto está no path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def main():
    log("=== Sincronização Movidesk iniciada ===")

    from utils.movidesk_sync import sync_tickets, sync_tickets_historical, sync_open_tickets, load_cache, extract_knowledge, get_stats

    hoje       = datetime.now()
    total_novos = 0

    # ── Etapa 0: Todos os chamados em ABERTO (sem filtro de data) ─────────────────
    # Captura tickets antigos ainda abertos que ficam fora da janela de 90 dias.
    log("Etapa 0: Sincronizando todos os chamados em aberto...")
    try:
        novos_abertos = sync_open_tickets(max_tickets=2000)
        total_novos += novos_abertos
        log(f"  {novos_abertos} novos chamados abertos adicionados.")
    except Exception as e:
        log(f"  ERRO no sync de abertos: {e}")

    # ── Etapa 1: Últimos 90 dias em 3 batches mensais ────────────────────────────
    # Dividir em batches garante que o passo 2 (resolvidos por lastUpdate)
    # seja executado para cada período, evitando perda de dados.
    log("Etapa 1: Sincronizando últimos 90 dias em batches mensais...")
    for i in range(3):
        date_to_dt   = hoje   - timedelta(days=30 * i)
        date_from_dt = hoje   - timedelta(days=30 * (i + 1))
        date_from    = date_from_dt.strftime('%Y-%m-%d')
        date_to      = date_to_dt.strftime('%Y-%m-%d')

        log(f"  Batch {i+1}/3: {date_from} → {date_to}...")
        try:
            novos = sync_tickets(max_tickets=2000, date_from=date_from, date_to=date_to)
            total_novos += novos
            log(f"    {novos} novos chamados.")
        except Exception as e:
            log(f"    ERRO: {e}")

    # ── Etapa 2: Histórico via /tickets/past (91-120 dias) ───────────────────────
    # /tickets retorna só tickets com lastUpdate nos últimos 90 dias.
    # Para chamados criados há mais de 90 dias sem atividade recente, usa /past.
    log("Etapa 2: Verificando histórico via /tickets/past (91-120 dias)...")
    try:
        hist_from = (hoje - timedelta(days=120)).strftime('%Y-%m-%d')
        hist_to   = (hoje - timedelta(days=90)).strftime('%Y-%m-%d')
        novos_hist = sync_tickets_historical(date_from=hist_from, date_to=hist_to, max_tickets=1000)
        total_novos += novos_hist
        log(f"  {novos_hist} chamados históricos adicionados.")
    except Exception as e:
        log(f"  Aviso no sync histórico: {e}")

    log(f"Sync concluído. Total geral: {total_novos} novos chamados.")

    # ── Etapa 3: Extração de problema+solução com IA ─────────────────────────────
    cache     = load_cache()
    pendentes = sum(1 for t in cache["tickets"].values() if not t.get("extracted"))
    log(f"{pendentes} chamados aguardando extração por IA.")

    if pendentes == 0:
        log("Nada a extrair. Encerrando.")
        _exibir_stats(get_stats)
        return

    log("Extraindo problema+solução com IA (lotes de 30)...")
    try:
        total_extraido = 0
        while True:
            n = extract_knowledge(batch=30)
            if n == 0:
                break
            total_extraido += n
            log(f"  {total_extraido} chamados extraídos até agora...")
        log(f"Extração concluída. Total: {total_extraido} chamados processados.")
    except Exception as e:
        log(f"ERRO na extração: {e}")

    _exibir_stats(get_stats)
    log("=== Concluído ===")


def _exibir_stats(get_stats):
    try:
        stats = get_stats()
        log("=== Estatísticas ===")
        log(f"Total chamados: {stats['total']}")
        log(f"Extraídos por IA: {stats['extraidos']}")
        log(f"Problemas recorrentes: {stats['recorrentes']}")
        if stats['top_categorias']:
            log("Top 3 categorias:")
            for cat, n in stats['top_categorias'][:3]:
                log(f"  {n}x {cat}")
    except Exception as e:
        log(f"ERRO ao gerar stats: {e}")


if __name__ == "__main__":
    main()
