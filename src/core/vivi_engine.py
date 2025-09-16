"""
Vivi Engine - Core AI assistant logic
"""

import threading
import time
from typing import Optional, Dict, Any
from .monitors.screen_monitor import ScreenMonitor
from .monitors.process_monitor import ProcessMonitor
from .monitors.input_monitor import InputMonitor
from .ai.analyzer import BehaviorAnalyzer
from .ai.feedback_engine import FeedbackEngine


class ViviEngine:
    """Main Vivi AI assistant engine"""
    
    def __init__(self):
        self.running = False
        self.thread = None
        
        # Initialize monitors
        self.screen_monitor = ScreenMonitor()
        self.process_monitor = ProcessMonitor()
        self.input_monitor = InputMonitor()
        
        # Initialize AI components
        self.analyzer = BehaviorAnalyzer()
        self.feedback_engine = FeedbackEngine()
        
        # User context
        self.user_tasks = []
        self.current_context = {}
        
    def start(self):
        """Start the Vivi engine"""
        if self.running:
            return
            
        self.running = True
        
        # Start input monitoring
        self.input_monitor.start_monitoring()
        
        self.thread = threading.Thread(target=self._main_loop, daemon=True)
        self.thread.start()
        
    def stop(self):
        """Stop the Vivi engine"""
        self.running = False
        
        # Stop input monitoring
        self.input_monitor.stop_monitoring()
        
        if self.thread:
            self.thread.join()
            
    def _main_loop(self):
        """Main processing loop"""
        while self.running:
            try:
                # Collect data from all monitors
                data = self._collect_data()
                
                # Analyze behavior
                analysis = self.analyzer.analyze(data)
                
                # Generate feedback if needed
                if analysis.get('needs_feedback'):
                    feedback = self.feedback_engine.generate_feedback(analysis)
                    self._deliver_feedback(feedback)
                    
                time.sleep(1)  # Process every second
                
            except Exception as e:
                print(f"Error in main loop: {e}")
                time.sleep(5)  # Wait before retrying
                
    def _collect_data(self) -> Dict[str, Any]:
        """Collect data from all monitors"""
        return {
            'screen': self.screen_monitor.capture_screen(),
            'processes': self.process_monitor.get_active_processes(),
            'window': self.process_monitor.get_active_window(),
            'input': self.input_monitor.get_recent_input(),
            'timestamp': time.time()
        }
        
    def _deliver_feedback(self, feedback: Dict[str, Any]):
        """Deliver feedback to user"""
        print(f"Vivi Feedback: {feedback}")
        # TODO: Implement actual feedback delivery (notifications, etc.)
        
    def add_task(self, task: str):
        """Add a task to user's work list"""
        self.user_tasks.append(task)
        
    def get_tasks(self) -> list:
        """Get current user tasks"""
        return self.user_tasks.copy()

