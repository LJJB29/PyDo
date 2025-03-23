import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLineEdit, QPushButton, QMessageBox, QColorDialog
)
from PyQt5.QtGui import QColor

class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        print("PyDo Version 0.4 Late Beta Test is Starting...")  # Updated terminal message
        self.dark_mode = False  # Track dark mode state
        self.accent_color = QColor(94, 129, 172)  # Default accent color (Nord blue)
        self.initUI()
        self.load_tasks()  # Load tasks when the app starts

    def initUI(self):
        # Set up the main window
        self.setWindowTitle("PyDo Version 0.4 Late Beta Test")  # Updated window title
        self.setGeometry(100, 100, 400, 400)

        # Create a vertical layout
        layout = QVBoxLayout()

        # Create a QListWidget to display tasks
        self.task_list = QListWidget()
        layout.addWidget(self.task_list)

        # Create a QLineEdit for task input
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter a New Task Here!")
        layout.addWidget(self.task_input)

        # Create buttons and their layouts
        button_layout = QHBoxLayout()

        add_button = QPushButton("Add Task!")
        add_button.clicked.connect(self.add_task)
        button_layout.addWidget(add_button)

        delete_button = QPushButton("Delete Task!")
        delete_button.clicked.connect(self.delete_task)
        button_layout.addWidget(delete_button)

        complete_button = QPushButton("Mark as Completed!")
        complete_button.clicked.connect(self.mark_completed)
        button_layout.addWidget(complete_button)

        clear_button = QPushButton("Clear All Tasks!")
        clear_button.clicked.connect(self.clear_all)
        button_layout.addWidget(clear_button)

        # Add a toggle button for dark mode
        dark_mode_button = QPushButton("Toggle Dark Mode")
        dark_mode_button.clicked.connect(self.toggle_dark_mode)
        button_layout.addWidget(dark_mode_button)

        # Add a settings button
        settings_button = QPushButton("Settings")
        settings_button.clicked.connect(self.open_settings)
        button_layout.addWidget(settings_button)

        layout.addLayout(button_layout)

        # Set the layout for the main window
        self.setLayout(layout)

        # Apply default light mode
        self.apply_light_mode()

    def add_task(self):
        task = self.task_input.text()
        if task:
            self.task_list.addItem(task)
            self.task_input.clear()
        else:
            QMessageBox.warning(self, "Error", "Please enter a task to add!")

    def delete_task(self):
        selected_task = self.task_list.currentRow()
        if selected_task >= 0:
            self.task_list.takeItem(selected_task)
        else:
            QMessageBox.warning(self, "Error", "Please select a task to delete!")

    def mark_completed(self):
        selected_task = self.task_list.currentRow()
        if selected_task >= 0:
            item = self.task_list.item(selected_task)
            item.setText("✔ " + item.text())
        else:
            QMessageBox.warning(self, "Error", "Please select a task to mark as completed!")

    def clear_all(self):
        self.task_list.clear()

    def save_tasks(self):
        tasks = [self.task_list.item(i).text() for i in range(self.task_list.count())]
        with open("tasks.json", "w") as file:
            json.dump(tasks, file)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as file:
                tasks = json.load(file)
                for task in tasks:
                    self.task_list.addItem(task)
        except FileNotFoundError:
            print("No saved tasks found.")

    def closeEvent(self, event):
        self.save_tasks()
        event.accept()

    def toggle_dark_mode(self):
        """Toggle between light and dark mode."""
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.apply_dark_mode()
        else:
            self.apply_light_mode()

    def apply_dark_mode(self):
        """Apply dark mode stylesheet."""
        dark_stylesheet = f"""
        QWidget {{
            background-color: #2E3440;
            color: #ECEFF4;
        }}
        QListWidget {{
            background-color: #3B4252;
            color: #ECEFF4;
            border: 1px solid #4C566A;
        }}
        QLineEdit {{
            background-color: #3B4252;
            color: #ECEFF4;
            border: 1px solid #4C566A;
        }}
        QPushButton {{
            background-color: {self.accent_color.name()};
            color: #ECEFF4;
            border: 1px solid #5E81AC;
            padding: 5px;
        }}
        QPushButton:hover {{
            background-color: #81A1C1;
        }}
        """
        self.setStyleSheet(dark_stylesheet)

    def apply_light_mode(self):
        """Apply light mode stylesheet."""
        light_stylesheet = f"""
        QWidget {{
            background-color: #F5F5F5;
            color: #000000;
        }}
        QListWidget {{
            background-color: #FFFFFF;
            color: #000000;
            border: 1px solid #CCCCCC;
        }}
        QLineEdit {{
            background-color: #FFFFFF;
            color: #000000;
            border: 1px solid #CCCCCC;
        }}
        QPushButton {{
            background-color: {self.accent_color.name()};
            color: #000000;
            border: 1px solid #CCCCCC;
            padding: 5px;
        }}
        QPushButton:hover {{
            background-color: #D3D3D3;
        }}
        """
        self.setStyleSheet(light_stylesheet)

    def open_settings(self):
        """Open a settings menu to change the accent color."""
        color = QColorDialog.getColor(self.accent_color, self, "Choose Accent Color")
        if color.isValid():
            self.accent_color = color
            if self.dark_mode:
                self.apply_dark_mode()
            else:
                self.apply_light_mode()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToDoApp()
    window.show()
    sys.exit(app.exec_())