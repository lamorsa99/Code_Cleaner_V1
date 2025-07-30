# 🧹 Code Cleaner V1

A powerful and intuitive PyQt6-based desktop application designed to streamline code cleaning by removing comments and empty lines while providing advanced error tracking capabilities for developers.

## ✨ Key Features

- **🧼 Smart Code Cleaning**: Automatically removes single-line (`//`) and multi-line (`/* */`) comments plus empty lines
- **❌ Interactive Error Marking**: Click line numbers to mark problematic lines for tracking through the cleaning process  
- **📊 Real-time Analytics**: Live statistics showing total lines, selected lines, clean lines, deleted lines, and errors found
- **🎯 Flexible Range Selection**: Select multiple consecutive lines using intuitive "from" and "to" input fields
- **📋 One-Click Copy**: Instantly copy cleaned code results to clipboard for immediate use
- **🎨 Modern Interface**: Clean, professional UI design with consistent styling and responsive layout
- **📖 Built-in Help**: Comprehensive instructions dialog with detailed usage guidelines
- **⚡ Performance Optimized**: Efficient processing for large code files with instant feedback

## 🚀 Quick Start Guide

### System Requirements

- **Python**: 3.8 or higher
- **PyQt6**: Latest version
- **Operating System**: Windows, macOS, or Linux

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Code_Cleaner_V1.git
   cd Code_Cleaner_V1
   ```

2. **Install required dependencies**
   ```bash
   pip install PyQt6
   ```

3. **Launch the application**
   ```bash
   python main/main.py
   ```

## 📚 Detailed Usage Instructions

### Getting Started
1. **Import Your Code**: Paste code into the left editor using `Ctrl+V` or `Shift+Insert`
2. **Mark Problem Areas**: Click line numbers to highlight potential errors or issues
3. **Process Code**: Hit the "🧼 Clean Code" button to remove comments and empty lines
4. **Review Results**: Check statistics and cleaned output in the right panel
5. **Export**: Use "📋 Copy Result" to copy the cleaned code

### Advanced Features

#### Error Line Marking
- **Single Line**: Click any line number to toggle error marking
- **Range Selection**: Use the "from" and "to" input boxes to select multiple lines
- **Visual Feedback**: Marked lines show red highlighting with ❌ indicators
- **Persistent Tracking**: Error markers are preserved and mapped to cleaned code

#### Statistics Dashboard
- **Left Panel**: Displays total lines and currently selected error lines
- **Right Panel**: Shows clean lines count, deleted lines, and errors found in cleaned code
- **Real-time Updates**: All counters update automatically as you work

## 🏗️ Project Architecture

```
Code_Cleaner_V1/
├── main/
│   ├── main.py                    # Application entry point and main window
│   ├── components/
│   │   └── line_number_area.py    # Custom line number widget with error marking
│   ├── styles/
│   │   └── style_manager.py       # Centralized styling and theme management
│   ├── dialogs/
│   │   └── instructions_dialog.py # User help and instruction dialogs
│   └── core/
│       └── code_processor.py      # Code cleaning algorithms and logic
├── README.md                      # Project documentation
└── requirements.txt               # Python dependencies
```

## 🎯 Use Cases & Applications

- **Code Review Workflows**: Mark suspicious lines before cleaning to track them through review process
- **Documentation Preparation**: Remove development comments while preserving error tracking
- **Code Analysis**: Analyze comment-to-code ratios and identify documentation gaps
- **Debugging Sessions**: Track problematic lines through cleaning and refactoring
- **Code Sharing**: Prepare clean code for presentations, tutorials, or public repositories
- **Legacy Code Maintenance**: Clean up old codebases while preserving error annotations

## 🛠️ Technical Implementation

### Core Technologies
- **PyQt6**: Modern cross-platform GUI framework with native look and feel
- **Python 3.8+**: Robust backend processing with regex-based comment detection
- **Modular Architecture**: Separated concerns for maintainability and extensibility

### Key Components
- **LineNumberArea**: Custom QPlainTextEdit subclass with interactive click handling
- **StyleManager**: Centralized theming system for consistent visual design
- **InstructionsDialog**: Scrollable help system with rich formatting
- **CodeProcessor**: Efficient regex-based cleaning with line mapping preservation

### Performance Features
- **Lazy Loading**: UI components load only when needed
- **Efficient Regex**: Optimized pattern matching for comment detection
- **Memory Management**: Proper cleanup and garbage collection
- **Event Handling**: Responsive UI with non-blocking operations

## 💡 Tips for Optimal Usage

1. **Pre-cleaning Strategy**: Mark all potential error lines before running the cleaning process
2. **Range Selection**: Use keyboard shortcuts (Tab between inputs) for faster range selection
3. **Statistics Monitoring**: Watch the statistics to understand the cleaning impact on your code
4. **Error Icon Interaction**: Click ❌ icons directly for quick error line toggling
5. **Workflow Integration**: Copy results directly to your IDE or version control system

## 🤝 Contributing to the Project

We welcome contributions from the developer community! Here's how to get involved:

### Getting Started
1. **Fork** the repository to your GitHub account
2. **Create** a feature branch (`git checkout -b feature/new-functionality`)
3. **Implement** your changes with proper testing
4. **Commit** with descriptive messages (`git commit -m 'Add: New error detection algorithm'`)
5. **Push** to your branch (`git push origin feature/new-functionality`)
6. **Submit** a Pull Request with detailed description

### Development Environment
```bash
# Set up development environment
git clone https://github.com/yourusername/Code_Cleaner_V1.git
cd Code_Cleaner_V1

# Install dependencies
pip install PyQt6

# Run in development mode
python main/main.py
```

### Contribution Guidelines
- Follow PEP 8 coding standards
- Add docstrings to new functions and classes
- Include unit tests for new features
- Update documentation for user-facing changes

## 📄 License & Legal

This project is open source and available under the **MIT License**. See the [LICENSE](LICENSE) file for complete terms and conditions.

## 🐛 Issue Reporting & Support

### Bug Reports
Encountered a problem? Help us improve by reporting it:

1. **Check** existing issues to avoid duplicates
2. **Create** a detailed bug report with:
   - Steps to reproduce the issue
   - Expected vs actual behavior
   - Screenshots if applicable
   - System information (OS, Python version)

### Feature Requests
Have an idea for improvement? We'd love to hear it:
- Describe the feature and its benefits
- Explain the use case and target users
- Suggest implementation approaches if possible

### Getting Help
- **Built-in Help**: Use the 📖 instructions dialog within the application
- **GitHub Issues**: [Report bugs and request features](https://github.com/yourusername/Code_Cleaner_V1/issues)
- **Discussions**: [Join community discussions](https://github.com/yourusername/Code_Cleaner_V1/discussions)

---

<div align="center">

**Crafted with ❤️ for the developer community**

*Simplifying code cleaning, one line at a time*

[![GitHub stars](https://img.shields.io/github/stars/yourusername/Code_Cleaner_V1?style=for-the-badge&logo=github)](https://github.com/yourusername/Code_Cleaner_V1/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/Code_Cleaner_V1?style=for-the-badge&logo=github)](https://github.com/yourusername/Code_Cleaner_V1/network)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge)](LICENSE)

</div>