import tkinter as tk
from tkinter import ttk, filedialog
import threading
import time
import re

try:
    from config import (
        COLOR_BG, COLOR_CARD, COLOR_CARD2, COLOR_CARD3,
        COLOR_TEXT, COLOR_TEXT_DIM, COLOR_TEXT_MUT,
        COLOR_ACCENT, COLOR_ACCENT_H, COLOR_ACCENT_BG,
        COLOR_SUCCESS, COLOR_ERROR, COLOR_WARNING,
        COLOR_BORDER, COLOR_DIVIDER,
        COLOR_MSG_AI, COLOR_MSG_USER,
        COLOR_INPUT_BG, MAX_CHAT_HISTORY,
        FONT_HEAD, FONT_BODY, FONT_LABEL, FONT_SMALL, FONT_TINY,
        FONT_BTN, FONT_BTN_S, FONT_MONO, FONT_MONO_S
    )
except ImportError:
    COLOR_BG       = "#0B0D16"
    COLOR_CARD     = "#141926"
    COLOR_CARD2    = "#19202F"
    COLOR_CARD3    = "#1E2638"
    COLOR_TEXT     = "#E2E8F6"
    COLOR_TEXT_DIM = "#6B7A94"
    COLOR_TEXT_MUT = "#3A4560"
    COLOR_ACCENT   = "#4F74F9"
    COLOR_ACCENT_H = "#6B8DFF"
    COLOR_ACCENT_BG= "#111830"
    COLOR_SUCCESS  = "#34D399"
    COLOR_ERROR    = "#F87171"
    COLOR_WARNING  = "#FBBF24"
    COLOR_BORDER   = "#1C2438"
    COLOR_DIVIDER  = "#141A28"
    COLOR_MSG_AI   = "#141926"
    COLOR_MSG_USER = "#0D1420"
    COLOR_INPUT_BG = "#131826"
    MAX_CHAT_HISTORY = 20
    FONT_HEAD   = ("Segoe UI", 11, "bold")
    FONT_BODY   = ("Segoe UI", 10)
    FONT_LABEL  = ("Segoe UI", 9)
    FONT_SMALL  = ("Segoe UI", 8)
    FONT_TINY   = ("Segoe UI", 7)
    FONT_BTN    = ("Segoe UI", 10, "bold")
    FONT_BTN_S  = ("Segoe UI", 9)
    FONT_MONO   = ("Consolas", 9)
    FONT_MONO_S = ("Consolas", 8)

from ai.client import ask, extract_queries
from ai.context_builder import build_system_prompt
from db.connector import execute_query, execute_modify, is_connected
from ui.confirm_dialog import ConfirmQueryDialog
from utils.query_log import log_query


def _hover(w, on, off):
    w.bind("<Enter>", lambda e: w.config(bg=on))
    w.bind("<Leave>", lambda e: w.config(bg=off))


# Largura maxima das mensagens (estilo Claude.ai)
MSG_MAX_WIDTH = 720


