# build_backend.spec — PyInstaller para o backend Flask do FarmaFacil Assistente
# Uso: pyinstaller build_backend.spec --distpath dist_backend
# Gera: dist_backend/backend.exe (Python + todas as dependencias embutidas)

import os
import sys
block_cipher = None

ROOT = os.path.abspath('.')

# Arquivos de dados a incluir
datas = [
    (os.path.join(ROOT, 'farmafacil_knowledge.md'), '.'),
    (os.path.join(ROOT, 'farmafacil_schema.md'),    '.'),
    (os.path.join(ROOT, 'users.json'),               '.'),
    (os.path.join(ROOT, 'ai'),                       'ai'),
    (os.path.join(ROOT, 'db'),                       'db'),
    (os.path.join(ROOT, 'utils'),                    'utils'),
]

# Inclui client_profile.json, connection.json e config.py se existirem
for f in ('client_profile.json', 'connection.json', 'config.py'):
    if os.path.exists(os.path.join(ROOT, f)):
        datas.append((os.path.join(ROOT, f), '.'))

# Inclui certifi (certificados SSL do httpx/openai)
try:
    import certifi
    datas.append((certifi.where(), 'certifi'))
except ImportError:
    pass

binaries = []

a = Analysis(
    [os.path.join(ROOT, 'backend', 'main.py')],
    pathex=[ROOT, os.path.join(ROOT, 'backend')],
    binaries=binaries,
    datas=datas,
    hiddenimports=[
        'utils.paths',
        # Flask e dependencias
        'flask',
        'flask.json',
        'flask.json.provider',
        'flask_cors',
        'werkzeug',
        'werkzeug.serving',
        'werkzeug.routing',
        'werkzeug.exceptions',
        'jinja2',
        'click',
        'itsdangerous',
        # PostgreSQL
        'psycopg2',
        'psycopg2.extras',
        'psycopg2._psycopg',
        # OpenAI SDK
        'openai',
        'openai._client',
        'openai._models',
        'openai._streaming',
        'openai._exceptions',
        'openai.resources',
        'openai.resources.chat',
        'openai.resources.chat.completions',
        'openai.types',
        'openai.types.chat',
        # HTTP stack
        'httpx',
        'httpcore',
        'httpcore._sync',
        'httpcore._async',
        'sniffio',
        'anyio',
        'anyio._backends._asyncio',
        'certifi',
        'h11',
        'h11._readers',
        'h11._writers',
        'h11._events',
        # Imagem
        'PIL',
        'PIL.ImageGrab',
        'PIL.Image',
        # Stdlib
        'json',
        'hashlib',
        'threading',
        're',
        'base64',
        'decimal',
        'datetime',
        'secrets',
        'pyautogui',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=['tkinter', 'tkinter.ttk', 'unittest', 'anthropic', 'cryptography'],
    noarchive=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='backend',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    onefile=True,
)
