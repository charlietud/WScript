import subprocess
from typing import Optional

class ServiceManager:
    @staticmethod
    def stop_service(service_name: str) -> bool:
        """
        Stop a Windows service.
        
        Args:
            service_name: The name of the service to stop
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            subprocess.run(["sc", "stop", service_name], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error stopping service {service_name}: {str(e)}")
            return False
    
    @staticmethod
    def disable_service(service_name: str) -> bool:
        """
        Disable a Windows service.
        
        Args:
            service_name: The name of the service to disable
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            subprocess.run(["sc", "config", service_name, "start=disabled"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error disabling service {service_name}: {str(e)}")
            return False
    
    @staticmethod
    def stop_and_disable_service(service_name: str) -> bool:
        """
        Stop and disable a Windows service.
        
        Args:
            service_name: The name of the service to stop and disable
            
        Returns:
            bool: True if successful, False otherwise
        """
        stop_success = ServiceManager.stop_service(service_name)
        disable_success = ServiceManager.disable_service(service_name)
        return stop_success and disable_success 