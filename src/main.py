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
    try:
        print("Starting Vivi application...")
        
        # Check if we can create QApplication
        print("Creating QApplication...")
        app = QApplication(sys.argv)
        app.setApplicationName("Vivi")
        app.setApplicationVersion("0.1.0")
        print("QApplication created successfully")
        
        # Initialize the Vivi engine
        print("Initializing Vivi engine...")
        engine = ViviEngine()
        print("Vivi engine initialized")
        
        # Create and show the main window
        print("Creating main window...")
        window = MainWindow(engine)
        print("Main window created")
        
        print("Showing main window...")
        window.show()
        print("Main window shown")
        
        # Start the engine
        print("Starting Vivi engine...")
        engine.start()
        print("Vivi engine started")
        
        print("Starting application event loop...")
        # Run the application
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"Error starting Vivi GUI: {e}")
        print("Falling back to console mode...")
        
        # Try console-only mode
        try:
            print("Starting Vivi in console mode...")
            engine = ViviEngine()
            engine.start()
            
            print("Vivi is running in console mode!")
            print("Press Ctrl+C to stop...")
            
            # Keep running until interrupted
            import time
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\nStopping Vivi...")
            engine.stop()
            print("Vivi stopped.")
        except Exception as console_error:
            print(f"Error in console mode: {console_error}")
            import traceback
            traceback.print_exc()
            input("Press Enter to exit...")


if __name__ == "__main__":
    main()

