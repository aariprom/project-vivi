"""
Main GUI window for Vivi
"""

import time
from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QPushButton,
    QTextEdit,
    QListWidget,
    QSplitter,
    QStatusBar,
)
from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtGui import QFont


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.init_ui()

        # Connect engine signals
        self.engine.feedback_generated.connect(self.display_feedback)

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Vivi - AI Assistant")
        self.setGeometry(100, 100, 800, 600)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create main layout
        main_layout = QHBoxLayout(central_widget)

        # Create splitter for resizable panels
        splitter = QSplitter()
        main_layout.addWidget(splitter)

        # Left panel - Tasks and controls
        left_panel = self._create_left_panel()
        splitter.addWidget(left_panel)

        # Right panel - Status and feedback
        right_panel = self._create_right_panel()
        splitter.addWidget(right_panel)

        # Set splitter proportions
        splitter.setSizes([300, 500])

        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Vivi is running...")

        # Setup update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_display)
        self.update_timer.start(1000)  # Update every second

    def _create_left_panel(self) -> QWidget:
        """Create the left control panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # Title
        title = QLabel("Vivi Control Panel")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        # Task management
        task_label = QLabel("Current Tasks:")
        layout.addWidget(task_label)

        self.task_list = QListWidget()
        layout.addWidget(self.task_list)

        # Add task section
        add_task_label = QLabel("Add New Task:")
        layout.addWidget(add_task_label)

        self.task_input = QTextEdit()
        self.task_input.setMaximumHeight(60)
        self.task_input.setPlaceholderText("Enter your task here...")
        layout.addWidget(self.task_input)

        add_button = QPushButton("Add Task")
        add_button.clicked.connect(self.add_task)
        layout.addWidget(add_button)

        # Control buttons
        self.start_button = QPushButton("Start Monitoring")
        self.start_button.clicked.connect(self.toggle_monitoring)
        layout.addWidget(self.start_button)

        return panel

    def _create_right_panel(self) -> QWidget:
        """Create the right status panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # Title
        title = QLabel("Vivi Status & Feedback")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        # Status display
        status_label = QLabel("Current Status:")
        layout.addWidget(status_label)

        self.status_display = QTextEdit()
        self.status_display.setReadOnly(True)
        layout.addWidget(self.status_display)

        # Feedback display
        feedback_label = QLabel("AI Feedback:")
        layout.addWidget(feedback_label)

        self.feedback_display = QTextEdit()
        self.feedback_display.setReadOnly(True)
        layout.addWidget(self.feedback_display)

        return panel

    def add_task(self):
        """Add a new task"""
        task_text = self.task_input.toPlainText().strip()
        if task_text:
            self.engine.add_task(task_text)
            self.task_list.addItem(task_text)
            self.task_input.clear()

    def toggle_monitoring(self):
        """Toggle monitoring on/off"""
        if self.engine.running:
            self.engine.stop()
            self.start_button.setText("Start Monitoring")
            self.status_bar.showMessage("Vivi stopped")
        else:
            self.engine.start()
            self.start_button.setText("Stop Monitoring")
            self.status_bar.showMessage("Vivi is running...")

    def update_display(self):
        """Update the display with current information"""
        try:
            # Update task list
            current_tasks = self.engine.get_tasks()
            self.task_list.clear()
            for task in current_tasks:
                self.task_list.addItem(task)

            # Update status display
            status_text = f"Engine Running: {self.engine.running}\n"
            status_text += f"Active Tasks: {len(current_tasks)}\n"
            status_text += f"Screen Monitor: Active\n"
            status_text += f"Process Monitor: Active\n"
            status_text += f"Input Monitor: Active"

            self.status_display.setPlainText(status_text)

        except Exception as e:
            print(f"Error updating display: {e}")
            # Don't crash the GUI, just log the error

    def display_feedback(self, feedback: dict):
        """Display AI feedback in the feedback section"""
        try:
            message = feedback.get("message", "No message")
            feedback_type = feedback.get("type", "unknown")
            priority = feedback.get("priority", "low")

            # Format the feedback message
            timestamp = time.strftime("%H:%M:%S")
            formatted_message = f"[{timestamp}] {message}\n"
            formatted_message += f"Type: {feedback_type} | Priority: {priority}\n"
            formatted_message += "-" * 50 + "\n"

            # Append to feedback display
            current_text = self.feedback_display.toPlainText()
            self.feedback_display.setPlainText(formatted_message + current_text)

        except Exception as e:
            print(f"Error displaying feedback: {e}")
