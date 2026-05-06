import tkinter as tk
import threading
import queue

try:
    from config import (
        COLOR_BG, COLOR_CARD, COLOR_CARD2, COLOR_CARD3,
        COLOR_TEXT, COLOR_TEXT_DIM, COLOR_TEXT_MUT,
        COLOR_ACCENT, COLOR_ACCENT_H, COLOR_ACCENT_D,
        COLOR_BORDER, COLOR_ERROR, COLOR_SUCCESS,
        APP_NAME, APP_VERSION,
        FONT_TITLE, FONT_HEAD, FONT_BODY, FONT_LABEL, FONT_SMALL, FONT_BTN
    )
except ImportError:
    COLOR_BG      = "#0B0D16"
    COLOR_CARD    = "#141926"
    COLOR_CARD2   = "#19202F"
    COLOR_CARD3   = "#1E2638"
    COLOR_TEXT    = "#E2E8F6"
    COLOR_TEXT_DIM= "#6B7A94"
    COLOR_TEXT_MUT= "#3A4560"
    COLOR_ACCENT  = "#4F74F9"
    COLOR_ACCENT_H= "#6B8DFF"
    COLOR_ACCENT_D= "#3A5CE0"
    COLOR_BORDER  = "#1C2438"
    COLOR_ERROR   = "#F87171"
    COLOR_SUCCESS = "#34D399"
    APP_NAME      = "FarmaFacil Assistente"
    APP_VERSION   = "1.0.0"
    FONT_TITLE = ("Segoe UI", 15, "bold")
    FONT_HEAD  = ("Segoe UI", 11, "bold")
    FONT_BODY  = ("Segoe UI", 10)
    FONT_LABEL = ("Segoe UI", 9)
    FONT_SMALL = ("Segoe UI", 8)
    FONT_BTN   = ("Segoe UI", 10, "bold")

from utils.auth import authenticate


def _hover(w, on, off):
    w.bind("<Enter>", lambda e: w.config(bg=on))
    w.bind("<Leave>", lambda e: w.config(bg=off))


