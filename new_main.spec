# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:/Users/Equipo/Documents/Laboratorio/PyLife_Wolife/Wolife-Pygame/new_main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/Equipo/Documents/Laboratorio/PyLife_Wolife/Wolife-Pygame/data.py', '.'), ('C:/Users/Equipo/Documents/Laboratorio/PyLife_Wolife/Wolife-Pygame/debug.py', '.'), ('C:/Users/Equipo/Documents/Laboratorio/PyLife_Wolife/Wolife-Pygame/new_main.py', '.'), ('C:/Users/Equipo/Documents/Laboratorio/PyLife_Wolife/Wolife-Pygame/new_mapa.py', '.'), ('C:/Users/Equipo/Documents/Laboratorio/PyLife_Wolife/Wolife-Pygame/new_necesidad.py', '.'), ('C:/Users/Equipo/Documents/Laboratorio/PyLife_Wolife/Wolife-Pygame/new_wosim.py', '.'), ('C:/Users/Equipo/Documents/Laboratorio/PyLife_Wolife/Wolife-Pygame/requeriments.txt', '.'), ('C:/Users/Equipo/Documents/Laboratorio/PyLife_Wolife/Wolife-Pygame/settings.py', '.'), ('C:/Users/Equipo/Documents/Laboratorio/PyLife_Wolife/Wolife-Pygame/support.py', '.'), ('C:/Users/Equipo/Documents/Laboratorio/PyLife_Wolife/Wolife-Pygame/venv', 'venv/'), ('C:/Users/Equipo/Documents/Laboratorio/PyLife_Wolife/Wolife-Pygame/assets', 'assets/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='new_main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='new_main',
)
