/* eslint-disable react-refresh/only-export-components */
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

const defaultThemeConfig: ThemeConfig = {
    primary: "#2a2a2a",
    secondary: "#545454",
    accent: "#5ce1e6",
    text: "#ffffff",
};

// fixed colors used by the UI; kept internal to this module
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
    const [themeConfig, setThemeConfig] = useState<ThemeConfig>(defaultThemeConfig);

    useEffect(() => {
        const storedTheme = localStorage.getItem("theme") as Theme | null;
        const storedConfig = localStorage.getItem("themeConfig");
        if (storedTheme) setTheme(storedTheme);
        if (storedConfig) {
            try {
                const parsed = JSON.parse(storedConfig) as Partial<ThemeConfig>;
                setThemeConfig((prev) => ({ ...prev, ...parsed }));
            } catch (err) {
                console.warn('Failed to parse stored themeConfig', err);
            }
        }
    }, []);

    useEffect(() => {
        const root = document.documentElement;
        // Aplicar theme como atributo (útil para selectors CSS [data-theme="light"])
        root.setAttribute("data-theme", theme);

        // Mapear basicamente themeConfig + fixedColors + background fallback
        const merged = { ...themeConfig, ...fixedColors };
        Object.entries(merged).forEach(([key, value]) => {
            root.style.setProperty(`--${key}`, value);
        });

        // garantir variáveis base usadas no CSS
        const background = theme === "light" ? "#f7f8fb" : "#0b0b0b";
        root.style.setProperty("--background", background);
        root.style.setProperty("--primary", themeConfig.primary);
        root.style.setProperty("--secondary", themeConfig.secondary);
        root.style.setProperty("--accent", themeConfig.accent);
        root.style.setProperty("--text", themeConfig.text);

        localStorage.setItem("themeConfig", JSON.stringify(themeConfig));
    }, [themeConfig, theme]);

    const toggleTheme = () => {
        const newTheme = theme === "light" ? "dark" : "light";
        setTheme(newTheme);
        localStorage.setItem("theme", newTheme);
    };

    const updateThemeConfig = (key: keyof ThemeConfig, value: string) => {
        setThemeConfig((prev) => ({ ...prev, [key]: value }));
    };

    const resetThemeConfig = () => {
        setThemeConfig(defaultThemeConfig);
    };

    const exportThemeConfig = () => {
        return JSON.stringify(themeConfig, null, 2);
    };

    const importThemeConfig = (json: string) => {
        try {
            const parsed = JSON.parse(json) as Partial<ThemeConfig>;
            // merge with defaults and validate keys present
            const merged: ThemeConfig = { ...defaultThemeConfig, ...parsed };
            setThemeConfig(merged);
        } catch (error) {
            console.error("Invalid theme config JSON: ", error);
            throw error;
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