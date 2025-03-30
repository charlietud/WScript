import subprocess
from ..core.admin_check import AdminCheck
from ..core.registry_manager import RegistryManager
from ..core.service_manager import ServiceManager

class CortanaManager:
    def __init__(self):
        self.is_admin = AdminCheck.is_admin()
        self.registry = RegistryManager()
        self.service = ServiceManager()
    
    def disable_cortana_registry(self) -> bool:
        """
        Disable only safe Cortana features through registry modifications.
        Returns True if successful, False otherwise.
        """
        # Only modify safe registry paths that don't affect core Windows functionality
        paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\SearchSettings"
        ]
        
        # Only disable personal assistant features, not core search functionality
        values = {
            "CortanaConsent": 0,
            "CortanaEnabled": 0,
            "AllowCortana": 0
        }
        
        success = True
        for path in paths:
            if not self.registry.set_multiple_values(path, values):
                success = False
                break
        
        return success
    
    def disable_cortana_service(self) -> bool:
        """
        Disable the Cortana service.
        Returns True if successful, False otherwise.
        """
        return self.service.stop_and_disable_service("Cortana")
    
    def disable_cortana_tasks(self) -> bool:
        """
        Disable only Cortana-specific scheduled tasks that don't affect core Windows functionality.
        Returns True if successful, False otherwise.
        """
        # Only disable Cortana-specific tasks, not Windows Search tasks
        tasks = [
            r"Microsoft\Windows\Windows Search\CortanaConsent"
        ]
        
        success = True
        for task in tasks:
            try:
                subprocess.run(["schtasks", "/change", "/tn", task, "/disable"], check=True)
                print(f"Successfully disabled task: {task}")
            except subprocess.CalledProcessError as e:
                print(f"Error disabling task {task}: {str(e)}")
                success = False
                break
        
        return success
    
    def disable_all_cortana(self) -> bool:
        """
        Disable only safe Cortana features using all available methods.
        Returns True if all operations were successful, False otherwise.
        """
        if not self.is_admin:
            print("This script requires administrator privileges to run properly.")
            return False
        
        print("Warning: This will only disable Cortana personal assistant features.")
        print("Core Windows Search functionality will remain intact.")
        
        results = {
            "Registry": self.disable_cortana_registry(),
            "Tasks": self.disable_cortana_tasks()
        }
        
        success = all(results.values())
        if success:
            print("\nSuccessfully disabled Cortana personal assistant features!")
            print("Note: Core Windows Search functionality remains active.")
        else:
            print("\nSome operations failed. Check the error messages above.")
        
        return success 