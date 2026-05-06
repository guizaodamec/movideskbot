"""
Servidor Flask — API HTTP para o frontend Electron/React.
Envolve os módulos Python existentes do ERP Assistant.
"""
import sys
import os
import threading
import json
import decimal
import datetime
import secrets
import re
import webbrowser

# Diretório raiz: usa sys._MEIPASS quando compilado com PyInstaller (onefile)
if getattr(sys, 'frozen', False):
    _ROOT = sys._MEIPASS
else:
    _ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)


from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ── Serializador JSON ─────────────────────────────────────────────────────────

class _Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return str(obj)
        if hasattr(obj, '_asdict'):
            return dict(obj)
        return super().default(obj)

try:
    from flask.json.provider import DefaultJSONProvider
    class _Provider(DefaultJSONProvider):
        def dumps(self, obj, **kw):
            kw.setdefault('cls', _Encoder)
            kw.setdefault('ensure_ascii', False)
            return json.dumps(obj, **kw)
        def loads(self, s, **kw):
            return json.loads(s, **kw)
    app.json_provider_class = _Provider
    app.json = _Provider(app)
except ImportError:
    app.json_encoder = _Encoder  # type: ignore[attr-defined]

def _jsonify(data, status=200):
    return app.response_class(
        response=json.dumps(data, cls=_Encoder, ensure_ascii=False),
        status=status,
        mimetype='application/json',
    )

# ── Banco de dados pré-configurados ──────────────────────────────────────────

DATABASES = [
    {"label": "NatuFarma Linhares",    "host": "192.168.0.121", "port": 5432, "dbname": "natufarma_linhares"},
    {"label": "FarmaFácil Univali",     "host": "192.168.0.102", "port": 5432, "dbname": "farmafacil_univali"},
    {"label": "FarmaFácil Boiron",      "host": "192.168.0.102", "port": 5432, "dbname": "farmafacil_boiron"},
    {"label": "Ouro FarmaCerto",        "host": "192.168.0.64",  "port": 5432, "dbname": "ourofarmacerto"},
    {"label": "FarmaFácil São Bernardo","host": "192.168.0.102", "port": 5432, "dbname": "farmafacil_fasaobernardo"},
    {"label": "Pronim",                 "host": "127.0.0.1",     "port": 5432, "dbname": "pronim"},
    {"label": "FarmaFácil (115)",       "host": "192.168.0.115", "port": 5432, "dbname": "farmafacil"},
    {"label": "FarmaFácil C&V",         "host": "192.168.0.102", "port": 5432, "dbname": "farmafacil_cienciaevida"},
]

# ── Sessões (token simples em memória) ────────────────────────────────────────

_sessions = {}   # token -> {username, is_admin, role, movidesk_name}

def _create_token(username, is_admin, role='analista', movidesk_name=''):
    token = secrets.token_hex(32)
    _sessions[token] = {
        "username":      username,
        "is_admin":      bool(is_admin),
        "role":          role,
        "movidesk_name": movidesk_name or username,
    }
    return token

def _get_session(req):
    auth = req.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        token = auth[7:]
        return _sessions.get(token)
    return None

def _require_auth(req):
    sess = _get_session(req)
    if not sess:
        return None, _jsonify({"error": "Não autenticado"}, 401)
    return sess, None

def _require_admin(req):
    sess, err = _require_auth(req)
    if err:
        return None, err
    if not sess.get("is_admin"):
        return None, _jsonify({"error": "Acesso negado — requer administrador"}, 403)
    return sess, None

# ── Estado do scan ────────────────────────────────────────────────────────────

_scan = {
    'running': False, 'pct': 0, 'msg': '',
    'done': False, 'error': None, 'profile': None,
}
_scan_lock = threading.Lock()

def _update_scan(**kw):
    with _scan_lock:
        _scan.update(kw)

def _get_scan():
    with _scan_lock:
        return dict(_scan)

# ── Helper: strip markdown bold ───────────────────────────────────────────────

_HALLUCINATION_PATTERNS = [
    # Tool call tags alucinadas
    (re.compile(r'<(read_code|search_code|tool|function|execute|run_command|file_read|path|recursive|file_pattern)[^>]*>[\s\S]*?</\1>', re.IGNORECASE), ''),
    (re.compile(r'<(read_code|search_code|tool|function|execute|run_command|file_read)[^>]*/>', re.IGNORECASE), ''),
    # Padrões de inventar nomes de classes/calculadoras de código que não existem
    (re.compile(r'`[A-Z][a-zA-Z]+Calculator`|`[A-Z][a-zA-Z]+Validator`|`[A-Z][a-zA-Z]+Service`'), ''),
]

# Marcadores muito específicos de alucinação de tool calls — não bloqueiam respostas legítimas
_CODE_HALLUCINATION_MARKERS = [
    'FormulaAdjustmentCalculator', 'CompatibilityValidator', 'StabilityCalculator',
    'recursive>true', 'file_pattern>', '<read_code>', '<search_code>',
]


def _detect_hallucination(text: str) -> bool:
    """Retorna True apenas se a resposta contém tool calls inventados óbvios."""
    if not text:
        return False
    return any(marker in text for marker in _CODE_HALLUCINATION_MARKERS)


def _strip_bold(text):
    """Remove markdown desnecessário e alucinações de tool-calls do output da IA."""
    if not text:
        return text

    # Se detectar alucinação grave, substitui por mensagem honesta
    if _detect_hallucination(text):
        return (
            "Desculpa, não tenho acesso ao código-fonte do FarmaFácil. 😅\n\n"
            "O que posso fazer:\n"
            "- Consultar o banco de dados real para verificar dados de SNGPC, estoque, fórmulas etc.\n"
            "- Buscar na base de conhecimento técnico sobre configurações e procedimentos\n\n"
            "Quer que eu faça uma consulta no banco para mostrar os dados reais?"
        )

    # Remove tool call tags alucinadas
    text = re.sub(r'<(read_code|search_code|tool|function|execute|run_command|file_read|path|recursive|file_pattern)[^>]*>[\s\S]*?</\1>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'<(read_code|search_code|tool|function|execute|run_command|file_read)[^>]*/>', '', text, flags=re.IGNORECASE)
    # Converte tabelas markdown em listas limpas
    def _convert_table(text):
        lines = text.split('\n')
        result = []
        headers = []
        for line in lines:
            # Linha separadora |---|---| → ignora
            if re.match(r'^\|[\s\|\-\:]+\|\s*$', line):
                continue
            # Linha de tabela com dados
            if re.match(r'^\s*\|', line):
                cells = [c.strip() for c in re.split(r'\|', line) if c.strip()]
                if not cells:
                    result.append(line)
                    continue
                # Primeira linha de tabela → cabeçalho
                if not headers:
                    headers = cells
                    result.append(' | '.join(headers))
                else:
                    # Formata como "Header1: valor — Header2: valor — ..."
                    if headers and len(cells) == len(headers):
                        partes = [f"{headers[i]}: {cells[i]}" for i in range(len(cells))]
                        result.append('  '.join(partes))
                    else:
                        result.append('  '.join(cells))
            else:
                if headers:
                    headers = []  # resetar cabeçalho ao sair da tabela
                result.append(line)
        return '\n'.join(result)
    text = _convert_table(text)
    # Remove linhas --- (horizontal rule)
    text = re.sub(r'^\s*-{2,}\s*$', '', text, flags=re.MULTILINE)
    # Remove **texto** → texto
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text, flags=re.DOTALL)
    # Remove *texto* → texto
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'\1', text, flags=re.DOTALL)
    # Remove headers ## Titulo → Titulo
    text = re.sub(r'^#{1,4}\s+', '', text, flags=re.MULTILINE)
    # Remove linhas em branco duplas geradas pelas remoções acima
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

# ── Health ────────────────────────────────────────────────────────────────────

@app.route('/api/health')
def health():
    return _jsonify({'ok': True})

# ── Auth ──────────────────────────────────────────────────────────────────────

@app.route('/api/login', methods=['POST'])
def login():
    data     = request.get_json(force=True) or {}
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''

    if not username or not password:
        return _jsonify({'error': 'Usuário e senha são obrigatórios'}, 400)

    try:
        from utils.auth import authenticate, get_role
        user = authenticate(username, password)
        if not user:
            return _jsonify({'error': 'Usuário ou senha incorretos'}, 401)

        role          = get_role(user)
        movidesk_name = user.get('movidesk_name') or user['username']
        token = _create_token(user['username'], user.get('is_admin', False), role, movidesk_name)
        return _jsonify({
            'token':               token,
            'username':            user['username'],
            'is_admin':            user.get('is_admin', False),
            'role':                role,
            'movidesk_name':       movidesk_name,
            'must_change_password': user.get('must_change_password', False),
        })
    except Exception as e:
        return _jsonify({'error': str(e)}, 500)

@app.route('/api/logout', methods=['POST'])
def logout():
    auth = request.headers.get('Authorization', '')
    if auth.startswith('Bearer '):
        _sessions.pop(auth[7:], None)
    return _jsonify({'ok': True})

@app.route('/api/me')
def me():
    sess, err = _require_auth(request)
    if err: return err
    return _jsonify(sess)

# ── Usuários ──────────────────────────────────────────────────────────────────

@app.route('/api/users', methods=['GET'])
def list_users():
    sess, err = _require_admin(request)
    if err: return err
    from utils.auth import list_users as _list
    return _jsonify(_list())

@app.route('/api/users', methods=['POST'])
def create_user():
    sess, err = _require_admin(request)
    if err: return err
    data                = request.get_json(force=True) or {}
    username            = (data.get('username') or '').strip()
    password            = data.get('password') or ''
    is_admin            = bool(data.get('is_admin', False))
    must_change_password = bool(data.get('must_change_password', False))
    role                = data.get('role') or None
    from utils.auth import create_user as _create
    ok, msg = _create(username, password, is_admin, must_change_password, role)
    if ok:
        return _jsonify({'ok': True})
    return _jsonify({'error': msg}, 400)

@app.route('/api/users/<username>', methods=['DELETE'])
def delete_user(username):
    sess, err = _require_admin(request)
    if err: return err
    if username.upper() == sess['username'].upper():
        return _jsonify({'error': 'Não é possível remover o próprio usuário'}, 400)
    from utils.auth import delete_user as _delete
    ok, msg = _delete(username)
    if ok:
        return _jsonify({'ok': True})
    return _jsonify({'error': msg}, 400)

@app.route('/api/users/<username>/password', methods=['PUT'])
def change_password(username):
    sess, err = _require_auth(request)
    if err: return err
    # Só admin pode trocar senha de outro usuário
    if username.upper() != sess['username'].upper() and not sess.get('is_admin'):
        return _jsonify({'error': 'Sem permissão'}, 403)
    data = request.get_json(force=True) or {}
    new_pwd = data.get('password') or ''
    from utils.auth import change_password as _change
    ok, msg = _change(username, new_pwd)
    if ok:
        return _jsonify({'ok': True})
    return _jsonify({'error': msg}, 400)

@app.route('/api/users/<username>/must_change_password', methods=['PUT'])
def set_must_change_password(username):
    sess, err = _require_auth(request)
    if err: return err
    data  = request.get_json(force=True) or {}
    value = bool(data.get('value', True))
    is_own   = username.upper() == sess['username'].upper()
    is_admin = sess.get('is_admin')
    # Admin pode forçar troca; o próprio usuário pode limpar a obrigação
    if not is_admin and not (is_own and not value):
        return _jsonify({'error': 'Sem permissão'}, 403)
    from utils.auth import set_must_change_password as _set
    ok, msg = _set(username, value)
    if ok:
        return _jsonify({'ok': True})
    return _jsonify({'error': msg}, 400)


@app.route('/api/users/<username>/role', methods=['PUT'])
def set_user_role(username):
    sess, err = _require_admin(request)
    if err: return err
    data = request.get_json(force=True) or {}
    role = data.get('role') or 'analista'
    from utils.auth import set_role as _set
    ok, msg = _set(username, role)
    if ok:
        return _jsonify({'ok': True})
    return _jsonify({'error': msg}, 400)


@app.route('/api/users/<username>/movidesk_name', methods=['PUT'])
def set_movidesk_name(username):
    sess, err = _require_admin(request)
    if err: return err
    data = request.get_json(force=True) or {}
    name = (data.get('movidesk_name') or '').strip()
    from utils.auth import set_movidesk_name as _set
    ok, msg = _set(username, name)
    if ok:
        # Atualiza a sessão ativa do usuário em tempo real
        for token, s in _sessions.items():
            if s.get('username', '').upper() == username.upper():
                s['movidesk_name'] = name or username
        return _jsonify({'ok': True})
    return _jsonify({'error': msg}, 400)


@app.route('/api/movidesk-analistas')
def movidesk_analistas():
    """Lista todos os analistas conhecidos no cache do Movidesk (para seleção)."""
    sess, err = _require_admin(request)
    if err: return err
    try:
        from utils.movidesk_sync import load_cache
        cache = load_cache()
        names = sorted({
            (t.get('owner_name') or '').strip()
            for t in cache.get('tickets', {}).values()
            if t.get('owner_name', '').strip()
        })
        return _jsonify(names)
    except Exception as e:
        return _jsonify({'error': str(e)}, 500)


# ── Correções de conhecimento ─────────────────────────────────────────────────

@app.route('/api/knowledge-corrections', methods=['GET'])
def list_corrections():
    sess, err = _require_admin(request)
    if err: return err
    import json as _json
    from utils.paths import get_bundle_dir
    path = os.path.join(get_bundle_dir(), 'knowledge_corrections.json')
    if not os.path.exists(path):
        return _jsonify([])
    with open(path, encoding='utf-8') as f:
        return _jsonify(_json.load(f))


