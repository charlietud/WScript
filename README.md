# Windows Customization and Automation Tool

A Python-based command-line tool for managing Windows system settings and privacy features. This tool provides a clean, efficient way to customize Windows behavior, starting with telemetry management.

## Features

- **Telemetry Management**
  - Disables Windows telemetry services
  - Modifies registry settings for privacy
  - Manages telemetry-related scheduled tasks
  - Safe and reversible changes

- **Disable both Cortana and Copilot**
  - Reversible changes
  - Modifies registry and disables services

- **Enable Win10 context menu**
  - This option enables the replaces the Windows 11 context menu with the one in Windows 10

- **Integrity Checks**
  - Runs both 'sfc' and 'DISM' command utilities to check for system integrity issues

- **Rollback** - *Coming Soon*

## Requirements

- Windows 10/11
- Python 3.6 or higher
- Administrator privileges

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/charlietud/WScript
   cd WScript
   ```

2. No additional package installation required - the tool uses built-in Python modules.

## Usage

The tool requires administrator privileges to run. Open PowerShell or Command Prompt as Administrator and run:

```bash
# Runs script and shows all the options available
python main.py
```

## Project Structure

```
wscript/
├── src/
│   ├── core/           # Core functionality
│   │   ├── admin_check.py
│   │   ├── log_manager.py
│   │   ├── service_manager.py
│   │   └── registry_manager.py
│   └── features/       # Feature implementations
│       ├── context_menu.py
│       ├── copilot.py
│       ├── cortana.py
│       ├── intscan.py
│       └── telemetry.py
├── main.py            # Main entry point
└── requirements.txt   # Python dependencies
```

## Safety Considerations

- All changes are made through official Windows APIs
- No critical system services are modified
- Changes are focused on privacy and telemetry settings
- Each operation includes error handling and status reporting

## Contributing

Contributions are welcome! Please feel free to submit a PR.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Ramham

## Acknowledgments

- Built with Python
- Uses Windows Management APIs
- Inspired by privacy-focused Windows customization needs

## Important Notes

- This tool was mostly made for educational purposes, I do not take any responsibility for any unwanted changes it may cause to your system (it should be safe though).
- This is definitely not a replacement for other more established tools like like Chris Titus's Windows Script.