import tkinter as tk
from tkinter import ttk
import threading
import time

try:
    from config import (
        COLOR_BG, COLOR_SIDEBAR, COLOR_CARD, COLOR_CARD2, COLOR_CARD3,
        COLOR_TEXT, COLOR_TEXT_DIM, COLOR_TEXT_MUT,
        COLOR_ACCENT, COLOR_ACCENT_H,
        COLOR_SUCCESS, COLOR_ERROR, COLOR_WARNING,
        COLOR_BORDER, COLOR_DIVIDER, COLOR_ACTIVE,
        APP_NAME, APP_VERSION,
        FONT_HEAD, FONT_BODY, FONT_LABEL, FONT_SMALL, FONT_TINY,
        FONT_NAV, FONT_BTN_S
    )
except ImportError:
    COLOR_BG       = "#0B0D16"
    COLOR_SIDEBAR  = "#0E1120"
    COLOR_CARD     = "#141926"
    COLOR_CARD2    = "#19202F"
    COLOR_CARD3    = "#1E2638"
    COLOR_TEXT     = "#E2E8F6"
    COLOR_TEXT_DIM = "#6B7A94"
    COLOR_TEXT_MUT = "#3A4560"
    COLOR_ACCENT   = "#4F74F9"
    COLOR_ACCENT_H = "#6B8DFF"
    COLOR_SUCCESS  = "#34D399"
    COLOR_ERROR    = "#F87171"
    COLOR_WARNING  = "#FBBF24"
    COLOR_BORDER   = "#1C2438"
    COLOR_DIVIDER  = "#141A28"
    COLOR_ACTIVE   = "#1E2840"
    APP_NAME       = "FarmaFacil Assistente"
    APP_VERSION    = "1.0.0"
    FONT_HEAD  = ("Segoe UI", 11, "bold")
    FONT_BODY  = ("Segoe UI", 10)
    FONT_LABEL = ("Segoe UI", 9)
    FONT_SMALL = ("Segoe UI", 8)
    FONT_TINY  = ("Segoe UI", 7)
    FONT_NAV   = ("Segoe UI", 9)
    FONT_BTN_S = ("Segoe UI", 9)

from ai.client import get_token_count
from db.connector import is_connected, get_host, get_dbname
from db.scanner import scan_bank
from utils.profile_cache import save_profile, load_profile, save_connection

from ui.chat_tab    import ChatTab
from ui.print_tab   import PrintTab
from ui.profile_tab import ProfileTab
from ui.config_tab  import ConfigTab
from ui.users_tab   import UsersTab


NAV_ITEMS = [
    ("chat",   "Chat"),
    ("print",  "Analise de Print"),
    ("perfil", "Perfil do Cliente"),
    ("config", "Configuracao"),
    ("users",  "Usuarios"),
]


