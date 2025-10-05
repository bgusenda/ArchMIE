# 📁 ArchMIE - Estrutura do Repositório

## 🎯 **Código Principal** (Raiz)
```
├── 🐍 index.py             # Entrada principal da aplicação
├── 🔧 utils.py             # Funções utilitárias (auth, logging)
├── 🎨 theme_variables.py   # Gerenciamento de temas
└── 📁 pages/               # Páginas da interface
    ├── commands_page.py    # Interface de comandos
    └── settings_page.py    # Interface de configurações
```

## 📚 **Documentação** (docs/)
```
├── 📝 CHANGELOG.md         # Histórico de versões
├── 🤝 CONTRIBUTING.md      # Guia de contribuição
├── 📜 CODE_OF_CONDUCT.md   # Código de conduta
└── 🚀 RELEASE_GUIDE.md     # Guia de releases
```

## 🎨 **Assets Visuais** (assets/)
```
├── 🖼️ archmie.svg          # Ícone vetorial (fonte)
└── 🖼️ archmie.png          # Ícone bitmap (distribuição)
```

## 📦 **Distribuição** (packaging/)
```
├── 📋 PKGBUILD            # Script de build para AUR
└── 🖥️ archmie.desktop     # Entrada do desktop Linux
```

## 🔧 **Configuração GitHub** (.github/)
```
├── 📝 ISSUE_TEMPLATE/     # Templates para issues
└── 📤 pull_request_template.md # Template para PRs
```

## 📁 **Arquivos Ignorados** (gerados automaticamente)
```
├── 🗃️ commands.json        # Comandos salvos pelo usuário
├── 🎨 theme.json          # Preferências de tema
├── 📋 archMIE.log         # Logs da aplicação
└── 🐍 __pycache__/        # Cache do Python
```

---

## ✨ **Vantagens da Nova Estrutura**

### 🎯 **Código Mais Visível**
- Arquivos Python principais na raiz
- Fácil identificação do ponto de entrada (`index.py`)
- Lógica organizada em módulos claros

### 📚 **Documentação Organizada**
- Toda documentação em `docs/`
- README principal na raiz para overview
- Links atualizados para novos caminhos

### 🎨 **Assets Separados**
- Ícones e recursos visuais em `assets/`
- Fácil manutenção e atualização
- Separação clara entre código e recursos

### 📦 **Packaging Centralizado**
- Arquivos de distribuição em `packaging/`
- PKGBUILD e desktop entry organizados
- Facilita criação de pacotes

### 🔄 **Manutenção Simplificada**
- Estrutura escalável para futuras funcionalidades
- Separação clara de responsabilidades
- Navegação intuitiva para contribuidores

---

💡 **Esta estrutura segue as melhores práticas de organização de projetos Python e facilita tanto o desenvolvimento quanto a distribuição!**