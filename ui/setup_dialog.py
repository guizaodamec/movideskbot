import tkinter as tk
from tkinter import ttk
import threading

try:
    from config import (
        COLOR_BG, COLOR_CARD, COLOR_CARD2, COLOR_TEXT, COLOR_TEXT_DIM,
        COLOR_ACCENT, COLOR_SUCCESS, COLOR_ERROR, COLOR_BORDER, APP_NAME
    )
except ImportError:
    COLOR_BG      = "#0D0F18"
    COLOR_CARD    = "#1A1E2E"
    COLOR_CARD2   = "#1F2437"
    COLOR_TEXT    = "#E2E8F0"
    COLOR_TEXT_DIM = "#8892A4"
    COLOR_ACCENT  = "#4B6BFB"
    COLOR_SUCCESS = "#10B981"
    COLOR_ERROR   = "#EF4444"
    COLOR_BORDER  = "#252840"
    APP_NAME      = "FarmaFacil Assistente"


class SetupDialog(object):
    """
    Dialog de configuracao de conexao ao banco.
    Retorna: self.host, self.dbname, self.confirmed
    """

    def __init__(self, parent):
        self.host      = ""
        self.dbname    = ""
        self.ai_host   = ""
        self.confirmed = False

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Configurar Conexao - " + APP_NAME)
        self.dialog.configure(bg=COLOR_BG)
        self.dialog.resizable(False, False)
        self.dialog.grab_set()
        self.dialog.focus_set()

        w, h = 440, 460
        self.dialog.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width()  - w) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - h) // 2
        self.dialog.geometry("{0}x{1}+{2}+{3}".format(w, h, x, y))

        self._build_ui()
        self._prefill()
        self.dialog.protocol("WM_DELETE_WINDOW", self._on_close)
        self.dialog.bind("<Return>", lambda e: self._connect())
        self.dialog.wait_window()

    def _build_ui(self):
        # Header
        hdr = tk.Frame(self.dialog, bg=COLOR_ACCENT, pady=16)
        hdr.pack(fill=tk.X)
        tk.Label(
            hdr, text=APP_NAME,
            bg=COLOR_ACCENT, fg="white",
            font=("Arial", 14, "bold")
        ).pack()
        tk.Label(
            hdr, text="Configure a conexao com o banco de dados",
            bg=COLOR_ACCENT, fg="#C7D2FE",
            font=("Arial", 9)
        ).pack()

        # Body
        body = tk.Frame(self.dialog, bg=COLOR_CARD, padx=24, pady=20)
        body.pack(fill=tk.BOTH, expand=True)

        # IP/Hostname
        tk.Label(
            body, text="IP ou Hostname do servidor",
            bg=COLOR_CARD, fg=COLOR_TEXT_DIM,
            font=("Arial", 9, "bold"), anchor=tk.W
        ).pack(fill=tk.X)
        tk.Label(
            body, text="Exemplos: 192.168.1.10 | servidor | DESKTOP-ABC123",
            bg=COLOR_CARD, fg=COLOR_TEXT_DIM,
            font=("Arial", 8), anchor=tk.W
        ).pack(fill=tk.X)

        self.entry_host = tk.Entry(
            body, font=("Arial", 11),
            bg=COLOR_CARD2, fg=COLOR_TEXT,
            insertbackground=COLOR_TEXT,
            relief=tk.FLAT, bd=6
        )
        self.entry_host.pack(fill=tk.X, pady=(4, 12))
        self.entry_host.focus_set()

        # Nome do banco
        tk.Label(
            body, text="Nome do banco de dados",
            bg=COLOR_CARD, fg=COLOR_TEXT_DIM,
            font=("Arial", 9, "bold"), anchor=tk.W
        ).pack(fill=tk.X)
        tk.Label(
            body, text="Exemplos: farmafacil | erp_producao | gestao",
            bg=COLOR_CARD, fg=COLOR_TEXT_DIM,
            font=("Arial", 8), anchor=tk.W
        ).pack(fill=tk.X)

        self.entry_db = tk.Entry(
            body, font=("Arial", 11),
            bg=COLOR_CARD2, fg=COLOR_TEXT,
            insertbackground=COLOR_TEXT,
            relief=tk.FLAT, bd=6
        )
        self.entry_db.pack(fill=tk.X, pady=(4, 12))

        # IP do servidor de IA
        tk.Label(
            body, text="IP do servidor de IA (Claude Code)",
            bg=COLOR_CARD, fg=COLOR_TEXT_DIM,
            font=("Arial", 9, "bold"), anchor=tk.W
        ).pack(fill=tk.X)
        tk.Label(
            body, text="Deixe em branco para usar esta maquina (localhost)",
            bg=COLOR_CARD, fg=COLOR_TEXT_DIM,
            font=("Arial", 8), anchor=tk.W
        ).pack(fill=tk.X)

        self.entry_ai = tk.Entry(
            body, font=("Arial", 11),
            bg=COLOR_CARD2, fg=COLOR_TEXT,
            insertbackground=COLOR_TEXT,
            relief=tk.FLAT, bd=6
        )
        self.entry_ai.pack(fill=tk.X, pady=(4, 16))

        # Status
        self.lbl_status = tk.Label(
            body, text="",
            bg=COLOR_CARD, fg=COLOR_TEXT_DIM,
            font=("Arial", 9), wraplength=390, anchor=tk.W
        )
        self.lbl_status.pack(fill=tk.X, pady=(0, 8))

        # Botao
        self.btn_connect = tk.Button(
            body,
            text="Conectar e escanear banco",
            font=("Arial", 10, "bold"),
            bg=COLOR_ACCENT, fg="white",
            activebackground="#6B8BFF",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            pady=8,
            command=self._connect
        )
        self.btn_connect.pack(fill=tk.X)

    def _prefill(self):
        """Preenche campos com valores salvos anteriormente."""
        try:
            from utils.profile_cache import load_connection
            conn = load_connection()
            if conn:
                if conn.get("host"):
                    self.entry_host.insert(0, conn["host"])
                if conn.get("dbname"):
                    self.entry_db.insert(0, conn["dbname"])
                ai = conn.get("ai_host", "192.168.0.118")
                if ai:
                    self.entry_ai.insert(0, ai)
        except Exception:
            pass
        # Se campo de IA ficou vazio, colocar o padrao
        if not self.entry_ai.get().strip():
            self.entry_ai.insert(0, "192.168.0.118")

    def _set_status(self, msg, color=None):
        if color is None:
            color = COLOR_TEXT_DIM
        self.lbl_status.config(text=msg, fg=color)
        self.dialog.update_idletasks()

    def _connect(self):
        host    = self.entry_host.get().strip()
        dbname  = self.entry_db.get().strip()
        ai_host = self.entry_ai.get().strip() or "localhost"

        if not host:
            self._set_status("IP/Hostname e obrigatorio.", COLOR_ERROR)
            return
        if not dbname:
            self._set_status("Nome do banco e obrigatorio.", COLOR_ERROR)
            return

        self.btn_connect.config(state=tk.DISABLED)
        self._set_status("Conectando...", COLOR_TEXT_DIM)

        def _do():
            from db.connector import connect
            ok, err = connect(host, dbname)
            self.dialog.after(0, lambda: self._on_connect_result(ok, err, host, dbname, ai_host))

        threading.Thread(target=_do, daemon=True).start()

    def _on_connect_result(self, ok, err, host, dbname, ai_host):
        if ok:
            self._set_status("Conectado com sucesso!", COLOR_SUCCESS)
            self.host      = host
            self.dbname    = dbname
            self.ai_host   = ai_host
            self.confirmed = True
            from utils.profile_cache import save_connection
            save_connection(host, dbname, ai_host)
            self.dialog.after(600, self.dialog.destroy)
        else:
            self._set_status(err, COLOR_ERROR)
            self.btn_connect.config(state=tk.NORMAL)

    def _on_close(self):
        self.confirmed = False
        self.dialog.destroy()