@app.route('/api/knowledge-corrections', methods=['POST'])
def add_correction():
    sess, err = _require_admin(request)
    if err: return err
    import json as _json, time
    from utils.paths import get_bundle_dir
    from utils.knowledge_search import invalidate_corrections_cache
    data = request.get_json(force=True) or {}
    titulo   = (data.get('titulo') or '').strip()
    conteudo = (data.get('conteudo') or '').strip()
    keywords = data.get('keywords') or []
    if not titulo or not conteudo:
        return _jsonify({'error': 'titulo e conteudo são obrigatórios'}, 400)
    path = os.path.join(get_bundle_dir(), 'knowledge_corrections.json')
    corrections = []
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            corrections = _json.load(f)
    from datetime import date
    corrections.append({
        'id': f'corr-{int(time.time())}',
        'titulo': titulo,
        'keywords': keywords,
        'conteudo': conteudo,
        'fonte': f'Adicionado por {sess["username"]} em {date.today().strftime("%d/%m/%Y")}',
        'data': date.today().strftime('%d/%m/%Y'),
        'prioridade': 100,
    })
    with open(path, 'w', encoding='utf-8') as f:
        _json.dump(corrections, f, ensure_ascii=False, indent=2)
    invalidate_corrections_cache()
    return _jsonify({'ok': True})


@app.route('/api/knowledge-corrections/<corr_id>', methods=['DELETE'])
def delete_correction(corr_id):
    sess, err = _require_admin(request)
    if err: return err
    import json as _json
    from utils.paths import get_bundle_dir
    from utils.knowledge_search import invalidate_corrections_cache
    path = os.path.join(get_bundle_dir(), 'knowledge_corrections.json')
    if not os.path.exists(path):
        return _jsonify({'error': 'Nenhuma correção cadastrada'}, 404)
    with open(path, encoding='utf-8') as f:
        corrections = _json.load(f)
    corrections = [c for c in corrections if c.get('id') != corr_id]
    with open(path, 'w', encoding='utf-8') as f:
        _json.dump(corrections, f, ensure_ascii=False, indent=2)
    invalidate_corrections_cache()
    return _jsonify({'ok': True})

@app.route('/api/users/<username>/admin', methods=['PUT'])
def set_admin(username):
    sess, err = _require_admin(request)
    if err: return err
    data = request.get_json(force=True) or {}
    is_admin = bool(data.get('is_admin', False))
    from utils.auth import set_admin as _set
    ok, msg = _set(username, is_admin)
    if ok:
        return _jsonify({'ok': True})
    return _jsonify({'error': msg}, 400)

# ── Databases pré-configurados ────────────────────────────────────────────────

@app.route('/api/databases')
def databases():
    return _jsonify(DATABASES)

# ── Conexão ───────────────────────────────────────────────────────────────────

@app.route('/api/connect', methods=['POST'])
def connect():
    data   = request.get_json(force=True) or {}
    host   = (data.get('host') or '').strip()
    dbname = (data.get('database') or '').strip()

    if not host or not dbname:
        return _jsonify({'error': 'Host e database são obrigatórios'}, 400)

    try:
        from db.connector import connect as db_connect
        ok, err = db_connect(host, dbname)
        if not ok:
            return _jsonify({'error': err or 'Falha na conexão'}, 500)

        from utils.profile_cache import save_connection
        save_connection(host, dbname)
        _start_scan()
        return _jsonify({'ok': True})
    except Exception as e:
        return _jsonify({'error': str(e)}, 500)

def _start_scan():
    _update_scan(running=True, done=False, error=None, pct=5, msg='Iniciando scan...')

    def _worker():
        def _progress(pct, msg):
            _update_scan(pct=pct, msg=msg)
        try:
            from db.scanner import scan_bank
            profile = scan_bank(progress_callback=_progress)
            from utils.profile_cache import save_profile
            save_profile(profile)
            _update_scan(profile=profile, pct=100, msg='Scan concluído.', done=True, running=False)
        except Exception as e:
            _update_scan(error=str(e), done=True, running=False)

    threading.Thread(target=_worker, daemon=True).start()

@app.route('/api/scan/status')
def scan_status():
    s = _get_scan()
    return _jsonify({'pct': s['pct'], 'msg': s['msg'], 'done': s['done'], 'error': s['error']})

@app.route('/api/scan', methods=['POST'])
def trigger_scan():
    _start_scan()
    return _jsonify({'ok': True})

# ── Perfil ────────────────────────────────────────────────────────────────────

@app.route('/api/profile')
def profile():
    p = _get_scan().get('profile')
    if not p:
        try:
            from utils.profile_cache import load_profile
            p = load_profile()
        except Exception:
            p = None
    return _jsonify(p or {})

# ── Chat ──────────────────────────────────────────────────────────────────────

def _build_chat_context(p, mensagem, historico, username):
    """Monta todo o contexto do chat em paralelo. Retorna (static_part, dynamic_part, msgs)."""
    from ai.context_builder import build_system_prompt
    from utils.memory import build_memory_prompt
    from concurrent.futures import ThreadPoolExecutor

    client_razao = (p.get('razao_social', '') if p else '') or ''
    hist_limited = historico[-8:] if len(historico) > 8 else historico

    def _safe(fn, *args):
        try: return fn(*args)
        except Exception: return None

    with ThreadPoolExecutor(max_workers=5) as ex:
        f_ctx  = ex.submit(build_system_prompt, p, query=mensagem)
        f_mem  = ex.submit(_safe, build_memory_prompt, username)
        f_anal = ex.submit(_safe, lambda: __import__('utils.movidesk_sync', fromlist=['get_analista_context']).get_analista_context(username))
        f_sim  = ex.submit(_safe, lambda: __import__('utils.movidesk_sync', fromlist=['find_similar']).find_similar(mensagem, client_name=client_razao or None))
        f_jira = ex.submit(_safe, _search_jira_context, mensagem)

    static_part, dynamic_part = f_ctx.result()

    mem = f_mem.result()
    if mem:
        dynamic_part += '\n\n## ' + mem

    ctx_analista = f_anal.result()
    if ctx_analista:
        dynamic_part += '\n\n' + ctx_analista

    similares = f_sim.result()
    if similares:
        linhas = []
        for s in similares[:2]:
            data_res = s.get('resolvedIn', '')[:10] or '?'
            prob = s.get('problema') or s.get('subject', '')
            sol  = s.get('solucao', '')
            linhas.append(
                f"- Chamado #{s['id']} ({data_res}) | {s.get('client_name','')} | "
                f"Problema: {prob[:120]} | Solução: {sol[:120]}"
            )
        dynamic_part += (
            "\n\n## ATENCAO: Chamados similares ja resolvidos\n"
            + "\n".join(linhas)
            + "\nSe o problema for o mesmo, sugira a solução acima antes de investigar."
        )

    jira_ctx = f_jira.result()
    if jira_ctx:
        dynamic_part += '\n\n' + jira_ctx

    msgs = list(hist_limited)
    if not msgs or msgs[-1].get('content') != mensagem:
        msgs.append({'role': 'user', 'content': mensagem})

    return static_part, dynamic_part, msgs


@app.route('/api/chat/stream', methods=['POST'])
def chat_stream():
    """Endpoint de streaming — envia tokens conforme chegam, sem esperar resposta completa."""
    from flask import Response, stream_with_context

    data           = request.get_json(force=True) or {}
    mensagem       = (data.get('mensagem') or '').strip()
    historico      = data.get('historico') or []
    imagem         = (data.get('imagem') or '')
    model_override = (data.get('model') or '').strip() or None

    if not mensagem and not imagem:
        return _jsonify({'error': 'Mensagem vazia'}, 400)

    try:
        p = _get_scan().get('profile')
        if not p:
            from utils.profile_cache import load_profile
            p = load_profile() or {}

        sess     = _get_session(request)
        username = sess['username'] if sess else 'anonimo'

        static_part, dynamic_part, msgs = _build_chat_context(p, mensagem, historico, username)

        from ai.client import ask_stream as _ask_stream

        def generate():
            full_text = ''
            try:
                for token in _ask_stream(dynamic_part, msgs,
                                         image_base64=imagem or None,
                                         static_prefix=static_part,
                                         model=model_override):
                    full_text += token
                    yield 'data: {0}\n\n'.format(json.dumps({'token': token}))
                processed = _strip_bold(full_text)
                yield 'data: {0}\n\n'.format(json.dumps({'done': True, 'text': processed}))
            except Exception as e:
                yield 'data: {0}\n\n'.format(json.dumps({'error': str(e)}))

        return Response(
            stream_with_context(generate()),
            content_type='text/event-stream',
            headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'},
        )
    except Exception as e:
        return _jsonify({'error': str(e)}, 500)


@app.route('/api/chat', methods=['POST'])
def chat():
    data      = request.get_json(force=True) or {}
    mensagem  = (data.get('mensagem') or '').strip()
    historico = data.get('historico') or []
    imagem    = (data.get('imagem') or '')
    model_override = (data.get('model') or '').strip() or None

    if not mensagem and not imagem:
        return _jsonify({'error': 'Mensagem vazia'}, 400)

    try:
        p = _get_scan().get('profile')
        if not p:
            from utils.profile_cache import load_profile
            p = load_profile() or {}

        # Usuário logado (para memória)
        sess = _get_session(request)
        username = sess['username'] if sess else 'anonimo'

        # Limita histórico a 8 turnos para controlar tokens
        hist_limited = historico[-8:] if len(historico) > 8 else historico

        from ai.context_builder import build_system_prompt
        from utils.memory import build_memory_prompt
        static_part, dynamic_part = build_system_prompt(p, query=mensagem)

        # Injeta memória do usuário no prompt dinâmico
        mem = build_memory_prompt(username)
        if mem:
            dynamic_part = dynamic_part + '\n\n## ' + mem

        # Injeta histórico do analista (categorias mais atendidas)
        try:
            from utils.movidesk_sync import get_analista_context
            ctx_analista = get_analista_context(username)
            if ctx_analista:
                dynamic_part = dynamic_part + '\n\n' + ctx_analista
        except Exception:
            pass

        # Detecção de chamado similar — alerta injetado no contexto
        try:
            from utils.movidesk_sync import find_similar
            client_razao = p.get('razao_social', '') if p else ''
            similares = find_similar(mensagem, client_name=client_razao or None)
            if similares:
                linhas = []
                for s in similares[:2]:
                    data_res = s.get('resolvedIn', '')[:10] or '?'
                    prob = s.get('problema') or s.get('subject', '')
                    sol  = s.get('solucao', '')
                    linhas.append(
                        f"- Chamado #{s['id']} ({data_res}) | {s.get('client_name','')} | "
                        f"Problema: {prob[:120]} | Solução: {sol[:120]}"
                    )
                aviso = (
                    "\n\n## ATENCAO: Chamados similares ja resolvidos\n"
                    + "\n".join(linhas)
                    + "\nSe o problema for o mesmo, sugira a solução acima antes de investigar."
                )
                dynamic_part = dynamic_part + aviso
        except Exception:
            pass

        # Contexto do Jira (somente leitura — nunca cria/edita issues)
        try:
            jira_ctx = _search_jira_context(mensagem)
            if jira_ctx:
                dynamic_part = dynamic_part + '\n\n' + jira_ctx
        except Exception:
            pass

        # Busca web — desativada temporariamente (causava alucinações de notícias)
        # Para reativar: remover o comentário abaixo
        # try:
        #     from utils.knowledge_search import search as kb_search
        #     from utils.web_search import search as web_search, format_for_prompt, should_search
        #     kb_preview = kb_search(mensagem, top_n=1, max_chars=500)
        #     if not imagem and should_search(mensagem, kb_preview):
        #         web_results = web_search(mensagem, max_results=3)
        #         if web_results:
        #             web_ctx = format_for_prompt(web_results)
        #             dynamic_part = dynamic_part + "\n\n" + web_ctx
        # except Exception as _we:
        #     logger.warning("Web search falhou: %s", _we)

        msgs = list(hist_limited)
        if not msgs or msgs[-1].get('content') != mensagem:
            msgs.append({'role': 'user', 'content': mensagem})

        from ai.client import ask, extract_queries
        from db.connector import execute_query as _eq

        resposta = _strip_bold(ask(dynamic_part, msgs,
                                   image_base64=imagem or None,
                                   static_prefix=static_part,
                                   model=model_override))

        # ── Executa todas as SELECTs da resposta e coleta resultados ──────────
        queries   = extract_queries(resposta)
        resultados_exec = []   # (sql, rows, cols, err)
        sql_errors      = []

        for q in queries:
            if q['type'] != 'SELECT':
                continue
            rows, cols, err = _eq(q['sql'])
            resultados_exec.append((q['sql'], rows, cols, err))
            if err and ('relação' in err or 'relation' in err or
                        'não existe' in err or 'does not exist' in err or
                        'coluna' in err or 'column' in err):
                sql_errors.append((q['sql'], err))

        # ── Caso 1: erro de tabela/coluna inexistente → corrige automaticamente ─
        if sql_errors:
            tabelas_reais = ''
            colunas_reais = ''
            try:
                rows_t, _, _ = _eq(
                    "SELECT table_schema || '.' || table_name AS tabela "
                    "FROM information_schema.tables "
                    "WHERE table_schema IN ('data','public') "
                    "ORDER BY table_schema, table_name"
                )
                if rows_t:
                    tabelas_reais = '\nTabelas reais no banco:\n' + \
                        '\n'.join('- ' + r.get('tabela', '') for r in rows_t[:80])
            except Exception:
                pass

            # Para erros de coluna: busca colunas reais da tabela em questão
            import re as _re
            tabelas_com_erro = set()
            for sql, err in sql_errors:
                # Extrai nome da tabela do FROM/UPDATE/JOIN
                for m in _re.findall(r'(?:FROM|JOIN|UPDATE)\s+([\w\.]+)', sql, _re.IGNORECASE):
                    tabelas_com_erro.add(m.lower())
                # Também tenta pegar do erro (ex: "tabela data.filial")
                for m in _re.findall(r'(?:data|public)\.\w+', err, _re.IGNORECASE):
                    tabelas_com_erro.add(m.lower())

            for tabela in list(tabelas_com_erro)[:5]:
                partes = tabela.split('.')
                schema = partes[0] if len(partes) == 2 else 'data'
                nome   = partes[-1]
                try:
                    rows_c, _, _ = _eq(
                        "SELECT column_name, data_type "
                        "FROM information_schema.columns "
                        "WHERE table_schema = '{0}' AND table_name = '{1}' "
                        "ORDER BY ordinal_position".format(schema, nome)
                    )
                    if rows_c:
                        cols_list = ', '.join(r.get('column_name', '') for r in rows_c)
                        colunas_reais += '\nColunas reais de {0}.{1}: {2}'.format(
                            schema, nome, cols_list)
                except Exception:
                    pass

            erros_fmt = '\n\n'.join(
                'SQL: ' + s[:200] + '\nErro: ' + e for s, e in sql_errors
            )
            correcao_msg = (
                'As seguintes queries retornaram erro:\n\n' +
                erros_fmt + colunas_reais + tabelas_reais +
                '\n\nUSE APENAS os nomes de colunas listados acima (exatamente como aparecem). '
                'Nao invente nomes de colunas. Corrija o SQL e execute novamente.'
            )
            msgs_retry = msgs + [
                {'role': 'assistant', 'content': resposta},
                {'role': 'user',      'content': correcao_msg},
            ]
            resposta = _strip_bold(ask(dynamic_part, msgs_retry, static_prefix=static_part))

        # ── Caso 2: queries executaram OK → interpreta os resultados ──────────
        elif resultados_exec:
            def _fmt_result(sql, rows, cols, err):
                if err:
                    return 'SQL: ' + sql[:150] + '\nErro: ' + err
                if cols and rows:
                    header = ' | '.join(cols)
                    linhas = [header]
                    for r in (rows[:10] if rows else []):
                        linhas.append(' | '.join(str(r.get(c, '')) for c in cols))
                    sufixo = (' (mostrando 10 de {0})'.format(len(rows))
                              if len(rows) > 10 else '')
                    return 'SQL: ' + sql[:150] + '\nResultado ({0} linhas{1}):\n'.format(
                        len(rows), sufixo) + '\n'.join(linhas[:11])
                if cols is None and rows is not None:
                    return 'SQL: ' + sql[:150] + '\n{0} linha(s) afetada(s).'.format(rows)
                return 'SQL: ' + sql[:150] + '\nSem resultados.'

            resultados_txt = '\n\n'.join(
                _fmt_result(s, r, c, e) for s, r, c, e in resultados_exec
            )

            interpretacao_msg = (
                'Resultados das queries executadas:\n\n' + resultados_txt +
                '\n\nAgora EXECUTE a consulta final com as colunas corretas e responda a pergunta do usuario. '
                'OBRIGATORIO: gere um SELECT completo com colunas reais (nao use "SELECT FROM", sempre liste as colunas). '
                'Depois interprete os resultados em texto claro.'
            )
            msgs_interp = msgs + [
                {'role': 'assistant', 'content': resposta},
                {'role': 'user',      'content': interpretacao_msg},
            ]
            resposta_final = _strip_bold(ask(dynamic_part, msgs_interp, static_prefix=static_part))
            # Retorna as queries originais + interpretação final
            resposta = resposta + '\n\n' + resposta_final

        try:
            from utils.chat_logger import log_chat
            log_chat(username, mensagem, resposta, has_image=bool(imagem))
        except Exception:
            pass

        return _jsonify({'resposta': resposta})

    except Exception as e:
        return _jsonify({'error': str(e)}, 500)


