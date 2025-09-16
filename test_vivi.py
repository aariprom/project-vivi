#!/usr/bin/env python3
"""
Simple test script for Vivi components
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from core.monitors.screen_monitor import ScreenMonitor
from core.monitors.process_monitor import ProcessMonitor
from core.monitors.input_monitor import InputMonitor
from core.ai.analyzer import BehaviorAnalyzer
from core.ai.feedback_engine import FeedbackEngine


def test_screen_monitor():
    """Test screen monitoring functionality"""
    print("🖥️  Testing Screen Monitor...")
    monitor = ScreenMonitor()

    # Test screen capture
    result = monitor.capture_screen()
    if result:
        print(f"✅ Screen captured successfully")
        print(f"   Dimensions: {result['analysis']['dimensions']}")
        print(f"   Brightness: {result['analysis']['brightness']:.1f}")
        print(f"   Contrast: {result['analysis']['contrast']:.1f}")
    else:
        print("❌ Screen capture failed")
    print()


def test_process_monitor():
    """Test process monitoring functionality"""
    print("⚙️  Testing Process Monitor...")
    monitor = ProcessMonitor()

    # Test process listing
    processes = monitor.get_active_processes()
    print(f"✅ Found {len(processes)} running processes")

    # Show first few processes
    for i, proc in enumerate(processes[:5]):
        print(f"   {i+1}. {proc['name']} (PID: {proc['pid']})")

    # Test active window
    window = monitor.get_active_window()
    if window:
        print(f"✅ Active window: {window['title']}")
        print(f"   Process: {window['process_name']}")
    else:
        print("❌ Could not get active window")
    print()


def test_input_monitor():
    """Test input monitoring functionality"""
    print("⌨️  Testing Input Monitor...")
    monitor = InputMonitor()

    # Test input patterns (without starting monitoring)
    patterns = monitor.get_input_patterns()
    print(f"✅ Input patterns analyzed")
    print(f"   Active: {patterns.get('input_active', False)}")
    print(f"   Typing rate: {patterns.get('typing_rate', 0):.2f} events/sec")
    print()


def test_analyzer():
    """Test behavior analyzer"""
    print("🧠 Testing Behavior Analyzer...")
    analyzer = BehaviorAnalyzer()

    # Create mock data
    mock_data = {
        "screen": {
            "analysis": {
                "brightness": 150,
                "contrast": 50,
                "change_detected": True,
                "dimensions": (1920, 1080, 3),
            }
        },
        "processes": [
            {"name": "code.exe", "pid": 1234},
            {"name": "chrome.exe", "pid": 5678},
        ],
        "window": {"title": "Visual Studio Code", "process_name": "code.exe"},
        "input": [
            {"type": "key_press", "description": "a", "timestamp": 1234567890},
            {"type": "key_press", "description": "b", "timestamp": 1234567891},
        ],
    }

    # Analyze the data
    analysis = analyzer.analyze(mock_data)
    print(f"✅ Analysis completed")
    print(f"   Focus score: {analysis['focus_score']:.2f}")
    print(f"   Needs feedback: {analysis['needs_feedback']}")
    print(f"   Distraction detected: {analysis.get('distraction_detected', False)}")
    print(f"   Productivity detected: {analysis.get('productivity_detected', False)}")
    print()


def test_feedback_engine():
    """Test feedback engine"""
    print("💬 Testing Feedback Engine...")
    engine = FeedbackEngine()

    # Create mock analysis
    mock_analysis = {
        "focus_score": 0.2,
        "distraction_detected": True,
        "productivity_detected": False,
        "needs_feedback": True,
    }

    # Generate feedback
    feedback = engine.generate_feedback(mock_analysis)
    print(f"✅ Feedback generated")
    print(f"   Type: {feedback['type']}")
    print(f"   Priority: {feedback['priority']}")
    print(f"   Message: {feedback['message']}")
    print()


def main():
    """Run all tests"""
    print("🧪 Running Vivi Component Tests")
    print("=" * 50)

    try:
        test_screen_monitor()
        test_process_monitor()
        test_input_monitor()
        test_analyzer()
        test_feedback_engine()

        print("🎉 All tests completed successfully!")
        print("\n💡 Note: Some features require Windows-specific libraries.")
        print(
            "   Make sure to install all requirements: pip install -r requirements.txt"
        )

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        print("   This might be due to missing dependencies or platform compatibility.")


if __name__ == "__main__":
    main()
