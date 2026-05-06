"""
FarmaFacil Assistente — Entry point
Compativel com Python 3.8+ / Windows XP (builds especiais) / 7 / 10 / Server
"""
import sys
import os

# Garantir que o diretorio do script esta no path
_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)

import tkinter as tk


def _check_deps():
    """Verifica dependencias criticas e exibe aviso amigavel se faltando."""
    missing = []
    try:
        import openai
    except ImportError:
        missing.append("openai  (pip install openai)")
    try:
        import psycopg2
    except ImportError:
        missing.append("psycopg2  (pip install psycopg2-binary)")
    try:
        from PIL import Image
    except ImportError:
        missing.append("Pillow  (pip install Pillow==6.2.2)")
    return missing


def main():
    # Verificar dependencias
    missing = _check_deps()
    if missing:
        root = tk.Tk()
        root.withdraw()
        msg = (
            "Dependencias necessarias nao encontradas:\n\n"
            + "\n".join("  - " + m for m in missing)
            + "\n\nInstale com:\n  pip install -r requirements.txt"
        )
        from tkinter import messagebox
        messagebox.showerror("FarmaFacil Assistente — Dependencias ausentes", msg)
        root.destroy()
        sys.exit(1)

    # Janela raiz temporaria (necessaria para Toplevel)
    root = tk.Tk()
    root.withdraw()
    root.title("FarmaFacil Assistente")

    # ── Tela de login
    from ui.login_dialog import LoginDialog
    login = LoginDialog(root)
    user_info = login.user_info

    if not user_info:
        root.destroy()
        sys.exit(0)

    root.destroy()

    # ── Janela principal
    from ui.app_window import AppWindow
    app = AppWindow(user_info)
    app.mainloop()


if __name__ == "__main__":
    main()