@app.route('/api/memory', methods=['POST'])
def add_memory():
    """Salva uma entrada de memória para o usuário logado."""
    sess, err = _require_auth(request)
    if err: return err
    data     = request.get_json(force=True) or {}
    content  = (data.get('content') or '').strip()
    category = (data.get('category') or 'geral').strip()
    if not content:
        return _jsonify({'error': 'Conteúdo vazio'}, 400)
    from utils.memory import add_memory as _add
    _add(sess['username'], content, category)
    return _jsonify({'ok': True})


@app.route('/api/memory', methods=['GET'])
def get_memory():
    """Retorna entradas de memória do usuário logado."""
    sess, err = _require_auth(request)
    if err: return err
    from utils.memory import load_memory
    return _jsonify(load_memory(sess['username']))

# ── Query ─────────────────────────────────────────────────────────────────────

@app.route('/api/query', methods=['POST'])
def execute_query():
    data = request.get_json(force=True) or {}
    sql  = (data.get('sql') or '').strip()

    if not sql:
        return _jsonify({'error': 'SQL vazio'}, 400)

    try:
        from db.connector import execute_query as _eq
        result, cols, err = _eq(sql)

        if err:
            return _jsonify({'error': err}, 500)

        if cols is not None:
            rows_plain = [dict(r) for r in (result or [])]
            return _jsonify({'columns': cols, 'rows': rows_plain, 'affected': None})

        sql_up = sql.upper().lstrip()
        if not (sql_up.startswith('SELECT') or sql_up.startswith('WITH')):
            try:
                from utils.query_log import log_query
                sess = _get_session(request)
                user = sess['username'] if sess else 'frontend'
                log_query(sql, '{0} linha(s) afetada(s)'.format(result or 0), user)
            except Exception:
                pass

        return _jsonify({'columns': [], 'rows': [], 'affected': result or 0})

    except Exception as e:
        return _jsonify({'error': str(e)}, 500)

# ── Screenshot ────────────────────────────────────────────────────────────────

@app.route('/api/screenshot', methods=['POST'])
def screenshot():
    try:
        from utils.screenshot import capture_screen
        return _jsonify({'imagem': capture_screen()})
    except Exception as e:
        return _jsonify({'error': str(e)}, 500)

# ── Análise de print ──────────────────────────────────────────────────────────

@app.route('/api/analyze-log', methods=['POST'])
def analyze_log():
    data     = request.get_json(force=True) or {}
    log_text = (data.get('log') or '').strip()
    contexto = (data.get('contexto') or '').strip()

    if not log_text:
        return _jsonify({'error': 'Log não fornecido'}, 400)

    # Limita tamanho do log para evitar excesso de tokens (~8k chars)
    if len(log_text) > 8000:
        log_text = log_text[:3800] + '\n...[meio do log omitido]...\n' + log_text[-3800:]

    try:
        p = _get_scan().get('profile')
        if not p:
            from utils.profile_cache import load_profile
            p = load_profile() or {}

        from ai.context_builder import build_system_prompt
        from ai.prompts import LOG_ANALYSIS_PROMPT
        from ai.client import ask

        static_part, dynamic_part = build_system_prompt(p)
        user_msg = LOG_ANALYSIS_PROMPT.format(
            log_content=log_text,
            contexto=contexto if contexto else 'Nenhum contexto adicional fornecido.'
        )
        resposta = _strip_bold(ask(dynamic_part, [{'role': 'user', 'content': user_msg}],
                                   static_prefix=static_part))

        try:
            sess = _get_session(request)
            username = sess['username'] if sess else 'anonimo'
            from utils.chat_logger import log_log_analysis
            log_log_analysis(username, log_text, contexto, resposta)
        except Exception:
            pass

        return _jsonify({'resposta': resposta})

    except Exception as e:
        return _jsonify({'error': str(e)}, 500)


@app.route('/api/analyze-print', methods=['POST'])
def analyze_print():
    data       = request.get_json(force=True) or {}
    imagem_b64 = data.get('imagem', '')
    descricao  = data.get('descricao', '')

    if not imagem_b64:
        return _jsonify({'error': 'Imagem não fornecida'}, 400)

    try:
        p = _get_scan().get('profile')
        if not p:
            from utils.profile_cache import load_profile
            p = load_profile() or {}

        from ai.context_builder import build_system_prompt
        from ai.prompts import IMAGE_ANALYSIS_PROMPT
        from ai.client import ask

        static_part, dynamic_part = build_system_prompt(p)
        user_msg = IMAGE_ANALYSIS_PROMPT.format(
            descricao=descricao.strip() if descricao.strip() else 'Não informada'
        )
        resposta = _strip_bold(ask(dynamic_part, [{'role': 'user', 'content': user_msg}],
                                   image_base64=imagem_b64, static_prefix=static_part))

        try:
            sess = _get_session(request)
            username = sess['username'] if sess else 'anonimo'
            from utils.chat_logger import log_print_analysis
            log_print_analysis(username, descricao, resposta)
        except Exception:
            pass

        return _jsonify({'resposta': resposta})

    except Exception as e:
        return _jsonify({'error': str(e)}, 500)

# ── Análise de XML ────────────────────────────────────────────────────────────

XML_ANALYSIS_PROMPT = """Analise os XMLs fiscais abaixo e explique de forma clara e objetiva:
- O que está acontecendo nesta nota
- Se há rejeição ou erro, qual é o motivo exato e como corrigir
- Informações relevantes: número da nota, CNPJ emitente, valor, status

XMLs:
{xmls}
{forum_section}"""

XML_ANALYSIS_PROMPT_FORUM = """
---
Resultados do fórum ACBR relacionados ao erro:
{forum_results}
---
Use as informações do fórum para complementar a análise e sugerir a solução correta."""


def _extrair_erros_xml(xmls_conteudo):
    """Extrai códigos e mensagens de erro dos XMLs (NFe cStat/xMotivo, NFSe cMsg/xMsg)."""
    erros = []
    padroes = [
        r'<cStat>(\d+)</cStat>',
        r'<xMotivo>([^<]+)</xMotivo>',
        r'<cMsg>(\d+)</cMsg>',
        r'<xMsg>([^<]+)</xMsg>',
        r'<descricaoRps>([^<]*[Ee]rro[^<]*)</descricaoRps>',
        r'<mensagem>([^<]+)</mensagem>',
        r'<codigo>(\d+)</codigo>',
    ]
    for conteudo in xmls_conteudo:
        for p in padroes:
            for m in re.findall(p, conteudo):
                v = m.strip()
                if v and v not in erros and len(v) < 200:
                    erros.append(v)
    return erros[:10]


def _buscar_forum_acbr(termos):
    """Busca no fórum ACBR pelos termos de erro. Retorna texto com resultados."""
    if not termos:
        return ''
    try:
        import urllib.request
        import urllib.parse
        query = ' '.join(termos[:3])
        url = 'https://www.acbr.com.br/forum/search.php?keywords=' + \
              urllib.parse.quote(query) + '&terms=all&author=&sc=1&sf=all&sr=posts&sk=t&sd=d&st=0&ch=300&t=0&submit=Pesquisar'
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')

        # Extrai títulos e trechos dos resultados
        titulos  = re.findall(r'class="topictitle"[^>]*>\s*<[^>]+>([^<]+)<', html)
        trechos  = re.findall(r'class="search-result-post-body"[^>]*>(.*?)</div>', html, re.DOTALL)
        links    = re.findall(r'href="(viewtopic\.php\?[^"]+)"', html)

        if not titulos:
            # Tenta formato alternativo (phpBB3)
            titulos = re.findall(r'<a[^>]+class="[^"]*topictitle[^"]*"[^>]*>([^<]+)</a>', html)

        resultados = []
        for i, titulo in enumerate(titulos[:4]):
            trecho = ''
            if i < len(trechos):
                trecho = re.sub(r'<[^>]+>', '', trechos[i]).strip()[:300]
            link = ('https://www.acbr.com.br/forum/' + links[i]) if i < len(links) else ''
            resultados.append('• {}{}\n{}'.format(
                titulo.strip(),
                (' — ' + link) if link else '',
                trecho
            ))

        return '\n\n'.join(resultados) if resultados else ''
    except Exception:
        return ''

def _buscar_xmls(numero_nota, tipo, data_ref, caminho_custom):
    """Busca XMLs pelo número da nota nos diretórios padrão."""
    encontrados = []  # lista de (caminho, conteudo)
    numero_nota = str(numero_nota).strip().lstrip('0')  # normaliza sem zeros à esq.

    def _varrer(diretorio, max_arquivos=20):
        if not os.path.exists(diretorio):
            return
        count = 0
        for root, _, files in os.walk(diretorio):
            for nome in files:
                if not nome.lower().endswith('.xml'):
                    continue
                caminho = os.path.join(root, nome)
                # Verifica no nome do arquivo
                nome_sem_ext = os.path.splitext(nome)[0]
                achou_nome = numero_nota in nome_sem_ext
                if not achou_nome:
                    # Verifica no conteúdo (primeiros 4KB)
                    try:
                        with open(caminho, 'r', encoding='utf-8', errors='ignore') as f:
                            amostra = f.read(4096)
                        if numero_nota not in amostra:
                            continue
                    except Exception:
                        continue
                # Lê conteúdo completo (limite 50KB)
                try:
                    with open(caminho, 'r', encoding='utf-8', errors='ignore') as f:
                        conteudo = f.read(51200)
                    encontrados.append((caminho, conteudo))
                    count += 1
                    if count >= max_arquivos:
                        return
                except Exception:
                    pass

    if caminho_custom:
        _varrer(caminho_custom)
    elif tipo == 'nfse':
        # C:\FarmaFacil\EXE\YYYYMM\NFSe\notas e recibos
        mes = data_ref or datetime.datetime.now().strftime('%Y%m')
        base = os.path.join('C:\\', 'FarmaFacil', 'EXE', mes, 'NFSe')
        _varrer(base)
    else:
        # NFe / NFCe padrão
        _varrer(os.path.join('C:\\', 'FarmaFacil', 'NFE'))

    return encontrados


