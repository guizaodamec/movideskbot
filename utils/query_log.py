import os
import time

try:
    from config import QUERY_LOG_FILE
except ImportError:
    QUERY_LOG_FILE = "query_log.txt"

def _log_path():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, QUERY_LOG_FILE)

def log_query(query, result_info, username="sistema"):
    """Registra query modificadora executada no log local."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    entry = (
        "[{ts}] EXECUTADO - {user} confirmou\n"
        "Query: {q}\n"
        "Resultado: {r}\n"
        "---\n"
    ).format(ts=timestamp, user=username, q=query.strip(), r=result_info)
    try:
        with open(_log_path(), "a", encoding="utf-8") as f:
            f.write(entry)
    except Exception:
        pass

def read_log(last_n=50):
    """Retorna as ultimas N entradas do log."""
    path = _log_path()
    if not os.path.exists(path):
        return ""
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        entries = content.split("---\n")
        entries = [e.strip() for e in entries if e.strip()]
        return "\n---\n".join(entries[-last_n:])
    except Exception:
        return ""
