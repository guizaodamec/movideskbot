import os
import json
import hashlib
import time

try:
    from config import USERS_FILE
except ImportError:
    USERS_FILE = "users.json"

try:
    from utils.paths import get_data_dir
except ImportError:
    def get_data_dir():
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_DEFAULT_ADMIN = {
    "username": "GUILHERME",
    "password": "Flamengo135@",
    "is_admin": True,
    "role":     "administrador",
}

VALID_ROLES = {"analista", "backservice", "fiscal", "lideres", "administrador"}


def get_role(user):
    """Retorna o role do usuário com fallback para compatibilidade."""
    r = user.get("role", "")
    if r in VALID_ROLES:
        return r
    return "administrador" if user.get("is_admin") else "analista"

def _hash_password(password):
    salt = "erp_assistant_salt_v1"
    combined = salt + password + salt
    return hashlib.sha256(combined.encode("utf-8")).hexdigest()

def _get_users_path():
    return os.path.join(get_data_dir(), USERS_FILE)

def load_users():
    path = _get_users_path()
    if not os.path.exists(path):
        _create_default_users(path)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"users": []}

def _create_default_users(path):
    data = {
        "users": [
            {
                "username":    _DEFAULT_ADMIN["username"],
                "password_hash": _hash_password(_DEFAULT_ADMIN["password"]),
                "is_admin":    True,
                "role":        "administrador",
                "created_at":  time.strftime("%Y-%m-%dT%H:%M:%S"),
            }
        ]
    }
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

def save_users(data):
    path = _get_users_path()
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False

def authenticate(username, password):
    """Retorna o usuario se autenticado, None caso contrario."""
    data = load_users()
    pwd_hash = _hash_password(password)
    for user in data.get("users", []):
        if user["username"].upper() == username.upper() and user["password_hash"] == pwd_hash:
            return user
    return None

def set_must_change_password(username, value):
    """Define se o usuario deve trocar a senha no proximo login."""
    data = load_users()
    for user in data.get("users", []):
        if user["username"].upper() == username.upper():
            user["must_change_password"] = bool(value)
            if save_users(data):
                return True, ""
            return False, "Erro ao salvar."
    return False, "Usuario nao encontrado."

def create_user(username, password, is_admin=False, must_change_password=False, role=None):
    """Cria um novo usuario. Retorna (True, '') ou (False, motivo)."""
    if not username or not username.strip():
        return False, "Nome de usuario nao pode ser vazio."
    if not password or len(password) < 4:
        return False, "Senha deve ter ao menos 4 caracteres."
    data = load_users()
    for user in data.get("users", []):
        if user["username"].upper() == username.upper():
            return False, "Usuario ja existe."
    if role not in VALID_ROLES:
        role = "administrador" if is_admin else "analista"
    new_user = {
        "username":            username.upper(),
        "password_hash":       _hash_password(password),
        "is_admin":            role == "administrador",
        "role":                role,
        "must_change_password": bool(must_change_password),
        "created_at":          time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    data.setdefault("users", []).append(new_user)
    if save_users(data):
        return True, ""
    return False, "Erro ao salvar arquivo de usuarios."

def delete_user(username):
    """Remove usuario. Retorna (True, '') ou (False, motivo)."""
    data = load_users()
    original = list(data.get("users", []))
    filtered = [u for u in original if u["username"].upper() != username.upper()]
    if len(filtered) == len(original):
        return False, "Usuario nao encontrado."
    if len(filtered) == 0:
        return False, "Nao e possivel remover o ultimo usuario."
    data["users"] = filtered
    if save_users(data):
        return True, ""
    return False, "Erro ao salvar arquivo de usuarios."

def set_admin(username, is_admin):
    """Altera status de admin. Retorna (True, '') ou (False, motivo)."""
    data = load_users()
    for user in data.get("users", []):
        if user["username"].upper() == username.upper():
            user["is_admin"] = is_admin
            if is_admin and user.get("role") != "administrador":
                user["role"] = "administrador"
            elif not is_admin and user.get("role") == "administrador":
                user["role"] = "analista"
            if save_users(data):
                return True, ""
            return False, "Erro ao salvar."
    return False, "Usuario nao encontrado."


def set_role(username, role):
    """Altera o role do usuario. Retorna (True, '') ou (False, motivo)."""
    if role not in VALID_ROLES:
        return False, f"Role invalida. Valores aceitos: {', '.join(sorted(VALID_ROLES))}"
    data = load_users()
    for user in data.get("users", []):
        if user["username"].upper() == username.upper():
            user["role"]     = role
            user["is_admin"] = role == "administrador"
            if save_users(data):
                return True, ""
            return False, "Erro ao salvar."
    return False, "Usuario nao encontrado."


def set_movidesk_name(username, movidesk_name):
    """Define o nome do usuário no Movidesk (para filtrar chamados). Admin only."""
    data = load_users()
    for user in data.get("users", []):
        if user["username"].upper() == username.upper():
            user["movidesk_name"] = movidesk_name.strip()
            if save_users(data):
                return True, ""
            return False, "Erro ao salvar."
    return False, "Usuario nao encontrado."


def list_users():
    """Retorna lista de usuarios (sem senha)."""
    data = load_users()
    result = []
    for user in data.get("users", []):
        result.append({
            "username":            user["username"],
            "is_admin":            user.get("is_admin", False),
            "role":                get_role(user),
            "movidesk_name":       user.get("movidesk_name", ""),
            "must_change_password": user.get("must_change_password", False),
            "created_at":          user.get("created_at", ""),
        })
    return result

def change_password(username, new_password):
    """Altera senha do usuario."""
    if not new_password or len(new_password) < 4:
        return False, "Senha deve ter ao menos 4 caracteres."
    data = load_users()
    for user in data.get("users", []):
        if user["username"].upper() == username.upper():
            user["password_hash"] = _hash_password(new_password)
            if save_users(data):
                return True, ""
            return False, "Erro ao salvar."
    return False, "Usuario nao encontrado."