@app.route('/api/analyze-xml', methods=['POST'])
def analyze_xml():
    data           = request.get_json(force=True) or {}
    numero_nota    = (data.get('numero_nota') or '').strip()
    tipo           = (data.get('tipo') or 'nfe').lower()        # nfe | nfse
    data_ref       = (data.get('data_ref') or '').strip()       # YYYYMM para NFSe
    caminho_custom = (data.get('caminho') or '').strip()
    # Upload direto: lista de {nome, conteudo}
    xml_upload     = data.get('xml_upload') or []

    try:
        nomes_arquivos = []

        # ── Modo upload direto (drag & drop) ──────────────────────────────────
        if xml_upload:
            pares = []
            for item in xml_upload:
                nome     = (item.get('nome') or 'arquivo.xml')
                conteudo = (item.get('conteudo') or '')[:51200]
                pares.append((nome, conteudo))
                nomes_arquivos.append(nome)

        # ── Modo busca por número da nota ─────────────────────────────────────
        else:
            if not numero_nota:
                return _jsonify({'error': 'Informe o número da nota ou arraste XMLs'}, 400)
            encontrados = _buscar_xmls(numero_nota, tipo, data_ref, caminho_custom)
            if not encontrados:
                return _jsonify({
                    'resposta': 'Nenhum XML encontrado para a nota **{}**.'.format(numero_nota) +
                                '\n\nVerifique:\n- Se o número está correto\n'
                                '- Se o diretório padrão existe\n'
                                '- Ou arraste os arquivos XML diretamente'
                })
            pares = [(os.path.basename(c), cont) for c, cont in encontrados]
            nomes_arquivos = [p[0] for p in pares]

        # ── Monta texto dos XMLs ───────────────────────────────────────────────
        xmls_fmt = ''
        for i, (nome, conteudo) in enumerate(pares, 1):
            xmls_fmt += '--- Arquivo {} de {}: {} ---\n{}\n\n'.format(
                i, len(pares), nome, conteudo[:8000])

        # ── Busca fórum ACBR (NFSe ou quando encontrar código de erro) ────────
        conteudos = [c for _, c in pares]
        erros     = _extrair_erros_xml(conteudos)
        forum_section = ''
        if erros and (tipo == 'nfse' or any(re.search(r'<cStat>(?!100\b|150\b|301\b)', c) for c in conteudos)):
            forum_txt = _buscar_forum_acbr(erros)
            if forum_txt:
                forum_section = XML_ANALYSIS_PROMPT_FORUM.format(forum_results=forum_txt)

        from ai.client import ask
        from ai.context_builder import build_system_prompt

        p = _get_scan().get('profile') or {}
        static_part, dynamic_part = build_system_prompt(p)
        user_msg = XML_ANALYSIS_PROMPT.format(xmls=xmls_fmt, forum_section=forum_section)

        resposta = _strip_bold(ask(dynamic_part,
                                   [{'role': 'user', 'content': user_msg}],
                                   static_prefix=static_part))
        return _jsonify({
            'resposta': resposta,
            'arquivos': nomes_arquivos,
            'erros_detectados': erros,
        })

    except Exception as e:
        return _jsonify({'error': str(e)}, 500)


# ── Tokens ────────────────────────────────────────────────────────────────────

@app.route('/api/tokens')
def tokens():
    try:
        from ai.client import get_token_count
        inp, out = get_token_count()
        return _jsonify({'input': inp, 'output': out, 'total': inp + out})
    except Exception:
        return _jsonify({'input': 0, 'output': 0, 'total': 0})

# ── Módulo Gestão — Movidesk ──────────────────────────────────────────────────

@app.route('/api/gestao/sync', methods=['POST'])
def gestao_sync():
    sess, err = _require_auth(request)
    if err: return err
    import threading
    from utils.movidesk_sync import sync_tickets
    body      = request.get_json(silent=True) or {}
    date_from = body.get('date_from')
    date_to   = body.get('date_to')
    def _run():
        sync_tickets(max_tickets=2000, date_from=date_from, date_to=date_to)
    threading.Thread(target=_run, daemon=True).start()
    msg = 'Sincronização iniciada'
    if date_from or date_to:
        msg += f' ({date_from or "?"} → {date_to or "hoje"})'
    return _jsonify({'ok': True, 'msg': msg + '.'})


@app.route('/api/gestao/sync/status')
def gestao_sync_status():
    from utils.movidesk_sync import sync_progress
    return _jsonify(sync_progress())


@app.route('/api/gestao/extract', methods=['POST'])
def gestao_extract():
    sess, err = _require_auth(request)
    if err: return err
    import threading
    from utils.movidesk_sync import extract_knowledge
    data  = request.get_json(force=True) or {}
    batch = int(data.get('batch', 30))
    def _run():
        extract_knowledge(batch=batch)
    threading.Thread(target=_run, daemon=True).start()
    return _jsonify({'ok': True, 'msg': f'Extração de até {batch} chamados iniciada.'})


@app.route('/api/gestao/stats')
def gestao_stats():
    try:
        from utils.movidesk_sync import get_stats
        date_from = request.args.get('date_from') or None
        date_to   = request.args.get('date_to')   or None
        analista  = request.args.get('analista')  or None
        categoria = request.args.get('categoria') or None
        grupo     = request.args.get('grupo')     or None
        return _jsonify(get_stats(date_from=date_from, date_to=date_to,
                                  analista=analista, categoria=categoria, grupo=grupo))
    except Exception as e:
        return _jsonify({'error': str(e)}, 500)


@app.route('/api/gestao/filters')
def gestao_filters():
    try:
        from utils.movidesk_sync import get_filter_options
        return _jsonify(get_filter_options())
    except Exception as e:
        return _jsonify({'error': str(e)}, 500)


@app.route('/api/gestao/tickets')
def gestao_tickets():
    try:
        from utils.movidesk_sync import get_tickets_list
        page      = int(request.args.get('page', 0))
        per_page  = int(request.args.get('per_page', 50))
        search    = request.args.get('search', '')
        analista  = request.args.get('analista', '')
        categoria = request.args.get('categoria', '')
        date_from = request.args.get('date_from') or None
        date_to   = request.args.get('date_to')   or None
        return _jsonify(get_tickets_list(page=page, per_page=per_page,
                                         search=search, analista=analista,
                                         categoria=categoria,
                                         date_from=date_from, date_to=date_to))
    except Exception as e:
        return _jsonify({'error': str(e)}, 500)


@app.route('/api/gestao/analise', methods=['POST'])
def gestao_analise():
    sess, err = _require_auth(request)
    if err: return err
    try:
        from utils.movidesk_sync import get_detailed_stats, build_ai_context
        from ai.client import ask

        data      = request.get_json(force=True) or {}
        date_from = data.get('date_from') or None
        date_to   = data.get('date_to')   or None
        days      = int(data.get('days', 30))
        stats     = get_detailed_stats(date_from=date_from, date_to=date_to, days=days)
        ctx   = build_ai_context(stats)

        system = (
            "Você é um especialista em gestão de suporte técnico de ERP farmacêutico. "
            "Analise os dados fornecidos e gere um relatório executivo direto e objetivo. "
            "Use linguagem clara. Cite números concretos. Destaque problemas críticos. "
            "Nunca use markdown com ** ou ##. Use seções numeradas e listas simples."
        )
        prompt = (
            ctx + "\n\n"
            "Gere um relatório executivo com estas seções:\n\n"
            "1. RESUMO EXECUTIVO\n"
            "Síntese em 3-4 linhas do que está acontecendo.\n\n"
            "2. VOLUME E TENDÊNCIAS\n"
            "Compare esta semana vs semana anterior. Destaque variações.\n\n"
            "3. PERFORMANCE DOS ANALISTAS\n"
            "Quem está resolvendo mais rápido. Quem tem mais chamados fora do SLA.\n\n"
            "4. CATEGORIAS CRÍTICAS\n"
            "Problemas mais frequentes e os que mais cresceram.\n\n"
            "5. FARMÁCIAS EM ATENÇÃO\n"
            "Clientes com mais chamados no período — podem precisar de suporte dedicado.\n\n"
            "6. SUGESTÕES DE AÇÃO\n"
            "Para cada problema identificado, sugira ação prática: treinamento, correção de sistema, "
            "ajuste de processo ou automação. Seja específico."
        )

        resposta = ask(system, [{"role": "user", "content": prompt}])
        return _jsonify({"resposta": resposta, "stats": stats})
    except Exception as e:
        return _jsonify({"error": str(e)}, 500)


@app.route('/api/gestao/ia-chat', methods=['POST'])
def gestao_ia_chat():
    sess, err = _require_auth(request)
    if err: return err
    try:
        from utils.movidesk_sync import get_detailed_stats, build_ai_context, get_metas_por_equipe
        from ai.client import ask

        data      = request.get_json(force=True) or {}
        pergunta  = (data.get('pergunta') or '').strip()
        historico = data.get('historico') or []
        date_from = data.get('date_from') or None
        date_to   = data.get('date_to')   or None
        days      = int(data.get('days', 30))

        if not pergunta:
            return _jsonify({'error': 'Pergunta vazia'}, 400)

        stats = get_detailed_stats(date_from=date_from, date_to=date_to, days=days)
        ctx   = build_ai_context(stats)

        try:
            metas = get_metas_por_equipe()
            metas_ctx = "\n\nMETAS POR EQUIPE (dados em tempo real):\n"
            for eq in metas:
                status_eq = "dentro da meta" if eq.get('atingiu') else "abaixo da meta"
                metas_ctx += (
                    f"\nEquipe {eq['grupo']} ({eq['membros_count']} analistas) — {status_eq}:\n"
                    f"  Meta/dia por analista: {eq['equilibrio_dia']} | Ritmo atual: {eq['taxa_dia_analista']}/dia\n"
                    f"  Fila total: {eq['fila_total']} | Fechados este mês: {eq['fechados_mes']} | Dias úteis decorridos: {eq['dias_uteis_dec']}\n"
                    f"  Entradas este mês: {eq.get('entradas_mes', '—')}\n"
                )
                for m in eq.get('membros', []):
                    status_m = "dentro da meta" if m['atingiu'] else "abaixo da meta"
                    metas_ctx += (
                        f"    {m['nome']}: fechou {m['fechou_mes']} este mês, "
                        f"ritmo {m['taxa_dia']}/dia, meta {m['meta_dia']}/dia, "
                        f"fila {m['fila']} [{status_m}]\n"
                    )
        except Exception:
            metas_ctx = ""

        system = (
            "Você é um especialista em gestão de suporte técnico de ERP farmacêutico.\n"
            "Responda perguntas sobre os dados de chamados fornecidos.\n\n"
            "DADOS DISPONÍVEIS:\n"
            "- Volumes, categorias e tendências dos chamados do período\n"
            "- Assuntos reais (títulos) dos chamados por categoria\n"
            "- Palavras-chave extraídas dos assuntos de cada categoria\n"
            "- Pares problema/solução de chamados já resolvidos\n"
            "- Desempenho por analista e metas por equipe\n\n"
            "REGRAS:\n"
            "- Seja direto e cite números concretos\n"
            "- Use os assuntos e palavras-chave reais para identificar padrões e causas raiz\n"
            "- Se a pergunta for sobre uma categoria, analise os títulos dos chamados dessa categoria\n"
            "- Compare períodos quando relevante (atual vs anterior)\n"
            "- Nunca invente dados — se não tiver a informação, diga claramente\n"
            "- Nunca use markdown com ** ou ## ou ---\n"
            "- Use texto simples e listas quando necessário\n"
            "- SEMPRE termine com 'SUGESTOES DE MELHORIA' com 2-3 ações práticas e específicas "
            "baseadas nos assuntos e padrões reais observados.\n\n"
            + ctx + metas_ctx
        )

        msgs = list(historico[-6:])
        msgs.append({"role": "user", "content": pergunta})

        resposta = ask(system, msgs)
        return _jsonify({"resposta": resposta})
    except Exception as e:
        return _jsonify({"error": str(e)}, 500)


@app.route('/api/gestao/analista-view')
def gestao_analista_view():
    sess, err = _require_auth(request)
    if err: return err
    try:
        movidesk_name = sess.get('movidesk_name') or sess.get('username')
        from utils.movidesk_sync import get_analista_tickets, find_similar
        from utils.checklists import get_checklist
        from datetime import datetime, date

        tickets = get_analista_tickets(movidesk_name)
        hoje = date.today()

        enriched = []
        for t in tickets:
            dias = None
            cd = (t.get("createdDate") or "")[:10]
            if cd:
                try:
                    dias = (hoje - date.fromisoformat(cd)).days
                except Exception:
                    pass
            cat = t.get("serviceSecond") or t.get("serviceFirst") or ""
            enriched.append({
                **t,
                "dias_aberto": dias,
                "checklist":   get_checklist(cat),
                "similares":   find_similar(t.get("subject", ""), t.get("client_name"))[:3],
            })

        return _jsonify({"tickets": enriched, "total": len(enriched), "analista": movidesk_name})
    except Exception as e:
        return _jsonify({"error": str(e)}, 500)


@app.route('/api/gestao/respostas-rapidas')
def gestao_respostas_rapidas():
    try:
        from utils.movidesk_sync import get_respostas_rapidas
        return _jsonify(get_respostas_rapidas())
    except Exception as e:
        return _jsonify({'error': str(e)}, 500)


@app.route('/api/gestao/sync-meta-historico', methods=['POST'])
def gestao_sync_meta_historico():
    try:
        from utils.movidesk_sync import sync_meta_entradas_historico
        months_back = int(request.json.get('months_back', 3)) if request.json else 3
        resultado   = sync_meta_entradas_historico(months_back=months_back)
        return _jsonify({'ok': True, 'resultado': resultado})
    except Exception as e:
        return _jsonify({'error': str(e)}, 500)


@app.route('/api/gestao/sync-abertos', methods=['POST'])
def gestao_sync_abertos():
    try:
        from utils.movidesk_sync import sync_open_tickets
        novos = sync_open_tickets(max_tickets=2000)
        return _jsonify({'ok': True, 'novos': novos})
    except Exception as e:
        return _jsonify({'error': str(e)}, 500)


@app.route('/api/gestao/duplicados')
def gestao_duplicados():
    try:
        from utils.movidesk_sync import get_chamados_duplicados
        so_abertos = request.args.get('abertos', 'true').lower() == 'true'
        grupo      = request.args.get('grupo', '') or None
        return _jsonify({'duplicados': get_chamados_duplicados(so_abertos, grupo=grupo)})
    except Exception as e:
        return _jsonify({'error': str(e)}, 500)


@app.route('/api/gestao/nova-versao')
def gestao_nova_versao():
    """Issues do sprint ativo. SOMENTE LEITURA — nunca escreve no Jira."""
    sess, err = _require_auth(request)
    if err: return err
    try:
        issues, sprint_name = _get_sprint_issues_cached()
        return _jsonify({'issues': issues, 'sprint_name': sprint_name})
    except Exception as e:
        return _jsonify({'error': str(e)}, 500)


