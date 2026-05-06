import tkinter as tk
from tkinter import ttk, filedialog
import threading

try:
    from config import (
        COLOR_BG, COLOR_CARD, COLOR_CARD2, COLOR_CARD3,
        COLOR_TEXT, COLOR_TEXT_DIM, COLOR_TEXT_MUT,
        COLOR_ACCENT, COLOR_ACCENT_H,
        COLOR_SUCCESS, COLOR_ERROR, COLOR_BORDER, COLOR_DIVIDER,
        FONT_HEAD, FONT_BODY, FONT_LABEL, FONT_SMALL, FONT_BTN, FONT_BTN_S
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
    COLOR_SUCCESS = "#34D399"
    COLOR_ERROR   = "#F87171"
    COLOR_BORDER  = "#1C2438"
    COLOR_DIVIDER = "#141A28"
    FONT_HEAD  = ("Segoe UI", 11, "bold")
    FONT_BODY  = ("Segoe UI", 10)
    FONT_LABEL = ("Segoe UI", 9)
    FONT_SMALL = ("Segoe UI", 8)
    FONT_BTN   = ("Segoe UI", 10, "bold")
    FONT_BTN_S = ("Segoe UI", 9)

from ai.client import ask
from ai.context_builder import build_system_prompt
from ai.prompts import IMAGE_ANALYSIS_PROMPT
from utils.screenshot import capture_screen, capture_screen_pil, pil_to_base64, pil_to_thumbnail


BTN_H = 9   # pady padrao para todos os botoes (altura uniforme)


def _hover(w, on, off):
    w.bind("<Enter>", lambda e: w.config(bg=on))
    w.bind("<Leave>", lambda e: w.config(bg=off))


class PrintTab(tk.Frame):
    def __init__(self, parent, app_ref):
        super(PrintTab, self).__init__(parent, bg=COLOR_BG)
        self.app             = app_ref
        self._screenshot_b64 = None
        self._build_ui()

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # ── Barra de acoes (top) ──────────────────────────────────────
        top = tk.Frame(self, bg=COLOR_CARD, padx=16, pady=14)
        top.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 1))

        tk.Label(top, text="Analise de Print",
                 bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=FONT_HEAD).pack(side=tk.LEFT, padx=(0, 24))

        self.btn_capture = tk.Button(
            top,
            text="Capturar Tela",
            font=FONT_BTN_S,
            bg=COLOR_ACCENT, fg="white",
            activebackground=COLOR_ACCENT_H, activeforeground="white",
            relief=tk.FLAT, cursor="hand2",
            padx=18, pady=BTN_H,
            command=self._capture
        )
        self.btn_capture.pack(side=tk.LEFT, padx=(0, 8))
        _hover(self.btn_capture, COLOR_ACCENT_H, COLOR_ACCENT)

        btn_load = tk.Button(
            top,
            text="Carregar Arquivo",
            font=FONT_BTN_S,
            bg=COLOR_CARD2, fg=COLOR_TEXT,
            activebackground=COLOR_CARD3, activeforeground=COLOR_TEXT,
            relief=tk.FLAT, cursor="hand2",
            padx=18, pady=BTN_H,
            command=self._load_image
        )
        btn_load.pack(side=tk.LEFT)
        _hover(btn_load, COLOR_CARD3, COLOR_CARD2)

        tk.Label(top, text="Ctrl+Shift+P",
                 bg=COLOR_CARD, fg=COLOR_TEXT_MUT,
                 font=("Segoe UI", 7)).pack(side=tk.RIGHT)

        # Linha separadora
        tk.Frame(self, bg=COLOR_BORDER, height=1).grid(
            row=0, column=0, sticky="sew")

        # ── Corpo principal (preview + form + resultado) ──────────────
        body = tk.Frame(self, bg=COLOR_BG)
        body.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        body.columnconfigure(0, weight=2)
        body.columnconfigure(1, weight=3)
        body.rowconfigure(0, weight=1)

        # Coluna esquerda — preview
        self._build_preview(body)

        # Linha divisoria vertical
        tk.Frame(body, bg=COLOR_BORDER, width=1).grid(
            row=0, column=0, sticky="nse", padx=(0,0))

        # Coluna direita — descricao + resultado
        self._build_form(body)

    def _build_preview(self, parent):
        left = tk.Frame(parent, bg=COLOR_CARD)
        left.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        left.columnconfigure(0, weight=1)
        left.rowconfigure(1, weight=1)

        # Header do preview
        hdr = tk.Frame(left, bg=COLOR_CARD2, padx=14, pady=10)
        hdr.grid(row=0, column=0, sticky="ew")

        tk.Label(hdr, text="PREVIEW",
                 bg=COLOR_CARD2, fg=COLOR_TEXT_MUT,
                 font=("Segoe UI", 7, "bold")).pack(side=tk.LEFT)

        self.lbl_preview_title = tk.Label(
            hdr, text="Nenhuma imagem",
            bg=COLOR_CARD2, fg=COLOR_TEXT_DIM,
            font=FONT_SMALL)
        self.lbl_preview_title.pack(side=tk.RIGHT)

        # Area da imagem
        img_frame = tk.Frame(left, bg=COLOR_CARD)
        img_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        img_frame.columnconfigure(0, weight=1)
        img_frame.rowconfigure(0, weight=1)

        # Placeholder
        placeholder = tk.Frame(img_frame, bg=COLOR_CARD2,
                                width=360, height=260)
        placeholder.grid(row=0, column=0)
        placeholder.grid_propagate(False)
        placeholder.columnconfigure(0, weight=1)
        placeholder.rowconfigure(0, weight=1)

        self.lbl_preview = tk.Label(
            placeholder,
            text="Nenhuma imagem carregada\n\nClique em 'Capturar Tela'\nou 'Carregar Arquivo'",
            bg=COLOR_CARD2, fg=COLOR_TEXT_MUT,
            font=FONT_SMALL, justify=tk.CENTER)
        self.lbl_preview.grid(row=0, column=0)

    def _build_form(self, parent):
        right = tk.Frame(parent, bg=COLOR_BG)
        right.grid(row=0, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)
        right.rowconfigure(2, weight=1)

        # Descricao
        desc_frame = tk.Frame(right, bg=COLOR_CARD, padx=16, pady=14)
        desc_frame.grid(row=0, column=0, sticky="ew")
        desc_frame.columnconfigure(0, weight=1)

        tk.Label(desc_frame, text="DESCRICAO DO PROBLEMA  (opcional)",
                 bg=COLOR_CARD, fg=COLOR_TEXT_MUT,
                 font=("Segoe UI", 7, "bold"), anchor=tk.W
                 ).grid(row=0, column=0, sticky="ew", pady=(0, 6))

        # Input com borda visivel
        entry_border = tk.Frame(desc_frame, bg=COLOR_BORDER, padx=1, pady=1)
        entry_border.grid(row=1, column=0, sticky="ew")
        entry_border.columnconfigure(0, weight=1)

        self.text_desc = tk.Text(
            entry_border, height=4,
            font=FONT_BODY,
            bg=COLOR_CARD3, fg=COLOR_TEXT,
            insertbackground=COLOR_ACCENT,
            relief=tk.FLAT, bd=0,
            wrap=tk.WORD, padx=10, pady=8
        )
        self.text_desc.grid(row=0, column=0, sticky="ew")

        def _focus_in(e):  entry_border.config(bg=COLOR_ACCENT)
        def _focus_out(e): entry_border.config(bg=COLOR_BORDER)
        self.text_desc.bind("<FocusIn>",  _focus_in)
        self.text_desc.bind("<FocusOut>", _focus_out)

        # Linha
        tk.Frame(right, bg=COLOR_BORDER, height=1).grid(
            row=1, column=0, sticky="ew")

        # Botao analisar
        btn_frame = tk.Frame(right, bg=COLOR_CARD, padx=16, pady=12)
        btn_frame.grid(row=1, column=0, sticky="ew")
        btn_frame.columnconfigure(0, weight=1)

        self.btn_analyze = tk.Button(
            btn_frame,
            text="Analisar com IA",
            font=FONT_BTN,
            bg="#6D4AE0", fg="white",
            activebackground="#7C5CF6", activeforeground="white",
            relief=tk.FLAT, cursor="hand2",
            pady=BTN_H,
            command=self._analyze,
            state=tk.DISABLED
        )
        self.btn_analyze.grid(row=0, column=0, sticky="ew")
        _hover(self.btn_analyze, "#7C5CF6", "#6D4AE0")

        self._thinking_pb = ttk.Progressbar(
            btn_frame, mode="indeterminate")
        # nao exibido ate chamar

        # Resultado
        result_outer = tk.Frame(right, bg=COLOR_CARD)
        result_outer.grid(row=2, column=0, sticky="nsew", padx=0, pady=0)
        result_outer.columnconfigure(0, weight=1)
        result_outer.rowconfigure(1, weight=1)

        res_hdr = tk.Frame(result_outer, bg=COLOR_CARD2, padx=14, pady=8)
        res_hdr.grid(row=0, column=0, sticky="ew")
        tk.Label(res_hdr, text="RESULTADO DA ANALISE",
                 bg=COLOR_CARD2, fg=COLOR_TEXT_MUT,
                 font=("Segoe UI", 7, "bold")).pack(side=tk.LEFT)

        # Botao copiar resultado
        self.btn_copy_result = tk.Button(
            res_hdr, text="Copiar",
            font=("Segoe UI", 7),
            bg=COLOR_CARD2, fg=COLOR_TEXT_MUT,
            activebackground=COLOR_CARD3, activeforeground=COLOR_TEXT,
            relief=tk.FLAT, cursor="hand2",
            padx=8, pady=2,
            command=self._copy_result
        )
        self.btn_copy_result.pack(side=tk.RIGHT)

        scroll_f = tk.Frame(result_outer, bg=COLOR_CARD)
        scroll_f.grid(row=1, column=0, sticky="nsew", padx=0)
        scroll_f.columnconfigure(0, weight=1)
        scroll_f.rowconfigure(0, weight=1)

        txt_scroll = tk.Scrollbar(scroll_f, orient=tk.VERTICAL)
        txt_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_result = tk.Text(
            scroll_f,
            font=FONT_BODY,
            bg=COLOR_CARD, fg=COLOR_TEXT,
            relief=tk.FLAT, bd=0,
            wrap=tk.WORD, state=tk.DISABLED,
            yscrollcommand=txt_scroll.set,
            padx=16, pady=12,
            selectbackground=COLOR_ACCENT,
            cursor="xterm"
        )
        self.text_result.pack(fill=tk.BOTH, expand=True)
        txt_scroll.config(command=self.text_result.yview)

    # ── Acoes ─────────────────────────────────────────────────────────

    def set_profile(self, profile):
        self._profile = profile

    def _capture(self):
        self.winfo_toplevel().iconify()
        self.after(400, self._do_capture)

    def _do_capture(self):
        try:
            img = capture_screen_pil()
            self._set_image(img)
            self.winfo_toplevel().deiconify()
            self.winfo_toplevel().lift()
        except Exception as e:
            self.winfo_toplevel().deiconify()
            self._set_result("Erro ao capturar tela: {0}".format(str(e)))

    def _load_image(self):
        path = filedialog.askopenfilename(
            title="Selecionar imagem",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.bmp *.gif"),
                       ("Todos", "*.*")]
        )
        if not path:
            return
        try:
            from PIL import Image
            img = Image.open(path)
            self._set_image(img)
        except Exception as e:
            self._set_result("Erro ao carregar imagem: {0}".format(str(e)))

    def _set_image(self, pil_img):
        from PIL import ImageTk
        self._screenshot_b64 = pil_to_base64(pil_img)
        thumb = pil_to_thumbnail(pil_img, 360, 260)
        self._tk_img = ImageTk.PhotoImage(thumb)
        self.lbl_preview.config(image=self._tk_img, text="")
        self.lbl_preview_title.config(
            text="{0} x {1} px".format(pil_img.size[0], pil_img.size[1]))
        self.btn_analyze.config(state=tk.NORMAL)

    def _analyze(self):
        if not self._screenshot_b64:
            return

        desc = self.text_desc.get("1.0", tk.END).strip()
        self.btn_analyze.config(state=tk.DISABLED, text="Analisando...")
        self._thinking_pb.grid(sticky="ew", pady=(8, 0))
        self._thinking_pb.start(12)
        self._set_result("Aguardando resposta da IA...")

        profile = getattr(self, "_profile", None)
        user_msg = IMAGE_ANALYSIS_PROMPT.format(
            descricao=desc if desc else "Nao informada"
        )
        msgs   = [{"role": "user", "content": user_msg}]
        img_b64 = self._screenshot_b64

        def _call():
            try:
                from db.connector import execute_query as _eq
                rows, _, _ = _eq(
                    "SELECT table_schema, table_name, table_type "
                    "FROM information_schema.tables "
                    "WHERE table_schema NOT IN "
                    "('pg_catalog','information_schema','pg_toast') "
                    "AND table_schema NOT LIKE 'pg_%' "
                    "ORDER BY table_schema, table_name"
                )
                live_schema = ""
                if rows:
                    lines = []
                    for r in rows:
                        s = str(r.get("table_schema", ""))
                        n = str(r.get("table_name", ""))
                        t = "VIEW" if str(r.get("table_type","")).upper()=="VIEW" \
                            else "TABLE"
                        prefix = "{0}.{1}".format(s, n) if s != "public" else n
                        lines.append("  {0} ({1})".format(prefix, t))
                    live_schema = "\n".join(lines)
                system_prompt = build_system_prompt(profile, live_schema=live_schema)
                response = ask(system_prompt, msgs, image_base64=img_b64)
                self.after(0, lambda: self._on_result(response))
            except Exception as e:
                _err = str(e)
                self.after(0, lambda: self._on_result("Erro: {0}".format(_err)))

        threading.Thread(target=_call, daemon=True).start()

    def _on_result(self, text):
        self._thinking_pb.stop()
        self._thinking_pb.grid_remove()
        self.btn_analyze.config(state=tk.NORMAL, text="Analisar com IA")
        self._set_result(text)
        self.app.update_token_display()

    def _set_result(self, text):
        self.text_result.config(state=tk.NORMAL)
        self.text_result.delete("1.0", tk.END)
        self.text_result.insert(tk.END, text)
        self.text_result.config(state=tk.DISABLED)

    def _copy_result(self):
        content = self.text_result.get("1.0", tk.END).strip()
        if not content:
            return
        self.clipboard_clear()
        self.clipboard_append(content)
        self.btn_copy_result.config(text="Copiado!", fg=COLOR_SUCCESS)
        self.after(1500, lambda: self.btn_copy_result.config(
            text="Copiar", fg=COLOR_TEXT_MUT))

    def trigger_capture_shortcut(self):
        self._capture()
