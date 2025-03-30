import subprocess
from ..core.admin_check import AdminCheck
from ..core.registry_manager import RegistryManager
from ..core.service_manager import ServiceManager
from ..core.log_manager import LogManager

class TelemetryManager:
    def __init__(self):
        self.is_admin = AdminCheck.is_admin()
        self.registry = RegistryManager()
        self.service = ServiceManager()
        self.log_manager = LogManager()
        self.logger = self.log_manager.get_logger('Telemetry')
    
    def disable_telemetry_registry(self) -> bool:
        """
        Disable telemetry through registry modifications.
        Returns True if successful, False otherwise.
        """
        # Registry paths for telemetry settings
        paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Diagnostics\DiagTrack",
            r"SOFTWARE\Policies\Microsoft\Windows\DataCollection",
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection"
        ]
        
        # Values to set
        values = {
            "DiagTrackAuthorization": 1,
            "AllowTelemetry": 0,
            "MaxTelemetryAllowed": 0,
            "AllowDeviceNameInTelemetry": 0,
            "AllowTelemetryToBeSent": 0
        }
        
        success = True
        for path in paths:
            self.logger.info(f"Attempting to modify registry path: {path}")
            if not self.registry.set_multiple_values(path, values):
                self.log_manager.log_registry_change(self.logger, path, values, False)
                success = False
                break
            else:
                self.log_manager.log_registry_change(self.logger, path, values, True)
        
        return success
    
    def disable_telemetry_service(self) -> bool:
        """
        Disable the telemetry service.
        Returns True if successful, False otherwise.
        """
        service_name = "DiagTrack"
        success = self.service.stop_and_disable_service(service_name)
        self.log_manager.log_service_change(self.logger, service_name, "stop and disable", success)
        return success
    
    def task_exists(self, task_name: str) -> bool:
        """
        Check if a scheduled task exists.
        
        Args:
            task_name: The name of the task to check
            
        Returns:
            bool: True if the task exists, False otherwise
        """
        try:
            result = subprocess.run(
                ["schtasks", "/query", "/tn", task_name],
                capture_output=True,
                text=True
            )
            exists = result.returncode == 0
            self.logger.info(f"Task '{task_name}' exists: {exists}")
            return exists
        except subprocess.CalledProcessError:
            self.logger.error(f"Error checking task '{task_name}'")
            return False
    
    def disable_telemetry_tasks(self) -> bool:
        """
        Disable telemetry-related scheduled tasks.
        Returns True if successful, False otherwise.
        """
        tasks = [
            r"Microsoft\Windows\Application Experience\Microsoft Compatibility Appraiser",
            r"Microsoft\Windows\Application Experience\ProgramDataUpdater",
            r"Microsoft\Windows\Customer Experience Improvement Program\Consolidator",
            r"Microsoft\Windows\Customer Experience Improvement Program\UsbCeip",
            r"Microsoft\Windows\Customer Experience Improvement Program\KernelCeipTask"
        ]
        
        success = True
        for task in tasks:
            if self.task_exists(task):
                try:
                    subprocess.run(["schtasks", "/change", "/tn", task, "/disable"], check=True)
                    self.log_manager.log_task_change(self.logger, task, "disable", True)
                except subprocess.CalledProcessError as e:
                    self.log_manager.log_task_change(self.logger, task, "disable", False)
                    success = False
                    break
            else:
                self.logger.info(f"Task not found: {task}")
        
        return success
    
    def disable_all_telemetry(self) -> bool:
        """
        Disable all telemetry features using all available methods.
        Returns True if all operations were successful, False otherwise.
        """
        self.logger.info("Starting telemetry disable process")
        
        if not self.is_admin:
            self.logger.error("Script requires administrator privileges")
            print("This script requires administrator privileges to run properly.")
            return False
        
        results = {
            "Registry": self.disable_telemetry_registry(),
            "Service": self.disable_telemetry_service(),
            "Tasks": self.disable_telemetry_tasks()
        }
        
        success = all(results.values())
        if success:
            self.log_manager.log_operation(self.logger, "Telemetry disable", "success", "All telemetry features disabled successfully")
            print("\nSuccessfully disabled all telemetry features!")
        else:
            self.log_manager.log_operation(self.logger, "Telemetry disable", "error", "Some operations failed")
            print("\nSome operations failed. Check the error messages above.")
        
        return success 