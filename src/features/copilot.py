import winreg

class CopilotManager:
    def __init__(self):
        self.path = r"Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32"

    def disable_copilot(self):
        try:
            key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, self.path, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, "DisableCopilot", 0, winreg.REG_DWORD, 1) #Set value 1
            winreg.CloseKey(key)
            print("Successfully disabled Copilot.")
        except WindowsError as e:
            print(f"Failed to disable Copilot: {str(e)}.")