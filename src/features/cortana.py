import subprocess
import winreg
from ..core.admin_check import AdminCheck
from ..core.registry_manager import RegistryManager
from ..core.service_manager import ServiceManager
from ..core.log_manager import LogManager

class CortanaManager:
    def __init__(self):
        self.is_admin = AdminCheck.is_admin()
        self.registry = RegistryManager()
        self.service = ServiceManager()
        self.log_manager = LogManager()
        self.logger = self.log_manager.get_logger('Cortana')
    
    def check_registry_key_exists(self, path: str) -> bool:
        """
        Check if a registry key exists.
        
        Args:
            path: The registry key path to check
            
        Returns:
            bool: True if the key exists, False otherwise
        """
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
            winreg.CloseKey(key)
            return True
        except WindowsError:
            return False
    
    def create_registry_key(self, path: str) -> bool:
        """
        Create a registry key if it doesn't exist.
        
        Args:
            path: The registry key path to create
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_WRITE)
            winreg.CloseKey(key)
            return True
        except WindowsError as e:
            self.logger.error(f"Failed to create registry key {path}: {str(e)}")
            return False
    
    def disable_cortana_registry(self) -> bool:
        """
        Disable only safe Cortana features through registry modifications.
        Returns True if successful, False otherwise.
        """
        # Registry paths for Cortana settings
        paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Search",
            r"SOFTWARE\Policies\Microsoft\Windows\Windows Search",
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Search\Flighting",
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Search\Flighting\0",
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Search\Flighting\1"
        ]
        
        # Values to set
        values = {
            "AllowCortana": 0,
            "CortanaEnabled": 0,
            "DisableWebSearch": 1,
            "BingSearchEnabled": 0
        }
        
        success = True
        for path in paths:
            self.logger.info(f"Checking registry path: {path}")
            
            # Check if key exists
            if not self.check_registry_key_exists(path):
                self.logger.info(f"Registry key does not exist: {path}")
                if not self.create_registry_key(path):
                    self.logger.error(f"Failed to create registry key: {path}")
                    success = False
                    continue
            
            # Set values
            self.logger.info(f"Setting values in registry path: {path}")
            if not self.registry.set_multiple_values(path, values):
                self.log_manager.log_registry_change(self.logger, path, values, False)
                success = False
                break
            else:
                self.log_manager.log_registry_change(self.logger, path, values, True)
        
        return success
    
    def verify_cortana_state(self) -> bool:
        """
        Verify if Cortana is disabled by checking various indicators.
        Returns True if Cortana appears to be disabled, False otherwise.
        """
        self.logger.info("Verifying Cortana state")
        
        # Check if Cortana service is running
        try:
            result = subprocess.run(["sc", "query", "Cortana"], capture_output=True, text=True)
            service_running = "RUNNING" in result.stdout
            self.logger.info(f"Cortana service running: {service_running}")
        except subprocess.CalledProcessError:
            self.logger.error("Failed to check Cortana service state")
            service_running = False
        
        # Check if Cortana process is running
        try:
            result = subprocess.run(["tasklist", "/FI", "IMAGENAME eq SearchApp.exe"], capture_output=True, text=True)
            process_running = "SearchApp.exe" in result.stdout
            self.logger.info(f"Cortana process running: {process_running}")
        except subprocess.CalledProcessError:
            self.logger.error("Failed to check Cortana process state")
            process_running = False
        
        # Check registry values
        registry_disabled = True
        for path in [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Search",
            r"SOFTWARE\Policies\Microsoft\Windows\Windows Search"
        ]:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
                for value_name in ["AllowCortana", "CortanaEnabled"]:
                    try:
                        value, _ = winreg.QueryValueEx(key, value_name)
                        if value != 0:
                            registry_disabled = False
                            self.logger.info(f"Registry value {value_name} in {path} is not disabled")
                    except WindowsError:
                        self.logger.info(f"Registry value {value_name} not found in {path}")
                winreg.CloseKey(key)
            except WindowsError:
                self.logger.info(f"Registry key {path} not found")
        
        self.logger.info(f"Registry appears disabled: {registry_disabled}")
        
        # Consider Cortana disabled if service and process are not running and registry values are set correctly
        return not service_running and not process_running and registry_disabled
    
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
                self.log_manager.log_task_change(self.logger, task, "disable", True)
            except subprocess.CalledProcessError as e:
                self.log_manager.log_task_change(self.logger, task, "disable", False)
                success = False
                break
        
        return success
    
    def disable_all_cortana(self) -> bool:
        """
        Disable only safe Cortana features using all available methods.
        Returns True if all operations were successful, False otherwise.
        """
        self.logger.info("Starting Cortana disable process")
        
        if not self.is_admin:
            self.logger.error("Script requires administrator privileges")
            print("This script requires administrator privileges to run properly.")
            return False
        
        # Check current state
        current_state = self.verify_cortana_state()
        self.logger.info(f"Current Cortana state: {'Disabled' if current_state else 'Enabled'}")
        
        self.logger.info("Warning: This will only disable Cortana personal assistant features")
        self.logger.info("Core Windows Search functionality will remain intact")
        print("Warning: This will only disable Cortana personal assistant features.")
        print("Core Windows Search functionality will remain intact.")
        
        results = {
            "Registry": self.disable_cortana_registry(),
            "Tasks": self.disable_cortana_tasks()
        }
        
        success = all(results.values())
        if success:
            # Verify changes
            new_state = self.verify_cortana_state()
            if new_state:
                self.log_manager.log_operation(self.logger, "Cortana disable", "success", "All features disabled successfully")
                print("\nSuccessfully disabled Cortana personal assistant features!")
                print("Note: Core Windows Search functionality remains active.")
            else:
                self.log_manager.log_operation(self.logger, "Cortana disable", "warning", "Changes applied but verification failed")
                print("\nChanges applied but some features may still be active.")
                print("Please check the logs for details.")
        else:
            self.log_manager.log_operation(self.logger, "Cortana disable", "error", "Some operations failed")
            print("\nSome operations failed. Check the error messages above.")
        
        return success 