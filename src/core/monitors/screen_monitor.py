"""
Screen capture and analysis module
"""

import time
from typing import Optional, Dict, Any
import numpy as np
import cv2

# Try to import platform-specific screenshot libraries
try:
    from PIL import ImageGrab
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import mss
    MSS_AVAILABLE = True
except ImportError:
    MSS_AVAILABLE = False


class ScreenMonitor:
    """Handles screen capture and basic analysis"""
    
    def __init__(self):
        self.last_screenshot = None
        self.screenshot_history = []
        self.max_history = 10
        
        # Initialize MSS if available
        if MSS_AVAILABLE:
            self.mss_instance = mss.mss()
        else:
            self.mss_instance = None
        
    def capture_screen(self) -> Optional[Dict[str, Any]]:
        """Capture current screen and return analysis"""
        try:
            # Capture screenshot using available method
            if PIL_AVAILABLE:
                screenshot = ImageGrab.grab()
                screenshot_np = np.array(screenshot)
            elif MSS_AVAILABLE and self.mss_instance:
                # Use MSS for cross-platform screenshot
                screenshot = self.mss_instance.grab(self.mss_instance.monitors[0])
                screenshot_np = np.array(screenshot)
            else:
                print("No screenshot library available")
                return None
            
            # Store in history
            self.last_screenshot = screenshot_np
            self.screenshot_history.append({
                'image': screenshot_np,
                'timestamp': time.time()
            })
            
            # Keep only recent screenshots
            if len(self.screenshot_history) > self.max_history:
                self.screenshot_history.pop(0)
                
            # Basic analysis
            analysis = self._analyze_screenshot(screenshot_np)
            
            return {
                'image': screenshot_np,
                'analysis': analysis,
                'timestamp': time.time()
            }
            
        except Exception as e:
            print(f"Error capturing screen: {e}")
            return None
            
    def _analyze_screenshot(self, image: np.ndarray) -> Dict[str, Any]:
        """Basic screenshot analysis"""
        # Convert to grayscale for analysis
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Calculate basic statistics
        brightness = np.mean(gray)
        contrast = np.std(gray)
        
        # Detect if screen is mostly static (low change)
        change_detected = False
        if len(self.screenshot_history) > 1:
            prev_image = self.screenshot_history[-2]['image']
            if prev_image.shape == image.shape:
                diff = cv2.absdiff(gray, cv2.cvtColor(prev_image, cv2.COLOR_RGB2GRAY))
                change_detected = np.mean(diff) > 10  # Threshold for change detection
                
        return {
            'brightness': float(brightness),
            'contrast': float(contrast),
            'change_detected': change_detected,
            'dimensions': image.shape
        }

