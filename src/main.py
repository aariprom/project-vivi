#!/usr/bin/env python3
"""
Vivi - Integrated AI Assistant
Main application entry point
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from .gui.main_window import MainWindow
from .core.vivi_engine import ViviEngine


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Vivi")
    app.setApplicationVersion("0.1.0")
    
    # Initialize the Vivi engine
    engine = ViviEngine()
    
    # Create and show the main window
    window = MainWindow(engine)
    window.show()
    
    # Start the engine
    engine.start()
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