class LoginDialog(object):
    def __init__(self, root):
        self.user_info = None
        self._result_queue = queue.Queue()

        self.dialog = tk.Toplevel(root)
        self.dialog.title(APP_NAME)
        self.dialog.configure(bg=COLOR_BG)
        self.dialog.resizable(False, False)
        self.dialog.grab_set()
        self.dialog.focus_set()

        w, h = 840, 540
        self.dialog.update_idletasks()
        sw = self.dialog.winfo_screenwidth()
        sh = self.dialog.winfo_screenheight()
        x  = (sw - w) // 2
        y  = (sh - h) // 2
        self.dialog.geometry("{0}x{1}+{2}+{3}".format(w, h, x, y))

        self._build_ui()
        self.dialog.protocol("WM_DELETE_WINDOW", self._on_close)
        self.dialog.bind("<Return>", lambda e: self._do_login())
        self.dialog.wait_window()

    def _build_ui(self):
        self.dialog.columnconfigure(0, weight=0)
        self.dialog.columnconfigure(1, weight=1)
        self.dialog.rowconfigure(0, weight=1)

        # ── Painel esquerdo (decorativo) ──────────────────────────────
        left = tk.Canvas(
            self.dialog,
            width=360, bg=COLOR_ACCENT, highlightthickness=0
        )
        left.grid(row=0, column=0, sticky="nsew")

        left.bind("<Configure>", lambda e: self._draw_left(left))

        # ── Painel direito (formulario) ───────────────────────────────
        right = tk.Frame(self.dialog, bg=COLOR_CARD)
        right.grid(row=0, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)
        right.rowconfigure(0, weight=1)

        inner = tk.Frame(right, bg=COLOR_CARD)
        inner.grid(row=0, column=0, sticky="nsew", padx=52, pady=0)
        inner.columnconfigure(0, weight=1)
        # Centrar verticalmente
        right.rowconfigure(0, weight=1)
        inner_wrap = tk.Frame(right, bg=COLOR_CARD)
        inner_wrap.place(relx=0.5, rely=0.5, anchor="center")
        inner_wrap.columnconfigure(0, weight=1)
        inner = inner_wrap

        # Ponto colorido + titulo
        title_row = tk.Frame(inner, bg=COLOR_CARD)
        title_row.pack(anchor=tk.W, pady=(0, 4))
        tk.Canvas(title_row, width=8, height=8, bg=COLOR_CARD,
                  highlightthickness=0).pack(side=tk.LEFT, padx=(0, 8))
        tk.Label(
            title_row, text="Acesse sua conta",
            bg=COLOR_CARD, fg=COLOR_TEXT,
            font=("Segoe UI", 16, "bold")
        ).pack(side=tk.LEFT)
        # Desenhar ponto
        c = title_row.winfo_children()[0]
        title_row.after(10, lambda: c.create_oval(0, 0, 8, 8,
                        fill=COLOR_ACCENT, outline=""))

        tk.Label(
            inner, text="Entre com suas credenciais para continuar",
            bg=COLOR_CARD, fg=COLOR_TEXT_DIM,
            font=("Segoe UI", 9), anchor=tk.W
        ).pack(anchor=tk.W, pady=(0, 30))

        # Campo usuario
        self._make_field(inner, "USUARIO")
        self.entry_user = self._make_entry(inner)
        self.entry_user.focus_set()

        # Campo senha
        self._make_field(inner, "SENHA", pady_top=18)
        self.entry_pass = self._make_entry(inner, show="*")

        # Mensagem de erro
        self.lbl_msg = tk.Label(
            inner, text="",
            bg=COLOR_CARD, fg=COLOR_ERROR,
            font=("Segoe UI", 8), wraplength=280, anchor=tk.W
        )
        self.lbl_msg.pack(fill=tk.X, pady=(10, 0))

        # Botao entrar
        self.btn_login = tk.Button(
            inner,
            text="Entrar",
            font=("Segoe UI", 10, "bold"),
            bg=COLOR_ACCENT, fg="white",
            activebackground=COLOR_ACCENT_H,
            activeforeground="white",
            relief=tk.FLAT, cursor="hand2",
            pady=11,
            command=self._do_login
        )
        self.btn_login.pack(fill=tk.X, pady=(16, 0))
        _hover(self.btn_login, COLOR_ACCENT_H, COLOR_ACCENT)

        # Rodape
        tk.Frame(inner, bg=COLOR_BORDER, height=1).pack(fill=tk.X, pady=(24, 12))
        tk.Label(
            inner, text="v{0}  —  Assistente ERP com IA".format(APP_VERSION),
            bg=COLOR_CARD, fg=COLOR_TEXT_MUT,
            font=("Segoe UI", 7)
        ).pack()

    def _make_field(self, parent, label, pady_top=0):
        tk.Label(
            parent, text=label,
            bg=COLOR_CARD, fg=COLOR_TEXT_DIM,
            font=("Segoe UI", 8, "bold"), anchor=tk.W
        ).pack(fill=tk.X, pady=(pady_top, 5))

    def _make_entry(self, parent, show=None):
        frame = tk.Frame(parent, bg=COLOR_BORDER, padx=1, pady=1)
        frame.pack(fill=tk.X)
        frame.columnconfigure(0, weight=1)

        kw = dict(
            font=("Segoe UI", 10),
            bg=COLOR_CARD3, fg=COLOR_TEXT,
            insertbackground=COLOR_ACCENT,
            relief=tk.FLAT, bd=0,
        )
        if show:
            kw["show"] = show

        entry = tk.Entry(frame, **kw)
        entry.pack(fill=tk.X, ipady=9, padx=12)

        def _fi(e, f=frame): f.config(bg=COLOR_ACCENT)
        def _fo(e, f=frame): f.config(bg=COLOR_BORDER)
        entry.bind("<FocusIn>",  _fi)
        entry.bind("<FocusOut>", _fo)
        return entry

    def _draw_left(self, canvas):
        canvas.delete("all")
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if w < 2 or h < 2:
            return

        # Fundo solido + faixas de degradê simulado (cores solidas, sem alpha)
        shades = [
            "#3D5EE8", "#3F61EA", "#4265EC",
            "#4569EE", "#486CF0", "#4B6FF2",
            "#4F74F9", "#4F74F9",
        ]
        band = max(1, h // len(shades))
        for i, color in enumerate(shades):
            canvas.create_rectangle(
                0, i * band, w, (i + 1) * band + 1,
                fill=color, outline=""
            )

        # Circulo grande decorativo (fundo)
        canvas.create_oval(
            -60, h // 2 - 200, w + 40, h // 2 + 120,
            fill="#3355CC", outline=""
        )
        canvas.create_oval(
            w - 100, h - 160, w + 80, h + 60,
            fill="#2D4BBF", outline=""
        )

        # Circulo do logo (cores solidas que imitam vidro)
        cx, cy = w // 2, h // 2 - 50
        canvas.create_oval(cx - 46, cy - 46, cx + 46, cy + 46,
                            fill="#5B7FFB", outline="#7090FC", width=1)
        canvas.create_oval(cx - 36, cy - 36, cx + 36, cy + 36,
                            fill="#4F74F9", outline="")
        canvas.create_text(cx, cy, text="ERP",
                            fill="white", font=("Segoe UI", 17, "bold"))

        # Nome do sistema
        canvas.create_text(
            w // 2, cy + 60, text=APP_NAME,
            fill="white", font=("Segoe UI", 13, "bold"))
        canvas.create_text(
            w // 2, cy + 82, text="Assistente tecnico inteligente",
            fill="#B8C8FF", font=("Segoe UI", 8))

        # Linha divisora
        canvas.create_line(
            w // 2 - 60, cy + 104, w // 2 + 60, cy + 104,
            fill="#6080E0", width=1)

        # Itens de destaque
        items = [
            "Banco de dados em tempo real",
            "Consultas SQL geradas por IA",
            "Analise de prints e erros",
        ]
        for i, txt in enumerate(items):
            y = cy + 128 + i * 26
            # Marcador
            canvas.create_rectangle(
                w // 2 - 80, y - 3, w // 2 - 72, y + 5,
                fill="#A0B8FF", outline="")
            canvas.create_text(
                w // 2 - 66, y + 1, text=txt,
                anchor=tk.W, fill="#C8D8FF",
                font=("Segoe UI", 8))

    # ── Logica ────────────────────────────────────────────────────────

    def _do_login(self):
        username = self.entry_user.get().strip()
        password = self.entry_pass.get()

        if not username or not password:
            self.lbl_msg.config(text="Preencha usuario e senha.")
            return

        self.btn_login.config(state=tk.DISABLED, text="Verificando...")
        self.lbl_msg.config(text="")

        def _check():
            result = authenticate(username, password)
            self._result_queue.put(result)

        threading.Thread(target=_check, daemon=True).start()
        self._poll_result()

    def _poll_result(self):
        try:
            result = self._result_queue.get_nowait()
            self._on_auth(result)
        except queue.Empty:
            self.dialog.after(50, self._poll_result)

    def _on_auth(self, result):
        if result:
            self.user_info = result
            self.dialog.destroy()
        else:
            self.lbl_msg.config(text="Usuario ou senha incorretos.")
            self.btn_login.config(state=tk.NORMAL, text="Entrar")
            self.entry_pass.delete(0, tk.END)
            self.entry_pass.focus_set()

    def _on_close(self):
        self.user_info = None
        self.dialog.destroy()