@app.route('/api/gestao/checklists')
def gestao_checklists():
    try:
        from utils.checklists import get_all_checklists
        return _jsonify(get_all_checklists())
    except Exception as e:
        return _jsonify({'error': str(e)}, 500)


@app.route('/api/gestao/aderencia')
def gestao_aderencia():
    """Aderência ao perfil: % dos chamados fechados dentro da categoria do grupo do analista."""
    sess, err = _require_auth(request)
    if err: return err
    try:
        from collections import Counter as _Counter
        from utils.movidesk_sync import load_cache, _filter_resolved_in_period
        from utils.gestao_config import load_config, get_grupo_for_ticket, get_excluir_metas

        date_from = request.args.get('date_from') or None
        date_to   = request.args.get('date_to')   or None

        cache      = load_cache()
        all_tix    = list(cache.get('tickets', {}).values())
        resolvidos = _filter_resolved_in_period(all_tix, date_from, date_to)

        cfg     = load_config()
        excluir = get_excluir_metas()

        resultado = []
        for grupo, membros in cfg.get('grupos', {}).items():
            for nome in membros:
                if nome.lower() in excluir:
                    continue
                res_analista = [
                    t for t in resolvidos
                    if (t.get('owner_name') or '').lower() == nome.lower()
                ]
                if not res_analista:
                    continue

                na_cat       = 0
                cats         = _Counter()
                tickets_fora = []
                for t in res_analista:
                    s1  = (t.get('serviceFirst')  or '').strip()
                    s2  = (t.get('serviceSecond') or '').strip()
                    cat = s1
                    if cat:
                        cats[cat] += 1
                    ticket_grupo = get_grupo_for_ticket(t)
                    if ticket_grupo == grupo:
                        na_cat += 1
                    else:
                        tickets_fora.append({
                            'id':       t.get('id', ''),
                            'subject':  (t.get('subject') or '')[:80],
                            'categoria': f"{s1}{' › ' + s2 if s2 else ''}",
                            'cliente':  (t.get('client_name') or '').strip(),
                            'data':     (t.get('resolvedIn') or t.get('lastUpdate') or t.get('closedIn') or '')[:10],
                            'grupo_cat': ticket_grupo or '—',
                        })

                # Ordena fora por data desc (mais recentes primeiro)
                tickets_fora.sort(key=lambda x: x['data'], reverse=True)

                total         = len(res_analista)
                fora_cat      = total - na_cat
                aderencia_pct = round((na_cat / total) * 100) if total > 0 else 0

                resultado.append({
                    'nome':             nome,
                    'grupo':            grupo,
                    'total_resolvidos': total,
                    'na_categoria':     na_cat,
                    'fora_categoria':   fora_cat,
                    'aderencia_pct':    aderencia_pct,
                    'top_categorias':   cats.most_common(6),
                    'tickets_fora':     tickets_fora,
                })

        resultado.sort(key=lambda x: (x['grupo'], -(x['total_resolvidos'] or 0)))
        return _jsonify({'analistas': resultado, 'periodo': {'from': date_from, 'to': date_to}})
    except Exception as e:
        import traceback
        return _jsonify({'error': str(e), 'trace': traceback.format_exc()}, 500)


@app.route('/api/gestao/metas')
def gestao_metas():
    try:
        from utils.movidesk_sync import get_metas_por_equipe
        semanas_alvo = int(request.args.get('semanas_alvo', 4))
        return _jsonify(get_metas_por_equipe(semanas_alvo=semanas_alvo))
    except Exception as e:
        return _jsonify({'error': str(e)}, 500)


@app.route('/api/gestao/metas-analise', methods=['POST'])
def gestao_metas_analise():
    sess, err = _require_auth(request)
    if err: return err
    try:
        from utils.movidesk_sync import get_metas_por_equipe
        from utils.knowledge_search import search
        from ai.client import ask

        data         = request.get_json(force=True) or {}
        grupo        = data.get('grupo', '')
        semanas_alvo = int(data.get('semanas_alvo', 4))

        equipes    = get_metas_por_equipe(semanas_alvo=semanas_alvo)
        grupo_data = next((e for e in equipes if e['grupo'] == grupo), None)
        if not grupo_data:
            return _jsonify({'error': 'Grupo não encontrado'}, 404)

        # Busca artigos relevantes para as top categorias
        top_cats = [cat for cat, _ in grupo_data['top_categorias'][:3]]
        knowledge_ctx = ""
        for cat in top_cats:
            artigos = search(cat, top_n=2, max_chars=2000)
            if artigos:
                knowledge_ctx += f"\n\n--- Artigos sobre '{cat}' ---\n{artigos}"

        status_txt = {
            "crescendo": "FILA CRESCENDO (entrada > fechamentos)",
            "estavel":   "fila estável",
            "reduzindo": "fila reduzindo"
        }.get(grupo_data["status"], "")

        mes_atual = next((m for m in grupo_data.get('historico_meses', []) if m.get('parcial')), {})
        membros_txt = "\n".join(
            f"  {m['nome']}: ritmo {m['taxa_dia']}/dia, meta {m['meta_dia']}/dia, fila {m['fila']}, fechou {m['fechou_mes']} este mês"
            for m in grupo_data.get('membros', [])
        )
        ctx = (
            f"EQUIPE: {grupo_data['grupo']}\n"
            f"Analistas: {grupo_data['membros_count']} | Fila atual: {grupo_data['fila_total']} chamados | Status: {status_txt}\n"
            f"Dias úteis decorridos: {grupo_data.get('dias_uteis_dec', '—')}\n"
            f"Fechados este mês: {grupo_data.get('fechados_mes', '—')} | Ritmo equipe: {grupo_data.get('taxa_dia_analista', '—')}/dia por analista\n"
            f"Entradas este mês: {mes_atual.get('entradas', '—')} | Meta/dia por analista: {grupo_data.get('equilibrio_dia', '—')}\n"
            f"Saldo semanal: {grupo_data.get('saldo_semana', '—')} (fechamentos − entradas)\n\n"
            f"DESEMPENHO POR ANALISTA:\n{membros_txt}\n\n"
            f"TOP CATEGORIAS NA FILA:\n"
            + "\n".join(f"  {n}x {cat}" for cat, n in grupo_data.get('top_categorias', []))
        )
        if knowledge_ctx:
            ctx += f"\n\nBASE DE CONHECIMENTO DISPONÍVEL:{knowledge_ctx}"

        system = (
            "Você é especialista em gestão de suporte técnico do ERP FarmaFácil (PrismaFive). "
            "Com base nos dados da equipe e na base de conhecimento disponível, responda em 4 seções:\n\n"
            "1. POR QUE A FILA CRESCEU — explique as prováveis causas com base nas categorias (ex: versão nova, período fiscal, sazonalidade)\n"
            "2. ARTIGOS PARA OS CLIENTES — liste artigos/tutoriais da base de conhecimento que os clientes podem acessar sozinhos antes de abrir chamado (reduz entrada)\n"
            "3. DICAS PARA OS ANALISTAS — orientações práticas para resolver essas categorias mais rápido, perguntas de triagem, soluções comuns\n"
            "4. AÇÃO DESTA SEMANA — 3 ações concretas e imediatas para a equipe reduzir a fila\n\n"
            "Seja direto e cite os números. Use os artigos da base de conhecimento quando relevante."
        )

        resposta = ask(system, [{"role": "user", "content": ctx}])
        return _jsonify({'resposta': resposta, 'grupo_data': grupo_data})
    except Exception as e:
        return _jsonify({'error': str(e)}, 500)


@app.route('/api/gestao/sazonalidade')
def gestao_sazonalidade():
    try:
        from utils.movidesk_sync import get_sazonalidade
        date_from   = request.args.get('date_from') or None
        date_to     = request.args.get('date_to')   or None
        agrupamento = request.args.get('agrupamento', 'semana')
        grupo       = request.args.get('grupo') or None
        return _jsonify(get_sazonalidade(date_from=date_from, date_to=date_to,
                                         agrupamento=agrupamento, grupo=grupo))
    except Exception as e:
        return _jsonify({'error': str(e)}, 500)


@app.route('/api/gestao/sazonalidade-analise', methods=['POST'])
def gestao_sazonalidade_analise():
    sess, err = _require_auth(request)
    if err: return err
    try:
        from utils.movidesk_sync import get_sazonalidade, build_sazonalidade_context
        from ai.client import ask

        data        = request.get_json(force=True) or {}
        date_from   = data.get('date_from') or None
        date_to     = data.get('date_to')   or None
        agrupamento = data.get('agrupamento', 'semana')
        grupo       = data.get('grupo') or None

        periodos = get_sazonalidade(date_from=date_from, date_to=date_to,
                                     agrupamento=agrupamento, grupo=grupo)
        ctx = build_sazonalidade_context(periodos, agrupamento=agrupamento)

        sistema = (
            "Você é especialista em gestão de suporte técnico de ERP farmacêutico. "
            "Analise os dados de sazonalidade de chamados e explique os padrões observados. "
            "Identifique os picos, explique possíveis causas (sazonalidade fiscal, lançamentos de versão, "
            "datas especiais, férias, viradas de ano/mês), e sugira ações preventivas. "
            "Seja objetivo e cite os números concretos dos dados."
        )
        prompt = (
            f"{ctx}\n\n"
            "Com base nesses dados:\n"
            "1. Quais períodos tiveram maior volume e qual o provável motivo?\n"
            "2. Há padrões sazonais (ex: início de mês, virada de ano, datas fiscais)?\n"
            "3. Quais categorias puxaram os picos?\n"
            "4. Que ações preventivas podem reduzir chamados nos próximos picos?\n"
        )

        resposta = ask(sistema, [{"role": "user", "content": prompt}])
        return _jsonify({'resposta': resposta, 'periodos': periodos})
    except Exception as e:
        return _jsonify({'error': str(e)}, 500)


@app.route('/api/gestao/similar', methods=['POST'])
def gestao_similar():
    try:
        from utils.movidesk_sync import find_similar
        data        = request.get_json(force=True) or {}
        subject     = data.get('subject', '')
        client_name = data.get('client_name', '')
        results     = find_similar(subject, client_name=client_name or None)
        return _jsonify({'similar': results})
    except Exception as e:
        return _jsonify({'error': str(e)}, 500)


# ── Tarefas — leitura do Jira (SOMENTE LEITURA, NUNCA ESCREVER NO JIRA) ───────
# Busca issues do projeto ID filtradas pela label sistema-farmafacil.
# REGRA: este endpoint é GET apenas. Nunca fazer POST/PUT/DELETE no Jira.

_JIRA_BASE  = 'https://prismadelphi.atlassian.net/rest/api/3'

def _load_jira_creds():
    try:
        from utils.paths import get_data_dir
        import json as _j
        with open(os.path.join(get_data_dir(), 'connection.json'), encoding='utf-8') as _f:
            _c = _j.load(_f)
        return _c.get('jira_email', ''), _c.get('jira_token', '')
    except Exception:
        return '', ''

_JIRA_EMAIL, _JIRA_TOKEN = _load_jira_creds()

import base64 as _b64
import urllib.request as _ur
import urllib.parse as _up
import threading as _threading
import time as _time_mod
_JIRA_AUTH = _b64.b64encode('{0}:{1}'.format(_JIRA_EMAIL, _JIRA_TOKEN).encode()).decode()

# Cache em memória das issues (somente leitura) — TTL 30 min
_jira_cache = {'issues': [], 'ts': 0}
_jira_cache_lock = _threading.Lock()
_JIRA_CACHE_TTL = 1800

# Cache separado para o sprint ativo (somente leitura) — TTL 30 min
_sprint_cache = {'issues': [], 'sprint_name': '', 'ts': 0}
_sprint_cache_lock = _threading.Lock()

def _fetch_sprint_issues():
    """Busca issues do sprint ativo. SOMENTE LEITURA — nunca escreve no Jira."""
    import re as _re_sp
    jql    = 'project = ID AND sprint in openSprints() ORDER BY status ASC'
    fields = ['summary', 'status', 'issuetype', 'priority', 'assignee', 'customfield_10020']
    body   = {'jql': jql, 'maxResults': 100, 'fields': fields}
    req    = _ur.Request(
        '{0}/search/jql'.format(_JIRA_BASE),
        data=json.dumps(body).encode('utf-8'),
        headers={'Authorization': 'Basic ' + _JIRA_AUTH, 'Accept': 'application/json', 'Content-Type': 'application/json'},
        method='POST',
    )
    with _ur.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())

    issues      = []
    sprint_name = ''
    for issue in data.get('issues', []):
        f          = issue.get('fields', {})
        status_name = (f.get('status') or {}).get('name', '')
        status_cat  = (((f.get('status') or {}).get('statusCategory')) or {}).get('key', '')

        # Tenta extrair nome do sprint (customfield_10020)
        sp_raw = f.get('customfield_10020') or []
        if sp_raw and isinstance(sp_raw, list):
            last = sp_raw[-1]
            if isinstance(last, dict):
                sprint_name = last.get('name', sprint_name)
            elif isinstance(last, str):
                m = _re_sp.search(r'name=([^,\]]+)', last)
                if m:
                    sprint_name = m.group(1).strip()

        issues.append({
            'key':        issue.get('key', ''),
            'titulo':     f.get('summary', ''),
            'tipo':       (f.get('issuetype') or {}).get('name', ''),
            'status':     status_name,
            'status_cat': status_cat,
            'prioridade': (f.get('priority') or {}).get('name', ''),
            'responsavel':((f.get('assignee') or {}).get('displayName') or ''),
            'url':        'https://prismadelphi.atlassian.net/browse/{0}'.format(issue.get('key')),
        })
    return issues, sprint_name


