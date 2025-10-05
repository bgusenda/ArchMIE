# index.py
# Imports
import tkinter as tk
from theme_variables import load_theme, toggle_theme
from pages.commands_page import CommandsPage
from pages.settings_page import SettingsPage

# App class
class App(tk.Tk): # Main window
    def __init__(self):
        super().__init__()

        # === Load set theme === #
        self.theme = load_theme()

        # === Main Window Setup === #
        self.title("ArchMie")
        self.geometry("900x680")
        self.configure(bg=self.theme["bg_color"])
        self.resizable(False, False)

        # === Main Grid === #
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
            # makes the main frame grow along the window

        # === Header === #
        header = tk.Frame(self, bg=self.theme["header_color"], height=60)
        header.grid(row=0, column=0, sticky="ew") # sticky="ew" uses whole available space

        title_label = tk.Label(
            header,
            text="ArchMIE",
            bg=self.theme["header_color"],
            fg=self.theme["accent_color"],
            font=("Segoe UI", 18, "bold")
        )
        title_label.pack(pady=10)

        # === Main Area === #
        self.main_frame = tk.Frame(self, bg=self.theme["bg_color"])
        self.main_frame.grid(row=1, column=0, sticky="nsew")

        # Starts with the homepage
        self.show_homepage()

    def toggle_theme_action(self):
        """Alternate between light and dark mode"""
        self.theme = toggle_theme(self.theme)
        self.destroy()
        start_app()

    def reload_theme(self):
        """Update all colors in the window"""
        self.configure(bg=self.theme["bg_color"])

        for widget in self.winfo_children():
            widget.destroy() # recreate with the new theme

        self.__init__() # restart the window with the new theme

    def show_homepage(self):
        # Clean current frame (in order to later change page)
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # === HomePage Content === #
        home_label = tk.Label(
            self.main_frame,
            text="Welcome to the ArchMIE!",
            bg=self.theme["bg_color"],
            fg=self.theme["text_color"],
            font=("Segoe UI",16)
        )
        home_label.pack(pady=50)

        # Main page buttons
        btn_commands = tk.Button(
            self.main_frame,
            text="Commands List",
            bg=self.theme["accent_color"],
            fg="white",
            font=("Segoe UI", 12, "bold"),
            relief="flat",
            padx=40, pady=10,
            command=self.show_commands
        )
        btn_commands.pack(pady=10)

        btn_settings = tk.Button(
            self.main_frame,
            text="Settings",
            bg=self.theme["button_color"],
            fg=self.theme["text_color"],
            font=("Segoe UI", 12),
            relief="flat",
            padx=70, pady=10,
            command=self.show_settings
        )
        btn_settings.pack(pady=10)

        btn_exit = tk.Button(
            self.main_frame,
            text="Exit",
            bg=self.theme["button_color"],
            fg=self.theme["text_color"],
            font=("Segoe UI", 12),
            relief="flat",
            padx=87, pady=10,
            command=self.destroy
        )
        btn_exit.pack(pady=10)

    def show_commands(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        commands_page = CommandsPage(self.main_frame, self)
        commands_page.pack(fill="both", expand=True)

    # === Open settings page function === #
    def show_settings(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Instance SettingsPage inside of main_frame
        settings_page = SettingsPage(self.main_frame, self)
        settings_page.pack(fill="both", expand=True)

# Start App function
def start_app():
    app = App()
    app.mainloop()

# App execution
if __name__ == "__main__":
    start_app()