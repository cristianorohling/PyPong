import cx_Freeze
import os

# Lista de arquivos para incluir na pasta do EXE
arquivos = [
    "intro.wav",
    "pop.wav", 
    "error.wav", 
    "popwall.wav", 
    "music.mp3",
    "Retro Gaming.ttf"  # <--- TEM QUE ESTAR ESCRITO EXATAMENTE IGUAL AO NOME DO ARQUIVO
]

# Configurações do executável
exe = [cx_Freeze.Executable(
    script="PyPong.py",       
    base="Win32GUI",          
    target_name="PyPong_Neo.exe",
    icon="PyPong.ico"  # <--- ADICIONE ESTA LINHA (com o nome exato do seu arquivo)
)]

cx_Freeze.setup(
    name = "PyPong Neo",
    version = "11.2",
    options = {
        "build_exe": {
            "packages": ["pygame", "json", "os", "sys", "random", "math"],
            "include_files": arquivos,
        }
    },
    executables = exe
)