# pages/settings_page.py
# === Imports === #
import tkinter as tk
from tkinter import colorchooser, messagebox, filedialog, scrolledtext
from theme_variables import save_theme, load_theme
from utils import get_log_content, clear_log, get_log_file_path, open_log_directory, export_commands, import_commands
import json
import os

# === Settings Page Class === #
class SettingsPage(tk.Frame):
    def __init__(self, parent, app_reference):
        super().__init__(parent, bg=app_reference.theme["bg_color"])
        self.app = app_reference  # Reference to the main window
        self.theme = app_reference.theme  # Current theme

        # === Theme Variables === #
        self.mode_var = tk.StringVar(value="light" if self.theme["light_mode"] else "dark")
        self.accent_color = self.theme["accent_color"]

        # === Initialize UI === #
        self.create_widgets()

    def create_widgets(self):
        """Create and configure all UI widgets"""
        # === Page Header === #
        header_label = tk.Label(
            self,
            text="Settings",
            bg=self.theme["bg_color"],
            fg=self.theme["text_color"],
            font=("Segoe UI", 18, "bold")
        )
        header_label.pack(pady=(30, 20))

        # === Create Notebook for tabs === #
        self.create_notebook()

    def create_notebook(self):
        """Create tabbed interface for settings"""
        # Simple tab simulation using frames
        tab_frame = tk.Frame(self, bg=self.theme["bg_color"])
        tab_frame.pack(fill="x", padx=20)

        # Tab buttons
        self.current_tab = "theme"
        
        self.theme_tab_btn = tk.Button(
            tab_frame,
            text="🎨 Theme",
            bg=self.theme["accent_color"],
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=20,
            pady=8,
            command=lambda: self.switch_tab("theme")
        )
        self.theme_tab_btn.pack(side="left", padx=2)

        self.logs_tab_btn = tk.Button(
            tab_frame,
            text="📋 Logs",
            bg=self.theme["button_color"],
            fg=self.theme["text_color"],
            font=("Segoe UI", 11),
            relief="flat",
            padx=20,
            pady=8,
            command=lambda: self.switch_tab("logs")
        )
        self.logs_tab_btn.pack(side="left", padx=2)

        self.commands_tab_btn = tk.Button(
            tab_frame,
            text="⚙️ Commands",
            bg=self.theme["button_color"],
            fg=self.theme["text_color"],
            font=("Segoe UI", 11),
            relief="flat",
            padx=20,
            pady=8,
            command=lambda: self.switch_tab("commands")
        )
        self.commands_tab_btn.pack(side="left", padx=2)

        # Content frame
        self.content_frame = tk.Frame(self, bg=self.theme["bg_color"])
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Show initial tab
        self.switch_tab("theme")

    def switch_tab(self, tab_name):
        """Switch between different tabs"""
        # Update button styles
        buttons = [self.theme_tab_btn, self.logs_tab_btn, self.commands_tab_btn]
        for btn in buttons:
            btn.configure(
                bg=self.theme["button_color"],
                fg=self.theme["text_color"],
                font=("Segoe UI", 11)
            )

        # Highlight active tab
        if tab_name == "theme":
            self.theme_tab_btn.configure(
                bg=self.theme["accent_color"],
                fg="white",
                font=("Segoe UI", 11, "bold")
            )
        elif tab_name == "logs":
            self.logs_tab_btn.configure(
                bg=self.theme["accent_color"],
                fg="white",
                font=("Segoe UI", 11, "bold")
            )
        elif tab_name == "commands":
            self.commands_tab_btn.configure(
                bg=self.theme["accent_color"],
                fg="white",
                font=("Segoe UI", 11, "bold")
            )

        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Show appropriate content
        self.current_tab = tab_name
        if tab_name == "theme":
            self.create_theme_content()
        elif tab_name == "logs":
            self.create_logs_content()
        elif tab_name == "commands":
            self.create_commands_content()

    def create_theme_content(self):
        """Create theme configuration content"""
        # === Theme Mode Selection === #
        self.create_mode_selection()

        # === Accent Color Selection === #
        self.create_color_selection()

        # === Save Theme Button === #
        save_button = tk.Button(
            self.content_frame,
            text="💾 Save Theme",
            bg=self.theme["accent_color"],
            fg="white",
            font=("Segoe UI", 12, "bold"),
            relief="flat",
            padx=30,
            pady=12,
            command=self.save_theme_action,
            activebackground=self.theme["accent_color"]
        )
        save_button.pack(pady=30)

        # Back button for theme tab
        back_button = tk.Button(
            self.content_frame,
            text="← Back to Home",
            bg=self.theme["button_color"],
            fg=self.theme["text_color"],
            font=("Segoe UI", 12),
            relief="flat",
            padx=30,
            pady=12,
            command=self.back_to_home,
            activebackground=self.theme["header_color"]
        )
        back_button.pack(pady=20)

    def create_logs_content(self):
        """Create logs viewer content"""
        # Log viewer label
        log_label = tk.Label(
            self.content_frame,
            text="📋 System Logs",
            bg=self.theme["bg_color"],
            fg=self.theme["text_color"],
            font=("Segoe UI", 14, "bold")
        )
        log_label.pack(pady=(10, 15))

        # Log text area
        log_frame = tk.Frame(self.content_frame, bg=self.theme["bg_color"])
        log_frame.pack(fill="both", expand=True, pady=10)

        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            bg=self.theme["button_color"],
            fg=self.theme["text_color"],
            font=("Consolas", 9),
            height=15,
            relief="flat",
            bd=5
        )
        self.log_text.pack(fill="both", expand=True)

        # Load and display logs
        self.refresh_logs()

        # Log control buttons
        log_buttons_frame = tk.Frame(self.content_frame, bg=self.theme["bg_color"])
        log_buttons_frame.pack(pady=15)

        tk.Button(
            log_buttons_frame,
            text="🔄 Refresh",
            bg=self.theme["accent_color"],
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=15,
            pady=8,
            command=self.refresh_logs
        ).pack(side="left", padx=5)

        tk.Button(
            log_buttons_frame,
            text="🗑️ Clear Logs",
            bg="#d9534f",
            fg="white",
            font=("Segoe UI", 10),
            relief="flat",
            padx=15,
            pady=8,
            command=self.clear_logs
        ).pack(side="left", padx=5)

        tk.Button(
            log_buttons_frame,
            text="📁 Open Location",
            bg=self.theme["button_color"],
            fg=self.theme["text_color"],
            font=("Segoe UI", 10),
            relief="flat",
            padx=15,
            pady=8,
            command=self.open_log_location
        ).pack(side="left", padx=5)

        # Back button for logs tab
        back_button = tk.Button(
            self.content_frame,
            text="← Back to Home",
            bg=self.theme["button_color"],
            fg=self.theme["text_color"],
            font=("Segoe UI", 12),
            relief="flat",
            padx=30,
            pady=12,
            command=self.back_to_home,
            activebackground=self.theme["header_color"]
        )
        back_button.pack(pady=20)

    def create_commands_content(self):
        """Create commands management content"""
        # Commands management label
        cmd_label = tk.Label(
            self.content_frame,
            text="⚙️ Commands Management",
            bg=self.theme["bg_color"],
            fg=self.theme["text_color"],
            font=("Segoe UI", 14, "bold")
        )
        cmd_label.pack(pady=(10, 20))

        # Import/Export section
        ie_frame = tk.Frame(self.content_frame, bg=self.theme["bg_color"])
        ie_frame.pack(pady=20)

        tk.Label(
            ie_frame,
            text="📦 Import/Export Commands",
            bg=self.theme["bg_color"],
            fg=self.theme["text_color"],
            font=("Segoe UI", 12, "bold")
        ).pack(pady=(0, 15))

        # Import/Export buttons
        ie_buttons_frame = tk.Frame(ie_frame, bg=self.theme["bg_color"])
        ie_buttons_frame.pack()

        tk.Button(
            ie_buttons_frame,
            text="📥 Import Commands",
            bg="#5cb85c",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=20,
            pady=10,
            command=self.import_commands
        ).pack(side="left", padx=10)

        tk.Button(
            ie_buttons_frame,
            text="📤 Export Commands",
            bg="#5bc0de",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=20,
            pady=10,
            command=self.export_commands
        ).pack(side="right", padx=10)

        # Info text
        info_text = tk.Label(
            ie_frame,
            text="Import/Export your command list as JSON files\nfor backup or sharing purposes.",
            bg=self.theme["bg_color"],
            fg=self.theme["text_color"],
            font=("Segoe UI", 10),
            justify="center"
        )
        info_text.pack(pady=15)

        # Back button at bottom
        back_button = tk.Button(
            self.content_frame,
            text="← Back to Home",
            bg=self.theme["button_color"],
            fg=self.theme["text_color"],
            font=("Segoe UI", 12),
            relief="flat",
            padx=30,
            pady=12,
            command=self.back_to_home,
            activebackground=self.theme["header_color"]
        )
        back_button.pack(side="bottom", pady=20)

    def create_mode_selection(self):
        """Create theme mode selection widgets"""
        mode_frame = tk.Frame(self.content_frame, bg=self.theme["bg_color"])
        mode_frame.pack(pady=20)

        mode_label = tk.Label(
            mode_frame,
            text="🤯 Theme Mode:",
            bg=self.theme["bg_color"],
            fg=self.theme["text_color"],
            font=("Segoe UI", 14, "bold")
        )
        mode_label.pack(pady=(0, 10))

        # Radio buttons container
        radio_container = tk.Frame(mode_frame, bg=self.theme["bg_color"])
        radio_container.pack()

        # Light mode radio button
        light_radio = tk.Radiobutton(
            radio_container,
            text="☀️ Light Mode",
            variable=self.mode_var,
            value="light",
            bg=self.theme["bg_color"],
            fg=self.theme["text_color"],
            selectcolor=self.theme["bg_color"],
            font=("Segoe UI", 12),
            activebackground=self.theme["bg_color"],
            activeforeground=self.theme["accent_color"]
        )
        light_radio.pack(side="left", padx=15)

        # Dark mode radio button
        dark_radio = tk.Radiobutton(
            radio_container,
            text="🌙 Dark Mode",
            variable=self.mode_var,
            value="dark",
            bg=self.theme["bg_color"],
            fg=self.theme["text_color"],
            selectcolor=self.theme["bg_color"],
            font=("Segoe UI", 12),
            activebackground=self.theme["bg_color"],
            activeforeground=self.theme["accent_color"]
        )
        dark_radio.pack(side="left", padx=15)

    def create_color_selection(self):
        """Create accent color selection widgets"""
        accent_frame = tk.Frame(self.content_frame, bg=self.theme["bg_color"])
        accent_frame.pack(pady=30)

        color_label = tk.Label(
            accent_frame,
            text="🐐 Accent Color:",
            bg=self.theme["bg_color"],
            fg=self.theme["text_color"],
            font=("Segoe UI", 14, "bold")
        )
        color_label.pack(pady=(0, 15))

        # Color picker container
        color_container = tk.Frame(accent_frame, bg=self.theme["bg_color"])
        color_container.pack()

        # Color preview
        self.color_preview = tk.Frame(
            color_container,
            bg=self.accent_color,
            width=30,
            height=30,
            relief="solid",
            bd=2
        )
        self.color_preview.pack(side="left", padx=(0, 10))
        self.color_preview.pack_propagate(False)

        # Color picker button
        self.color_button = tk.Button(
            color_container,
            text="🎨 Pick Color",
            bg=self.theme["button_color"],
            fg=self.theme["text_color"],
            font=("Segoe UI", 12),
            relief="flat",
            padx=20,
            pady=8,
            command=self.pick_color,
            activebackground=self.theme["accent_color"],
            activeforeground="white"
        )
        self.color_button.pack(side="left")

    # === Event Handlers === #
    def pick_color(self):
        """Open color picker dialog"""
        color_code = colorchooser.askcolor(
            title="Choose Accent Color",
            color=self.accent_color
        )
        if color_code[1]:  # color_code[1] contains the HEX value
            self.accent_color = color_code[1]
            self.color_preview.configure(bg=self.accent_color)

    def save_theme_action(self):
        """Save theme settings and restart application"""
        try:
            # Update the theme according to user's choice
            new_theme = self.theme.copy()
            new_theme["accent_color"] = self.accent_color

            if self.mode_var.get() == "light":
                new_theme.update({
                    "bg_color": "#f2f2f2",
                    "header_color": "#e6e6e6",
                    "text_color": "#000000",
                    "button_color": "#d4d4d4",
                    "light_mode": True
                })
            else:
                new_theme.update({
                    "bg_color": "#1e1e1e",
                    "header_color": "#252526",
                    "text_color": "#ffffff",
                    "button_color": "#3a3d41",
                    "light_mode": False
                })

            # Save to JSON file
            save_theme(new_theme)

            # Update main app theme and restart
            self.app.theme = new_theme
            messagebox.showinfo("Success", "Theme saved successfully!\nApplication will restart.")
            self.app.destroy()  # Close current window
            self.app.__class__()  # Restart the application

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save theme: {str(e)}")

    def back_to_home(self):
        """Return to the homepage"""
        self.app.show_homepage()

    # === New Functions for Logs Management === #
    def refresh_logs(self):
        """Refresh the log display"""
        if hasattr(self, 'log_text'):
            self.log_text.delete("1.0", tk.END)
            log_content = get_log_content()
            self.log_text.insert("1.0", log_content)
            self.log_text.see(tk.END)  # Scroll to bottom

    def clear_logs(self):
        """Clear the log file"""
        if messagebox.askyesno("Clear Logs", "Are you sure you want to clear all logs?"):
            if clear_log():
                messagebox.showinfo("Success", "Logs cleared successfully!")
                self.refresh_logs()
            else:
                messagebox.showerror("Error", "Failed to clear logs!")

    def open_log_location(self):
        """Open the directory containing the log file"""
        if open_log_directory():
            messagebox.showinfo("Location", f"Log file location:\n{get_log_file_path()}")
        else:
            messagebox.showerror("Error", "Failed to open log directory!")

    # === New Functions for Commands Import/Export === #
    def import_commands(self):
        """Import commands from JSON file"""
        file_path = filedialog.askopenfilename(
            title="Import Commands",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            defaultextension=".json"
        )
        
        if file_path:
            success, result = import_commands(file_path)
            if success:
                # Load current commands from the app
                from pathlib import Path
                commands_file = Path("commands.json")
                
                if messagebox.askyesno(
                    "Import Commands", 
                    f"Found {len(result)} commands to import.\nReplace existing commands?"
                ):
                    try:
                        with open(commands_file, 'w', encoding='utf-8') as f:
                            json.dump(result, f, indent=4, ensure_ascii=False)
                        messagebox.showinfo("Success", f"Successfully imported {len(result)} commands!")
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to save imported commands: {str(e)}")
            else:
                messagebox.showerror("Import Error", f"Failed to import commands:\n{result}")

    def export_commands(self):
        """Export commands to JSON file"""
        try:
            # Load current commands
            from pathlib import Path
            commands_file = Path("commands.json")
            
            if not commands_file.exists():
                messagebox.showwarning("Warning", "No commands file found!")
                return
            
            with open(commands_file, 'r', encoding='utf-8') as f:
                commands_list = json.load(f)
            
            if not commands_list:
                messagebox.showwarning("Warning", "No commands to export!")
                return
            
            file_path = filedialog.asksaveasfilename(
                title="Export Commands",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                defaultextension=".json",
                initialfile="archMIE_commands_backup.json"
            )
            
            if file_path:
                success, error = export_commands(commands_list, file_path)
                if success:
                    messagebox.showinfo("Success", f"Successfully exported {len(commands_list)} commands!")
                else:
                    messagebox.showerror("Export Error", f"Failed to export commands:\n{error}")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export commands: {str(e)}")