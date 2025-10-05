# 🚀 Guia de Release - ArchMIE

Este guia explica como criar releases oficiais do ArchMIE no GitHub e preparar para distribuição no AUR.

## 📋 Pré-requisitos

### Repositório Configurado
- ✅ Código principal na branch `main`
- ✅ Todos os arquivos de documentação criados
- ✅ GitHub Actions configurado
- ✅ Templates de issues/PRs criados

### Arquivos Necessários
- ✅ `README.md` - Documentação principal
- ✅ `CONTRIBUTING.md` - Guia de contribuição
- ✅ `CODE_OF_CONDUCT.md` - Código de conduta
- ✅ `CHANGELOG.md` - Histórico de mudanças
- ✅ `LICENSE` - Licença GNU GPL v3
- ✅ `PKGBUILD` - Para distribuição AUR
- ✅ `archmie.desktop` - Desktop entry
- ✅ `archmie.svg` / `archmie.png` - Ícones

## 🔄 Processo de Release

### 1. 📝 Preparação

```bash
# 1. Atualizar CHANGELOG.md
# - Mover items de [Unreleased] para [X.Y.Z]
# - Adicionar data do release
# - Revisar todas as mudanças

# 2. Verificar versão nos arquivos
# - PKGBUILD: pkgver=1.0.0
# - CHANGELOG.md: ## [1.0.0] - 2025-10-05

# 3. Commit final
git add .
git commit -m "chore: prepare release v1.0.0"
git push origin main
```

### 2. 🏷️ Criar Tag e Release

#### Via GitHub Web Interface (Recomendado)

1. **Ir para GitHub → Releases**
   ```
   https://github.com/bgusenda/ArchMIE/releases
   ```

2. **Clicar "Create a new release"**

3. **Configurar Release:**
   - **Tag version**: `v1.0.0`
   - **Release title**: `🚀 ArchMIE v1.0.0 - Initial Release`
   - **Target**: `main` branch

4. **Descrição do Release:**
   ```markdown
   # 🚀 ArchMIE v1.0.0 - Initial Release
   
   ## 🎉 Welcome to ArchMIE!
   
   This is the first official release of **ArchMIE** (Arch Linux Management Interface & Environment) - a modern, user-friendly GUI application for managing Arch Linux system commands with style and security.
   
   ## ✨ What's New
   
   ### 🎯 Core Features
   - 🖥️ **Intuitive GUI** - Clean, modern Tkinter interface
   - 📋 **Command Management** - Add, edit, delete system commands
   - 🔐 **Secure Authentication** - Password protection for sudo commands
   - 📝 **Comprehensive Logging** - Track all command executions
   - 🎨 **Theme Customization** - Dark/light modes with custom colors
   - 📥📤 **Import/Export** - Backup and restore command configurations
   
   ### 🛡️ Security & Quality
   - ✅ No password storage or persistence
   - ✅ Input validation and sanitization
   - ✅ Timeout protection for commands
   - ✅ Comprehensive error handling
   
   ## 🔧 Installation
   
   ### Quick Start
   ```bash
   # Download and extract
   wget https://github.com/bgusenda/ArchMIE/archive/v1.0.0.tar.gz
   tar -xzf v1.0.0.tar.gz
   cd ArchMIE-1.0.0
   
   # Run the application
   python index.py
   ```
   
   ### AUR Package (Coming Soon)
   ```bash
   # Will be available as
   yay -S archmie
   ```
   
   ## 📊 Release Statistics
   - **Lines of Code**: 2000+
   - **Features**: 20+ major features
   - **Documentation**: Complete guides and examples
   - **Python Compatibility**: 3.8 - 3.12
   
   ## 🙏 Acknowledgments
   
   Special thanks to the Arch Linux community and everyone who provided feedback during development!
   
   ---
   
   **📖 Full Changelog**: [CHANGELOG.md](https://github.com/bgusenda/ArchMIE/blob/v1.0.0/CHANGELOG.md)
   **🐛 Bug Reports**: [Create Issue](https://github.com/bgusenda/ArchMIE/issues/new/choose)
   **💬 Discussions**: [GitHub Discussions](https://github.com/bgusenda/ArchMIE/discussions)
   ```

