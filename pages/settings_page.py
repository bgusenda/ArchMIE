# pages/settings_page.py
# === Imports === #
import tkinter as tk
from tkinter import colorchooser, messagebox
from theme_variables import save_theme, load_theme

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
            text="Theme Settings",
            bg=self.theme["bg_color"],
            fg=self.theme["text_color"],
            font=("Segoe UI", 18, "bold")
        )
        header_label.pack(pady=(30, 20))

        # === Theme Mode Selection === #
        self.create_mode_selection()

        # === Accent Color Selection === #
        self.create_color_selection()

        # === Navigation Buttons === #
        self.create_buttons()

    def create_mode_selection(self):
        """Create theme mode selection widgets"""
    def create_mode_selection(self):
        """Create theme mode selection widgets"""
        mode_frame = tk.Frame(self, bg=self.theme["bg_color"])
        mode_frame.pack(pady=20)

        mode_label = tk.Label(
            mode_frame,
            text="Theme Mode:",
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
    def create_color_selection(self):
        """Create accent color selection widgets"""
        accent_frame = tk.Frame(self, bg=self.theme["bg_color"])
        accent_frame.pack(pady=30)

        color_label = tk.Label(
            accent_frame,
            text="Accent Color:",
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

    def create_buttons(self):
        """Create navigation and action buttons"""
        button_frame = tk.Frame(self, bg=self.theme["bg_color"])
        button_frame.pack(pady=40, fill="x", padx=50)

        # Back button
        back_button = tk.Button(
            button_frame,
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

        # Save button
        save_button = tk.Button(
            button_frame,
            text="💾 Save Theme",
            bg=self.accent_color,
            fg="white",
            font=("Segoe UI", 12, "bold"),
            relief="flat",
            padx=25,
            pady=12,
            command=self.save_theme_action,
            activebackground=self.accent_color
        )
        save_button.pack(side="right")

    # === Event Handlers === #
    def pick_color(self):
        """Open color picker dialog"""
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