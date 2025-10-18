import { Outlet, Link, useLocation } from "react-router-dom";
import { useState } from "react";
import { Home, Settings, Menu, Terminal, LogOut } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { getCurrentWindow } from "@tauri-apps/api/window"; // optional fallback when running in Tauri
import { invoke } from "@tauri-apps/api/core";
import "./AppLayout.scss";

export default function AppLayout() {
    const [open, setOpen] = useState(true);
    const location = useLocation();

    const navItems = [
        {
            path: "/",
            label: "Início",
            icon: <Home size={22} />,
            badge: "New"
        },
        {
            path: "/settings",
            label: "Configurações",
            icon: <Settings size={22} />,
            badge: "v2.0"
        },
        {
            path: "/commands",
            label: "Comandos",
            icon: <Terminal size={22} />,
            badge: "v2.0"
        },
    ];

    const Particles = () => (
        <div className="particles">
            {[...Array(15)].map((_, i) => (
                <div key={i} className="particle" />
            ))}
        </div>
    );

    const handleExit = async () => {
        try {
            // tenta encerrar via backend Rust
            await invoke("app_exit");
        } catch (e) {
            console.error("Erro ao chamar app_exit:", e);
            // fallback: tenta fechar a janela do Tauri (se disponível) ou do navegador
            try {
                const win = getCurrentWindow();
                await win.close();
            } catch {
                try { window.close(); } catch (e3) { console.warn('window.close fallback falhou', e3); }
            }
        }
    };

    return (
        <div className="app-layout">
            <Particles />

            {/* Sidebar */}
            <motion.aside
                animate={{ width: open ? 280 : 80 }}
                className={`sidebar ${open ? "open" : "closed"}`}
                initial={false}
            >
                <button
                    onClick={() => setOpen(!open)}
                    className="sidebar__toggle"
                >
                    <Menu size={22} />
                    <AnimatePresence>
                        {open && (
                            <motion.span
                                initial={{ opacity: 0, x: -10 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: -10 }}
                                className="sidebar__brand"
                            >
                                ArchMIE
                            </motion.span>
                        )}
                    </AnimatePresence>
                </button>

                <nav className="sidebar__nav">
                    {navItems.map(({ path, label, icon, badge }) => {
                        const active = location.pathname === path;
                        return (
                            <Link
                                key={path}
                                to={path}
                                className={`sidebar__link ${active ? "active" : ""}`}
                            >
                                <span className="sidebar__link-icon">
                                    {icon}
                                </span>
                                <AnimatePresence>
                                    {open && (
                                        <motion.span
                                            initial={{ opacity: 0, x: -10 }}
                                            animate={{ opacity: 1, x: 0 }}
                                            exit={{ opacity: 0, x: -10 }}
                                            className="sidebar__link-text"
                                        >
                                            {label}
                                        </motion.span>
                                    )}
                                </AnimatePresence>
                                {open && badge && (
                                    <span className="sidebar__link-badge">
                                        {badge}
                                    </span>
                                )}
                            </Link>
                        );
                    })}
                </nav>

                {/* Botão Sair no final da Sidebar */}
                <div className="sidebar__footer">
                    <button
                        className="sidebar__logout"
                        onClick={handleExit}
                    >
                        <LogOut size={18} />
                        <AnimatePresence>
                            {open && (
                                <motion.span
                                    initial={{ opacity: 0, x: -8 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    exit={{ opacity: 0, x: -8 }}
                                    className="sidebar__logout-text"
                                >
                                    Sair
                                </motion.span>
                            )}
                        </AnimatePresence>
                    </button>
                </div>
            </motion.aside>

            {/* Conteúdo principal */}
            <main className="app-layout__main">

                <Outlet />
            </main>
        </div>
    );
}