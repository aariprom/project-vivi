"""
Keyboard and mouse input monitoring module
"""

import time
from typing import List, Dict, Any
from collections import deque
from pynput import keyboard, mouse
from pynput.keyboard import Key, Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener


class InputMonitor:
    """Monitors keyboard and mouse input"""
    
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.input_history = deque(maxlen=max_history)
        self.keyboard_listener = None
        self.mouse_listener = None
        self.is_monitoring = False
        
    def start_monitoring(self):
        """Start monitoring input"""
        if self.is_monitoring:
            return
            
        self.is_monitoring = True
        
        # Start keyboard listener
        self.keyboard_listener = KeyboardListener(
            on_press=self._on_key_press,
            on_release=self._on_key_release
        )
        self.keyboard_listener.start()
        
        # Start mouse listener
        self.mouse_listener = MouseListener(
            on_click=self._on_mouse_click,
            on_scroll=self._on_mouse_scroll,
            on_move=self._on_mouse_move
        )
        self.mouse_listener.start()
        
    def stop_monitoring(self):
        """Stop monitoring input"""
        self.is_monitoring = False
        
        if self.keyboard_listener:
            self.keyboard_listener.stop()
            self.keyboard_listener = None
            
        if self.mouse_listener:
            self.mouse_listener.stop()
            self.mouse_listener = None
            
    def _on_key_press(self, key):
        """Handle key press events"""
        try:
            key_name = key.name if hasattr(key, 'name') else str(key)
            self._add_input_event('key_press', key_name)
        except AttributeError:
            pass
            
    def _on_key_release(self, key):
        """Handle key release events"""
        try:
            key_name = key.name if hasattr(key, 'name') else str(key)
            self._add_input_event('key_release', key_name)
        except AttributeError:
            pass
            
    def _on_mouse_click(self, x, y, button, pressed):
        """Handle mouse click events"""
        action = 'mouse_press' if pressed else 'mouse_release'
        self._add_input_event(action, f"{button.name} at ({x}, {y})")
        
    def _on_mouse_scroll(self, x, y, dx, dy):
        """Handle mouse scroll events"""
        direction = 'up' if dy > 0 else 'down'
        self._add_input_event('mouse_scroll', f"{direction} at ({x}, {y})")
        
    def _on_mouse_move(self, x, y):
        """Handle mouse move events"""
        # Only log significant movements to avoid spam
        if len(self.input_history) == 0 or \
           abs(x - self.input_history[-1].get('x', 0)) > 10 or \
           abs(y - self.input_history[-1].get('y', 0)) > 10:
            self._add_input_event('mouse_move', f"to ({x}, {y})", x=x, y=y)
            
    def _add_input_event(self, event_type: str, description: str, **kwargs):
        """Add input event to history"""
        event = {
            'type': event_type,
            'description': description,
            'timestamp': time.time(),
            **kwargs
        }
        self.input_history.append(event)
        
    def get_recent_input(self, seconds: int = 10) -> List[Dict[str, Any]]:
        """Get recent input events within specified seconds"""
        current_time = time.time()
        cutoff_time = current_time - seconds
        
        return [event for event in self.input_history if event['timestamp'] >= cutoff_time]
        
    def get_input_patterns(self) -> Dict[str, Any]:
        """Analyze input patterns for behavior detection"""
        if not self.input_history:
            return {}
            
        recent_events = self.get_recent_input(60)  # Last minute
        
        # Count event types
        event_counts = {}
        for event in recent_events:
            event_type = event['type']
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
            
        # Detect rapid typing (high key press rate)
        key_events = [e for e in recent_events if e['type'] in ['key_press', 'key_release']]
        typing_rate = len(key_events) / 60  # events per second
        
        # Detect mouse activity
        mouse_events = [e for e in recent_events if e['type'].startswith('mouse')]
        mouse_activity = len(mouse_events) / 60
        
        return {
            'event_counts': event_counts,
            'typing_rate': typing_rate,
            'mouse_activity': mouse_activity,
            'total_events': len(recent_events),
            'is_active': typing_rate > 0.5 or mouse_activity > 0.1
        }

