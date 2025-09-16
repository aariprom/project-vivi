"""
Feedback generation and delivery module
"""

import time
from typing import Dict, Any, List
import random


class FeedbackEngine:
    """Generates and delivers feedback to the user"""
    
    def __init__(self):
        self.feedback_history = []
        self.max_history = 100
        
    def generate_feedback(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate appropriate feedback based on analysis"""
        feedback_type = self._determine_feedback_type(analysis)
        message = self._generate_message(feedback_type, analysis)
        priority = self._determine_priority(analysis)
        
        feedback = {
            'type': feedback_type,
            'message': message,
            'priority': priority,
            'timestamp': time.time(),
            'analysis': analysis
        }
        
        # Store in history
        self.feedback_history.append(feedback)
        if len(self.feedback_history) > self.max_history:
            self.feedback_history.pop(0)
            
        return feedback
        
    def _determine_feedback_type(self, analysis: Dict[str, Any]) -> str:
        """Determine the type of feedback needed"""
        if analysis.get('distraction_detected'):
            return 'distraction_alert'
        elif analysis.get('focus_score', 0.5) < 0.3:
            return 'focus_reminder'
        elif analysis.get('screen_static') and not analysis.get('input_active'):
            return 'inactivity_reminder'
        elif analysis.get('rapid_typing'):
            return 'stress_alert'
        else:
            return 'general_encouragement'
            
    def _generate_message(self, feedback_type: str, analysis: Dict[str, Any]) -> str:
        """Generate appropriate message for feedback type"""
        messages = {
            'distraction_alert': [
                "🚨 Focus alert! I noticed you're on a potentially distracting site.",
                "⏰ Time to get back to work! You've got important tasks to complete.",
                "🎯 Stay focused! Your productivity goals are waiting for you.",
                "💪 Let's refocus on your tasks. You've got this!"
            ],
            'focus_reminder': [
                "🌟 Your focus score is low. Let's get back on track!",
                "📚 Time to dive deep into your work. Focus mode activated!",
                "🎯 Remember your goals. Every moment counts!",
                "💡 Take a deep breath and refocus on what matters most."
            ],
            'inactivity_reminder': [
                "🤔 I notice you haven't been active. Are you still working?",
                "⏸️ Taking a break? That's fine, just remember to come back!",
                "💭 Lost in thought? Don't forget about your tasks!",
                "🔄 Ready to get back to work? Your tasks are waiting."
            ],
            'stress_alert': [
                "😌 Slow down a bit. Rapid typing might indicate stress.",
                "🧘 Take a moment to breathe. You're doing great!",
                "⏱️ Pace yourself. Quality over speed!",
                "💆‍♀️ Remember to take breaks. Your well-being matters."
            ],
            'general_encouragement': [
                "👍 Great job staying focused! Keep it up!",
                "🎉 You're doing well! Stay on track!",
                "⭐ Excellent work! You're making progress!",
                "🚀 Keep the momentum going! You're on fire!"
            ]
        }
        
        message_list = messages.get(feedback_type, messages['general_encouragement'])
        return random.choice(message_list)
        
    def _determine_priority(self, analysis: Dict[str, Any]) -> str:
        """Determine feedback priority"""
        if analysis.get('distraction_detected'):
            return 'high'
        elif analysis.get('focus_score', 0.5) < 0.2:
            return 'high'
        elif analysis.get('rapid_typing'):
            return 'medium'
        else:
            return 'low'
            
    def get_feedback_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent feedback history"""
        return self.feedback_history[-limit:] if self.feedback_history else []
        
    def get_feedback_stats(self) -> Dict[str, Any]:
        """Get feedback statistics"""
        if not self.feedback_history:
            return {}
            
        # Count feedback types
        type_counts = {}
        priority_counts = {}
        
        for feedback in self.feedback_history:
            feedback_type = feedback['type']
            priority = feedback['priority']
            
            type_counts[feedback_type] = type_counts.get(feedback_type, 0) + 1
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
            
        return {
            'total_feedback': len(self.feedback_history),
            'type_distribution': type_counts,
            'priority_distribution': priority_counts,
            'last_feedback': self.feedback_history[-1] if self.feedback_history else None
        }

