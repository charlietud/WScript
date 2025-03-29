import ctypes
from typing import Optional

class AdminCheck:
    @staticmethod
    def is_admin() -> bool:
        """
        Check if the current process has administrator privileges.
        
        Returns:
            bool: True if running with admin rights, False otherwise
        """
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    @staticmethod
    def require_admin(func):
        """
        Decorator to ensure a function runs with administrator privileges.
        
        Args:
            func: The function to decorate
            
        Returns:
            The decorated function
            
        Raises:
            PermissionError: If the function is called without admin rights
        """
        def wrapper(*args, **kwargs):
            if not AdminCheck.is_admin():
                raise PermissionError("This function requires administrator privileges")
            return func(*args, **kwargs)
        return wrapper 