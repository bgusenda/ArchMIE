import { useState } from "react";
import { useTheme } from "../context/ThemeContext";
import "./Settings.scss";

export default function Settings() {
    const {
        themeConfig,
        updateThemeConfig,
        resetThemeConfig,
        exportThemeConfig,
        importThemeConfig,
    } = useTheme();

    const [importValue, setImportValue] = useState("");
    const [isResetting, setIsResetting] = useState(false);

    const handleImport = () => {
        try {
            importThemeConfig(importValue);
            setImportValue("");
            // Feedback visual opcional
        } catch (error) {
            console.error("Erro ao importar configuração:", error);
        }
    };

    const handleExport = () => {
        const json = exportThemeConfig();
        const blob = new Blob([json], { type: "application/json" });
        const url = URL.createObjectURL(blob);

        const a = document.createElement("a");
        a.href = url;
        a.download = `theme-config-${new Date().toISOString().split('T')[0]}.json`;
        a.click();

        URL.revokeObjectURL(url);
    };

    const handleReset = async () => {
        setIsResetting(true);
        await new Promise(resolve => setTimeout(resolve, 300)); // Pequeno delay para animação
        resetThemeConfig();
        setIsResetting(false);
    };

    const fillWithPreview = () => {
        setImportValue(exportThemeConfig());
    };

    return (
        <div className="settings">
            <div className="settings__header">
                <h1 className="settings__title">Personalização do Tema</h1>
                <p className="settings__subtitle">
                    Customize as cores do seu tema e exporte/importe suas configurações
                </p>
            </div>

            <div className="settings__section">
                <h2 className="settings__section-title">Cores do Tema</h2>
                <div className="settings__grid">
                    {Object.entries(themeConfig).map(([key, value]) => (
                        <div key={key} className="settings__control">
                            <label className="settings__label">{key.replace(/([A-Z])/g, ' $1').toLowerCase()}</label>
                            <input
                                type="color"
                                value={value}
                                onChange={(e) =>
                                    updateThemeConfig(key as keyof typeof themeConfig, e.target.value)
                                }
                                className="settings__color-input"
                                title={`Alterar cor ${key}`}
                            />
                        </div>
                    ))}
                </div>
            </div>

            <div className="settings__section">
                <h2 className="settings__section-title">Ações Rápidas</h2>
                <div className="settings__actions">
                    <button
                        onClick={handleReset}
                        className={`btn btn--restore ${isResetting ? 'opacity-50' : ''}`}
                        disabled={isResetting}
                    >
                        {isResetting ? 'Restaurando...' : 'Restaurar Padrão'}
                    </button>
                    <button onClick={handleExport} className="btn btn--export">
                        Exportar Configuração
                    </button>
                </div>
            </div>

            <div className="settings__section">
                <h2 className="settings__section-title">Importar Configuração</h2>
                <div className="settings__textarea-container">
                    <label className="settings__textarea-label">
                        Cole o JSON da configuração
                    </label>
                    <textarea
                        placeholder='{"primary": "#000000", "secondary": "#ffffff", ...}'
                        value={importValue}
                        onChange={(e) => setImportValue(e.target.value)}
                        className="settings__textarea"
                        spellCheck="false"
                    />
                </div>

                <div className="settings__action-group">
                    <button
                        onClick={handleImport}
                        className="btn btn--import"
                        disabled={!importValue.trim()}
                    >
                        Importar JSON
                    </button>
                    <button onClick={fillWithPreview} className="btn btn--accent">
                        Preencher com Preview
                    </button>
                    <button
                        onClick={() => setImportValue("")}
                        className="btn"
                        style={{
                            background: 'rgba(255, 255, 255, 0.1)',
                            color: 'white'
                        }}
                    >
                        Limpar
                    </button>
                </div>
            </div>
        </div>
    );
}