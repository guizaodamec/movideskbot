"""
Aba de gerenciamento de usuarios — visivel apenas para administradores.
"""
import tkinter as tk
from tkinter import ttk, messagebox

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

from utils.auth import list_users, create_user, delete_user, set_admin


class UsersTab(tk.Frame):
    def __init__(self, parent, app_ref):
        super(UsersTab, self).__init__(parent, bg=COLOR_BG)
        self.app = app_ref
        self._build_ui()
        self.refresh_list()

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # ── Header
        hdr = tk.Frame(self, bg=COLOR_CARD, padx=16, pady=12)
        hdr.grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 4))

        tk.Label(
            hdr, text="Gerenciamento de Usuarios",
            bg=COLOR_CARD, fg=COLOR_ACCENT,
            font=("Arial", 12, "bold")
        ).pack(side=tk.LEFT)

        tk.Label(
            hdr, text="Apenas administradores podem gerenciar usuarios",
            bg=COLOR_CARD, fg=COLOR_TEXT_DIM,
            font=("Arial", 8, "italic")
        ).pack(side=tk.LEFT, padx=12)

        # ── Conteudo
        body = tk.Frame(self, bg=COLOR_BG)
        body.grid(row=1, column=0, sticky="nsew", padx=8, pady=4)
        body.columnconfigure(0, weight=2)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        # ── Lista de usuarios
        list_card = tk.Frame(body, bg=COLOR_CARD, padx=14, pady=12)
        list_card.grid(row=0, column=0, sticky="nsew", padx=(0, 4))
        list_card.columnconfigure(0, weight=1)
        list_card.rowconfigure(1, weight=1)

        tk.Label(list_card, text="Usuarios cadastrados",
                 bg=COLOR_CARD, fg=COLOR_ACCENT,
                 font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=(0, 8))

        style = ttk.Style()
        style.configure("Users.Treeview",
            background=COLOR_CARD2, foreground=COLOR_TEXT,
            rowheight=24, fieldbackground=COLOR_CARD2, font=("Arial", 9))
        style.configure("Users.Treeview.Heading",
            background=COLOR_ACCENT, foreground="white", font=("Arial", 9, "bold"))
        style.map("Users.Treeview", background=[("selected", COLOR_ACCENT)])

        cols = ("usuario", "admin", "criado_em")
        self.tree = ttk.Treeview(list_card, columns=cols, show="headings",
                                  style="Users.Treeview", selectmode="browse")
        self.tree.heading("usuario",    text="Usuario")
        self.tree.heading("admin",      text="Administrador")
        self.tree.heading("criado_em",  text="Criado em")
        self.tree.column("usuario",   width=160)
        self.tree.column("admin",     width=120, anchor=tk.CENTER)
        self.tree.column("criado_em", width=160, anchor=tk.CENTER)
        self.tree.grid(row=1, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(list_card, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky="ns")
        list_card.columnconfigure(0, weight=1)

        # Botoes de acao
        act = tk.Frame(list_card, bg=COLOR_CARD)
        act.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(8, 0))

        tk.Button(
            act, text="Excluir selecionado",
            font=("Arial", 9), bg="#7F1D1D", fg="white",
            activebackground="#991B1B", relief=tk.FLAT, cursor="hand2",
            padx=10, pady=5, command=self._delete_selected
        ).pack(side=tk.LEFT, padx=(0, 6))

        tk.Button(
            act, text="Alternar Admin",
            font=("Arial", 9), bg="#78350F", fg="white",
            activebackground="#92400E", relief=tk.FLAT, cursor="hand2",
            padx=10, pady=5, command=self._toggle_admin
        ).pack(side=tk.LEFT, padx=(0, 6))

        tk.Button(
            act, text="Atualizar lista",
            font=("Arial", 9), bg=COLOR_CARD2, fg=COLOR_TEXT,
            activebackground=COLOR_ACCENT, relief=tk.FLAT, cursor="hand2",
            padx=10, pady=5, command=self.refresh_list
        ).pack(side=tk.LEFT)

        # ── Formulario criar usuario
        form_card = tk.Frame(body, bg=COLOR_CARD, padx=14, pady=12)
        form_card.grid(row=0, column=1, sticky="nsew", padx=(4, 0))

        tk.Label(form_card, text="Novo Usuario",
                 bg=COLOR_CARD, fg=COLOR_ACCENT,
                 font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 12))

        tk.Label(form_card, text="Nome de usuario:", bg=COLOR_CARD, fg=COLOR_TEXT_DIM,
                 font=("Arial", 9), anchor=tk.W).pack(fill=tk.X)
        self.entry_new_user = tk.Entry(
            form_card, font=("Arial", 10),
            bg=COLOR_CARD2, fg=COLOR_TEXT,
            insertbackground=COLOR_TEXT, relief=tk.FLAT, bd=6
        )
        self.entry_new_user.pack(fill=tk.X, pady=(2, 10))

        tk.Label(form_card, text="Senha:", bg=COLOR_CARD, fg=COLOR_TEXT_DIM,
                 font=("Arial", 9), anchor=tk.W).pack(fill=tk.X)
        self.entry_new_pass = tk.Entry(
            form_card, font=("Arial", 10),
            bg=COLOR_CARD2, fg=COLOR_TEXT,
            insertbackground=COLOR_TEXT, relief=tk.FLAT, bd=6,
            show="*"
        )
        self.entry_new_pass.pack(fill=tk.X, pady=(2, 10))

        self.var_is_admin = tk.BooleanVar(value=False)
        ck = tk.Checkbutton(
            form_card, text="Administrador",
            variable=self.var_is_admin,
            bg=COLOR_CARD, fg=COLOR_TEXT,
            activebackground=COLOR_CARD,
            activeforeground=COLOR_TEXT,
            selectcolor=COLOR_CARD2,
            font=("Arial", 9), anchor=tk.W
        )
        ck.pack(fill=tk.X, pady=(0, 12))

        self.lbl_form_msg = tk.Label(
            form_card, text="",
            bg=COLOR_CARD, fg=COLOR_ERROR,
            font=("Arial", 9), wraplength=200
        )
        self.lbl_form_msg.pack(fill=tk.X, pady=(0, 8))

        tk.Button(
            form_card,
            text="Criar Usuario",
            font=("Arial", 10, "bold"),
            bg=COLOR_ACCENT, fg="white",
            activebackground="#6B8BFF",
            relief=tk.FLAT, cursor="hand2",
            pady=8, command=self._create_user
        ).pack(fill=tk.X)

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        users = list_users()
        for u in users:
            admin_text = "Sim" if u["is_admin"] else "Nao"
            self.tree.insert("", tk.END, values=(
                u["username"], admin_text, u.get("created_at", "")[:19]
            ))

    def _get_selected_username(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atencao", "Selecione um usuario na lista.")
            return None
        item  = self.tree.item(sel[0])
        return item["values"][0]

    def _delete_selected(self):
        username = self._get_selected_username()
        if not username:
            return
        current = getattr(self.app, "current_user", {}).get("username", "")
        if username.upper() == current.upper():
            messagebox.showerror("Erro", "Nao e possivel excluir o proprio usuario.")
            return
        if not messagebox.askyesno("Confirmar", "Excluir o usuario '{0}'?".format(username)):
            return
        ok, err = delete_user(username)
        if ok:
            self.refresh_list()
        else:
            messagebox.showerror("Erro", err)

    def _toggle_admin(self):
        username = self._get_selected_username()
        if not username:
            return
        users = list_users()
        current_admin = False
        for u in users:
            if u["username"].upper() == username.upper():
                current_admin = u["is_admin"]
                break
        ok, err = set_admin(username, not current_admin)
        if ok:
            self.refresh_list()
        else:
            messagebox.showerror("Erro", err)

    def _create_user(self):
        username = self.entry_new_user.get().strip()
        password = self.entry_new_pass.get()
        is_admin = self.var_is_admin.get()

        ok, err = create_user(username, password, is_admin)
        if ok:
            self.lbl_form_msg.config(text="Usuario criado com sucesso!", fg=COLOR_SUCCESS)
            self.entry_new_user.delete(0, tk.END)
            self.entry_new_pass.delete(0, tk.END)
            self.var_is_admin.set(False)
            self.refresh_list()
        else:
            self.lbl_form_msg.config(text=err, fg=COLOR_ERROR)
