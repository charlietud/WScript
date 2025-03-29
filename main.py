from src.features.telemetry import TelemetryManager
from src.core.admin_check import AdminCheck

def main():
    if not AdminCheck.is_admin():
        print("Please run this script as administrator!")
        return
    
    print("Starting Windows customization process...")
    
    # Initialize feature managers
    telemetry = TelemetryManager()
    
    # Execute telemetry deactivation
    print("\nDisabling telemetry...")
    telemetry.disable_all_telemetry()
    
    # Future features can be added here
    # cortana = CortanaManager()
    # copilot = CopilotManager()
    # etc...

if __name__ == "__main__":
    main() 