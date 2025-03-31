import argparse
from src.features.telemetry import TelemetryManager
from src.features.cortana import CortanaManager
from src.core.admin_check import AdminCheck
from src.features.context_menu import ContextMenuManager
from src.features.copilot import CopilotManager

def print_header():
    """Print a formatted header for the application."""
    print("\n" + "="*50)
    print("WScript - Customization and Automation Tool")
    print("="*50 + "\n")

def print_section_header(title):
    """Print a formatted section header."""
    print("\n" + "-"*30)
    print(f" {title}")
    print("-"*30)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Thank you for using WScript! A tool for disabling Windows telemetry and Cortana. More features to come!',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Add arguments
    parser.add_argument(
        '--telemetry',
        action='store_true',
        help='Disable Windows telemetry'
    )
    parser.add_argument(
        '--cortana',
        action='store_true',
        help='Disable Cortana'
    )
    parser.add_argument(
        '--context-menu',
        action='store_true',
        help='Activate older Windows 10 context menu'
    )
    parser.add_argument(
        '--copilot',
        action='store_true',
        help='Disables Windows Copilot'
    )
    
    # Parse arguments
    args = parser.parse_args()

    # Check for admin rights
    if not AdminCheck.is_admin():
        print("ERROR: This script requires administrator privileges!")
        print("Please run this script as administrator.")
        return

    print_header()

    # Initialize feature managers
    telemetry = TelemetryManager()
    cortana = CortanaManager()
    context_menu = ContextMenuManager()
    copilot = CopilotManager()

    # Handle command line arguments
    if args.telemetry:
        print_section_header("Disabling Telemetry")
        telemetry.disable_all_telemetry()
    elif args.cortana:
        print_section_header("Disabling Cortana")
        cortana.disable_all_cortana()
    elif args.context_menu:
        print_section_header("Activating Win10 Context Menu")
        context_menu.old_context_menu_all()
    elif args.copilot:
        print_section_header("Disabling Copilot")
        copilot.disable_copilot()
    else:
        print("No options specified. Use one of the following options:")
        print("\nAvailable options:")
        print("  --telemetry    Disable Windows telemetry")
        print("  --cortana     Disable Cortana")
        print("  --context-menu     Activate Win10 Context Menu")
        print("  --help        Show this help message")

if __name__ == "__main__":
    main() 