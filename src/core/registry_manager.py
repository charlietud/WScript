import winreg
from typing import Dict, List, Union, Optional

class RegistryManager:
    @staticmethod
    def set_registry_value(
        key_path: str,
        value_name: str,
        value: Union[int, str],
        value_type: int = winreg.REG_DWORD
    ) -> bool:
        """
        Set a registry value.
        
        Args:
            key_path: The registry key path
            value_name: The name of the value to set
            value: The value to set
            value_type: The type of the value (default: REG_DWORD)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, value_name, 0, value_type, value)
            winreg.CloseKey(key)
            return True
        except WindowsError as e:
            print(f"Error setting registry value {value_name} in {key_path}: {str(e)}")
            return False
    
    @staticmethod
    def set_multiple_values(
        key_path: str,
        values: Dict[str, Union[int, str]],
        value_type: int = winreg.REG_DWORD
    ) -> bool:
        """
        Set multiple registry values at once.
        
        Args:
            key_path: The registry key path
            values: Dictionary of value names and their values
            value_type: The type of the values (default: REG_DWORD)
            
        Returns:
            bool: True if all values were set successfully, False otherwise
        """
        try:
            key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE)
            for name, value in values.items():
                winreg.SetValueEx(key, name, 0, value_type, value)
            winreg.CloseKey(key)
            return True
        except WindowsError as e:
            print(f"Error setting multiple registry values in {key_path}: {str(e)}")
            return False
    
    @staticmethod
    def delete_value(key_path: str, value_name: str) -> bool:
        """
        Delete a registry value.
        
        Args:
            key_path: The registry key path
            value_name: The name of the value to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE)
            winreg.DeleteValue(key, value_name)
            winreg.CloseKey(key)
            return True
        except WindowsError as e:
            print(f"Error deleting registry value {value_name} in {key_path}: {str(e)}")
            return False 