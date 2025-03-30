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
        Disable Cortana through registry modifications.
        Returns True if successful, False otherwise.
        """
        # Registry path for Cortana settings
        path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Search"
        
        # Values to set
        values = {
            "AllowCortana": 0,
            "CortanaEnabled": 0,
            "DisableWebSearch": 1,
            "BingSearchEnabled": 0
        }
        
        self.logger.info(f"Checking registry path: {path}")
        
        # Check if key exists
        if not self.check_registry_key_exists(path):
            self.logger.info(f"Registry key does not exist: {path}")
            if not self.create_registry_key(path):
                self.logger.error(f"Failed to create registry key: {path}")
                return False
        
        # Set values
        self.logger.info(f"Setting values in registry path: {path}")
        if not self.registry.set_multiple_values(path, values):
            self.log_manager.log_registry_change(self.logger, path, values, False)
            return False
        else:
            self.log_manager.log_registry_change(self.logger, path, values, True)
            return True
    
    def verify_cortana_state(self) -> bool:
        """
        Verify if Cortana is disabled by checking registry values.
        Returns True if Cortana appears to be disabled, False otherwise.
        """
        self.logger.info("Verifying Cortana state")
        
        # Check registry values
        path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Search"
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
            for value_name in ["AllowCortana", "CortanaEnabled"]:
                try:
                    value, _ = winreg.QueryValueEx(key, value_name)
                    if value != 0:
                        self.logger.info(f"Registry value {value_name} is not disabled")
                        winreg.CloseKey(key)
                        return False
                except WindowsError:
                    self.logger.info(f"Registry value {value_name} not found")
            winreg.CloseKey(key)
            self.logger.info("Cortana appears to be disabled")
            return True
        except WindowsError:
            self.logger.info("Registry key not found")
            return True  # Consider it disabled if the key doesn't exist
    
    def disable_cortana_service(self) -> bool:
        """
        Disable only the Cortana service while keeping Windows Search service intact.
        Returns True if successful, False otherwise.
        """
        # Only disable Cortana service, not Windows Search service
        service_name = "Cortana"
        
        try:
            # First check if the service exists
            result = subprocess.run(["sc", "query", service_name], capture_output=True, text=True)
            if "The specified service does not exist" in result.stdout:
                self.logger.info(f"Service {service_name} does not exist - skipping service disable")
                return True  # Consider this a success since Cortana is effectively disabled
            
            # If service exists, try to stop it
            subprocess.run(["sc", "stop", service_name], check=True)
            self.logger.info(f"Stopped {service_name} service")
            
            # Then disable it
            subprocess.run(["sc", "config", service_name, "start=disabled"], check=True)
            self.logger.info(f"Disabled {service_name} service")
            
            self.log_manager.log_service_change(self.logger, service_name, "disable", True)
            return True
        except subprocess.CalledProcessError as e:
            self.log_manager.log_service_change(self.logger, service_name, "disable", False)
            return False
    
    def disable_all_cortana(self) -> bool:
        """
        Disable Cortana through registry modifications.
        Returns True if successful, False otherwise.
        """
        self.logger.info("Starting Cortana disable process")
        
        if not self.is_admin:
            self.logger.error("Script requires administrator privileges")
            print("This script requires administrator privileges to run properly.")
            return False
        
        # Check current state
        current_state = self.verify_cortana_state()
        self.logger.info(f"Current Cortana state: {'Disabled' if current_state else 'Enabled'}")
        
        self.logger.info("Warning: This will disable Cortana personal assistant features")
        self.logger.info("Core Windows Search functionality will remain intact")
        print("Warning: This will disable Cortana personal assistant features.")
        print("Core Windows Search functionality will remain intact.")
        
        # Perform registry operation
        success = self.disable_cortana_registry()
        
        if success:
            # Verify changes
            new_state = self.verify_cortana_state()
            if new_state:
                self.log_manager.log_operation(self.logger, "Cortana disable", "success", "Cortana disabled successfully")
                print("\nSuccessfully disabled Cortana personal assistant features!")
                print("Note: Core Windows Search functionality remains active.")
            else:
                self.log_manager.log_operation(self.logger, "Cortana disable", "warning", "Changes applied but verification failed")
                print("\nChanges applied but some features may still be active.")
                print("Please check the logs for details.")
        else:
            self.log_manager.log_operation(self.logger, "Cortana disable", "error", "Failed to disable Cortana")
            print("\nFailed to disable Cortana. Check the error messages above.")
        
        return success 