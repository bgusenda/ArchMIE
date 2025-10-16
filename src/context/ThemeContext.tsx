import { createContext, useContext, useEffect, useState } from "react";
import type { ReactNode } from "react";

type Theme = "light" | "dark";

interface ThemeConfig {
    primary: string;
    secondary: string;
    accent: string;
    text: string;
}

interface ThemeContextType {
    theme: Theme;
    themeConfig: ThemeConfig;
    toggleTheme: () => void;
    updateThemeConfig: (key: keyof ThemeConfig, value: string) => void;
    resetThemeConfig: () => void;
    exportThemeConfig: () => string;
    importThemeConfig: (json: string) => void;
}

const defaulThemeConfig: ThemeConfig = {
    primary: "#2a2a2a",
    secondary: "#545454",
    accent: "#5ce1e6",
    text: "#ffffff",
};

const fixedColors = {
    "header-color": "#171717",
    "run-command-btn": "#5e17eb",
    "edit-command-btn": "#ff7a00",
    "save-command-btn": "#7ed957",
    "delete-command-btn": "#ff0000",
    "command-accent": "#19898d",
};

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const ThemeProvider = ({ children }: { children: ReactNode }) => {
    const [theme, setTheme] = useState<Theme>("dark");
    const [themeConfig, setThemeConfig] = useState<ThemeConfig>(defaulThemeConfig);

    useEffect(() => {
        const storedTheme = localStorage.getItem("theme") as Theme | null;
        const storedConfig = localStorage.getItem("themeConfig");
        if (storedTheme) setTheme(storedTheme);
        if (storedConfig) setThemeConfig(JSON.parse(storedConfig));
    }, []);

    useEffect(() => {
        const root = document.documentElement;
        Object.entries({ ...themeConfig, ...fixedColors }).forEach(([key, value]) => {
            root.style.setProperty(`--${key}`, value);
        });
        localStorage.setItem("themeConfig", JSON.stringify(themeConfig));
    }, [themeConfig]);

    const toggleTheme = () => {
        const newTheme = theme === "light" ? "dark" : "light";
        setTheme(newTheme);
        localStorage.setItem("theme", newTheme);
    };

    const updateThemeConfig = (key: keyof ThemeConfig, value: string) => {
        setThemeConfig((prev) => ({ ...prev, [key]: value }));
    };

    const resetThemeConfig = () => {
        setThemeConfig(defaulThemeConfig);
    };

    const exportThemeConfig = () => {
        return JSON.stringify(themeConfig, null, 2);
    };

    const importThemeConfig = (json: string) => {
        try {
            const parsed = JSON.parse(json) as ThemeConfig;
            setThemeConfig(parsed);
        } catch (error) {
            console.error("Invalid theme config JSON: ", error);
        }
    };

    return (
        <ThemeContext.Provider
            value={{
                theme,
                themeConfig,
                toggleTheme,
                updateThemeConfig,
                resetThemeConfig,
                exportThemeConfig,
                importThemeConfig,
            }}
        >
            {children}
        </ThemeContext.Provider>
    );
};

export const useTheme = () => {
    const context = useContext(ThemeContext);
    if (!context) throw new Error("useTheme must be used within a ThemeProvider");
    return context;
};