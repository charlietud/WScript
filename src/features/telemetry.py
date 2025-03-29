import subprocess
from ..core.admin_check import AdminCheck
from ..core.registry_manager import RegistryManager
from ..core.service_manager import ServiceManager

class TelemetryManager:
    def __init__(self):
        self.is_admin = AdminCheck.is_admin()
        self.registry = RegistryManager()
        self.service = ServiceManager()
    
    def disable_telemetry_registry(self) -> bool:
        """
        Disable Windows telemetry through registry modifications.
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
            "AllowDeviceNameInTelemetry": 0,
            "AllowTelemetry": 0,
            "MaxTelemetryAllowed": 0
        }
        
        success = True
        for path in paths:
            if not self.registry.set_multiple_values(path, values):
                success = False
                break
        
        return success
    
    def disable_telemetry_service(self) -> bool:
        """
        Disable the Windows telemetry service (DiagTrack).
        Returns True if successful, False otherwise.
        """
        return self.service.stop_and_disable_service("DiagTrack")
    
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
            try:
                subprocess.run(["schtasks", "/change", "/tn", task, "/disable"], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error disabling task {task}: {str(e)}")
                success = False
                break
        
        return success
    
    def disable_all_telemetry(self) -> bool:
        """
        Disable all telemetry features using all available methods.
        Returns True if all operations were successful, False otherwise.
        """
        if not self.is_admin:
            print("This script requires administrator privileges to run properly.")
            return False
        
        results = {
            "Registry": self.disable_telemetry_registry(),
            "Service": self.disable_telemetry_service(),
            "Tasks": self.disable_telemetry_tasks()
        }
        
        success = all(results.values())
        if success:
            print("Successfully disabled all telemetry features!")
        else:
            print("Some operations failed. Check the error messages above.")
        
        return success 