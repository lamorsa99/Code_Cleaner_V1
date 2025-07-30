from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QScrollArea, QWidget, QApplication
)
from PyQt6.QtCore import Qt
from styles.style_manager import StyleManager

class InstructionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_dialog()
        self._create_content()
        self.dont_show = False
    
    def _setup_dialog(self):
        """Configura las propiedades básicas del diálogo"""
        self.setWindowTitle("📖 Code Cleaner V1 - Quick Start Guide")
        self.setFixedSize(650, 550)  # Ligeramente más grande para mejor legibilidad
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
        title = QLabel("🧹 <b>Code Cleaner V1</b> - <i>Quick Start Guide</i>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 20px; 
            color: #1e3a8a; 
            margin-bottom: 6px;
            font-weight: bold;
            padding: 6px 12px;
            background-color: #f8fafc;
            border: 1px solid #000000;
            border-radius: 0px;
            font-family: 'Segoe UI', 'Calibri', Arial, sans-serif;
        """)
        layout.addWidget(title)

    def _create_instructions_content(self):
        """Retorna las instrucciones como lista de tuplas - Versión mejorada y más concisa"""
        return [
            ("🧹 Code Cleaner", "Removes comments & empty lines while preserving error tracking."),
            
            ("� Quick Start", ""),
            ("📥 1. Add Code", "Paste code (Ctrl+V) in the left panel. Direct typing is disabled."),
            ("🎯 2. Mark Errors", "Click line numbers or use from/to boxes + Select button to mark problematic lines."),
            ("🧼 3. Clean", "Hit 'Clean Code' button. Comments and empty lines disappear, errors stay tracked."),
            ("📋 4. Copy", "Use 'Copy Result' to get your cleaned code."),
            
            ("📊 Understanding Statistics", ""),
            ("📈 Left Panel", "• Total Lines: Original code line count\n• Selected Lines: How many lines you marked as errors"),
            ("📉 Right Panel", "• Clean Lines: Final code line count\n• Deleted Lines: How many lines were removed\n• Errors Found: Your marked errors in clean code"),
            
            ("💡 Pro Tips", ""),
            ("⚡ Efficiency", "• Mark error lines BEFORE cleaning for better tracking\n• Use range selection (from/to) for multiple lines\n• Real-time stats help you understand the cleaning impact"),
            ("� Workflow", "• Perfect for code reviews and bug documentation\n• Preserves your error tracking through the cleaning process\n• Great for preparing code for presentations or documentation")
        ]

    def _create_scroll_content(self, layout):
        """Crea el contenido scrolleable con las instrucciones"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        content_widget = QWidget()
        content_widget.setObjectName("content")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(8)  # Reducido de 12 a 8
        content_layout.setContentsMargins(15, 15, 15, 15)  # Reducido de 20 a 15
        
        # Agregar instrucciones
        for title_text, desc_text in self._create_instructions_content():
            section_title = QLabel(title_text)
            section_title.setStyleSheet("""
                font-size: 15px; 
                font-weight: bold; 
                color: #1e40af; 
                margin-top: 3px;
                padding: 4px 8px;
                background-color: #dbeafe;
                border: 1px solid #000000;
                border-radius: 0px;
            """)
            content_layout.addWidget(section_title)
            
            if desc_text:
                section_desc = QLabel(desc_text)
                section_desc.setWordWrap(True)
                section_desc.setStyleSheet("""
                    font-size: 13px; 
                    color: #374151; 
                    margin-left: 8px; 
                    margin-bottom: 6px;
                    padding: 6px;
                    background-color: #f8fafc;
                    border: 1px solid #e5e7eb;
                    border-radius: 0px;
                """)
                content_layout.addWidget(section_desc)
        
        # Nota final
        note = QLabel("🚀 <b>Ready to start?</b> Close this dialog and begin cleaning your code!")
        note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        note.setStyleSheet("""
            font-size: 15px; 
            color: #16a34a; 
            font-weight: bold;
            margin-top: 10px; 
            padding: 8px; 
            background-color: #dcfce7; 
            border-radius: 0px; 
            border: 1px solid #000000;
        """)
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
                background-color: #fee2e2;
                color: #991b1b;
                font-weight: bold;
                font-size: 12px;
                padding: 8px 16px;
                border: 1px solid #000000;
                border-radius: 0px;
            }
            QPushButton:hover {
                background-color: #fca5a5;
            }
        """)
        self.dont_show_again.clicked.connect(self.dont_show_clicked)
        
        close_btn = QPushButton("🚀 Start Using Code Cleaner")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #dcfce7;
                color: #166534;
                font-weight: bold;
                font-size: 12px;
                padding: 8px 16px;
                border: 1px solid #000000;
                border-radius: 0px;
            }
            QPushButton:hover {
                background-color: #bbf7d0;
            }
        """)
        close_btn.clicked.connect(self.accept)
        
        button_layout.addWidget(self.dont_show_again)
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)

    def _create_content(self):
        """Crea todo el contenido del diálogo"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)  # Reducido de 15 a 10
        layout.setContentsMargins(15, 15, 15, 15)  # Reducido de 20 a 15
        
        self._create_title(layout)
        self._create_scroll_content(layout)
        self._create_buttons(layout)

    def dont_show_clicked(self):
        self.dont_show = True
        self.accept()