class AppWindow(tk.Tk):
    def __init__(self, user_info):
        super(AppWindow, self).__init__()

        self.current_user = user_info
        self._profile     = None
        self._active_tab  = "chat"

        self.title(APP_NAME + " v" + APP_VERSION)
        self.configure(bg=COLOR_BG)
        self.geometry("1280x760")
        self.minsize(900, 560)

        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x  = (sw - 1280) // 2
        y  = (sh - 760)  // 2
        self.geometry("1280x760+{0}+{1}".format(x, y))

        self._build_ui()
        self._bind_shortcuts()
        self.after(100, self._startup)

    # ── Build ─────────────────────────────────────────────────────────

    def _build_ui(self):
        # Layout: sidebar | conteudo
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)

        self._build_titlebar()
        self._build_sidebar()
        self._build_content()
        self._build_statusbar()

    def _build_titlebar(self):
        bar = tk.Frame(self, bg=COLOR_SIDEBAR)
        bar.grid(row=0, column=0, columnspan=2, sticky="ew")
        bar.columnconfigure(1, weight=1)

        # Logo
        logo_f = tk.Frame(bar, bg=COLOR_SIDEBAR)
        logo_f.grid(row=0, column=0, padx=(16, 0), pady=9)

        c = tk.Canvas(logo_f, width=24, height=24,
                      bg=COLOR_SIDEBAR, highlightthickness=0)
        c.pack(side=tk.LEFT, padx=(0, 9))
        c.create_oval(2, 2, 22, 22, fill=COLOR_ACCENT, outline="")
        c.create_text(12, 12, text="E", fill="white",
                      font=("Segoe UI", 8, "bold"))

        tk.Label(logo_f, text=APP_NAME,
                 bg=COLOR_SIDEBAR, fg=COLOR_TEXT,
                 font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT)

        # Usuario + sair
        user_f = tk.Frame(bar, bg=COLOR_SIDEBAR)
        user_f.grid(row=0, column=2, padx=16, pady=9)

        is_admin = self.current_user.get("is_admin", False)
        uname    = self.current_user.get("username", "")
        role     = "Admin" if is_admin else "Operador"

        tk.Label(user_f,
                 text="{0}  |  {1}".format(uname, role),
                 bg=COLOR_SIDEBAR, fg=COLOR_TEXT_DIM,
                 font=FONT_SMALL).pack(side=tk.LEFT, padx=(0, 12))

        btn_sair = tk.Button(
            user_f, text="Sair",
            font=FONT_SMALL,
            bg=COLOR_CARD2, fg=COLOR_TEXT_DIM,
            activebackground=COLOR_CARD3, activeforeground=COLOR_TEXT,
            relief=tk.FLAT, cursor="hand2",
            padx=10, pady=3,
            command=self._logout)
        btn_sair.pack(side=tk.LEFT)

        # Linha inferior
        tk.Frame(self, bg=COLOR_BORDER, height=1).grid(
            row=0, column=0, columnspan=2, sticky="sew")

    def _build_sidebar(self):
        sb = tk.Frame(self, bg=COLOR_SIDEBAR, width=188)
        sb.grid(row=1, column=0, sticky="nsew")
        sb.grid_propagate(False)
        sb.columnconfigure(0, weight=1)
        self._sidebar = sb
        self._nav_btns = {}
        self._nav_inds = {}

        tk.Frame(sb, bg=COLOR_SIDEBAR, height=8).pack(fill=tk.X)

        for key, label in NAV_ITEMS:
            if key == "users" and not self.current_user.get("is_admin", False):
                continue

            row_f = tk.Frame(sb, bg=COLOR_SIDEBAR)
            row_f.pack(fill=tk.X)

            ind = tk.Frame(row_f, bg=COLOR_SIDEBAR, width=3)
            ind.pack(side=tk.LEFT, fill=tk.Y)

            btn = tk.Button(
                row_f, text=label,
                font=FONT_NAV,
                bg=COLOR_SIDEBAR, fg=COLOR_TEXT_DIM,
                activebackground=COLOR_ACTIVE, activeforeground=COLOR_TEXT,
                relief=tk.FLAT, cursor="hand2",
                anchor=tk.W, padx=14, pady=11,
                command=lambda k=key: self._switch_tab(k))
            btn.pack(side=tk.LEFT, fill=tk.X, expand=True)

            self._nav_btns[key] = btn
            self._nav_inds[key] = ind

        tk.Frame(sb, bg=COLOR_BORDER, height=1).pack(fill=tk.X, padx=12, pady=10)

        # Info conexao
        self._lbl_conn_sb = tk.Label(
            sb, text="Sem conexao",
            bg=COLOR_SIDEBAR, fg=COLOR_TEXT_MUT,
            font=("Segoe UI", 7), wraplength=160, justify=tk.LEFT)
        self._lbl_conn_sb.pack(fill=tk.X, padx=14, side=tk.BOTTOM, pady=8)

    def _build_content(self):
        outer = tk.Frame(self, bg=COLOR_BG)
        outer.grid(row=1, column=1, sticky="nsew")
        outer.columnconfigure(0, weight=1)
        outer.rowconfigure(0, weight=1)
        self._content_outer = outer

        self._tabs = {}
        self._tabs["chat"]   = ChatTab(outer, self)
        self._tabs["print"]  = PrintTab(outer, self)
        self._tabs["perfil"] = ProfileTab(outer, self)
        self._tabs["config"] = ConfigTab(outer, self)
        if self.current_user.get("is_admin", False):
            self._tabs["users"] = UsersTab(outer, self)

        for tab in self._tabs.values():
            tab.grid(row=0, column=0, sticky="nsew")
            tab.grid_remove()

        self._switch_tab("chat")

    def _build_statusbar(self):
        bar = tk.Frame(self, bg=COLOR_CARD2)
        bar.grid(row=2, column=0, columnspan=2, sticky="ew")

        tk.Frame(self, bg=COLOR_BORDER, height=1).grid(
            row=2, column=0, columnspan=2, sticky="new")

        self._dot = tk.Label(bar, text="●", bg=COLOR_CARD2,
                              fg=COLOR_ERROR, font=("Segoe UI", 9))
        self._dot.pack(side=tk.LEFT, padx=(12, 4))

        self.lbl_conn_status = tk.Label(
            bar, text="Sem conexao",
            bg=COLOR_CARD2, fg=COLOR_TEXT_DIM, font=FONT_TINY)
        self.lbl_conn_status.pack(side=tk.LEFT, padx=(0, 12))

        self._vsep(bar)

        self.lbl_db_status = tk.Label(
            bar, text="Banco: —",
            bg=COLOR_CARD2, fg=COLOR_TEXT_DIM, font=FONT_TINY)
        self.lbl_db_status.pack(side=tk.LEFT, padx=(6, 12))

        self._vsep(bar)

        self.lbl_scan_status = tk.Label(
            bar, text="Scan: —",
            bg=COLOR_CARD2, fg=COLOR_TEXT_DIM, font=FONT_TINY)
        self.lbl_scan_status.pack(side=tk.LEFT, padx=(6, 12))

        self._vsep(bar)

        self.lbl_tokens = tk.Label(
            bar, text="Tokens: 0",
            bg=COLOR_CARD2, fg=COLOR_TEXT_DIM, font=FONT_TINY)
        self.lbl_tokens.pack(side=tk.LEFT, padx=(6, 0))

        tk.Label(bar, text="v" + APP_VERSION,
                 bg=COLOR_CARD2, fg=COLOR_TEXT_MUT,
                 font=FONT_TINY).pack(side=tk.RIGHT, padx=12)

        bar.pack_propagate(False)
        bar.config(height=28)

    def _vsep(self, parent):
        tk.Frame(parent, bg=COLOR_BORDER,
                 width=1, height=12).pack(side=tk.LEFT, padx=2)

    # ── Navegacao ─────────────────────────────────────────────────────

    def _switch_tab(self, key):
        if key not in self._tabs:
            return
        for k, btn in self._nav_btns.items():
            ind = self._nav_inds[k]
            if k == key:
                btn.config(bg=COLOR_ACTIVE, fg=COLOR_TEXT)
                ind.config(bg=COLOR_ACCENT)
            else:
                btn.config(bg=COLOR_SIDEBAR, fg=COLOR_TEXT_DIM)
                ind.config(bg=COLOR_SIDEBAR)
        for k, tab in self._tabs.items():
            tab.grid() if k == key else tab.grid_remove()
        self._active_tab = key

    # ── Conexao ───────────────────────────────────────────────────────

    def _startup(self):
        from utils.profile_cache import load_connection
        conn = load_connection()
        if conn:
            host   = conn.get("host", "")
            dbname = conn.get("dbname", "")
            if host and dbname:
                self._auto_connect(host, dbname)
                return
        self._open_setup_dialog()

    def _auto_connect(self, host, dbname):
        self.update_statusbar(False, host, dbname)

        def _do():
            from db.connector import connect
            ok, err = connect(host, dbname)
            self.after(0, lambda: self._on_connect(ok, err, host, dbname))

        threading.Thread(target=_do, daemon=True).start()

    def _on_connect(self, ok, err, host, dbname):
        if ok:
            self.update_statusbar(True, host, dbname)
            cached = load_profile()
            if cached:
                self._apply_profile(cached)
            self.run_scanner()
        else:
            self.update_statusbar(False, host, dbname)
            self._log("Falha na conexao: {0}".format(err))

    def _open_setup_dialog(self):
        from ui.setup_dialog import SetupDialog
        dlg = SetupDialog(self)
        if dlg.confirmed:
            save_connection(dlg.host, dlg.dbname)
            self.update_statusbar(True, dlg.host, dlg.dbname)
            self.run_scanner()
        else:
            self.update_statusbar(False, "-", "-")

    # ── Scanner ───────────────────────────────────────────────────────

    def run_scanner(self):
        tab = self._tabs.get("config")
        if tab:
            tab.clear_log()

        def _progress(pct, msg):
            self.after(0, lambda: self._on_scan_progress(pct, msg))

        def _do():
            try:
                profile = scan_bank(progress_callback=_progress)
                self.after(0, lambda: self._on_scan_done(profile))
            except Exception as e:
                _err = str(e)
                self.after(0, lambda: self._on_scan_error(_err))

        threading.Thread(target=_do, daemon=True).start()

    def _on_scan_progress(self, pct, msg):
        self._log("[{0}%] {1}".format(pct, msg))

    def _on_scan_done(self, profile):
        self._apply_profile(profile)
        save_profile(profile)
        self.lbl_scan_status.config(
            text="Scan: " + time.strftime("%H:%M"))
        self._log("Scan concluido.")

    def _on_scan_error(self, err):
        self._log("Erro no scanner: " + err)

    def _apply_profile(self, profile):
        self._profile = profile

        chat_tab = self._tabs.get("chat")
        if chat_tab:
            chat_tab.set_profile(profile)
            if not chat_tab.messages:
                from ai.context_builder import build_welcome_message
                chat_tab.add_welcome(build_welcome_message(profile))

        print_tab = self._tabs.get("print")
        if print_tab:
            print_tab.set_profile(profile)

        profile_tab = self._tabs.get("perfil")
        if profile_tab:
            profile_tab.update_profile(profile)

    # ── Utilidades ────────────────────────────────────────────────────

    def update_statusbar(self, connected, host="", dbname=""):
        if connected:
            self._dot.config(fg=COLOR_SUCCESS)
            self.lbl_conn_status.config(
                text="Conectado: {0}".format(host), fg=COLOR_SUCCESS)
            self.lbl_db_status.config(
                text="Banco: {0}".format(dbname), fg=COLOR_TEXT_DIM)
            self._lbl_conn_sb.config(
                text="{0}  /  {1}".format(host, dbname), fg=COLOR_TEXT_DIM)
        else:
            self._dot.config(fg=COLOR_ERROR)
            self.lbl_conn_status.config(text="Sem conexao", fg=COLOR_ERROR)
            self.lbl_db_status.config(text="Banco: —", fg=COLOR_TEXT_DIM)
            self._lbl_conn_sb.config(text="Sem conexao", fg=COLOR_TEXT_MUT)

        config_tab = self._tabs.get("config")
        if config_tab:
            config_tab.refresh_status()

    def update_token_display(self):
        inp, out = get_token_count()
        self.lbl_tokens.config(text="Tokens: {:,}".format(inp + out))

    def _log(self, msg):
        tab = self._tabs.get("config")
        if tab:
            self.after(0, lambda: tab.append_log(msg))

    def _bind_shortcuts(self):
        try:
            self.bind("<Control-Shift-P>", self._shortcut_print)
            self.bind("<Control-shift-P>", self._shortcut_print)
        except Exception:
            pass

    def _shortcut_print(self, event=None):
        self._switch_tab("print")
        pt = self._tabs.get("print")
        if pt:
            self.after(200, pt.trigger_capture_shortcut)

    def _logout(self):
        from tkinter import messagebox
        if messagebox.askyesno("Sair", "Deseja sair do sistema?"):
            self.destroy()
