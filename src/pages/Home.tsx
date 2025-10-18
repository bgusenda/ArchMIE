import { ArrowRight, Terminal, Palette, Download, Upload, Shield, Zap } from "lucide-react";
import { Link } from "react-router-dom";
import "./Home.scss";

export default function Home() {
    const features = [
        {
            icon: <Terminal size={24} />,
            title: "Terminal Integrado",
            description: "Execute comandos Arch Linux diretamente na interface com feedback em tempo real.",
            features: ["Comandos seguros", "Histórico de execução", "Auto-complete"]
        },
        {
            icon: <Palette size={24} />,
            title: "Temas Customizáveis",
            description: "Personalize completamente a aparência do seu ambiente com nosso editor de temas avançado.",
            features: ["Cores personalizadas", "Export/Import", "Preview em tempo real"]
        },
        {
            icon: <Shield size={24} />,
            title: "Ambiente Seguro",
            description: "Aprenda e experimente comandos sem riscos em um ambiente controlado e educativo.",
            features: ["Sandbox seguro", "Validação de comandos", "Backup automático"]
        },
        {
            icon: <Download size={24} />,
            title: "Exportação Fácil",
            description: "Salve e compartilhe suas configurações com o sistema de exportação integrado.",
            features: ["Formato JSON", "Backup cloud", "Compartilhamento"]
        },
        {
            icon: <Upload size={24} />,
            title: "Importação Rápida",
            description: "Carregue configurações salvas anteriormente ou compartilhadas pela comunidade.",
            features: ["Drag & Drop", "Validação automática", "Multi-formatos"]
        },
        {
            icon: <Zap size={24} />,
            title: "Performance Otimizada",
            description: "Interface rápida e responsiva construída com as melhores práticas modernas.",
            features: ["Carregamento rápido", "Offline support", "Sync em tempo real"]
        }
    ];

    const stats = [
        { number: "50+", label: "Comandos" },
        { number: "100%", label: "Open Source" },
        { number: "24/7", label: "Disponível" },
        { number: "v2.0", label: "Versão" }
    ];

    // location removed (unused)

    return (
        <div className="home">
            {/* Hero Section */}
            <section className="home__hero">
                <h1 className="home__title">
                    Bem-vindo ao ArchMIE
                </h1>
                <p className="home__subtitle">
                    Sua plataforma completa para dominar o Arch Linux com segurança,
                    customização total e performance excepcional.
                </p>
            </section>

            {/* Features Grid */}
            <section className="home__grid">
                {features.map((feature, index) => (
                    <div key={index} className="home__card">
                        <div className="home__card-header">
                            <div className="home__card-icon">
                                {feature.icon}
                            </div>
                            <ArrowRight size={20} className="home__card-arrow" />
                        </div>
                        <h2>{feature.title}</h2>
                        <p>{feature.description}</p>
                        <ul className="home__card-features">
                            {feature.features.map((item, idx) => (
                                <li key={idx} className="home__card-feature">
                                    {item}
                                </li>
                            ))}
                        </ul>
                    </div>
                ))}
            </section>

            {/* Stats Section */}
            <section className="home__stats">
                {stats.map((stat, index) => (
                    <div key={index} className="home__stat">
                        <div className="home__stat-number">{stat.number}</div>
                        <div className="home__stat-label">{stat.label}</div>
                    </div>
                ))}
            </section>

            {/* CTA Section */}
            <section className="home__cta">
                <h3 className="home__cta-title">
                    Pronto para Começar?
                </h3>
                <p style={{ color: 'rgba(255, 255, 255, 0.7)', marginBottom: '2rem' }}>
                    Explore as configurações e personalize sua experiência agora mesmo.
                </p>
                <Link
                    key={"/commands"}
                    to={"/commands"}
                >
                    <button className="home__cta-button">

                        Começar Agora <ArrowRight size={20} />
                    </button>
                </Link>
            </section>
        </div>
    );
}