def _get_sprint_issues_cached():
    """Retorna issues do sprint ativo via cache. SOMENTE LEITURA."""
    with _sprint_cache_lock:
        if _time_mod.time() - _sprint_cache['ts'] < _JIRA_CACHE_TTL and _sprint_cache['issues']:
            return list(_sprint_cache['issues']), _sprint_cache['sprint_name']
    try:
        issues, sprint_name = _fetch_sprint_issues()
        with _sprint_cache_lock:
            _sprint_cache['issues']      = issues
            _sprint_cache['sprint_name'] = sprint_name
            _sprint_cache['ts']          = _time_mod.time()
        return issues, sprint_name
    except Exception:
        return list(_sprint_cache.get('issues', [])), _sprint_cache.get('sprint_name', '')


def _fetch_all_jira_issues():
    """Busca todas as issues do projeto ID. Somente GET/POST de busca."""
    import re as _re2

    def _adf_text(node):
        if not node: return ''
        if isinstance(node, str): return node
        t = ''
        if node.get('type') == 'text': t = node.get('text', '')
        for child in node.get('content', []):
            t += ' ' + _adf_text(child)
        return t

    jql = 'project = ID ORDER BY created DESC'
    fields = ['summary', 'status', 'issuetype', 'priority', 'assignee', 'updated',
              'description', 'labels', 'comment', 'components']
    issues = []
    next_page_token = None
    while True:
        body = {'jql': jql, 'maxResults': 100, 'fields': fields}
        if next_page_token:
            body['nextPageToken'] = next_page_token
        payload = json.dumps(body).encode('utf-8')
        req = _ur.Request(
            '{0}/search/jql'.format(_JIRA_BASE),
            data=payload,
            headers={'Authorization': 'Basic ' + _JIRA_AUTH, 'Accept': 'application/json', 'Content-Type': 'application/json'},
            method='POST',
        )
        with _ur.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
        batch = data.get('issues', [])
        for issue in batch:
            f = issue.get('fields', {})
            # Extrai texto plano da descrição (ADF v3 ou string)
            desc_raw = f.get('description') or ''
            if isinstance(desc_raw, dict):
                desc_text = _re2.sub(r'\s+', ' ', _adf_text(desc_raw)).strip()[:3000]
            else:
                desc_text = _re2.sub(r'<[^>]+>', ' ', str(desc_raw))[:3000]
            # Texto dos comentários (últimos 20) — trata corpo ADF ou string
            comment_parts = []
            for c in (f.get('comment') or {}).get('comments', [])[-20:]:
                body_raw = c.get('body') or ''
                if isinstance(body_raw, dict):
                    part = _re2.sub(r'\s+', ' ', _adf_text(body_raw)).strip()[:500]
                else:
                    part = _re2.sub(r'\s+', ' ', str(body_raw))[:500]
                comment_parts.append(part)
            comment_text = ' '.join(comment_parts)
            # Componentes (ex: "Betha", "WebISS", etc.)
            components_text = ' '.join(
                (c.get('name') or '') for c in (f.get('components') or [])
            )
            issues.append({
                'key':          issue.get('key', ''),
                'titulo':       f.get('summary', ''),
                'tipo':         (f.get('issuetype') or {}).get('name', ''),
                'status':       (f.get('status') or {}).get('name', ''),
                'status_cat':   (((f.get('status') or {}).get('statusCategory')) or {}).get('key', ''),
                'prioridade':   (f.get('priority') or {}).get('name', ''),
                'responsavel':  ((f.get('assignee') or {}).get('displayName') or ''),
                'atualizado':   (f.get('updated') or '')[:10],
                'labels':       [l for l in (f.get('labels') or [])],
                'components':   components_text,
                'desc_text':    desc_text,
                'comment_text': comment_text,
            })
        next_page_token = data.get('nextPageToken')
        if not batch or not next_page_token or data.get('isLast', False):
            break
    return issues

def _get_jira_issues_cached():
    """Retorna issues do cache, atualizando se TTL expirou."""
    with _jira_cache_lock:
        if _time_mod.time() - _jira_cache['ts'] < _JIRA_CACHE_TTL and _jira_cache['issues']:
            return list(_jira_cache['issues'])
    try:
        issues = _fetch_all_jira_issues()
        with _jira_cache_lock:
            _jira_cache['issues'] = issues
            _jira_cache['ts'] = _time_mod.time()
        return issues
    except Exception:
        return list(_jira_cache.get('issues', []))

def _strip_html(html):
    """Remove tags HTML e retorna texto simples, truncado a 1500 chars."""
    import re as _re
    text = _re.sub(r'<[^>]+>', ' ', html or '')
    text = _re.sub(r'\s{2,}', ' ', text).strip()
    return text[:1500]

_jira_detail_cache = {}  # key → (desc, comments, ts)
_JIRA_DETAIL_TTL = 3600  # 1 hora — detalhes de issues raramente mudam

def _fetch_jira_detail_text(key):
    """Busca descrição + comentários de uma issue como texto puro. Somente leitura."""
    cached = _jira_detail_cache.get(key)
    if cached and _time_mod.time() - cached[2] < _JIRA_DETAIL_TTL:
        return cached[0], cached[1]
    try:
        url = 'https://prismadelphi.atlassian.net/rest/api/2/issue/{0}?expand=renderedFields'.format(key)
        req = _ur.Request(url, headers={'Authorization': 'Basic ' + _JIRA_AUTH, 'Accept': 'application/json'})
        with _ur.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        rf = data.get('renderedFields', {})
        f  = data.get('fields', {})
        desc = _strip_html(rf.get('description') or '')
        comentarios = []
        for c in (rf.get('comment') or {}).get('comments', [])[-5:]:
            autor = (f.get('comment', {}).get('comments', [{}]) or [{}])
            # pega autor do campo fields
            raw_comments = f.get('comment', {}).get('comments', [])
            autor_nome = ''
            for rc in raw_comments:
                if rc.get('id') == c.get('id'):
                    autor_nome = (rc.get('author') or {}).get('displayName', '')
                    break
            corpo = _strip_html(c.get('body', ''))
            if corpo:
                comentarios.append('[{autor}]: {corpo}'.format(autor=autor_nome or '?', corpo=corpo[:400]))
        _jira_detail_cache[key] = (desc, comentarios, _time_mod.time())
        return desc, comentarios
    except Exception:
        return '', []

def _search_jira_context(query):
    """Retorna contexto de issues relevantes para injetar no chat. Somente leitura."""
    import re as _re
    q_low = query.lower()

    # Pergunta sobre sprint/versão → injeta issues do sprint ativo
    _versao_kw = ('versao', 'versão', 'sprint', 'proxima versao', 'próxima versão',
                  'nova versao', 'nova versão', 'novidade', 'lançamento', 'lancamento',
                  'vai sair', 'vai ser lançado', 'proximo release')
    if any(k in q_low for k in _versao_kw):
        try:
            sp_issues, sp_name = _get_sprint_issues_cached()
            if sp_issues:
                lines = ['## Sprint atual — próxima versão do FarmaFácil ({0}):'.format(sp_name or 'em andamento')]
                status_order = {'indeterminate': 0, 'new': 1, 'done': 2}
                for iss in sorted(sp_issues, key=lambda x: status_order.get(x.get('status_cat', ''), 1)):
                    lines.append('- {key}: [{tipo}] {titulo} — {status}'.format(
                        key=iss['key'], tipo=iss['tipo'], titulo=iss['titulo'], status=iss['status']
                    ))
                return '\n'.join(lines)
        except Exception:
            pass

    issues = _get_jira_issues_cached()
    if not issues:
        return ''

    # Match exato por key (ex: ID-123) → detalhe completo
    key_match = _re.search(r'\bID-\d+\b', query, _re.IGNORECASE)
    if key_match:
        key = key_match.group(0).upper()
        matched = [i for i in issues if i['key'].upper() == key]
        if matched:
            desc, comments = _fetch_jira_detail_text(key)
            return _format_jira_ctx(matched[:1], details=[(key, desc, comments)])

    # Busca ampla: título + descrição + comentários + labels
    q = query.lower()
    words = [w for w in _re.split(r'\W+', q) if len(w) > 2]
    if not words:
        return ''

    def _slug(s):
        return _re.sub(r'[^a-z0-9]', '', s.lower())

    # Slug da query inteira (ex: "siltecnologia") para bater em "Sil Tecnologia"
    query_slug = _slug(q)

    scored = []
    for issue in issues:
        full_text = ' '.join([
            issue['titulo'],
            issue['key'],
            issue.get('desc_text', ''),
            issue.get('comment_text', ''),
            ' '.join(issue.get('labels', [])),
        ]).lower()
        full_slug = _slug(full_text)

        # Peso: título vale mais (3x), conteúdo vale 1x
        title_slug  = _slug(issue['titulo'])
        title_score   = sum(3 for w in words if w in issue['titulo'].lower())
        content_score = sum(1 for w in words if w in full_text)
        # Bônus: slug da query bate no slug do texto (captura "sil tecnologia" == "siltecnologia")
        slug_bonus = 10 if query_slug and query_slug in full_slug else 0
        slug_bonus += 5 if query_slug and query_slug in title_slug else 0

        score = title_score + content_score + slug_bonus
        if score > 0:
            scored.append((score, issue))

    scored.sort(key=lambda x: -x[0])
    if not scored:
        return ''
    # Lista completa (até 20), descrição detalhada das top 3
    top = [x[1] for x in scored[:20]]
    details = []
    for issue in top[:3]:
        desc, comments = _fetch_jira_detail_text(issue['key'])
        if desc or comments:
            details.append((issue['key'], desc, comments))
    return _format_jira_ctx(top, details=details)

def _format_jira_ctx(issues, details=None):
    lines = ['## Tarefas do Jira relacionadas (somente leitura):']
    for i in issues:
        lines.append('- {key} [{status}] {titulo} (Tipo: {tipo}, Responsável: {resp})'.format(
            key=i['key'], status=i['status'], titulo=i['titulo'],
            tipo=i['tipo'], resp=i['responsavel'] or '—'
        ))
    for key, desc, comentarios in (details or []):
        if desc:
            lines.append('\n### Descrição completa — {key}:'.format(key=key))
            lines.append(desc)
        if comentarios:
            lines.append('### Comentários recentes — {key}:'.format(key=key))
            lines.extend(comentarios)
    return '\n'.join(lines)


