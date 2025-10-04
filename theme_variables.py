# theme_variables.py
# === Imports === #
import json
import os

# === Constants === #
THEME_FILE = "theme.json"

# === Default Themes === #
default_dark_theme = {
    "bg_color": "#1e1e1e",
    "header_color": "#252526",
    "text_color": "#ffffff",
    "accent_color": "#569cd6",
    "button_color": "#3a3d41",
    "light_mode": False
}

default_light_theme = {
    "bg_color": "#f2f2f2",
    "header_color": "#e6e6e6",
    "text_color": "#000000",
    "accent_color": "#007acc",
    "button_color": "#d4d4d4",
    "light_mode": True
}

# === Theme Management Functions === #
def load_theme():
    """Load current theme from the JSON file, or create a default one"""
    if not os.path.exists(THEME_FILE):
        save_theme(default_dark_theme)
        return default_dark_theme

    try:
        with open(THEME_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        # If file is corrupted or missing, return default theme
        save_theme(default_dark_theme)
        return default_dark_theme

def save_theme(theme_dict):
    """Save current theme to a JSON file"""
    try:
        with open(THEME_FILE, "w") as file:
            json.dump(theme_dict, file, indent=4)
    except IOError as e:
        print(f"Error saving theme: {e}")

def toggle_theme(current_theme):
    """Toggle between light and dark mode"""
    new_theme = (
        default_light_theme.copy() if not current_theme["light_mode"] 
        else default_dark_theme.copy()
    )
    save_theme(new_theme)
    return new_theme