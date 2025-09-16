# Vivi - Integrated AI Assistant

Vivi is an intelligent AI assistant that monitors your screen, tracks your input, and provides contextual feedback to help you stay focused and productive.

## Features

- **Screen Monitoring**: Captures and analyzes your screen activity
- **Process Tracking**: Monitors running applications and active windows
- **Input Analysis**: Tracks keyboard and mouse input patterns
- **AI-Powered Feedback**: Provides intelligent alerts and encouragement
- **Focus Scoring**: Calculates your focus level and suggests improvements
- **Task Management**: Helps you track and stay focused on your goals

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd project-vivi
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python -m src.main
```

## Building for Windows

To create a Windows executable:

```bash
python build.py
```

This will create a standalone `Vivi.exe` file in the `dist` folder.

## Usage

1. Launch Vivi
2. Add your current tasks in the control panel
3. Click "Start Monitoring" to begin
4. Vivi will analyze your behavior and provide feedback when needed

## Architecture

- `src/core/` - Core AI engine and monitoring components
- `src/gui/` - PyQt6-based user interface
- `src/core/monitors/` - Data collection modules (screen, process, input)
- `src/core/ai/` - AI analysis and feedback generation

## Requirements

- Python 3.8+
- Windows 10/11 (for system monitoring features)
- PyQt6 for GUI
- Various monitoring libraries (see requirements.txt)

## Development

This project is in active development. Current version: 0.1.0

## License

[Add your license here]
