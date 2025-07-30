from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QScrollArea, QWidget, QApplication
)
from PyQt6.QtCore import Qt
from ..styles.style_manager import StyleManager

class InstructionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_dialog()
        self._create_content()
        self.dont_show = False
    
    def _setup_dialog(self):
        """Configura las propiedades básicas del diálogo"""
        self.setWindowTitle("📖 Code Cleaner V1 - Instructions")
        self.setFixedSize(600, 500)
        self.setModal(True)
        self.setStyleSheet(StyleManager.get_dialog_style())
        self._center_dialog()

    def _center_dialog(self):
        """Centra el diálogo en el medio de la pantalla"""
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def _create_title(self, layout):
        """Crea el título principal"""
        title = QLabel("🧹 <b>Welcome to Code Cleaner V1!</b>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; color: #1976d2; margin-bottom: 10px;")
        layout.addWidget(title)

    def _create_instructions_content(self):
        """Retorna las instrucciones como lista de tuplas"""
        return [
            ("🎯 <b>Purpose:</b>", "This tool helps you clean code by removing comments and empty lines, and allows you to mark specific lines as errors for tracking."),
            ("📝 <b>How to Use:</b>", ""),
            ("1️⃣ <b>Add Code:</b>", "• Paste your code in the left editor (Original Code)\n• Only Ctrl+V or Shift+Insert are allowed for pasting\n• You cannot type directly in the editor"),
            ("2️⃣ <b>Select Error Lines:</b>", "• Click on line numbers to mark/unmark error lines\n• Use 'from' and 'to' boxes to select a range of lines\n• Click 'Select' to mark the range or 'Unselect' to clear all selections\n• Selected lines will be highlighted in red with ❌ markers"),
            ("3️⃣ <b>Clean Code:</b>", "• Click '🧼 Clean Code' to process your code\n• Comments (//, /* */) and empty lines will be removed\n• The cleaned code appears in the right panel\n• Error lines are automatically mapped to the cleaned code"),
            ("4️⃣ <b>Review Results:</b>", "• Check the statistics at the bottom of each panel:\n  - Left: Total Lines, Selected Lines\n  - Right: Clean Lines, Deleted Lines, Errors Found\n• Errors Found shows how many of your marked lines appear in the cleaned code"),
            ("5️⃣ <b>Copy Results:</b>", "• Click '📋 Copy Result' to copy the cleaned code to clipboard"),
            ("🧽 <b>Additional Features:</b>", "• '🗑️ Clear Code' - Clears the original code editor\n• Line numbers with ❌ can be clicked to toggle error marking\n• Real-time statistics update as you work"),
            ("💡 <b>Tips:</b>", "• Mark lines with potential bugs or issues before cleaning\n• The tool preserves your error markings across the cleaning process\n• Use this for code review and bug tracking workflows")
        ]

    def _create_scroll_content(self, layout):
        """Crea el contenido scrolleable con las instrucciones"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        content_widget = QWidget()
        content_widget.setObjectName("content")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(12)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Agregar instrucciones
        for title_text, desc_text in self._create_instructions_content():
            section_title = QLabel(title_text)
            section_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #1976d2; margin-top: 5px;")
            content_layout.addWidget(section_title)
            
            if desc_text:
                section_desc = QLabel(desc_text)
                section_desc.setWordWrap(True)
                section_desc.setStyleSheet("font-size: 14px; color: #333; margin-left: 10px; margin-bottom: 8px;")
                content_layout.addWidget(section_desc)
        
        # Nota final
        note = QLabel("🚀 <b>Ready to start?</b> Close this dialog and begin cleaning your code!")
        note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        note.setStyleSheet("font-size: 16px; color: #ff9800; margin-top: 15px; padding: 10px; background-color: #fff3e0; border-radius: 8px; border: 1px solid #ffcc02;")
        content_layout.addWidget(note)
        
        content_layout.addStretch()
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)

    def _create_buttons(self, layout):
        """Crea los botones del diálogo"""
        button_layout = QHBoxLayout()
        
        self.dont_show_again = QPushButton("✅ Don't show again")
        self.dont_show_again.setStyleSheet("""
            QPushButton {
                background-color: #ff9800;
                color: white;
            }
            QPushButton:hover {
                background-color: #f57c00;
            }
        """)
        self.dont_show_again.clicked.connect(self.dont_show_clicked)
        
        close_btn = QPushButton("🚀 Start Using Code Cleaner")
        close_btn.clicked.connect(self.accept)
        
        button_layout.addWidget(self.dont_show_again)
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)

    def _create_content(self):
        """Crea todo el contenido del diálogo"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        self._create_title(layout)
        self._create_scroll_content(layout)
        self._create_buttons(layout)

    def dont_show_clicked(self):
        self.dont_show = True
        self.accept()