5. **Anexar Arquivos (GitHub irá gerar automaticamente):**
   - Source code (zip)
   - Source code (tar.gz)

6. **Publicar Release**

#### Via Linha de Comando (Alternativo)

```bash
# Criar tag
git tag -a v1.0.0 -m "ArchMIE v1.0.0 - Initial Release"
git push origin v1.0.0

# Criar release com GitHub CLI (se disponível)
gh release create v1.0.0 \
  --title "🚀 ArchMIE v1.0.0 - Initial Release" \
  --notes-file RELEASE_NOTES.md \
  --draft=false \
  --prerelease=false
```

### 3. 📦 Verificar Download

Após criar o release, verificar se o download funciona:

```bash
# Testar URL de download
curl -L -o test-download.tar.gz \
  https://github.com/bgusenda/ArchMIE/archive/v1.0.0.tar.gz

# Ou usando wget
wget https://github.com/bgusenda/ArchMIE/archive/v1.0.0.tar.gz
```

### 4. 🎯 AUR (Arch User Repository)

#### Preparar PKGBUILD

1. **Calcular checksum do release:**
   ```bash
   wget https://github.com/bgusenda/ArchMIE/archive/v1.0.0.tar.gz
   sha256sum v1.0.0.tar.gz
   ```

2. **Atualizar PKGBUILD:**
   ```bash
   # Substituir 'SKIP' pelo checksum real
   sha256sums=('checksum_aqui')
   ```

#### Submeter para AUR

1. **Criar conta no AUR:** https://aur.archlinux.org/
2. **Configurar SSH keys**
3. **Clonar repositório AUR:**
   ```bash
   git clone ssh://aur@aur.archlinux.org/archmie.git
   cd archmie
   ```

4. **Adicionar arquivos:**
   ```bash
   cp ../ArchMIE/PKGBUILD .
   makepkg --printsrcinfo > .SRCINFO
   ```

5. **Submeter:**
   ```bash
   git add PKGBUILD .SRCINFO
   git commit -m "Initial upload: ArchMIE v1.0.0"
   git push
   ```

## 🔄 Releases Futuros

### Processo Simplificado

1. **Atualizar CHANGELOG.md**
2. **Bump version no PKGBUILD**
3. **Commit e push**
4. **Criar novo release no GitHub**
5. **Atualizar AUR package**

### Versionamento

Seguir [Semantic Versioning](https://semver.org/):
- **Major** (X.0.0): Breaking changes
- **Minor** (1.X.0): New features
- **Patch** (1.0.X): Bug fixes

## 🛠️ Automação

### GitHub Actions

O arquivo `.github/workflows/ci.yml` automaticamente:
- ✅ Executa testes em multiple Python versions
- ✅ Verifica qualidade do código
- ✅ Cria artifacts para releases
- ✅ Gera checksums automaticamente

### Release Automation (Futuro)

Possível adicionar:
- Automatic CHANGELOG generation
- Automatic version bumping
- Automatic AUR updates

## 📋 Checklist de Release

### Antes do Release
- [ ] ✅ Todos os testes passando
- [ ] ✅ Documentação atualizada
- [ ] ✅ CHANGELOG.md atualizado
- [ ] ✅ Versão bumped em todos os arquivos
- [ ] ✅ Código limpo e comentado

### Durante o Release
- [ ] ✅ Tag criada corretamente
- [ ] ✅ Release notes completas
- [ ] ✅ Assets anexados
- [ ] ✅ Download testado

### Após o Release
- [ ] ✅ Anúncio nas redes sociais
- [ ] ✅ AUR package atualizado
- [ ] ✅ Documentação deploy
- [ ] ✅ Feedback coletado

## 🎉 Sucesso!

Parabéns! Seu release está pronto. Agora os usuários podem:

1. **Baixar via GitHub**: https://github.com/bgusenda/ArchMIE/releases
2. **Instalar via AUR**: `yay -S archmie`
3. **Contribuir**: Seguindo CONTRIBUTING.md
4. **Reportar issues**: Using GitHub templates

---

💡 **Dica**: Mantenha este guia atualizado conforme o processo evolui!