"""
Behavior analysis module using AI
"""

import time
from typing import Dict, Any, List
import numpy as np


class BehaviorAnalyzer:
    """Analyzes user behavior patterns and detects interesting events"""
    
    def __init__(self):
        self.distraction_keywords = [
            'youtube', 'facebook', 'twitter', 'instagram', 'tiktok', 
            'reddit', 'netflix', 'gaming', 'game', 'entertainment'
        ]
        self.productivity_keywords = [
            'code', 'programming', 'work', 'document', 'email', 
            'meeting', 'project', 'task', 'development'
        ]
        
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze collected data and return insights"""
        analysis = {
            'timestamp': time.time(),
            'needs_feedback': False,
            'distraction_detected': False,
            'productivity_detected': False,
            'focus_score': 0.0,
            'recommendations': []
        }
        
        # Analyze screen data
        if 'screen' in data and data['screen']:
            screen_analysis = self._analyze_screen_data(data['screen'])
            analysis.update(screen_analysis)
            
        # Analyze process data
        if 'processes' in data:
            process_analysis = self._analyze_process_data(data['processes'])
            analysis.update(process_analysis)
            
        # Analyze window data
        if 'window' in data and data['window']:
            window_analysis = self._analyze_window_data(data['window'])
            analysis.update(window_analysis)
            
        # Analyze input data
        if 'input' in data:
            input_analysis = self._analyze_input_data(data['input'])
            analysis.update(input_analysis)
            
        # Calculate overall focus score
        analysis['focus_score'] = self._calculate_focus_score(analysis)
        
        # Determine if feedback is needed
        analysis['needs_feedback'] = self._should_provide_feedback(analysis)
        
        return analysis
        
    def _analyze_screen_data(self, screen_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze screen capture data"""
        analysis = screen_data.get('analysis', {})
        
        # Detect if screen is static (user might be away)
        is_static = not analysis.get('change_detected', True)
        
        # Detect if screen is too dark (might be sleeping)
        brightness = analysis.get('brightness', 128)
        is_dark = brightness < 50
        
        return {
            'screen_static': is_static,
            'screen_dark': is_dark,
            'screen_brightness': brightness
        }
        
    def _analyze_process_data(self, processes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze running processes"""
        process_names = [p['name'].lower() for p in processes]
        
        # Count distraction processes
        distraction_count = sum(1 for name in process_names 
                              if any(keyword in name for keyword in self.distraction_keywords))
        
        # Count productivity processes
        productivity_count = sum(1 for name in process_names 
                               if any(keyword in name for keyword in self.productivity_keywords))
        
        return {
            'distraction_processes': distraction_count,
            'productivity_processes': productivity_count,
            'total_processes': len(processes)
        }
        
    def _analyze_window_data(self, window_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze active window data"""
        window_title = window_data.get('title', '').lower()
        process_name = window_data.get('process_name', '').lower()
        
        # Check for distraction indicators
        distraction_detected = any(keyword in window_title or keyword in process_name 
                                 for keyword in self.distraction_keywords)
        
        # Check for productivity indicators
        productivity_detected = any(keyword in window_title or keyword in process_name 
                                  for keyword in self.productivity_keywords)
        
        return {
            'distraction_detected': distraction_detected,
            'productivity_detected': productivity_detected,
            'active_window': window_title,
            'active_process': process_name
        }
        
    def _analyze_input_data(self, input_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze input patterns"""
        if not input_data:
            return {'input_active': False, 'typing_rate': 0.0}
            
        # Calculate typing rate
        key_events = [e for e in input_data if e['type'] in ['key_press', 'key_release']]
        time_span = input_data[-1]['timestamp'] - input_data[0]['timestamp'] if len(input_data) > 1 else 1
        typing_rate = len(key_events) / max(time_span, 1)
        
        # Detect rapid typing (might indicate stress or urgency)
        rapid_typing = typing_rate > 5.0
        
        return {
            'input_active': len(input_data) > 0,
            'typing_rate': typing_rate,
            'rapid_typing': rapid_typing,
            'total_input_events': len(input_data)
        }
        
    def _calculate_focus_score(self, analysis: Dict[str, Any]) -> float:
        """Calculate a focus score from 0.0 to 1.0"""
        score = 0.5  # Start with neutral score
        
        # Positive factors
        if analysis.get('productivity_detected'):
            score += 0.3
        if analysis.get('input_active'):
            score += 0.2
        if not analysis.get('screen_static'):
            score += 0.1
            
        # Negative factors
        if analysis.get('distraction_detected'):
            score -= 0.4
        if analysis.get('screen_dark'):
            score -= 0.2
        if analysis.get('screen_static'):
            score -= 0.1
            
        # Normalize to 0.0-1.0 range
        return max(0.0, min(1.0, score))
        
    def _should_provide_feedback(self, analysis: Dict[str, Any]) -> bool:
        """Determine if feedback should be provided"""
        # Provide feedback for low focus score
        if analysis.get('focus_score', 0.5) < 0.3:
            return True
            
        # Provide feedback for distraction detection
        if analysis.get('distraction_detected'):
            return True
            
        # Provide feedback for extended inactivity
        if analysis.get('screen_static') and not analysis.get('input_active'):
            return True
            
        return False

