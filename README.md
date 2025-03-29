# WScript Customization Tool

A Python-based command-line tool for managing Windows system settings and privacy features. This tool provides a clean, efficient way to customize Windows behavior, starting with telemetry management.

## Features

- **Telemetry Management**
  - Disables Windows telemetry services
  - Modifies registry settings for privacy
  - Manages telemetry-related scheduled tasks
  - Safe and reversible changes

## Requirements

- Windows 10/11
- Python 3.6 or higher
- Administrator privileges
- Required Python packages:
  ```
  pywin32>=305
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/wscript.git
   cd wscript
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

The tool requires administrator privileges to run. Open PowerShell or Command Prompt as Administrator and run:

```bash
# Show help
python main.py --help

# Disable telemetry
python main.py --telemetry
```

## Project Structure

```
wscript/
├── src/
│   ├── core/           # Core functionality
│   │   ├── admin_check.py
│   │   ├── registry_manager.py
│   │   └── service_manager.py
│   └── features/       # Feature implementations
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

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

RGra

## Acknowledgments

- Built with Python
- Uses Windows Management APIs
- Inspired by privacy-focused Windows customization needs

## Important Notes

- This tool was mostly made for educational purposes, I do not take any responsibility for any unwanted changes it may cause to your system (it should be safe though).
- This is definitely not a replacement for other more established tools like like Chris Titus's Windows Script.