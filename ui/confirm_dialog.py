import tkinter as tk

try:
    from config import (
        COLOR_BG, COLOR_CARD, COLOR_TEXT, COLOR_TEXT_DIM,
        COLOR_WARNING, COLOR_ERROR, COLOR_BORDER
    )
except ImportError:
    COLOR_BG      = "#0D0F18"
    COLOR_CARD    = "#1A1E2E"
    COLOR_TEXT    = "#E2E8F0"
    COLOR_TEXT_DIM = "#8892A4"
    COLOR_WARNING = "#F59E0B"
    COLOR_ERROR   = "#EF4444"
    COLOR_BORDER  = "#252840"


class ConfirmQueryDialog(object):
    """
    Dialog de confirmacao para queries UPDATE/DELETE/INSERT.
    Uso:
        dlg = ConfirmQueryDialog(parent, query, explanation)
        if dlg.result:
            # executar
    """

    def __init__(self, parent, query, explanation=""):
        self.result = False

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Confirmacao necessaria")
        self.dialog.configure(bg=COLOR_CARD)
        self.dialog.resizable(False, False)
        self.dialog.grab_set()
        self.dialog.focus_set()

        # Centralizar na tela
        self.dialog.update_idletasks()
        w = 520
        h = 400
        x = parent.winfo_rootx() + (parent.winfo_width()  - w) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - h) // 2
        self.dialog.geometry("{0}x{1}+{2}+{3}".format(w, h, x, y))

        # Faixa de aviso
        warn_frame = tk.Frame(self.dialog, bg="#7C2D12", pady=12, padx=16)
        warn_frame.pack(fill=tk.X)

        tk.Label(
            warn_frame,
            text="ATENCAO",
            bg="#7C2D12", fg="#FED7AA",
            font=("Arial", 11, "bold")
        ).pack(anchor=tk.W)

        tk.Label(
            warn_frame,
            text="Esta operacao ira modificar dados no banco de dados.",
            bg="#7C2D12", fg="#FEF3C7",
            font=("Arial", 9),
            wraplength=488
        ).pack(anchor=tk.W)

        # Explicacao
        if explanation:
            exp_frame = tk.Frame(self.dialog, bg=COLOR_CARD, padx=16, pady=8)
            exp_frame.pack(fill=tk.X)
            tk.Label(
                exp_frame,
                text="O que sera feito:",
                font=("Arial", 9, "bold"),
                bg=COLOR_CARD, fg=COLOR_TEXT,
                anchor=tk.W
            ).pack(fill=tk.X)
            tk.Label(
                exp_frame,
                text=explanation,
                font=("Arial", 9),
                bg=COLOR_CARD, fg=COLOR_TEXT_DIM,
                wraplength=488,
                anchor=tk.W,
                justify=tk.LEFT
            ).pack(fill=tk.X)

        # Query
        qf = tk.Frame(self.dialog, bg=COLOR_CARD, padx=16, pady=8)
        qf.pack(fill=tk.BOTH, expand=True)
        tk.Label(
            qf,
            text="Query a ser executada:",
            font=("Arial", 9, "bold"),
            bg=COLOR_CARD, fg=COLOR_TEXT,
            anchor=tk.W
        ).pack(fill=tk.X)

        qt_frame = tk.Frame(qf, bg="#1A150A", bd=1, relief=tk.SOLID)
        qt_frame.pack(fill=tk.BOTH, expand=True, pady=(4, 0))

        qt = tk.Text(
            qt_frame,
            height=8,
            font=("Courier New", 9),
            bg="#1A150A",
            fg="#FCD34D",
            relief=tk.FLAT,
            bd=8,
            wrap=tk.WORD
        )
        qt.insert(tk.END, query)
        qt.config(state=tk.DISABLED)
        qt.pack(fill=tk.BOTH, expand=True)

        # Botoes
        bf = tk.Frame(self.dialog, bg=COLOR_CARD, padx=16, pady=12)
        bf.pack(fill=tk.X)

        tk.Label(
            bf,
            text="Deseja continuar com esta operacao?",
            font=("Arial", 9),
            bg=COLOR_CARD, fg=COLOR_TEXT_DIM
        ).pack(side=tk.LEFT)

        btn_cancel = tk.Button(
            bf,
            text="Cancelar",
            width=12,
            font=("Arial", 9),
            bg="#374151", fg=COLOR_TEXT,
            activebackground="#4B5563",
            activeforeground=COLOR_TEXT,
            relief=tk.FLAT,
            cursor="hand2",
            command=self._cancel
        )
        btn_cancel.pack(side=tk.RIGHT, padx=(8, 0))

        btn_exec = tk.Button(
            bf,
            text="EXECUTAR",
            width=12,
            font=("Arial", 9, "bold"),
            bg="#DC2626", fg="white",
            activebackground="#EF4444",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self._confirm
        )
        btn_exec.pack(side=tk.RIGHT)

        # Bind Escape
        self.dialog.bind("<Escape>", lambda e: self._cancel())

        self.dialog.wait_window()

    def _confirm(self):
        self.result = True
        self.dialog.destroy()

    def _cancel(self):
        self.result = False
        self.dialog.destroy()
