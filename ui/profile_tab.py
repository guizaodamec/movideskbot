import tkinter as tk
from tkinter import ttk
import threading
import time

try:
    from config import (
        COLOR_BG, COLOR_CARD, COLOR_CARD2, COLOR_TEXT, COLOR_TEXT_DIM,
        COLOR_ACCENT, COLOR_SUCCESS, COLOR_ERROR, COLOR_WARNING, COLOR_BORDER
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
    COLOR_WARNING  = "#F59E0B"
    COLOR_BORDER   = "#252840"


class ProfileTab(tk.Frame):
    def __init__(self, parent, app_ref):
        super(ProfileTab, self).__init__(parent, bg=COLOR_BG)
        self.app     = app_ref
        self._profile = None
        self._build_ui()

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Header com botao atualizar
        hdr = tk.Frame(self, bg=COLOR_CARD, padx=16, pady=10)
        hdr.grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 4))

        tk.Label(
            hdr,
            text="Perfil do Cliente",
            bg=COLOR_CARD, fg=COLOR_TEXT,
            font=("Arial", 12, "bold")
        ).pack(side=tk.LEFT)

        self.lbl_scan_time = tk.Label(
            hdr, text="",
            bg=COLOR_CARD, fg=COLOR_TEXT_DIM,
            font=("Arial", 8)
        )
        self.lbl_scan_time.pack(side=tk.LEFT, padx=16)

        self.btn_refresh = tk.Button(
            hdr,
            text="Atualizar scan agora",
            font=("Arial", 9),
            bg=COLOR_ACCENT, fg="white",
            activebackground="#6B8BFF",
            relief=tk.FLAT, cursor="hand2",
            padx=10, pady=4,
            command=self._refresh
        )
        self.btn_refresh.pack(side=tk.RIGHT)

        # Scrollable content
        canvas = tk.Canvas(self, bg=COLOR_BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.grid(row=1, column=1, sticky="ns")
        canvas.grid(row=1, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.content_frame = tk.Frame(canvas, bg=COLOR_BG)
        self._cw = canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        self.content_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>",
            lambda e: canvas.itemconfig(self._cw, width=e.width))
        canvas.bind("<MouseWheel>",
            lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        self._canvas = canvas

    def _card(self, parent, title, pady=(8, 4)):
        frame = tk.Frame(parent, bg=COLOR_CARD, padx=14, pady=12)
        frame.pack(fill=tk.X, padx=8, pady=pady)
        tk.Label(
            frame, text=title,
            bg=COLOR_CARD, fg=COLOR_ACCENT,
            font=("Arial", 10, "bold"), anchor=tk.W
        ).pack(fill=tk.X, pady=(0, 6))
        return frame

    def update_profile(self, profile):
        self._profile = profile
        self._render()

    def _render(self):
        for w in self.content_frame.winfo_children():
            w.destroy()

        p = self._profile
        if not p:
            tk.Label(
                self.content_frame,
                text="Nenhum perfil carregado. Conecte ao banco primeiro.",
                bg=COLOR_BG, fg=COLOR_TEXT_DIM,
                font=("Arial", 10)
            ).pack(padx=16, pady=32)
            return

        # Atualizar tempo do scan
        scanned_at = p.get("scanned_at", "")
        if scanned_at:
            self.lbl_scan_time.config(text="Ultimo scan: {0}".format(scanned_at))

        # ── Card: Dados da Empresa
        c = self._card(self.content_frame, "Dados da Empresa")
        fields = [
            ("Razao Social",       p.get("razao_social", "N/A")),
            ("CNPJ",               p.get("cnpj", "N/A")),
            ("Cidade / UF",        "{0} / {1}".format(p.get("cidade","N/A"), p.get("uf","N/A"))),
            ("Regime Tributario",  p.get("regime_tributario", "N/A")),
            ("Versao do Sistema",  p.get("versao_sistema", "N/A")),
            ("PostgreSQL",         p.get("versao_postgres", "N/A")[:60]),
            ("Ultimo Backup",      p.get("ultimo_backup", "N/A")),
        ]
        for label, value in fields:
            row = tk.Frame(c, bg=COLOR_CARD)
            row.pack(fill=tk.X, pady=1)
            tk.Label(row, text=label + ":", bg=COLOR_CARD, fg=COLOR_TEXT_DIM,
                     font=("Arial", 9), width=22, anchor=tk.W).pack(side=tk.LEFT)
            tk.Label(row, text=value, bg=COLOR_CARD, fg=COLOR_TEXT,
                     font=("Arial", 9, "bold"), anchor=tk.W).pack(side=tk.LEFT)

        # ── Card: Modulos
        c2 = self._card(self.content_frame, "Modulos Detectados")
        modulos = p.get("modulos_detectados", [])
        all_mods = [
            "Fiscal (NF-e)", "Fiscal (NFS)", "Producao", "Estoque",
            "Produtos", "Financeiro", "RH / Folha", "Vendas"
        ]
        grid_frame = tk.Frame(c2, bg=COLOR_CARD)
        grid_frame.pack(fill=tk.X)
        for i, mod in enumerate(all_mods):
            detected = mod in modulos
            color = COLOR_SUCCESS if detected else COLOR_ERROR
            icon  = "✓" if detected else "✗"
            status = "Ativo" if detected else "Nao encontrado"
            cell = tk.Frame(grid_frame, bg=COLOR_CARD2, padx=10, pady=6)
            cell.grid(row=i // 4, column=i % 4, padx=4, pady=2, sticky="nsew")
            grid_frame.columnconfigure(i % 4, weight=1)
            tk.Label(cell, text=icon + " " + mod, bg=COLOR_CARD2, fg=color,
                     font=("Arial", 9, "bold"), anchor=tk.W).pack(fill=tk.X)
            tk.Label(cell, text=status, bg=COLOR_CARD2, fg=COLOR_TEXT_DIM,
                     font=("Arial", 8), anchor=tk.W).pack(fill=tk.X)

        # ── Card: Top 10 tabelas por volume
        c3 = self._card(self.content_frame, "Top Tabelas por Volume")
        volumes = p.get("volumes", [])[:10]
        if volumes:
            tree = ttk.Treeview(c3, columns=("tabela", "registros"), show="headings", height=len(volumes))
            style = ttk.Style()
            style.configure("Profile.Treeview",
                background=COLOR_CARD2, foreground=COLOR_TEXT,
                rowheight=20, fieldbackground=COLOR_CARD2, font=("Arial", 8))
            style.configure("Profile.Treeview.Heading",
                background=COLOR_ACCENT, foreground="white", font=("Arial", 8, "bold"))
            tree.configure(style="Profile.Treeview")
            tree.heading("tabela", text="Tabela")
            tree.heading("registros", text="Registros")
            tree.column("tabela", width=300)
            tree.column("registros", width=120, anchor=tk.E)
            for v in volumes:
                tree.insert("", tk.END, values=(v["table"], "{:,}".format(v["registros"])))
            tree.pack(fill=tk.X)
        else:
            tk.Label(c3, text="Dados nao disponiveis.", bg=COLOR_CARD,
                     fg=COLOR_TEXT_DIM, font=("Arial", 9)).pack(anchor=tk.W)

        # ── Card: Erros recorrentes
        c4 = self._card(self.content_frame, "Erros Recorrentes (ultimos registros)")
        erros = p.get("erros_recorrentes", [])
        if erros:
            for err in erros[:5]:
                row_text = " | ".join("{0}: {1}".format(k, str(v)[:60]) for k, v in err.items())
                tk.Label(c4, text=row_text, bg=COLOR_CARD, fg=COLOR_TEXT_DIM,
                         font=("Courier New", 8), anchor=tk.W, wraplength=800,
                         justify=tk.LEFT).pack(fill=tk.X, pady=1)
        else:
            tk.Label(c4, text="Nenhum erro encontrado ou tabela nao localizada.",
                     bg=COLOR_CARD, fg=COLOR_TEXT_DIM, font=("Arial", 9)).pack(anchor=tk.W)

        # ── Card: Queries lentas
        c5 = self._card(self.content_frame, "Queries Lentas")
        qs = p.get("queries_lentas", [])
        if qs:
            for q in qs[:5]:
                text = "{0:.1f}ms (calls: {1}) — {2}".format(
                    q.get("mean_ms", 0), q.get("calls", 0), q.get("query", "")[:150]
                )
                tk.Label(c5, text=text, bg=COLOR_CARD, fg=COLOR_TEXT_DIM,
                         font=("Courier New", 8), anchor=tk.W, wraplength=800,
                         justify=tk.LEFT).pack(fill=tk.X, pady=1)
        else:
            tk.Label(c5, text="pg_stat_statements nao disponivel ou sem dados.",
                     bg=COLOR_CARD, fg=COLOR_TEXT_DIM, font=("Arial", 9)).pack(anchor=tk.W)

        # ── Card: Conexoes e Locks
        c6 = self._card(self.content_frame, "Conexoes e Locks")
        conexoes = p.get("conexoes_ativas", {})
        locks    = p.get("locks_ativos", 0)
        for state, cnt in conexoes.items():
            tk.Label(c6, text="{0}: {1} conexoes".format(state, cnt),
                     bg=COLOR_CARD, fg=COLOR_TEXT_DIM, font=("Arial", 9)).pack(anchor=tk.W)
        lock_color = COLOR_ERROR if locks > 0 else COLOR_SUCCESS
        tk.Label(c6, text="Locks aguardando: {0}".format(locks),
                 bg=COLOR_CARD, fg=lock_color, font=("Arial", 9, "bold")).pack(anchor=tk.W)

        self._canvas.after(100, lambda: self._canvas.yview_moveto(0))

    def _refresh(self):
        self.app.run_scanner()
