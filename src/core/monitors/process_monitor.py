"""
Process and window monitoring module
"""

import time
import psutil
from typing import List, Dict, Any, Optional

# Try to import Windows-specific modules
try:
    import win32gui
    import win32process
    WINDOWS_API_AVAILABLE = True
except ImportError:
    WINDOWS_API_AVAILABLE = False


class ProcessMonitor:
    """Monitors running processes and active windows"""
    
    def __init__(self):
        self.last_processes = {}
        self.process_history = []
        self.max_history = 50
        
    def get_active_processes(self) -> List[Dict[str, Any]]:
        """Get list of currently running processes"""
        processes = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'create_time']):
                try:
                    proc_info = proc.info
                    processes.append({
                        'pid': proc_info['pid'],
                        'name': proc_info['name'],
                        'cpu_percent': proc_info['cpu_percent'],
                        'memory_percent': proc_info['memory_percent'],
                        'create_time': proc_info['create_time']
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
            # Store in history
            self.process_history.append({
                'processes': processes,
                'timestamp': time.time()
            })
            
            if len(self.process_history) > self.max_history:
                self.process_history.pop(0)
                
        except Exception as e:
            print(f"Error getting processes: {e}")
            
        return processes
        
    def get_active_window(self) -> Optional[Dict[str, Any]]:
        """Get information about the currently active window"""
        if not WINDOWS_API_AVAILABLE:
            print("Windows API not available - active window detection disabled")
            return None
            
        try:
            # Get active window handle
            hwnd = win32gui.GetForegroundWindow()
            
            if hwnd == 0:
                return None
                
            # Get window title
            window_title = win32gui.GetWindowText(hwnd)
            
            # Get process ID
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            
            # Get process name
            try:
                process = psutil.Process(pid)
                process_name = process.name()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                process_name = "Unknown"
                
            # Get window rectangle
            rect = win32gui.GetWindowRect(hwnd)
            
            return {
                'hwnd': hwnd,
                'title': window_title,
                'pid': pid,
                'process_name': process_name,
                'rect': rect,
                'timestamp': time.time()
            }
            
        except Exception as e:
            print(f"Error getting active window: {e}")
            return None
            
    def get_process_changes(self) -> Dict[str, Any]:
        """Detect changes in running processes"""
        current_processes = {p['pid']: p for p in self.get_active_processes()}
        
        # Find new processes
        new_processes = []
        for pid, proc in current_processes.items():
            if pid not in self.last_processes:
                new_processes.append(proc)
                
        # Find terminated processes
        terminated_processes = []
        for pid, proc in self.last_processes.items():
            if pid not in current_processes:
                terminated_processes.append(proc)
                
        # Update last processes
        self.last_processes = current_processes.copy()
        
        return {
            'new_processes': new_processes,
            'terminated_processes': terminated_processes,
            'total_processes': len(current_processes)
        }

