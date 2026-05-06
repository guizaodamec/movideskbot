"""
Salva histórico de conversas em arquivos TXT por usuário.
Pasta: <data_dir>/chat_logs/<username>/YYYY-MM-DD.txt
"""
import os
from datetime import datetime
from utils.paths import get_data_dir

_SEP = "=" * 80


def _logs_dir(username: str) -> str:
    safe = username.lower().replace(" ", "_").replace("/", "_").replace("\\", "_")
    path = os.path.join(get_data_dir(), "chat_logs", safe)
    os.makedirs(path, exist_ok=True)
    return path


def _log_file(username: str) -> str:
    hoje = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(_logs_dir(username), f"{hoje}.txt")


def _append(username: str, texto: str):
    try:
        with open(_log_file(username), "a", encoding="utf-8") as f:
            f.write(texto + "\n")
    except Exception:
        pass


def log_chat(username: str, user_msg: str, ai_response: str, has_image: bool = False):
    """Registra uma interação do chat principal."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    img_aviso = " [imagem anexada]" if has_image else ""
    bloco = (
        f"\n{_SEP}\n"
        f"[{ts}] USUÁRIO{img_aviso}\n"
        f"{user_msg}\n\n"
        f"[{ts}] IA\n"
        f"{ai_response}\n"
        f"{_SEP}"
    )
    _append(username, bloco)


def log_print_analysis(username: str, descricao: str, ai_response: str):
    """Registra uma análise de print/imagem."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bloco = (
        f"\n{_SEP}\n"
        f"[{ts}] ANÁLISE DE PRINT\n"
        f"Descrição: {descricao or 'Não informada'}\n\n"
        f"[{ts}] IA\n"
        f"{ai_response}\n"
        f"{_SEP}"
    )
    _append(username, bloco)


def log_log_analysis(username: str, log_preview: str, contexto: str, ai_response: str):
    """Registra uma análise de log."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    preview = log_preview[:500] + "..." if len(log_preview) > 500 else log_preview
    bloco = (
        f"\n{_SEP}\n"
        f"[{ts}] ANÁLISE DE LOG\n"
        f"Contexto: {contexto or 'Não informado'}\n"
        f"Log (prévia):\n{preview}\n\n"
        f"[{ts}] IA\n"
        f"{ai_response}\n"
        f"{_SEP}"
    )
    _append(username, bloco)
