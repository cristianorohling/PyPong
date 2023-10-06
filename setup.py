import cx_Freeze

exe = [cx_Freeze.Executable("PyPong.py", base = "Win32GUI")] # <-- HERE

cx_Freeze.setup(
    name = "Pong.Py",
    version = "1.0",
    options = {"build_exe": {"packages": ["pygame", "random"],  
        "include_files": ["error.wav", "intro.wav", "pop.wav", "popwall.wav", "AtariSmall.ttf"]}},
    executables = exe
) 