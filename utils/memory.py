"""
Memória por usuário — salva insights das conversas para enriquecer contextos futuros.
Arquivo: memory/<username>.md
"""
import os
import json
import datetime

try:
    from utils.paths import get_data_dir
    _MEM_DIR = os.path.join(get_data_dir(), 'memory')
except ImportError:
    _MEM_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'memory')


def _ensure_dir():
    os.makedirs(_MEM_DIR, exist_ok=True)


def _mem_file(username):
    _ensure_dir()
    safe = username.lower().replace(' ', '_')
    return os.path.join(_MEM_DIR, safe + '.json')


def load_memory(username):
    """Retorna lista de entradas de memória do usuário."""
    path = _mem_file(username)
    if not os.path.exists(path):
        return []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def save_memory(username, entries):
    """Salva lista de entradas de memória."""
    path = _mem_file(username)
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def add_memory(username, content, category='geral'):
    """Adiciona uma entrada de memória. Limite de 50 entradas por usuário."""
    entries = load_memory(username)
    entries.append({
        'date': datetime.datetime.now().strftime('%Y-%m-%d'),
        'category': category,
        'content': content[:500],  # Máximo 500 chars por entrada
    })
    # Mantém apenas as 50 mais recentes
    entries = entries[-50:]
    save_memory(username, entries)


def build_memory_prompt(username):
    """Monta texto de memória para incluir no prompt. Máximo ~800 tokens."""
    entries = load_memory(username)
    if not entries:
        return ''

    lines = ['Memorias anteriores deste usuario:']
    for e in entries[-20:]:  # Últimas 20 entradas
        lines.append('[{date}] ({category}) {content}'.format(**e))

    return '\n'.join(lines)
