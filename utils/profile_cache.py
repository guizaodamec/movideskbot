import os
import json
import time

try:
    from config import PROFILE_FILE, CONNECTION_FILE
except ImportError:
    PROFILE_FILE    = "client_profile.json"
    CONNECTION_FILE = "connection.json"

try:
    from utils.paths import get_data_dir as _base_dir
except ImportError:
    def _base_dir():
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def save_profile(profile):
    path = os.path.join(_base_dir(), PROFILE_FILE)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=2, ensure_ascii=False, default=str)
        return True
    except Exception:
        return False

def load_profile():
    path = os.path.join(_base_dir(), PROFILE_FILE)
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def save_connection(host, dbname, ai_host=None):
    path = os.path.join(_base_dir(), CONNECTION_FILE)
    data = {
        "host": host,
        "dbname": dbname,
        "ai_host": ai_host or "localhost",
        "saved_at": time.strftime("%Y-%m-%dT%H:%M:%S")
    }
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception:
        return False

def load_connection():
    path = os.path.join(_base_dir(), CONNECTION_FILE)
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def delete_connection():
    path = os.path.join(_base_dir(), CONNECTION_FILE)
    try:
        if os.path.exists(path):
            os.remove(path)
        return True
    except Exception:
        return False
