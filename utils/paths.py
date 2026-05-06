"""
Resolução de caminhos para modo desenvolvimento e modo compilado (PyInstaller).

- get_bundle_dir(): arquivos somente-leitura embutidos no exe (knowledge.md etc.)
- get_data_dir():   arquivos graváveis persistentes (users.json, connection.json etc.)
"""
import os
import sys


def get_bundle_dir():
    """
    Diretório com arquivos somente-leitura (farmafacil_knowledge.md etc.).
    Em modo frozen: sys._MEIPASS.
    Em modo dev: raiz do projeto.
    """
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_data_dir():
    """
    Diretório para arquivos graváveis persistentes (users.json, connection.json etc.).
    - Modo compilado (backend.exe): pasta ao lado do executável (dist_backend/).
    - Modo desenvolvimento (python): raiz do projeto.
    Evita C:\\ProgramData para não depender de permissões de administrador.
    """
    if getattr(sys, 'frozen', False):
        data_dir = os.path.dirname(sys.executable)
    else:
        data_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    os.makedirs(data_dir, exist_ok=True)
    _migrate_if_needed(data_dir)
    return data_dir


def _migrate_if_needed(data_dir):
    """Copia users.json do ProgramData (local antigo) se necessário."""
    dest = os.path.join(data_dir, 'users.json')
    if os.path.exists(dest):
        return

    # Tenta recuperar do ProgramData (instalações anteriores)
    programdata = os.environ.get('PROGRAMDATA', 'C:\\ProgramData')
    candidatos = [
        os.path.join(programdata, 'FarmaFacilAssistente', 'users.json'),
    ]
    for src in candidatos:
        if os.path.exists(src):
            try:
                import shutil
                shutil.copy2(src, dest)
            except Exception:
                pass
            break
