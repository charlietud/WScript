#!/usr/bin/env python3
import os
import subprocess
import winreg
import ctypes
from typing import Optional

class TelemetryManager:
    def __init__(self):
        self.is_admin = self._check_admin_rights()
    
    def _check_admin_rights(self) -> bool:
        """Check if the script is running with administrator privileges."""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def disable_telemetry_registry(self) -> bool:
        """
        Disable Windows telemetry through registry modifications.
        Returns True if successful, False otherwise.
        """
        try:
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
            
            for path in paths:
                try:
                    key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_WRITE)
                    for name, value in values.items():
                        winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, value)
                    winreg.CloseKey(key)
                except WindowsError as e:
                    print(f"Error modifying registry path {path}: {str(e)}")
                    continue
            
            return True
        except Exception as e:
            print(f"Error in disable_telemetry_registry: {str(e)}")
            return False
    
    def disable_telemetry_service(self) -> bool:
        """
        Disable the Windows telemetry service (DiagTrack).
        Returns True if successful, False otherwise.
        """
        try:
            # Stop the service
            subprocess.run(["sc", "stop", "DiagTrack"], check=True)
            # Disable the service
            subprocess.run(["sc", "config", "DiagTrack", "start=disabled"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error disabling telemetry service: {str(e)}")
            return False
    
    def disable_telemetry_tasks(self) -> bool:
        """
        Disable telemetry-related scheduled tasks.
        Returns True if successful, False otherwise.
        """
        try:
            tasks = [
                "Microsoft\Windows\Application Experience\Microsoft Compatibility Appraiser",
                "Microsoft\Windows\Application Experience\ProgramDataUpdater",
                "Microsoft\Windows\Customer Experience Improvement Program\Consolidator",
                "Microsoft\Windows\Customer Experience Improvement Program\UsbCeip",
                "Microsoft\Windows\Customer Experience Improvement Program\KernelCeipTask"
            ]
            
            for task in tasks:
                try:
                    subprocess.run(["schtasks", "/change", "/tn", task, "/disable"], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Error disabling task {task}: {str(e)}")
                    continue
            
            return True
        except Exception as e:
            print(f"Error in disable_telemetry_tasks: {str(e)}")
            return False
    
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

def main():
    manager = TelemetryManager()
    if not manager.is_admin:
        print("Please run this script as administrator!")
        return
    
    print("Starting telemetry deactivation process...")
    manager.disable_all_telemetry()

if __name__ == "__main__":
    main() 