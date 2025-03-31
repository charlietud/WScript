import winreg

class ContextMenuManager:
    def __init__(self):
        self.path = r"Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32"

    def create_old_context_menu_key(self):
        """
        Create the registry key to activate the older Windows 10 context menu.
        """
        try:
            # Create the registry key
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, self.path)
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "")  # Set default value to an empty string
            winreg.CloseKey(key)
            print(f"Successfully created registry key: {self.path}")
        except WindowsError as e:
            print(f"Failed to create registry key {self.path}: {str(e)}")

    def check_key_exists(self):
        """
        Check if the context menu registry key exists.
        """
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.path)
            winreg.CloseKey(key)
            return True
        except WindowsError:
            return False
