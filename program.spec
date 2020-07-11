# -*- mode: python ; coding: utf-8 -*-

block_cipher = None
add_files=[("ico\\icon.png","."),("ico\\image1.jpg","."),("ico\\image2.jpg","."),("ico\\image3.jpg","."),("ico\\image4.jpg","."),("ico\\image5.jpg","."),("ico\\image6.jpg",".")]

a = Analysis(['program.py'],
             pathex=['D:\\美少女俄罗斯方块'],
             binaries=[],
             datas=add_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='program',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='ico\\icon.ico')
