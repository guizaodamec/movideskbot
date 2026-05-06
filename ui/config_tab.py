import tkinter as tk
from tkinter import scrolledtext
import threading

try:
    from config import (
        COLOR_BG, COLOR_CARD, COLOR_CARD2, COLOR_TEXT, COLOR_TEXT_DIM,
        COLOR_ACCENT, COLOR_SUCCESS, COLOR_ERROR, COLOR_BORDER
    )
except ImportError:
    COLOR_BG       = "#0D0F18"
    COLOR_CARD     = "#1A1E2E"
    COLOR_CARD2    = "#1F2437"
    COLOR_TEXT     = "#E2E8F0"
    COLOR_TEXT_DIM = "#8892A4"
    COLOR_ACCENT   = "#4B6BFB"
    COLOR_SUCCESS  = "#10B981"
    COLOR_ERROR    = "#EF4444"
    COLOR_BORDER   = "#252840"

from db.connector import connect, is_connected, get_host, get_dbname
from utils.profile_cache import save_connection


class ConfigTab(tk.Frame):
    def __init__(self, parent, app_ref):
        super(ConfigTab, self).__init__(parent, bg=COLOR_BG)
        self.app = app_ref
        self._build_ui()

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        # ── Card: Conexao
        conn_card = tk.Frame(self, bg=COLOR_CARD, padx=20, pady=16)
        conn_card.grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 4))
        conn_card.columnconfigure(1, weight=1)

        tk.Label(
            conn_card, text="Configuracao de Conexao",
            bg=COLOR_CARD, fg=COLOR_ACCENT,
            font=("Arial", 11, "bold")
        ).grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))

        # IP
        tk.Label(conn_card, text="IP / Hostname:", bg=COLOR_CARD, fg=COLOR_TEXT_DIM,
                 font=("Arial", 9), width=18, anchor=tk.W).grid(row=1, column=0, sticky=tk.W)
        self.entry_host = tk.Entry(
            conn_card, font=("Arial", 10),
            bg=COLOR_CARD2, fg=COLOR_TEXT,
            insertbackground=COLOR_TEXT, relief=tk.FLAT, bd=6
        )
        self.entry_host.grid(row=1, column=1, sticky="ew", padx=(8, 8))

        # Banco
        tk.Label(conn_card, text="Banco de dados:", bg=COLOR_CARD, fg=COLOR_TEXT_DIM,
                 font=("Arial", 9), width=18, anchor=tk.W).grid(row=2, column=0, sticky=tk.W, pady=(8, 0))
        self.entry_db = tk.Entry(
            conn_card, font=("Arial", 10),
            bg=COLOR_CARD2, fg=COLOR_TEXT,
            insertbackground=COLOR_TEXT, relief=tk.FLAT, bd=6
        )
        self.entry_db.grid(row=2, column=1, sticky="ew", padx=(8, 8), pady=(8, 0))

        self.btn_reconnect = tk.Button(
            conn_card,
            text="Reconectar",
            font=("Arial", 9, "bold"),
            bg=COLOR_ACCENT, fg="white",
            activebackground="#6B8BFF",
            relief=tk.FLAT, cursor="hand2",
            padx=12, pady=6,
            command=self._reconnect
        )
        self.btn_reconnect.grid(row=1, column=2, rowspan=2, padx=(0, 0), pady=(0, 0))

        # Status
        self.lbl_status = tk.Label(
            conn_card, text="",
            bg=COLOR_CARD, fg=COLOR_TEXT_DIM,
            font=("Arial", 9), anchor=tk.W
        )
        self.lbl_status.grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=(8, 0))

        # ── Card: Status atual
        status_card = tk.Frame(self, bg=COLOR_CARD, padx=20, pady=12)
        status_card.grid(row=1, column=0, sticky="ew", padx=8, pady=4)

        tk.Label(
            status_card, text="Status da Conexao",
            bg=COLOR_CARD, fg=COLOR_ACCENT,
            font=("Arial", 10, "bold")
        ).pack(anchor=tk.W, pady=(0, 6))

        self.lbl_conn_info = tk.Label(
            status_card, text="Verificando...",
            bg=COLOR_CARD, fg=COLOR_TEXT_DIM,
            font=("Arial", 9)
        )
        self.lbl_conn_info.pack(anchor=tk.W)

        # ── Log do scanner
        log_card = tk.Frame(self, bg=COLOR_CARD, padx=20, pady=12)
        log_card.grid(row=2, column=0, sticky="nsew", padx=8, pady=(4, 8))
        log_card.columnconfigure(0, weight=1)
        log_card.rowconfigure(1, weight=1)

        tk.Label(
            log_card, text="Log do Scanner",
            bg=COLOR_CARD, fg=COLOR_ACCENT,
            font=("Arial", 10, "bold")
        ).grid(row=0, column=0, sticky=tk.W, pady=(0, 6))

        self.log_text = tk.Text(
            log_card, font=("Courier New", 9),
            bg=COLOR_CARD2, fg="#86EFAC",
            relief=tk.FLAT, bd=6,
            state=tk.DISABLED
        )
        self.log_text.grid(row=1, column=0, sticky="nsew")

        self._load_current()

    def _load_current(self):
        host   = get_host() or ""
        dbname = get_dbname() or ""
        self.entry_host.insert(0, host)
        self.entry_db.insert(0, dbname)
        self._update_status()

    def _update_status(self):
        connected = is_connected()
        host   = get_host() or "-"
        dbname = get_dbname() or "-"
        if connected:
            self.lbl_conn_info.config(
                text="Conectado a {0} / banco {1}".format(host, dbname),
                fg=COLOR_SUCCESS
            )
        else:
            self.lbl_conn_info.config(text="Sem conexao", fg=COLOR_ERROR)

    def _set_status(self, msg, color=None):
        if color is None:
            color = COLOR_TEXT_DIM
        self.lbl_status.config(text=msg, fg=color)
        self.update_idletasks()

    def _reconnect(self):
        host   = self.entry_host.get().strip()
        dbname = self.entry_db.get().strip()
        if not host or not dbname:
            self._set_status("Preencha IP e nome do banco.", COLOR_ERROR)
            return

        self.btn_reconnect.config(state=tk.DISABLED)
        self._set_status("Conectando...", COLOR_TEXT_DIM)

        def _do():
            ok, err = connect(host, dbname)
            self.after(0, lambda: self._on_reconnect(ok, err, host, dbname))

        threading.Thread(target=_do, daemon=True).start()

    def _on_reconnect(self, ok, err, host, dbname):
        self.btn_reconnect.config(state=tk.NORMAL)
        if ok:
            save_connection(host, dbname)
            self._set_status("Conectado com sucesso!", COLOR_SUCCESS)
            self._update_status()
            self.app.run_scanner()
        else:
            self._set_status(err, COLOR_ERROR)

    def append_log(self, msg):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def clear_log(self):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.config(state=tk.DISABLED)

    def refresh_status(self):
        self._update_status()
