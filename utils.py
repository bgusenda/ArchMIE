# utils.py
# === Imports === #
import tkinter as tk
from tkinter import simpledialog, messagebox
import datetime
import os
import subprocess
from pathlib import Path

# === Constants === #
LOG_FILE = "archMIE.log"

# === Password Dialog Class === #
class PasswordDialog:
    def __init__(self, parent, title="Enter Password"):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("350x180")
        self.dialog.configure(bg=parent.theme["bg_color"])
        self.dialog.grab_set()
        self.dialog.resizable(False, False)
        
        # Center the dialog
        self.dialog.transient(parent)
        
        # Create UI
        self.create_widgets(parent)
        
        # Focus on password entry
        self.password_entry.focus()
        
        # Bind Enter key
        self.dialog.bind('<Return>', lambda e: self.ok_clicked())
        self.dialog.bind('<Escape>', lambda e: self.cancel_clicked())
        
    def create_widgets(self, parent):
        """Create password dialog widgets"""
        # Icon and message
        message_frame = tk.Frame(self.dialog, bg=parent.theme["bg_color"])
        message_frame.pack(pady=20)
        
        tk.Label(
            message_frame,
            text="🔐 Administrator Password Required",
            bg=parent.theme["bg_color"],
            fg=parent.theme["text_color"],
            font=("Segoe UI", 12, "bold")
        ).pack()
        
        tk.Label(
            message_frame,
            text="Enter your password to execute system command:",
            bg=parent.theme["bg_color"],
            fg=parent.theme["text_color"],
            font=("Segoe UI", 10)
        ).pack(pady=(5, 15))
        
        # Password entry
        self.password_entry = tk.Entry(
            message_frame,
            show="*",
            bg=parent.theme["button_color"],
            fg=parent.theme["text_color"],
            font=("Segoe UI", 11),
            width=25,
            relief="flat",
            bd=5
        )
        self.password_entry.pack(pady=5)
        
        # Buttons
        button_frame = tk.Frame(self.dialog, bg=parent.theme["bg_color"])
        button_frame.pack(pady=20)
        
        tk.Button(
            button_frame,
            text="✓ OK",
            bg=parent.theme["accent_color"],
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=8,
            relief="flat",
            command=self.ok_clicked
        ).pack(side="left", padx=10)
        
        tk.Button(
            button_frame,
            text="✗ Cancel",
            bg=parent.theme["button_color"],
            fg=parent.theme["text_color"],
            font=("Segoe UI", 10),
            padx=20,
            pady=8,
            relief="flat",
            command=self.cancel_clicked
        ).pack(side="right", padx=10)
    
    def ok_clicked(self):
        """Handle OK button click"""
        self.result = self.password_entry.get()
        self.dialog.destroy()
    
    def cancel_clicked(self):
        """Handle Cancel button click"""
        self.result = None
        self.dialog.destroy()
    
    def get_password(self):
        """Wait for dialog to close and return password"""
        self.dialog.wait_window()
        return self.result

# === Logging Functions === #
def log_action(action, status, details="", command=""):
    """Log command execution results"""
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {status.upper()}: {action}\n"
        
        if command:
            log_entry += f"  Command: {command}\n"
        
        if details:
            log_entry += f"  Details: {details}\n"
        
        log_entry += "-" * 50 + "\n"
        
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
            
    except Exception as e:
        print(f"Error writing to log: {e}")

def get_log_content():
    """Read and return log file content"""
    try:
        if not os.path.exists(LOG_FILE):
            return "No log entries found."
        
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        
        return content if content.strip() else "Log file is empty."
    
    except Exception as e:
        return f"Error reading log file: {e}"

def clear_log():
    """Clear the log file"""
    try:
        if os.path.exists(LOG_FILE):
            open(LOG_FILE, "w").close()
        return True
    except Exception:
        return False

def get_log_file_path():
    """Get absolute path of log file"""
    return os.path.abspath(LOG_FILE)

def open_log_directory():
    """Open the directory containing the log file"""
    try:
        log_dir = os.path.dirname(get_log_file_path())
        if os.name == 'nt':  # Windows
            os.startfile(log_dir)
        elif os.name == 'posix':  # Linux/Mac
            subprocess.run(['xdg-open', log_dir])
        return True
    except Exception:
        return False

# === Import/Export Functions === #
def export_commands(commands_list, file_path):
    """Export commands list to JSON file"""
    try:
        import json
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(commands_list, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        return False, str(e)

def import_commands(file_path):
    """Import commands list from JSON file"""
    try:
        import json
        with open(file_path, 'r', encoding='utf-8') as f:
            commands = json.load(f)
        
        # Validate format
        if not isinstance(commands, list):
            return False, "Invalid file format: must be a list"
        
        for cmd in commands:
            if not isinstance(cmd, dict) or 'name' not in cmd or 'command' not in cmd:
                return False, "Invalid command format: each command must have 'name' and 'command' fields"
        
        return True, commands
    
    except json.JSONDecodeError:
        return False, "Invalid JSON file"
    except Exception as e:
        return False, str(e)

# === Secure Command Execution === #
def execute_secure_command(command, password=None, timeout=30):
    """Execute command securely with optional password"""
    try:
        if password and command.startswith("sudo"):
            # Use echo to pass password to sudo
            full_command = f"echo '{password}' | sudo -S {command[5:]}"
        else:
            full_command = command
        
        result = subprocess.run(
            full_command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        return result
    
    except subprocess.TimeoutExpired:
        raise subprocess.TimeoutExpired(command, timeout)
    except Exception as e:
        raise e