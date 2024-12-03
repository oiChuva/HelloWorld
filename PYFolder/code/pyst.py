from PyInstaller.__main__ import run

# Analysis step
a = Analysis(
    ['RequisiçãoEstoqueV1.4alt.py'],
    pathex=[],
    binaries=[],
    datas=[('logojan.ico', '.')],  # Adds the window icon to the data
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

# Compile the Python files into an executable
pyz = PYZ(a.pure)

# Create the executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='RequisiçãoEstoqueV1.4alt',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Do not open a console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='Logo-01.ico',  # Set the icon of the executable
)

run(['RequisiçãoEstoqueV1.4alt.py', '--onefile', '--icon=Logo-01.ico'])
