# build.spec — PyInstaller
# Gera: FarmaFacilAssistente.exe (arquivo unico, sem instalacao)
# Uso: pyinstaller build.spec

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('farmafacil_knowledge.md', '.'),
        ('users.json',        '.') if __import__('os').path.exists('users.json') else ('','.'),
    ],
    hiddenimports=[
        'psycopg2',
        'psycopg2.extras',
        'psycopg2._psycopg',
        'PIL._tkinter_finder',
        'PIL.ImageGrab',
        'openai',
        'tkinter',
        'tkinter.ttk',
        'tkinter.scrolledtext',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'json',
        'hashlib',
        'threading',
        're',
        'base64',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=['asyncio', 'pathlib', 'anthropic'],
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
    name='FarmaFacilAssistente',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,          # Sem janela de console (GUI puro)
    icon=None,
    onefile=True,
)
