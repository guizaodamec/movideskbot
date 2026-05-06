import threading

try:
    import psycopg2
    import psycopg2.extras
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False

try:
    from config import DB_USER, DB_PASSWORD, DB_PORT
except ImportError:
    DB_USER     = "sistema"
    DB_PASSWORD = "sistemafarmafacil123"
    DB_PORT     = 5432

_lock = threading.Lock()
_connection = None
_host = None
_dbname = None


def connect(host, dbname, timeout=10):
    """Conecta ao banco PostgreSQL. Retorna (True, '') ou (False, msg_erro)."""
    global _connection, _host, _dbname

    if not HAS_PSYCOPG2:
        return False, "psycopg2 nao esta instalado. Instale com: pip install psycopg2-binary"

    try:
        with _lock:
            if _connection is not None:
                try:
                    _connection.close()
                except Exception:
                    pass
                _connection = None

            conn = psycopg2.connect(
                host=host,
                port=DB_PORT,
                dbname=dbname,
                user=DB_USER,
                password=DB_PASSWORD,
                connect_timeout=timeout,
                options="-c statement_timeout=30000"
            )
            conn.autocommit = True
            _connection = conn
            _host   = host
            _dbname = dbname
        return True, ""
    except psycopg2.OperationalError as e:
        msg = str(e)
        if "password" in msg.lower() or "authentication" in msg.lower():
            return False, "Falha de autenticacao. Verifique usuario/senha do banco."
        if "connection refused" in msg.lower():
            return False, "Conexao recusada. Verifique se o PostgreSQL esta rodando na porta {0}.".format(DB_PORT)
        if "could not translate" in msg.lower() or "name or service" in msg.lower():
            return False, "Host '{0}' nao encontrado. Verifique o IP/hostname.".format(host)
        if "does not exist" in msg.lower():
            return False, "Banco '{0}' nao encontrado no servidor.".format(dbname)
        return False, "Erro de conexao: {0}".format(msg)
    except Exception as e:
        return False, "Erro inesperado: {0}".format(str(e))


def get_connection():
    return _connection


def is_connected():
    global _connection
    if _connection is None:
        return False
    try:
        with _lock:
            cur = _connection.cursor()
            cur.execute("SELECT 1")
            cur.close()
        return True
    except Exception:
        _connection = None
        return False


def execute_query(sql, params=None, fetch=True):
    """
    Executa uma query.
    Retorna (rows, col_names, None) para SELECT ou (None, None, None) para DML.
    Em caso de erro retorna (None, None, msg_erro).
    """
    global _connection
    if _connection is None:
        return None, None, "Sem conexao com o banco."
    try:
        with _lock:
            cur = _connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute(sql, params)
            if fetch and cur.description:
                rows = cur.fetchall()
                cols = [d[0] for d in cur.description]
                cur.close()
                return rows, cols, None
            else:
                rowcount = cur.rowcount
                cur.close()
                return rowcount, None, None
    except psycopg2.Error as e:
        return None, None, "Erro SQL: {0}".format(str(e))
    except Exception as e:
        return None, None, "Erro: {0}".format(str(e))


def execute_modify(sql, params=None):
    """
    Executa query modificadora (UPDATE/DELETE/INSERT).
    Retorna (linhas_afetadas, None) ou (None, msg_erro).
    """
    global _connection
    if _connection is None:
        return None, "Sem conexao com o banco."
    try:
        with _lock:
            cur = _connection.cursor()
            cur.execute(sql, params)
            rowcount = cur.rowcount
            cur.close()
        return rowcount, None
    except psycopg2.Error as e:
        return None, "Erro SQL: {0}".format(str(e))
    except Exception as e:
        return None, "Erro: {0}".format(str(e))


def get_host():
    return _host


def get_dbname():
    return _dbname