@app.route('/api/tarefas', methods=['GET'])
def tarefas_list():
    sess, err = _require_auth(request)
    if err: return err
    try:
        jql = 'project = ID ORDER BY created DESC'
        fields = ['summary', 'status', 'issuetype', 'priority', 'assignee', 'created', 'updated']
        issues = []
        next_page_token = None
        while True:
            body = {
                'jql': jql,
                'maxResults': 100,
                'fields': fields,
            }
            if next_page_token:
                body['nextPageToken'] = next_page_token
            payload = json.dumps(body).encode('utf-8')
            req = _ur.Request(
                '{0}/search/jql'.format(_JIRA_BASE),
                data=payload,
                headers={
                    'Authorization': 'Basic ' + _JIRA_AUTH,
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                method='POST',
            )
            with _ur.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
            batch = data.get('issues', [])
            for issue in batch:
                f = issue.get('fields', {})
                status_name = (f.get('status') or {}).get('name', '')
                status_cat  = (((f.get('status') or {}).get('statusCategory')) or {}).get('key', '')
                issues.append({
                    'id':          issue.get('key'),
                    'titulo':      f.get('summary', ''),
                    'tipo':        (f.get('issuetype') or {}).get('name', ''),
                    'status':      status_name,
                    'status_cat':  status_cat,
                    'prioridade':  (f.get('priority') or {}).get('name', ''),
                    'responsavel': ((f.get('assignee') or {}).get('displayName') or ''),
                    'criado_em':   (f.get('created') or '')[:10],
                    'atualizado':  (f.get('updated') or '')[:10],
                    'url': 'https://prismadelphi.atlassian.net/browse/{0}'.format(issue.get('key')),
                })
            next_page_token = data.get('nextPageToken')
            if not batch or not next_page_token or data.get('isLast', False):
                break
        return _jsonify(issues)
    except Exception as e:
        return _jsonify({'error': str(e)}, 500)


@app.route('/api/tarefas/<key>/detail', methods=['GET'])
def tarefa_detail(key):
    """Detalhe completo de uma issue — somente leitura."""
    sess, err = _require_auth(request)
    if err: return err
    try:
        url = (
            'https://prismadelphi.atlassian.net/rest/api/2/issue/{0}'
            '?expand=renderedFields'
            '&fields=summary,description,status,assignee,reporter,created,updated,'
            'comment,attachment,issuetype,priority,labels,components,fixVersions,'
            'versions,issuelinks,subtasks,customfield_10020,customfield_10016,resolution'
        ).format(key)
        req = _ur.Request(url, headers={
            'Authorization': 'Basic ' + _JIRA_AUTH,
            'Accept': 'application/json',
        })
        with _ur.urlopen(req, timeout=15) as resp:
            d = json.loads(resp.read())
        f  = d.get('fields', {})
        rf = d.get('renderedFields', {})

        import re as _re

        def _proxy_html(html):
            if not html:
                return ''
            def repl(m):
                src = m.group(1)
                if 'atlassian.net' in src:
                    return 'src="/api/img?url={0}"'.format(_up.quote(src, safe=''))
                return m.group(0)
            return _re.sub(r'src="([^"]+)"', repl, html)

        # Comentários: usa renderedFields.comment.comments (tem HTML renderizado)
        rf_comments = (rf.get('comment') or {}).get('comments', [])
        raw_comments = (f.get('comment') or {}).get('comments', [])
        comments = []
        for i, rc in enumerate(rf_comments):
            raw = raw_comments[i] if i < len(raw_comments) else {}
            corpo = _proxy_html(rc.get('body') or '')
            if not corpo:
                corpo = rc.get('body') or raw.get('body') or ''
            comments.append({
                'autor':    (raw.get('author') or rc.get('author') or {}).get('displayName', ''),
                'criado':   (raw.get('created') or '')[:16].replace('T', ' '),
                'corpo':    corpo,
            })

        attachments = []
        for a in (f.get('attachment') or []):
            att_url = '/api/img?url={0}'.format(_up.quote(a.get('content', ''), safe=''))
            thumb_url = '/api/img?url={0}'.format(_up.quote(a.get('thumbnail') or a.get('content', ''), safe=''))
            attachments.append({
                'id':        a.get('id'),
                'nome':      a.get('filename'),
                'mime':      a.get('mimeType', ''),
                'tamanho':   a.get('size', 0),
                'url':       att_url,
                'thumb':     thumb_url,
                'eh_imagem': (a.get('mimeType', '')).startswith('image/'),
            })

        # Sprint
        sprint = None
        sp_raw = f.get('customfield_10020')
        if sp_raw and isinstance(sp_raw, list) and sp_raw:
            sprint = sp_raw[-1].get('name') if isinstance(sp_raw[-1], dict) else str(sp_raw[-1])

        # Issue links
        links = []
        for il in (f.get('issuelinks') or []):
            lt = il.get('type', {})
            if il.get('outwardIssue'):
                links.append({
                    'tipo': lt.get('outward', ''),
                    'key':  il['outwardIssue'].get('key'),
                    'titulo': (il['outwardIssue'].get('fields') or {}).get('summary', ''),
                    'status': ((il['outwardIssue'].get('fields') or {}).get('status') or {}).get('name', ''),
                })
            elif il.get('inwardIssue'):
                links.append({
                    'tipo': lt.get('inward', ''),
                    'key':  il['inwardIssue'].get('key'),
                    'titulo': (il['inwardIssue'].get('fields') or {}).get('summary', ''),
                    'status': ((il['inwardIssue'].get('fields') or {}).get('status') or {}).get('name', ''),
                })

        # Subtasks
        subtasks = []
        for st in (f.get('subtasks') or []):
            subtasks.append({
                'key':    st.get('key'),
                'titulo': (st.get('fields') or {}).get('summary', ''),
                'status': ((st.get('fields') or {}).get('status') or {}).get('name', ''),
            })

        return _jsonify({
            'key':         d.get('key'),
            'titulo':      f.get('summary', ''),
            'tipo':        (f.get('issuetype') or {}).get('name', ''),
            'status':      (f.get('status') or {}).get('name', ''),
            'resolucao':   (f.get('resolution') or {}).get('name', '') if f.get('resolution') else '',
            'prioridade':  (f.get('priority') or {}).get('name', ''),
            'responsavel': (f.get('assignee') or {}).get('displayName', '') or '—',
            'reporter':    (f.get('reporter') or {}).get('displayName', '') or '—',
            'criado_em':   (f.get('created') or '')[:16].replace('T', ' '),
            'atualizado':  (f.get('updated') or '')[:16].replace('T', ' '),
            'labels':      f.get('labels', []),
            'components':  [c.get('name') for c in (f.get('components') or [])],
            'fix_versions': [v.get('name') for v in (f.get('fixVersions') or [])],
            'sprint':      sprint,
            'story_points': f.get('customfield_10016'),
            'descricao':   _proxy_html(rf.get('description') or ''),
            'comentarios': comments,
            'anexos':      attachments,
            'links':       links,
            'subtasks':    subtasks,
            'url':         'https://prismadelphi.atlassian.net/browse/{0}'.format(d.get('key')),
        })
    except Exception as e:
        return _jsonify({'error': str(e)}, 500)


@app.route('/api/tarefas/<key>/img', methods=['GET'])
def tarefa_img_proxy(key):
    """Proxy legado — redireciona para /api/img."""
    return tarefa_img_proxy_global()


@app.route('/api/tarefas/<key>/analisar', methods=['POST'])
def tarefa_analisar(key):
    """Analisa issue do Jira com IA. SOMENTE LEITURA — zero escrita no Jira."""
    sess, err = _require_auth(request)
    if err: return err
    try:
        # Busca issue completa — GET apenas, nunca escreve
        url = (
            'https://prismadelphi.atlassian.net/rest/api/2/issue/{0}'
            '?expand=renderedFields'
            '&fields=summary,description,status,assignee,reporter,created,updated,'
            'comment,attachment,issuetype,priority,labels,components,fixVersions,'
            'issuelinks,subtasks,customfield_10020,customfield_10016,resolution'
        ).format(key)
        req = _ur.Request(url, headers={'Authorization': 'Basic ' + _JIRA_AUTH, 'Accept': 'application/json'})
        with _ur.urlopen(req, timeout=15) as resp:
            d = json.loads(resp.read())
        f  = d.get('fields', {})
        rf = d.get('renderedFields', {})

        # Monta texto estruturado da issue
        lines = []
        lines.append('Issue: {0} — {1}'.format(key, f.get('summary', '')))
        lines.append('Tipo: {0} | Status: {1} | Prioridade: {2}'.format(
            (f.get('issuetype') or {}).get('name', ''),
            (f.get('status') or {}).get('name', ''),
            (f.get('priority') or {}).get('name', ''),
        ))
        lines.append('Responsável: {0} | Reporter: {1} | Criado: {2} | Atualizado: {3}'.format(
            (f.get('assignee') or {}).get('displayName', '—'),
            (f.get('reporter') or {}).get('displayName', '—'),
            (f.get('created') or '')[:10],
            (f.get('updated') or '')[:10],
        ))
        labels = f.get('labels', [])
        if labels:
            lines.append('Labels: ' + ', '.join(labels))
        components = [c.get('name') for c in (f.get('components') or [])]
        if components:
            lines.append('Componentes: ' + ', '.join(components))
        sp_raw = f.get('customfield_10020')
        if sp_raw and isinstance(sp_raw, list) and sp_raw:
            sprint = sp_raw[-1].get('name') if isinstance(sp_raw[-1], dict) else str(sp_raw[-1])
            lines.append('Sprint: ' + sprint)

        desc = _strip_html(rf.get('description') or f.get('description') or '')
        if desc:
            lines.append('\nDESCRIÇÃO:\n' + desc[:2500])

        # Comentários (últimos 10, sem HTML)
        rf_comments = (rf.get('comment') or {}).get('comments', [])
        raw_comments = (f.get('comment') or {}).get('comments', [])
        if rf_comments:
            lines.append('\nCOMENTÁRIOS:')
            for i, rc in enumerate(rf_comments[-10:]):
                raw = raw_comments[i] if i < len(raw_comments) else {}
                autor = (raw.get('author') or {}).get('displayName', '?')
                corpo = _strip_html(rc.get('body', ''))[:400]
                if corpo:
                    lines.append('[{0}] {1}'.format(autor, corpo))

        # Issues relacionadas
        link_lines = []
        for il in (f.get('issuelinks') or []):
            lt = il.get('type', {})
            tgt = il.get('outwardIssue') or il.get('inwardIssue')
            rel = lt.get('outward' if il.get('outwardIssue') else 'inward', '')
            if tgt:
                link_lines.append('{0} {1}: {2}'.format(
                    rel, tgt.get('key', ''),
                    (tgt.get('fields') or {}).get('summary', '')
                ))
        if link_lines:
            lines.append('\nISSUES RELACIONADAS:\n' + '\n'.join(link_lines))

        # Subtarefas
        sub_lines = []
        for st in (f.get('subtasks') or []):
            sub_lines.append('{0}: {1} [{2}]'.format(
                st.get('key'), (st.get('fields') or {}).get('summary', ''),
                ((st.get('fields') or {}).get('status') or {}).get('name', '')
            ))
        if sub_lines:
            lines.append('\nSUBTAREFAS:\n' + '\n'.join(sub_lines))

        issue_text = '\n'.join(lines)

        # Baixa primeira imagem como base64 para análise visual (GET — somente leitura)
        import base64 as _b64_img
        image_b64 = None
        all_imgs = [a for a in (f.get('attachment') or []) if (a.get('mimeType', '')).startswith('image/')]
        if all_imgs:
            try:
                img_req = _ur.Request(all_imgs[0].get('content', ''), headers={
                    'Authorization': 'Basic ' + _JIRA_AUTH, 'User-Agent': 'Mozilla/5.0'
                })
                with _ur.urlopen(img_req, timeout=15) as resp:
                    image_b64 = _b64_img.b64encode(resp.read()).decode()
            except Exception:
                pass
            if len(all_imgs) > 1:
                issue_text += '\n\n[{0} imagens no total — apenas a primeira foi analisada visualmente]'.format(len(all_imgs))

        from ai.client import ask
        system_prompt = (
            'Você é um analista técnico sênior da Prismafive que analisa issues do Jira do sistema FarmaFácil. '
            'Analise a issue a seguir e forneça um resumo claro e objetivo em português brasileiro.\n\n'
            'Sua análise deve cobrir:\n'
            '1. O que está sendo pedido ou corrigido (resumo direto)\n'
            '2. Impacto para o usuário final e urgência\n'
            '3. Pontos de atenção ou dependências identificadas\n'
            '4. Se houver imagem anexada, descreva o que ela mostra e como se relaciona com a issue\n'
            '5. Próximos passos recomendados\n\n'
            'Seja direto e técnico. Evite repetir informações óbvias da issue.'
        )
        resposta = _strip_bold(ask(system_prompt, [{'role': 'user', 'content': issue_text}], image_base64=image_b64))

        return _jsonify({
            'resposta':    resposta,
            'issue_text':  issue_text,
            'key':         key,
            'titulo':      f.get('summary', ''),
            'tem_imagem':  image_b64 is not None,
        })
    except Exception as e:
        return _jsonify({'error': str(e)}, 500)


@app.route('/api/img', methods=['GET'])
def tarefa_img_proxy_global():
    """Proxy para imagens/anexos do Jira — sem token Bearer (usado por <img> tags)."""
    from flask import Response
    img_url = request.args.get('url', '')
    if not img_url or 'atlassian.net' not in img_url:
        return _jsonify({'error': 'URL inválida'}, 400)
    try:
        req = _ur.Request(img_url, headers={
            'Authorization': 'Basic ' + _JIRA_AUTH,
            'User-Agent': 'Mozilla/5.0',
        })
        with _ur.urlopen(req, timeout=15) as resp:
            content_type = resp.headers.get('Content-Type', 'application/octet-stream')
            data = resp.read()
        return Response(data, content_type=content_type)
    except Exception as e:
        return Response(b'', status=404)


# ── Provedores NFS-e ──────────────────────────────────────────────────────────

import unicodedata as _unicodedata

_ACBR_INI_URL = 'https://raw.githubusercontent.com/MirrorProjetoACBr/ACBr/master/Fontes/ACBrDFe/ACBrNFSeX/ACBrNFSeXServicos.ini'

_ini_cache      = {'data': None, 'ts': 0.0}
_ini_cache_lock = _threading.Lock()
_INI_CACHE_TTL  = 86400  # 24h


def _norm_mun(nome):
    """Normaliza nome de município para comparação: remove acentos, apóstrofe, hífen, lowercase."""
    n = _unicodedata.normalize('NFKD', nome or '')
    n = ''.join(c for c in n if not _unicodedata.combining(c))
    n = n.lower()
    n = re.sub(r"['\-]", ' ', n)
    n = re.sub(r'\s+', ' ', n).strip()
    return n


def _fetch_acbr_ini():
    """Baixa e parseia o INI do ACBr. Chave: nome_normalizado (sem UF, para máximo match)."""
    req = _ur.Request(_ACBR_INI_URL, headers={'User-Agent': 'FarmaFacil-Assistente/1.0'})
    with _ur.urlopen(req, timeout=30) as resp:
        raw = resp.read().decode('utf-8', errors='ignore')
    municipios = {}  # nome_norm → {nome, uf, provedor}
    current = {}
    for line in raw.splitlines():
        line = line.strip()
        if line.startswith('[') and line.endswith(']'):
            if current.get('provedor') and current.get('nome'):
                key = _norm_mun(current['nome'])
                municipios.setdefault(key, current)  # primeiro encontrado ganha
            current = {}
        elif '=' in line:
            k, _, v = line.partition('=')
            k = k.strip().lower()
            v = v.strip()
            if k in ('nome', 'uf', 'provedor'):
                current[k] = v
    if current.get('provedor') and current.get('nome'):
        key = _norm_mun(current['nome'])
        municipios.setdefault(key, current)
    return municipios


def _get_acbr_ini_cached():
    with _ini_cache_lock:
        if _ini_cache['data'] is not None and _time_mod.time() - _ini_cache['ts'] < _INI_CACHE_TTL:
            return _ini_cache['data']
    try:
        data = _fetch_acbr_ini()
        with _ini_cache_lock:
            _ini_cache['data'] = data
            _ini_cache['ts']   = _time_mod.time()
        return data
    except Exception:
        with _ini_cache_lock:
            return _ini_cache['data'] or {}


_NFSE_KW_TICKETS = (
    'nfse', 'nfs-e', 'nfs e', 'nf-se', 'nf se',
    'nota fiscal de servi', 'nota de servi',
    'nota servico', 'nota serviço',
    'prefeitura', 'rps ', ' rps',
    'danfse', 'dan-fse',
    'emissao de nota', 'emissão de nota', 'emitir nota',
    'lote nfs', 'webiss', 'ginfes',
)

def _get_farmacias_do_cache():
    """
    Lê o cache local de tickets e retorna todos os clientes únicos com cidade.
    O cruzamento com o INI do ACBr determina quem realmente usa NFS-e
    (se o município tem provedor configurado, a farmácia usa NFS-e).
    Retorna (lista_clientes, total_clientes).
    """
    try:
        cache_path = os.path.join(_ROOT, 'movidesk_tickets.json')
        if not os.path.exists(cache_path):
            return [], 0
        with open(cache_path, encoding='utf-8') as _f:
            _data = json.load(_f)
        tickets = _data.get('tickets', {})
        seen = {}  # nome_upper → {nome, municipio}
        for t in (tickets.values() if isinstance(tickets, dict) else tickets):
            nome = (t.get('client_name') or '').strip()
            city = (t.get('client_city') or '').strip()
            if not nome or not city:
                continue
            key = nome.upper()
            if key not in seen:
                seen[key] = {'nome': nome, 'municipio': city}
        total = len(seen)
        return list(seen.values()), total
    except Exception:
        return [], 0


def _match_municipio_ini(city, municipios_ini):
    """Retorna o dict do município no INI pelo nome normalizado, ou None."""
    return municipios_ini.get(_norm_mun(city))


_PRIORIDADES_ALTAS = {'highest', 'high', 'blocker', 'crítico', 'critico', 'alta', 'alto'}

_NFSE_KW = (
    'nfse', 'nfs-e', 'nfs e', 'nf-se', 'nf se',
    'nota fiscal de servi', 'nota de servi', 'nota servico', 'nota serviço',
    'emissão de nota', 'emissao de nota', 'emissor de nota',
    'prefeitura', 'provedor nfs', 'webservice nfs', 'lote nfs',
)

def _is_nfse_issue(issue):
    texto = ' '.join([
        issue.get('titulo', ''),
        issue.get('desc_text', ''),
        issue.get('comment_text', ''),
    ]).lower()
    return any(kw in texto for kw in _NFSE_KW)

def _provedor_in_issue(prov_nome, issue):
    texto = ' '.join([
        issue.get('titulo', ''),
        issue.get('desc_text', ''),
        issue.get('comment_text', ''),
        issue.get('components', ''),
        ' '.join(issue.get('labels', [])),
    ])
    return bool(re.search(r'\b' + re.escape(prov_nome) + r'\b', texto, re.IGNORECASE))


@app.route('/api/provedor/status', methods=['GET'])
def provedor_status():
    sess, err = _require_auth(request)
    if err: return err
    try:
        municipios_ini          = _get_acbr_ini_cached()
        farmacias_mv, total_mv  = _get_farmacias_do_cache()
        jira_issues             = _get_jira_issues_cached()

        issues_abertas = [i for i in jira_issues if i.get('status_cat', '') != 'done']

        # Mapeia farmácias ao provedor via município
        farmacias_por_provedor = {}
        for farm in farmacias_mv:
            city = farm['municipio']
            mun  = _match_municipio_ini(city, municipios_ini)
            if not mun:
                continue
            prov = mun.get('provedor', '').strip()
            if not prov:
                continue
            farmacias_por_provedor.setdefault(prov, []).append({
                'nome':      farm['nome'],
                'municipio': city,
                'uf':        mun.get('uf', ''),
            })

        # Provedores únicos que têm pelo menos uma farmácia nossa
        provedores_com_farm = sorted(farmacias_por_provedor.keys())

        resultado = []
        for prov_nome in provedores_com_farm:
            farmacias = farmacias_por_provedor[prov_nome]
            # Farmácias únicas (evita duplicatas do mesmo cliente com vários tickets)
            seen_nomes = set()
            farmacias_unicas = []
            for f in farmacias:
                if f['nome'].upper() not in seen_nomes:
                    seen_nomes.add(f['nome'].upper())
                    farmacias_unicas.append(f)

            issues_prov = [
                i for i in issues_abertas
                if _provedor_in_issue(prov_nome, i)
            ]

            if issues_prov:
                tem_critico = any(i.get('prioridade', '').lower() in _PRIORIDADES_ALTAS for i in issues_prov)
                status = 'critico' if tem_critico else 'alerta'
            else:
                status = 'ok'

            total_mun = sum(
                1 for m in municipios_ini.values()
                if m.get('provedor', '').strip() == prov_nome
            )

            resultado.append({
                'nome':             prov_nome,
                'status':           status,
                'issues':           [{
                    'key':         i['key'],
                    'titulo':      i['titulo'],
                    'status':      i['status'],
                    'prioridade':  i.get('prioridade', ''),
                    'tipo':        i.get('tipo', ''),
                    'responsavel': i.get('responsavel', ''),
                    'atualizado':  i.get('atualizado', ''),
                } for i in issues_prov],
                'farmacias':        farmacias_unicas,
                'total_municipios': total_mun,
            })

        _ORDER = {'critico': 0, 'alerta': 1, 'ok': 2}
        resultado.sort(key=lambda x: (_ORDER.get(x['status'], 2), x['nome']))

        com_alerta               = sum(1 for p in resultado if p['status'] != 'ok')
        farmacias_afetadas_total = sum(len(p['farmacias']) for p in resultado if p['status'] != 'ok')

        total_farmacias_nfse = sum(len(p['farmacias']) for p in resultado)

        return _jsonify({
            'provedores':               resultado,
            'total_provedores':         len(resultado),
            'com_alerta':               com_alerta,
            'farmacias_afetadas_total': farmacias_afetadas_total,
            'total_municipios_ini':     len(municipios_ini),
            'total_farmacias_nfse':     total_farmacias_nfse,
            'total_clientes_mv':        total_mv,
        })
    except Exception as e:
        import traceback
        return _jsonify({'error': str(e), 'trace': traceback.format_exc()}, 500)


@app.route('/api/provedor/atualizar-ini', methods=['POST'])
def provedor_atualizar_ini():
    """Invalida o cache do INI e força re-download imediato."""
    sess, err = _require_auth(request)
    if err: return err
    try:
        with _ini_cache_lock:
            _ini_cache['ts'] = 0.0
        data = _get_acbr_ini_cached()
        return _jsonify({'ok': True, 'total_municipios': len(data)})
    except Exception as e:
        return _jsonify({'error': str(e)}, 500)


@app.route('/api/provedor/atualizar-jira', methods=['POST'])
def provedor_atualizar_jira():
    """Invalida o cache de issues do Jira e força re-busca imediata."""
    sess, err = _require_auth(request)
    if err: return err
    try:
        with _jira_cache_lock:
            _jira_cache['ts'] = 0.0
        issues = _get_jira_issues_cached()
        return _jsonify({'ok': True, 'total_issues': len(issues)})
    except Exception as e:
        return _jsonify({'error': str(e)}, 500)


# ── TV Auto-login ─────────────────────────────────────────────────────────────

_TV_KEY = "tv-suporte-2026"

@app.route('/api/tv-login')
def tv_login():
    key = request.args.get('key', '')
    if key != _TV_KEY:
        return _jsonify({'error': 'Chave inválida'}, 401)
    token = _create_token('TV', is_admin=False, role='lideres', movidesk_name='')
    return _jsonify({'token': token, 'username': 'TV', 'role': 'lideres', 'is_admin': False})


# ── Painel TV — Metas Semanais & Desempenho por Equipe ───────────────────────

_PAINEL_ANALISTAS = [
    {"nome": "Vinicius",                       "display": "Vinicius",  "equipe": "Fiscal"},
    {"nome": "Rebeca medeiros",                "display": "Rebeca",    "equipe": "Fiscal"},
    {"nome": "Rubens Milton Destro Junior",    "display": "Rubens",    "equipe": "Fiscal"},
    {"nome": "Matheus Miranda de Lima Araujo", "display": "Matheus",   "equipe": "Producao"},
    {"nome": "Boeira",                         "display": "Boeira",    "equipe": "Producao"},
    {"nome": "Isaac Santos",                   "display": "Isaac",     "equipe": "Producao"},
    {"nome": "Raul Neto",                      "display": "Raul",      "equipe": "Producao"},
    {"nome": "Ruam Pereira de Sá",             "display": "Ruam",      "equipe": "Producao"},
    {"nome": "Alan vieira",                    "display": "Alan",      "equipe": "G1"},
    {"nome": "Marcello Filho",                 "display": "Marcello",  "equipe": "G1"},
    {"nome": "Keven Silva dos Santos",         "display": "Keven",     "equipe": "G1"},
    {"nome": "Nathan Lopes",                   "display": "Nathan",    "equipe": "GW"},
]

_PAINEL_EQUIPES = {
    "Fiscal":   {"nome": "Fiscal",   "cor": "#F59E0B"},
    "Producao": {"nome": "Produção", "cor": "#10B981"},
    "G1":       {"nome": "G1",       "cor": "#8B5CF6"},
    "GW":       {"nome": "GW",       "cor": "#EC4899"},
}

_painel_cache = {"data": None, "ts": 0.0}
_painel_lock  = threading.Lock()
_PAINEL_TTL   = 120  # 2 minutos


def _painel_match(owner_name, lookup):
    """Match case-insensitive do nome do analista no Movidesk. Exact first, partial fallback."""
    if not owner_name:
        return None
    ol = owner_name.lower().strip()
    if ol in lookup:
        return ol
    for key in lookup:
        if len(key) >= 4 and (key in ol or ol in key):
            return key
    return None


@app.route('/api/painel/semanal')
def painel_semanal():
    sess, err = _require_auth(request)
    if err:
        return err
    role = sess.get('role', '')
    if role not in ('lideres', 'administrador') and not sess.get('is_admin'):
        return _jsonify({'error': 'Acesso negado'}, 403)

    import time as _t
    now = _t.time()
    with _painel_lock:
        if _painel_cache["data"] and now - _painel_cache["ts"] < _PAINEL_TTL:
            return _jsonify(_painel_cache["data"])

    try:
        from utils.movidesk_client import fetch_tickets_page, fetch_resolved_page
        from datetime import timedelta as _td

        today  = datetime.datetime.now()
        monday = today - _td(days=today.weekday())
        friday = monday + _td(days=4)
        monday_str = monday.strftime("%Y-%m-%d")
        friday_str = friday.strftime("%Y-%m-%d")
        lookup = {}
        for a in _PAINEL_ANALISTAS:
            lookup[a["nome"].lower()] = {
                "nome":     a["nome"],
                "display":  a["display"],
                "equipe":   a["equipe"],
                "entrados": 0,
                "fechados": 0,
            }

        top = 100

        # Tickets entrados (criados na semana Mon-Fri)
        skip = 0
        while True:
            page = fetch_tickets_page(skip=skip, top=top,
                                      since_date=monday_str, until_date=friday_str)
            if not page:
                break
            for t in page:
                owner = ((t.get("owner") or {}).get("businessName") or "").strip()
                key = _painel_match(owner, lookup)
                if key:
                    lookup[key]["entrados"] += 1
            if len(page) < top:
                break
            skip += top

        # Tickets resolvidos na semana
        skip = 0
        while True:
            page = fetch_resolved_page(skip=skip, top=top,
                                       since_date=monday_str, until_date=friday_str)
            if not page:
                break
            for t in page:
                owner = ((t.get("owner") or {}).get("businessName") or "").strip()
                key = _painel_match(owner, lookup)
                if key:
                    lookup[key]["fechados"] += 1
            if len(page) < top:
                break
            skip += top

        for a in lookup.values():
            a["saldo"] = a["fechados"] - a["entrados"]

        analistas = sorted(lookup.values(), key=lambda x: x["saldo"], reverse=True)

        equipes = []
        for eq_key, eq_meta in _PAINEL_EQUIPES.items():
            membros = [a for a in analistas if a["equipe"] == eq_key]
            total_e = sum(m["entrados"] for m in membros)
            total_f = sum(m["fechados"] for m in membros)
            saldo_eq = total_f - total_e
            equipes.append({
                "chave":          eq_key,
                "nome":           eq_meta["nome"],
                "cor":            eq_meta["cor"],
                "analistas":      len(membros),
                "entrados":       total_e,
                "fechados":       total_f,
                "saldo":          saldo_eq,
                "taxa_resolucao": round(total_f / total_e * 100, 1) if total_e > 0 else 0,
            })

        total_e = sum(a["entrados"] for a in analistas)
        total_f = sum(a["fechados"] for a in analistas)

        result = {
            "semana_inicio": monday_str,
            "semana_fim":    friday_str,
            "analistas":     analistas,
            "equipes":       equipes,
            "totais": {
                "entrados": total_e,
                "fechados": total_f,
                "saldo":    total_f - total_e,
            },
            "updated_at": datetime.datetime.now().strftime("%H:%M"),
        }

        with _painel_lock:
            _painel_cache["data"] = result
            _painel_cache["ts"]   = now

        return _jsonify(result)

    except Exception as e:
        return _jsonify({"error": str(e)}, 500)


@app.route('/api/painel/reset-cache', methods=['POST'])
def painel_reset_cache():
    sess, err = _require_auth(request)
    if err:
        return err
    role = sess.get('role', '')
    if role not in ('lideres', 'administrador') and not sess.get('is_admin'):
        return _jsonify({'error': 'Acesso negado'}, 403)
    with _painel_lock:
        _painel_cache["ts"] = 0.0
    return _jsonify({"ok": True})


# ── Painel TV standalone ──────────────────────────────────────────────────────

@app.route('/tv')
def tv_page():
    tv_path = os.path.join(_ROOT, 'tv.html')
    if os.path.exists(tv_path):
        with open(tv_path, encoding='utf-8') as f:
            return f.read(), 200, {'Content-Type': 'text/html; charset=utf-8'}
    return _jsonify({'error': 'tv.html não encontrado'}, 404)


# ── Servir frontend React (modo navegador) ────────────────────────────────────

# Procura o frontend/dist em varios locais possiveis
def _find_dist():
    candidatos = [
        # Ao lado do exe (modo servidor standalone)
        os.path.join(os.path.dirname(sys.executable), 'frontend', 'dist'),
        # Pasta pai do exe
        os.path.join(os.path.dirname(os.path.dirname(sys.executable)), 'frontend', 'dist'),
        # Relativo ao script Python (modo desenvolvimento)
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'dist'),
        # _ROOT (PyInstaller)
        os.path.join(_ROOT, 'frontend', 'dist'),
    ]
    for c in candidatos:
        if os.path.exists(os.path.join(c, 'index.html')):
            return c
    return candidatos[0]  # fallback

_DIST = _find_dist()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    if path and os.path.exists(os.path.join(_DIST, path)):
        return send_from_directory(_DIST, path)
    index = os.path.join(_DIST, 'index.html')
    if os.path.exists(index):
        return send_from_directory(_DIST, 'index.html')
    return _jsonify({'error': 'Frontend não encontrado. Execute npm run build primeiro.'}, 404)

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    port = 5000
    url  = 'http://localhost:{0}'.format(port)

    print('')
    print('  FarmaFacil Assistente — Backend iniciando...')
    print('  Acesse: {0}'.format(url))
    print('')

    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