class ChatTab(tk.Frame):
    def __init__(self, parent, app_ref):
        super(ChatTab, self).__init__(parent, bg=COLOR_BG)
        self.app      = app_ref
        self.messages = []
        self._build_ui()

    # ── Layout ────────────────────────────────────────────────────────

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        self._build_messages()
        self._build_input()

    def _build_messages(self):
        wrap = tk.Frame(self, bg=COLOR_BG)
        wrap.grid(row=0, column=0, sticky="nsew")
        wrap.columnconfigure(0, weight=1)
        wrap.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(wrap, bg=COLOR_BG, highlightthickness=0)
        vsb = tk.Scrollbar(wrap, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vsb.set)

        vsb.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        wrap.rowconfigure(0, weight=1)

        self.msgs_frame = tk.Frame(self.canvas, bg=COLOR_BG)
        self._cw = self.canvas.create_window(
            (0, 0), window=self.msgs_frame, anchor="nw")

        self.msgs_frame.bind("<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        self.canvas.bind("<MouseWheel>", self._scroll)
        self.msgs_frame.bind("<MouseWheel>", self._scroll)

        # Barra "pensando"
        self.thinking_bar = tk.Frame(self, bg=COLOR_CARD2, pady=6)
        tk.Label(self.thinking_bar, text="Aguardando IA...",
                 bg=COLOR_CARD2, fg=COLOR_TEXT_DIM,
                 font=("Segoe UI", 9, "italic")).pack(side=tk.LEFT, padx=16)
        self._thinking_pb = ttk.Progressbar(
            self.thinking_bar, mode="indeterminate", length=120)
        self._thinking_pb.pack(side=tk.LEFT)

    def _build_input(self):
        # Linha separadora
        tk.Frame(self, bg=COLOR_BORDER, height=1).grid(
            row=1, column=0, sticky="ew")

        bar = tk.Frame(self, bg=COLOR_BG, pady=16)
        bar.grid(row=1, column=0, sticky="ew")
        bar.columnconfigure(0, weight=1)

        # Container centralizado
        center = tk.Frame(bar, bg=COLOR_BG)
        center.pack(fill=tk.X, padx=60)
        center.columnconfigure(0, weight=1)

        # Borda do campo de texto
        border = tk.Frame(center, bg=COLOR_BORDER, padx=1, pady=1)
        border.grid(row=0, column=0, sticky="ew")
        border.columnconfigure(0, weight=1)

        inner = tk.Frame(border, bg=COLOR_CARD2)
        inner.grid(row=0, column=0, sticky="ew")
        inner.columnconfigure(0, weight=1)

        self.text_input = tk.Text(
            inner, height=3,
            font=FONT_BODY,
            bg=COLOR_CARD2, fg=COLOR_TEXT,
            insertbackground=COLOR_ACCENT,
            relief=tk.FLAT, bd=0,
            wrap=tk.WORD,
            padx=16, pady=12
        )
        self.text_input.grid(row=0, column=0, sticky="ew")
        self.text_input.bind("<Return>",       self._on_enter)
        self.text_input.bind("<Shift-Return>", lambda e: None)

        def _fi(e): border.config(bg=COLOR_ACCENT)
        def _fo(e): border.config(bg=COLOR_BORDER)
        self.text_input.bind("<FocusIn>",  _fi)
        self.text_input.bind("<FocusOut>", _fo)

        # Botoes abaixo do input
        btns = tk.Frame(center, bg=COLOR_BG)
        btns.grid(row=1, column=0, sticky="ew", pady=(6, 0))

        self.btn_send = tk.Button(
            btns, text="Enviar",
            font=("Segoe UI", 9, "bold"),
            bg=COLOR_ACCENT, fg="white",
            activebackground=COLOR_ACCENT_H, activeforeground="white",
            relief=tk.FLAT, cursor="hand2",
            padx=20, pady=7,
            command=self._send_message)
        self.btn_send.pack(side=tk.RIGHT, padx=(6, 0))
        _hover(self.btn_send, COLOR_ACCENT_H, COLOR_ACCENT)

        btn_copy = tk.Button(
            btns, text="Copiar chat",
            font=("Segoe UI", 8),
            bg=COLOR_CARD2, fg=COLOR_TEXT_DIM,
            activebackground=COLOR_CARD3, activeforeground=COLOR_TEXT,
            relief=tk.FLAT, cursor="hand2",
            padx=12, pady=7,
            command=self._copy_chat)
        btn_copy.pack(side=tk.RIGHT)
        _hover(btn_copy, COLOR_CARD3, COLOR_CARD2)

        btn_export = tk.Button(
            btns, text="Exportar",
            font=("Segoe UI", 8),
            bg=COLOR_CARD2, fg=COLOR_TEXT_DIM,
            activebackground=COLOR_CARD3, activeforeground=COLOR_TEXT,
            relief=tk.FLAT, cursor="hand2",
            padx=12, pady=7,
            command=self._export)
        btn_export.pack(side=tk.RIGHT, padx=(0, 6))
        _hover(btn_export, COLOR_CARD3, COLOR_CARD2)

        tk.Label(btns, text="Enter envia  |  Shift+Enter nova linha",
                 bg=COLOR_BG, fg=COLOR_TEXT_MUT,
                 font=("Segoe UI", 7)).pack(side=tk.LEFT)

    # ── Canvas ────────────────────────────────────────────────────────

    def _on_canvas_resize(self, event):
        self.canvas.itemconfig(self._cw, width=event.width)

    def _scroll(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _to_bottom(self):
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def _on_enter(self, event):
        if not (event.state & 0x1):
            self._send_message()
            return "break"

    # ── Perfil ────────────────────────────────────────────────────────

    def set_profile(self, profile):
        self._profile = profile

    def add_welcome(self, msg):
        self._add_bubble("assistant", msg)

    # ── Bolhas ────────────────────────────────────────────────────────

    def _add_bubble(self, role, text, bg=None):
        is_ai = (role == "assistant")
        bg    = bg or (COLOR_MSG_AI if is_ai else COLOR_MSG_USER)

        # Linha de separacao sutil entre mensagens
        tk.Frame(self.msgs_frame, bg=COLOR_BG, height=2).pack(fill=tk.X)

        outer = tk.Frame(self.msgs_frame, bg=COLOR_BG)
        outer.pack(fill=tk.X, padx=0, pady=0)

        # Centralizar com padding lateral
        outer.columnconfigure(0, weight=1)
        inner_pad = tk.Frame(outer, bg=COLOR_BG)
        inner_pad.pack(fill=tk.X, padx=48)

        bubble = tk.Frame(inner_pad, bg=bg, padx=20, pady=14)
        bubble.pack(fill=tk.X)

        # Remetente
        sender      = "Assistente" if is_ai else \
            getattr(self.app, "current_user", {}).get("username", "Voce")
        sender_color = COLOR_ACCENT if is_ai else COLOR_SUCCESS

        meta = tk.Frame(bubble, bg=bg)
        meta.pack(fill=tk.X, pady=(0, 6))
        tk.Label(meta, text=sender, bg=bg,
                 fg=sender_color, font=("Segoe UI", 8, "bold")
                 ).pack(side=tk.LEFT)
        tk.Label(meta, text="  " + time.strftime("%H:%M"),
                 bg=bg, fg=COLOR_TEXT_MUT,
                 font=("Segoe UI", 7)).pack(side=tk.LEFT)

        # Texto seleccionavel
        txt = tk.Text(
            bubble,
            font=FONT_BODY,
            bg=bg, fg=COLOR_TEXT,
            relief=tk.FLAT, bd=0,
            wrap=tk.WORD,
            cursor="xterm", height=1,
            selectbackground=COLOR_ACCENT,
            padx=0, pady=0,
        )
        txt.insert("1.0", text)
        txt.config(state=tk.DISABLED)
        txt.pack(fill=tk.X)
        txt.bind("<MouseWheel>", self._scroll)

        def _resize(e, t=txt):
            lines = int(t.index(tk.END).split(".")[0]) - 1
            t.config(height=max(1, lines))
        txt.bind("<Configure>", _resize)

        self._to_bottom()
        return outer

    # ── Bloco de query colapsavel ─────────────────────────────────────

    def _add_query_block(self, sql, rows, cols, err=None):
        """Adiciona bloco colapsavel de query + resultado no chat."""
        tk.Frame(self.msgs_frame, bg=COLOR_BG, height=2).pack(fill=tk.X)

        outer = tk.Frame(self.msgs_frame, bg=COLOR_BG)
        outer.pack(fill=tk.X)

        inner_pad = tk.Frame(outer, bg=COLOR_BG)
        inner_pad.pack(fill=tk.X, padx=48)

        # Cor do bloco
        blk_bg  = "#091A10" if not err else "#1A0A0A"
        hdr_fg  = "#34D399" if not err else COLOR_ERROR
        n_rows  = len(rows) if rows else 0
        summary = "{0} linhas".format(n_rows) if not err \
                  else "Erro"

        # Cabecalho (sempre visivel) — clica para expandir
        hdr = tk.Frame(inner_pad, bg=blk_bg, padx=14, pady=9,
                       cursor="hand2")
        hdr.pack(fill=tk.X)
        hdr.columnconfigure(1, weight=1)

        self._lbl_toggle = tk.Label(
            hdr, text="+ Ver query",
            bg=blk_bg, fg=hdr_fg,
            font=("Segoe UI", 8, "bold"), cursor="hand2")
        self._lbl_toggle.grid(row=0, column=0, sticky=tk.W)

        sql_preview = sql.strip().replace("\n", " ")[:80]
        if len(sql.strip()) > 80:
            sql_preview += "..."
        tk.Label(hdr,
                 text=sql_preview,
                 bg=blk_bg, fg=COLOR_TEXT_MUT,
                 font=("Consolas", 8),
                 anchor=tk.W).grid(row=0, column=1, sticky="ew", padx=(12, 0))

        tk.Label(hdr, text=summary,
                 bg=blk_bg, fg=hdr_fg,
                 font=("Segoe UI", 8)).grid(row=0, column=2, padx=(8, 0))

        # Corpo colapsavel (oculto por padrao)
        body = tk.Frame(inner_pad, bg=blk_bg)
        _expanded = [False]

        def _toggle(e=None):
            if _expanded[0]:
                body.pack_forget()
                self._lbl_toggle.config(text="+ Ver query")
                _expanded[0] = False
            else:
                body.pack(fill=tk.X)
                self._lbl_toggle.config(text="- Ocultar query")
                _expanded[0] = True
            self._to_bottom()

        hdr.bind("<Button-1>", _toggle)
        for child in hdr.winfo_children():
            child.bind("<Button-1>", _toggle)

        # SQL dentro do corpo
        sql_frame = tk.Frame(body, bg="#040E08", padx=14, pady=10)
        sql_frame.pack(fill=tk.X)

        sql_txt = tk.Text(
            sql_frame, font=("Consolas", 9),
            bg="#040E08", fg="#86EFAC",
            relief=tk.FLAT, bd=0,
            wrap=tk.WORD, height=1,
            cursor="xterm",
            selectbackground=COLOR_ACCENT)
        sql_txt.insert("1.0", sql.strip())
        sql_txt.config(state=tk.DISABLED)
        sql_txt.pack(fill=tk.X)

        def _rsz(e, t=sql_txt):
            n = int(t.index(tk.END).split(".")[0]) - 1
            t.config(height=max(1, n))
        sql_txt.bind("<Configure>", _rsz)

        # Botao copiar SQL
        btn_cp = tk.Button(
            sql_frame, text="Copiar SQL",
            font=("Segoe UI", 7),
            bg="#040E08", fg="#86EFAC",
            activebackground="#0A1A10", activeforeground="#86EFAC",
            relief=tk.FLAT, cursor="hand2", padx=8, pady=2)
        def _cp(s=sql):
            self.clipboard_clear()
            self.clipboard_append(s)
            btn_cp.config(text="Copiado!")
            self.after(1400, lambda: btn_cp.config(text="Copiar SQL"))
        btn_cp.config(command=_cp)
        btn_cp.pack(anchor=tk.E, pady=(6, 0))

        if err:
            tk.Label(body,
                     text="Erro: {0}".format(err),
                     bg=blk_bg, fg=COLOR_ERROR,
                     font=FONT_SMALL, wraplength=700,
                     anchor=tk.W, padx=14, pady=8).pack(fill=tk.X)
            self._to_bottom()
            return

        # Tabela de resultado
        if rows and cols:
            tbl_frame = tk.Frame(body, bg=blk_bg, padx=8, pady=8)
            tbl_frame.pack(fill=tk.X)

            tree = ttk.Treeview(
                tbl_frame, columns=cols,
                show="headings",
                height=min(len(rows), 12))

            style = ttk.Style()
            style.configure("Q.Treeview",
                background=COLOR_CARD2, foreground=COLOR_TEXT,
                rowheight=24, fieldbackground=COLOR_CARD2,
                font=("Segoe UI", 9))
            style.configure("Q.Treeview.Heading",
                background=COLOR_CARD3, foreground=COLOR_TEXT_DIM,
                font=("Segoe UI", 8, "bold"))
            style.map("Q.Treeview",
                background=[("selected", COLOR_ACCENT)])
            tree.configure(style="Q.Treeview")

            for col in cols:
                tree.heading(col, text=col)
                tree.column(col, width=max(80, len(col)*10), minwidth=60)

            for row in rows[:200]:
                vals = [
                    str(row.get(c, "")) if hasattr(row, "get") else str(row)
                    for c in cols
                ]
                tree.insert("", tk.END, values=vals)

            # Scrollbar horizontal
            hsb = ttk.Scrollbar(tbl_frame, orient=tk.HORIZONTAL,
                                 command=tree.xview)
            tree.configure(xscrollcommand=hsb.set)
            tree.pack(fill=tk.X)
            hsb.pack(fill=tk.X)

            info = "{0} linhas".format(len(rows))
            if len(rows) > 200:
                info += "  (exibindo 200 de {0})".format(len(rows))
            tk.Label(body, text=info,
                     bg=blk_bg, fg=COLOR_TEXT_MUT,
                     font=("Segoe UI", 7),
                     anchor=tk.W, padx=14, pady=4).pack(fill=tk.X)

        self._to_bottom()

    def _add_modify_block(self, sql):
        """Bloco de confirmacao para DML."""
        tk.Frame(self.msgs_frame, bg=COLOR_BG, height=2).pack(fill=tk.X)

        outer = tk.Frame(self.msgs_frame, bg=COLOR_BG)
        outer.pack(fill=tk.X)
        inner_pad = tk.Frame(outer, bg=COLOR_BG)
        inner_pad.pack(fill=tk.X, padx=48)

        blk = tk.Frame(inner_pad, bg="#1A1306", padx=14, pady=12)
        blk.pack(fill=tk.X)

        tk.Label(blk, text="Operacao de modificacao — aguarda confirmacao",
                 bg="#1A1306", fg=COLOR_WARNING,
                 font=("Segoe UI", 8, "bold")).pack(anchor=tk.W, pady=(0, 8))

        sql_txt = tk.Text(
            blk, font=("Consolas", 9),
            bg="#0F0A02", fg="#FCD34D",
            relief=tk.FLAT, bd=0,
            wrap=tk.WORD, height=1,
            cursor="xterm", padx=10, pady=8)
        sql_txt.insert("1.0", sql.strip())
        sql_txt.config(state=tk.DISABLED)
        sql_txt.pack(fill=tk.X, pady=(0, 10))

        def _rsz(e, t=sql_txt):
            n = int(t.index(tk.END).split(".")[0]) - 1
            t.config(height=max(1, n))
        sql_txt.bind("<Configure>", _rsz)

        btn = tk.Button(
            blk, text="Executar  (requer confirmacao)",
            font=("Segoe UI", 9, "bold"),
            bg="#92400E", fg="white",
            activebackground="#B45309", activeforeground="white",
            relief=tk.FLAT, cursor="hand2",
            padx=16, pady=8)
        def _run(q=sql):
            self._execute_modify_with_confirm(q)
        btn.config(command=_run)
        btn.pack(anchor=tk.W)

        self._to_bottom()

    # ── Envio ─────────────────────────────────────────────────────────

    def _fetch_live_schema(self):
        rows, cols, err = execute_query(
            "SELECT table_schema, table_name, table_type "
            "FROM information_schema.tables "
            "WHERE table_schema NOT IN "
            "('pg_catalog','information_schema','pg_toast') "
            "AND table_schema NOT LIKE 'pg_%' "
            "ORDER BY table_schema, table_name"
        )
        if err or not rows:
            return ""
        lines = []
        for r in rows:
            s = str(r.get("table_schema", ""))
            n = str(r.get("table_name",   ""))
            t = "VIEW" if str(r.get("table_type","")).upper() == "VIEW" \
                else "TABLE"
            p = "{0}.{1}".format(s, n) if s != "public" else n
            lines.append("  {0} ({1})".format(p, t))
        return "\n".join(lines)

    def _send_message(self):
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            return
        if not is_connected():
            self._add_bubble("assistant",
                "Sem conexao com o banco. Reconecte na aba Configuracao.")
            return

        self.text_input.delete("1.0", tk.END)
        self._add_bubble("user", text)

        self.messages.append({"role": "user", "content": text})
        if len(self.messages) > MAX_CHAT_HISTORY * 2:
            self.messages = self.messages[-(MAX_CHAT_HISTORY * 2):]

        self._show_thinking(True)
        self.btn_send.config(state=tk.DISABLED)

        profile       = getattr(self, "_profile", None)
        msgs_snapshot = list(self.messages)

        def _call():
            try:
                live   = self._fetch_live_schema()
                sysp   = build_system_prompt(profile, live_schema=live)
                resp   = ask(sysp, msgs_snapshot)
                self.after(0, lambda: self._on_response(resp))
            except Exception as e:
                _e = str(e)
                self.after(0, lambda: self._on_error(_e))

        threading.Thread(target=_call, daemon=True).start()

    def _on_response(self, response):
        self._show_thinking(False)
        self.btn_send.config(state=tk.NORMAL)

        self.messages.append({"role": "assistant", "content": response})

        queries = extract_queries(response)

        # Texto limpo (sem blocos SQL)
        clean = re.sub(r"```sql\s*\n.*?\n```", "", response,
                       flags=re.DOTALL | re.IGNORECASE).strip()
        if clean:
            self._add_bubble("assistant", clean)

        # Queries como blocos colapsaveis
        for q in queries:
            if q["type"] == "SELECT":
                rows, cols, err = execute_query(q["sql"])
                self._add_query_block(q["sql"], rows, cols, err)
                if err:
                    self._auto_fix(q["sql"], err)
            else:
                self._add_modify_block(q["sql"])

        self.app.update_token_display()

    def _auto_fix(self, sql, err):
        fix = (
            "A query retornou erro. Corrija usando apenas tabelas e colunas "
            "existentes no schema.\n\nQuery:\n```sql\n{0}\n```\n\nErro:\n{1}"
        ).format(sql, err)

        self.messages.append({"role": "user", "content": fix})
        self._show_thinking(True)
        self.btn_send.config(state=tk.DISABLED)

        profile = getattr(self, "_profile", None)
        snap    = list(self.messages)

        def _call():
            try:
                live = self._fetch_live_schema()
                sysp = build_system_prompt(profile, live_schema=live)
                resp = ask(sysp, snap)
                self.after(0, lambda: self._on_response(resp))
            except Exception as e:
                _e = str(e)
                self.after(0, lambda: self._on_error(_e))

        threading.Thread(target=_call, daemon=True).start()

    def _on_error(self, error):
        self._show_thinking(False)
        self.btn_send.config(state=tk.NORMAL)
        self._add_bubble("assistant",
            "Erro ao contatar a IA: {0}".format(error), bg=COLOR_CARD2)

    def _show_thinking(self, show):
        if show:
            self.thinking_bar.grid(row=0, column=0, sticky="sew")
            self._thinking_pb.start(12)
        else:
            self._thinking_pb.stop()
            self.thinking_bar.grid_remove()

    # ── DML ───────────────────────────────────────────────────────────

    def _execute_modify_with_confirm(self, sql):
        dlg = ConfirmQueryDialog(self.winfo_toplevel(), sql)
        if dlg.result:
            rowcount, err = execute_modify(sql)
            uname = getattr(self.app, "current_user", {}).get("username", "sistema")
            if err:
                self._add_bubble("assistant",
                    "Erro ao executar: {0}".format(err), bg=COLOR_CARD2)
                log_query(sql, "ERRO: " + err, uname)
            else:
                self._add_bubble("assistant",
                    "{0} linha(s) afetada(s).".format(rowcount))
                log_query(sql, "{0} linhas".format(rowcount), uname)

    # ── Copiar / Exportar ─────────────────────────────────────────────

    def _copy_chat(self):
        if not self.messages:
            return
        lines = []
        for m in self.messages:
            role = "Assistente" if m["role"] == "assistant" else "Voce"
            c    = m.get("content", "")
            if isinstance(c, list):
                c = " ".join(p.get("text","") for p in c
                             if isinstance(p, dict) and p.get("type") == "text")
            lines.append("[{0}]\n{1}".format(role, c))
        self.clipboard_clear()
        self.clipboard_append("\n\n---\n\n".join(lines))

    def _export(self):
        path = filedialog.asksaveasfilename(
            title="Exportar conversa",
            defaultextension=".txt",
            filetypes=[("Texto", "*.txt"), ("Todos", "*.*")])
        if not path:
            return
        lines = ["FarmaFacil Assistente — Exportacao",
                 time.strftime("%Y-%m-%d %H:%M:%S"),
                 "=" * 60, ""]
        for m in self.messages:
            role = "Assistente" if m["role"] == "assistant" else "Usuario"
            c    = m.get("content", "")
            if isinstance(c, list):
                c = " ".join(p.get("text","") for p in c
                             if isinstance(p, dict) and p.get("type") == "text")
            lines.append("[{0}]\n{1}\n".format(role, c))
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
        except Exception:
            pass

    def clear_history(self):
        self.messages = []
        for w in self.msgs_frame.winfo_children():
            w.destroy()
