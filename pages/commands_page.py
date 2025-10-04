# pages/commands_page.py
# === Imports === #
import tkinter as tk
from tkinter import messagebox
import json
import subprocess
from pathlib import Path

# === Commands Page Class === #
class CommandsPage(tk.Frame):
    def __init__(self, parent, app_reference, json_path="commands.json"):
        super().__init__(parent, bg=app_reference.theme["bg_color"])
        self.app = app_reference
        self.theme = app_reference.theme
        self.json_path = Path(json_path)
        self.commands_list = []

        # === Initialize UI === #
        self.create_widgets()
        self.load_commands()

    def create_widgets(self):
        """Create and configure all UI widgets"""
        # === Page Header === #
        header_label = tk.Label(
            self,
            text="ArchMIE Commands",
            bg=self.theme["bg_color"],
            fg=self.theme["accent_color"],
            font=("Segoe UI", 18, "bold")
        )
        header_label.pack(pady=(30, 20))

        # === Commands List Section === #
        self.create_commands_list()

        # === Command Editor Section === #
        self.create_command_editor()

        # === Execution Options === #
        self.create_execution_options()

        # === Action Buttons === #
        self.create_action_buttons()

    def create_commands_list(self):
        """Create the commands list with scrollbar"""
        list_container = tk.Frame(self, bg=self.theme["bg_color"])
        list_container.pack(pady=10, fill="x", padx=50)

        # Add button to create a new command
        add_button = tk.Button(
            list_container,
            text="➕ Add Command",
            bg=self.theme["accent_color"],
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=15,
            pady=8,
            command=self.add_command_popup,
            activebackground=self.theme["accent_color"]
        )
        add_button.pack(anchor="e", pady=(0, 10))

        # List label
        list_label = tk.Label(
            list_container,
            text="📋 Available Commands:",
            bg=self.theme["bg_color"],
            fg=self.theme["text_color"],
            font=("Segoe UI", 12, "bold")
        )
        list_label.pack(anchor="w", pady=(0, 10))

        # List frame with scrollbar
        list_frame = tk.Frame(list_container, bg=self.theme["bg_color"])
        list_frame.pack(fill="x")

        self.listbox = tk.Listbox(
            list_frame,
            bg=self.theme["button_color"],
            fg=self.theme["text_color"],
            font=("Segoe UI", 11),
            selectbackground=self.theme["accent_color"],
            selectforeground="white",
            height=6,
            relief="flat",
            bd=2,
            highlightthickness=0
        )
        self.listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame, bg=self.theme["button_color"])
        scrollbar.pack(side="right", fill="y")

        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)
        self.listbox.bind("<<ListboxSelect>>", self.on_select_command)

    def create_command_editor(self):
        """Create the command editor section"""
        editor_container = tk.Frame(self, bg=self.theme["bg_color"])
        editor_container.pack(pady=20, fill="x", padx=50)

        # Editor label
        editor_label = tk.Label(
            editor_container,
            text="✏️ Selected Command:",
            bg=self.theme["bg_color"],
            fg=self.theme["text_color"],
            font=("Segoe UI", 12, "bold")
        )
        editor_label.pack(anchor="w", pady=(0, 10))

        # Command entry field
        self.command_entry = tk.Entry(
            editor_container,
            bg=self.theme["button_color"],
            fg=self.theme["text_color"],
            font=("Segoe UI", 11),
            relief="flat",
            bd=5,
            highlightthickness=0
        )
        self.command_entry.pack(fill="x", ipady=8)

    def create_execution_options(self):
        """Create execution scope options"""
        options_container = tk.Frame(self, bg=self.theme["bg_color"])
        options_container.pack(pady=20)

        # Options label
        options_label = tk.Label(
            options_container,
            text="⚙️ Execution Scope:",
            bg=self.theme["bg_color"],
            fg=self.theme["text_color"],
            font=("Segoe UI", 12, "bold")
        )
        options_label.pack(pady=(0, 10))

        # Scope frame
        self.scope_frame = tk.Frame(options_container, bg=self.theme["bg_color"])
        self.scope_frame.pack()

        self.system_var = tk.BooleanVar()
        self.user_var = tk.BooleanVar()

        # System scope checkbox
        system_check = tk.Checkbutton(
            self.scope_frame,
            text="🔧 System",
            variable=self.system_var,
            bg=self.theme["bg_color"],
            fg=self.theme["text_color"],
            font=("Segoe UI", 11),
            selectcolor=self.theme["bg_color"],
            activebackground=self.theme["bg_color"],
            activeforeground=self.theme["accent_color"]
        )
        system_check.pack(side="left", padx=20)

        # User scope checkbox
        user_check = tk.Checkbutton(
            self.scope_frame,
            text="👤 User",
            variable=self.user_var,
            bg=self.theme["bg_color"],
            fg=self.theme["text_color"],
            font=("Segoe UI", 11),
            selectcolor=self.theme["bg_color"],
            activebackground=self.theme["bg_color"],
            activeforeground=self.theme["accent_color"]
        )
        user_check.pack(side="left", padx=20)

    def create_action_buttons(self):
        """Create action buttons"""
        button_container = tk.Frame(self, bg=self.theme["bg_color"])
        button_container.pack(pady=30, fill="x", padx=50)

        # Back button
        back_button = tk.Button(
            button_container,
            text="← Back",
            bg=self.theme["button_color"],
            fg=self.theme["text_color"],
            font=("Segoe UI", 12),
            relief="flat",
            padx=25,
            pady=12,
            command=self.back_to_home,
            activebackground=self.theme["header_color"]
        )
        back_button.pack(side="left")

        # Delete button
        delete_button = tk.Button(
            button_container,
            text="🗑️ Delete",
            bg="#d9534f",
            fg="white",
            font=("Segoe UI", 12),
            relief="flat",
            padx=20,
            pady=12,
            command=self.delete_command,
            activebackground="#c9302c"
        )
        delete_button.pack(side="left", padx=(10, 0))

        # Save changes button
        save_button = tk.Button(
            button_container,
            text="💾 Save Changes",
            bg="#5cb85c",
            fg="white",
            font=("Segoe UI", 12),
            relief="flat",
            padx=20,
            pady=12,
            command=self.save_command_edit,
            activebackground="#449d44"
        )
        save_button.pack(side="right", padx=(0, 10))

        # Execute button
        execute_button = tk.Button(
            button_container,
            text="▶️ Execute Command",
            bg=self.theme["accent_color"],
            fg="white",
            font=("Segoe UI", 12, "bold"),
            relief="flat",
            padx=25,
            pady=12,
            command=self.execute_command,
            activebackground=self.theme["accent_color"]
        )
        execute_button.pack(side="right")

    # === Data Management Methods === #
    def load_commands(self):
        """Load commands from JSON file"""
        try:
            if not self.json_path.exists():
                # Create default commands if file doesn't exist
                default_commands = [
                    {"name": "Update System", "command": "sudo pacman -Syu"},
                    {"name": "Install Package", "command": "sudo pacman -S {package}"},
                    {"name": "Remove Package", "command": "sudo pacman -R {package}"},
                    {"name": "List Installed Packages", "command": "pacman -Q"},
                    {"name": "Search Package", "command": "pacman -Ss {search_term}"}
                ]
                with open(self.json_path, "w") as f:
                    json.dump(default_commands, f, indent=4)

            with open(self.json_path, "r") as f:
                self.commands_list = json.load(f)

            # Populate the listbox
            self.listbox.delete(0, tk.END)
            for cmd in self.commands_list:
                self.listbox.insert(tk.END, cmd["name"])

        except (json.JSONDecodeError, IOError) as e:
            messagebox.showerror("Error", f"Failed to load commands: {str(e)}")

    def save_commands(self):
        """Save commands_list to JSON file"""
        try:
            with open(self.json_path, "w") as f:
                json.dump(self.commands_list, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save commands: {str(e)}")

    # === Event Handlers === #
    def on_select_command(self, event):
        """Handle command selection from listbox"""
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            command_text = self.commands_list[index]["command"]
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, command_text)

    def add_command_popup(self):
        """Open popup to add new command"""
        popup = tk.Toplevel(self)
        popup.title("Add New Command")
        popup.geometry("450x250")
        popup.configure(bg=self.theme["bg_color"])
        popup.grab_set()  # Focus on popup
        popup.resizable(False, False)

        # Center the popup
        popup.transient(self)

        # Name entry
        tk.Label(
            popup, 
            text="Command Name:", 
            bg=self.theme["bg_color"], 
            fg=self.theme["text_color"],
            font=("Segoe UI", 12)
        ).pack(pady=(20, 5))
        
        name_entry = tk.Entry(
            popup, 
            width=40,
            bg=self.theme["button_color"],
            fg=self.theme["text_color"],
            font=("Segoe UI", 11)
        )
        name_entry.pack(pady=5)

        # Command entry
        tk.Label(
            popup, 
            text="Command:", 
            bg=self.theme["bg_color"], 
            fg=self.theme["text_color"],
            font=("Segoe UI", 12)
        ).pack(pady=(15, 5))
        
        cmd_entry = tk.Entry(
            popup, 
            width=40,
            bg=self.theme["button_color"],
            fg=self.theme["text_color"],
            font=("Segoe UI", 11)
        )
        cmd_entry.pack(pady=5)

        # Button frame
        button_frame = tk.Frame(popup, bg=self.theme["bg_color"])
        button_frame.pack(pady=30)

        def save_new_command():
            name = name_entry.get().strip()
            cmd = cmd_entry.get().strip()
            if not name or not cmd:
                messagebox.showwarning("Warning", "Please fill both fields!")
                return
            self.commands_list.append({"name": name, "command": cmd})
            self.save_commands()
            self.load_commands()
            popup.destroy()
            messagebox.showinfo("Success", "Command added successfully!")

        # Save button
        tk.Button(
            button_frame, 
            text="💾 Save", 
            bg=self.theme["accent_color"], 
            fg="white",
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=8,
            command=save_new_command
        ).pack(side="left", padx=10)

        # Cancel button
        tk.Button(
            button_frame, 
            text="❌ Cancel", 
            bg=self.theme["button_color"], 
            fg=self.theme["text_color"],
            font=("Segoe UI", 11),
            padx=20,
            pady=8,
            command=popup.destroy
        ).pack(side="right", padx=10)

        # Focus on name entry
        name_entry.focus()

    def delete_command(self):
        """Delete selected command"""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Select a command to delete!")
            return
        
        index = selection[0]
        command_name = self.commands_list[index]['name']
        
        if messagebox.askyesno("Confirm Delete", f"Delete command '{command_name}'?"):
            self.commands_list.pop(index)
            self.save_commands()
            self.load_commands()
            self.command_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Command deleted successfully!")

    def save_command_edit(self):
        """Save changes to selected command"""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Select a command to edit!")
            return
        
        index = selection[0]
        new_cmd = self.command_entry.get().strip()
        if not new_cmd:
            messagebox.showwarning("Warning", "Command cannot be empty!")
            return
        
        self.commands_list[index]["command"] = new_cmd
        self.save_commands()
        self.load_commands()
        messagebox.showinfo("Success", "Command updated successfully!")

    def execute_command(self):
        """Execute the selected/edited command"""
        command_to_run = self.command_entry.get().strip()
        
        # Validation
        if not command_to_run:
            messagebox.showwarning("Warning", "No command to execute!")
            return
        
        if not self.system_var.get() and not self.user_var.get():
            messagebox.showwarning("Warning", "Please select execution scope (System or User)!")
            return

        # Prepare command
        final_command = command_to_run
        if self.system_var.get() and not final_command.startswith("sudo"):
            final_command = "sudo " + final_command

        # Confirmation dialog
        if not messagebox.askyesno(
            "Confirm Execution", 
            f"Execute command:\n\n{final_command}\n\nContinue?"
        ):
            return

        try:
            # Execute command
            result = subprocess.run(
                final_command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            if result.returncode == 0:
                messagebox.showinfo("Success", "Command executed successfully!")
                if result.stdout:
                    messagebox.showinfo("Output", result.stdout[:500])  # Show first 500 chars
            else:
                messagebox.showerror("Error", f"Command failed:\n{result.stderr}")
                
        except subprocess.TimeoutExpired:
            messagebox.showerror("Error", "Command timed out (30s limit)")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to execute command:\n{str(e)}")

    def back_to_home(self):
        """Return to the homepage"""
        self.app.show_homepage()
