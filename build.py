#!/usr/bin/env python3
"""
Build script for Vivi Windows executable
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def build_executable():
    """Build the Windows executable using PyInstaller"""
    
    # Ensure we're in the project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    print("🔨 Building Vivi executable...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Single executable file
        "--windowed",  # No console window
        "--name", "Vivi",
        "--icon", "assets/icon.ico",  # Will create this later
        "--add-data", "src;src",  # Include source code
        "src/main.py"
    ]
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build successful!")
        print(f"Executable created: {project_dir / 'dist' / 'Vivi.exe'}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False
        
    except FileNotFoundError:
        print("❌ PyInstaller not found. Please install it with: pip install pyinstaller")
        return False
        
    return True


def create_assets():
    """Create necessary asset files"""
    assets_dir = Path("assets")
    assets_dir.mkdir(exist_ok=True)
    
    # Create a simple icon placeholder (you can replace this later)
    icon_path = assets_dir / "icon.ico"
    if not icon_path.exists():
        print("📝 Creating placeholder icon...")
        # For now, we'll skip the icon requirement
        pass


def main():
    """Main build process"""
    print("🚀 Starting Vivi build process...")
    
    # Create assets
    create_assets()
    
    # Build executable
    if build_executable():
        print("🎉 Vivi build completed successfully!")
        print("📁 Check the 'dist' folder for your executable.")
    else:
        print("💥 Build failed. Check the error messages above.")
        sys.exit(1)


if __name__ == "__main__":
    main()

