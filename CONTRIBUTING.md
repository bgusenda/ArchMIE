# 🤝 Contributing to ArchMIE

Thank you for your interest in contributing to **ArchMIE** (Arch Linux Management Interface & Environment)! We welcome contributions from the community and appreciate your help in making this project better.

## 📋 Table of Contents

- [🌟 Ways to Contribute](#-ways-to-contribute)
- [🚀 Getting Started](#-getting-started)
- [🐛 Reporting Bugs](#-reporting-bugs)
- [✨ Suggesting Features](#-suggesting-features)
- [🔧 Development Setup](#-development-setup)
- [📝 Code Style Guidelines](#-code-style-guidelines)
- [🔄 Pull Request Process](#-pull-request-process)
- [📚 Documentation](#-documentation)
- [❓ Getting Help](#-getting-help)

## 🌟 Ways to Contribute

There are many ways you can contribute to ArchMIE:

- 🐛 **Report bugs** and issues
- ✨ **Suggest new features** or improvements
- 🔧 **Submit code** patches and enhancements
- 📚 **Improve documentation** and examples
- 🎨 **Design improvements** for UI/UX
- 🧪 **Testing** on different systems
- 🌍 **Translations** (future feature)
- 💬 **Help other users** in discussions

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** installed on your system
- **Git** for version control
- **Arch Linux** recommended for testing (but not required for development)
- Basic knowledge of **Python** and **Tkinter**

### Fork and Clone

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ArchMIE.git
   cd ArchMIE
   ```
3. **Add upstream** remote:
   ```bash
   git remote add upstream https://github.com/bgusenda/ArchMIE.git
   ```

## 🐛 Reporting Bugs

Before creating a bug report, please:

1. **Search existing issues** to avoid duplicates
2. **Check the troubleshooting section** in README.md
3. **Test with the latest version** of ArchMIE

### Creating a Bug Report

Use the **Bug Report** template when creating an issue. Include:

- 📝 Clear description of the problem
- 🔄 Steps to reproduce the issue
- ✅ Expected vs actual behavior
- 💻 System information (OS, Python version, etc.)
- 📸 Screenshots if applicable
- 📋 Relevant log entries from `archMIE.log`

## ✨ Suggesting Features

We love feature suggestions! Before submitting:

1. **Check existing feature requests** to avoid duplicates
2. **Consider the scope** - does it fit ArchMIE's goals?
3. **Think about implementation** complexity

### Feature Request Guidelines

- 🎯 **Clear use case** - explain why this feature is needed
- 📝 **Detailed description** - how should it work?
- 🎨 **UI/UX considerations** - where should it appear?
- 🔧 **Implementation ideas** (optional but helpful)

## 🔧 Development Setup

### Local Development

1. **Clone the repository** (see Getting Started)
2. **Create a development branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Test the application**:
   ```bash
   python index.py
   ```

### Development Environment

- **IDE**: Any Python IDE (VS Code, PyCharm, etc.)
- **Python**: 3.8+ with Tkinter support
- **Testing**: Manual testing on Arch Linux preferred
- **Debugging**: Use Python debugger and application logs

### Project Structure

```
ArchMIE/
├── index.py              # Main application entry point
├── utils.py               # Utility functions (auth, logging, etc.)
├── theme_variables.py     # Theme management
├── pages/
│   ├── commands_page.py   # Command management interface
│   └── settings_page.py   # Settings and configuration
├── .github/              # GitHub templates and workflows
├── commands.json          # User's saved commands (auto-generated)
├── theme.json            # User's theme preferences (auto-generated)
├── archMIE.log           # Application logs (auto-generated)
└── README.md             # Project documentation
```

## 📝 Code Style Guidelines

### Python Code Style

Follow **PEP 8** guidelines with these specifics:

- **Line length**: Maximum 88 characters
- **Indentation**: 4 spaces (no tabs)
- **Naming conventions**:
  - Variables and functions: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_CASE`

### Code Quality

- ✅ **Add docstrings** for all functions and classes
- ✅ **Use type hints** where appropriate
- ✅ **Add comments** for complex logic
- ✅ **Handle exceptions** gracefully
- ✅ **Validate user inputs**

### Example Code Style

```python
def execute_secure_command(command: str, use_sudo: bool = False) -> tuple[bool, str]:
    """
    Execute a command securely with optional sudo authentication.
    
    Args:
        command: The command to execute
        use_sudo: Whether to use sudo authentication
        
    Returns:
        Tuple of (success: bool, output: str)
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        log_action(f"Command execution failed: {str(e)}", "ERROR")
        return False, str(e)
```

## 🔄 Pull Request Process

### Before Submitting

1. **Update your fork**:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes** following the code style guidelines

4. **Test thoroughly**:
   - Test all affected functionality
   - Test on different screen sizes
   - Check error handling
   - Verify logging works correctly

### Submitting the PR

1. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

2. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create Pull Request** using the provided template

### Commit Message Format

Use conventional commit format:

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

Examples:
```
feat: add password authentication for sudo commands
fix: resolve theme saving issue on startup
docs: update installation instructions
style: format code according to PEP 8
```

## 📚 Documentation

### Documentation Standards

- **Clear and concise** explanations
- **Code examples** where helpful
- **Screenshots** for UI changes
- **Update README.md** if needed
- **Add docstrings** to new functions

### Areas Needing Documentation

- 📝 **Function documentation** - docstrings for all public functions
- 🎯 **Feature documentation** - how to use new features
- 🔧 **Setup guides** - installation and configuration
- 🐛 **Troubleshooting** - common issues and solutions

## ❓ Getting Help

### Development Questions

- 💬 **GitHub Discussions** - For general questions
- 🐛 **GitHub Issues** - For bug reports and feature requests
- 📧 **Direct Contact** - For sensitive matters

### Resources

- 📚 **Python Documentation** - https://docs.python.org/
- 🎨 **Tkinter Tutorial** - https://docs.python.org/3/library/tkinter.html
- 🐧 **Arch Linux Wiki** - https://wiki.archlinux.org/
- 📖 **PEP 8 Style Guide** - https://pep8.org/

## 🎉 Recognition

Contributors will be:

- ✨ **Listed in CONTRIBUTORS.md** (coming soon)
- 🏷️ **Mentioned in release notes** for significant contributions
- 💫 **Recognized in project documentation**

## 🤝 Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project, you agree to abide by its terms.

---

Thank you for contributing to ArchMIE! Every contribution, no matter how small, helps make this project better for the entire Arch Linux community. 🚀