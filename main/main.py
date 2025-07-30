import sys
import re
from PyQt6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPlainTextEdit, QPushButton, QLabel, QFrame, QSizePolicy, QTextEdit, QLineEdit, QGroupBox, QDialog, QScrollArea
)
from PyQt6.QtGui import QFont, QTextCursor, QTextCharFormat, QColor, QPainter, QPixmap
from PyQt6.QtCore import Qt

class LineNumberArea(QPlainTextEdit):
    def __init__(self, editor, parent_widget=None):
        super().__init__()
        self.editor = editor
        self.parent_widget = parent_widget
        self.setReadOnly(True)
        self.setMaximumWidth(75)  # Aumentado de 55 a 75 para dar más espacio
        self.setFont(QFont("Consolas", 11))
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setStyleSheet("background-color: #f5f5f5; color: #888; border: none;")
        self.editor.verticalScrollBar().valueChanged.connect(self.sync_scroll)
        self.editor.blockCountChanged.connect(self.update_numbers)
        self.editor.updateRequest.connect(self.update_numbers)
        self.clicked_line = None

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self.viewport())
        font_metrics = self.fontMetrics()
        block = self.editor.document().firstBlock()
        block_number = 0

        while block.isValid():
            rect = self.editor.blockBoundingGeometry(block).translated(
                self.editor.contentOffset()
            )
            top = int(rect.top())
            block_height = font_metrics.height()
            y = top + block_height // 2 + font_metrics.ascent() // 2

            highlighted = False
            if self.parent_widget:
                if self.editor is self.parent_widget.editor:
                    highlighted = block_number in self.parent_widget.highlighted_lines
                elif self.editor is self.parent_widget.output:
                    highlighted = block_number in self.parent_widget.highlighted_output_lines

            # --- Dibujar contenido de la línea ---
            number_str = str(block_number + 1)
            number_width = font_metrics.horizontalAdvance(number_str)
            area_width = self.width()

            if highlighted:
                # Dibujar el icono ❌ a la izquierda
                x_icon = 4
                painter.setPen(QColor(255, 0, 0))  # Rojo para el ❌
                painter.drawText(x_icon, y, "❌")
                
                # Calcular el ancho del icono para posicionar el número después
                icon_width = font_metrics.horizontalAdvance("❌")
                
                # Dibujar el número después del icono con espacio
                number_x = x_icon + icon_width + 4  # 4px de separación
                painter.setPen(QColor(136, 136, 136))
                painter.drawText(number_x, y, number_str)
            else:
                # Sin icono, centrar el número en el área
                number_x = (area_width - number_width) // 2
                painter.setPen(QColor(136, 136, 136))
                painter.drawText(number_x, y, number_str)
                
            block = block.next()
            block_number += 1

    def sync_scroll(self, value):
        self.verticalScrollBar().setValue(value)

    def update_numbers(self, *args):
        self.update()
        self.setFixedHeight(self.editor.viewport().height())

    def mousePressEvent(self, event):
        y = event.position().y()
        editor = self.editor
        block = editor.firstVisibleBlock()
        block_number = block.blockNumber()
        top = editor.blockBoundingGeometry(block).translated(editor.contentOffset()).top()
        bottom = top + editor.blockBoundingRect(block).height()

        while block.isValid() and top <= y:
            if top <= y <= bottom:
                break
            block = block.next()
            top = bottom
            bottom = top + editor.blockBoundingRect(block).height()
            block_number = block.blockNumber()

        line = block_number

        font_metrics = self.fontMetrics()
        rect = editor.blockBoundingGeometry(block).translated(editor.contentOffset())
        x_x = 4  # La X está a la izquierda
        if self.parent_widget:
            highlighted = False
            if editor is self.parent_widget.editor:
                highlighted = line in self.parent_widget.highlighted_lines
            elif editor is self.parent_widget.output:
                highlighted = line in self.parent_widget.highlighted_output_lines
            if highlighted:
                rect_x = x_x
                rect_y = int(rect.top())
                rect_w = font_metrics.horizontalAdvance("❌") + 4
                rect_h = font_metrics.height()
                if (rect_x <= event.position().x() <= rect_x + rect_w and
                    rect_y <= y <= rect_y + rect_h):
                    if editor is self.parent_widget.editor:
                        self.parent_widget.toggle_highlight_line(line)
                    elif editor is self.parent_widget.output:
                        self.parent_widget.toggle_highlight_output_line(line)
                    return
        if self.parent_widget:
            if editor is self.parent_widget.editor:
                self.parent_widget.toggle_highlight_line(line)
            elif editor is self.parent_widget.output:
                self.parent_widget.toggle_highlight_output_line(line)
        super().mousePressEvent(event)

    def wheelEvent(self, event):
        event.ignore()

class InstructionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📖 Code Cleaner V1 - Instructions")
        self.setFixedSize(600, 500)
        self.setModal(True)
        
        # Centrar el diálogo en la pantalla
        self.center_dialog()
        
        # Configurar el estilo del diálogo usando los mismos colores de la ventana principal
        self.setStyleSheet("""
            QDialog {
                background-color: #f7fafd;
                border-radius: 12px;
            }
            QLabel {
                color: #222;
                font-size: 14px;
                line-height: 1.5;
            }
            QPushButton {
                background-color: #e3e6ee;
                color: #222;
                border-radius: 8px;
                padding: 10px 22px;
                font-size: 15px;
                border: 1px solid #b0b0b0;
            }
            QPushButton:hover {
                background-color: #d0d6e0;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QWidget#content {
                background-color: #fff;
                border-radius: 10px;
                border: 1px solid #e0e0e0;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título principal
        title = QLabel("🧹 <b>Welcome to Code Cleaner V1!</b>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; color: #1976d2; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Área de scroll para las instrucciones
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Widget contenedor del contenido
        content_widget = QWidget()
        content_widget.setObjectName("content")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(12)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Instrucciones paso a paso
        instructions = [
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
        
        for title_text, desc_text in instructions:
            # Título de la sección
            section_title = QLabel(title_text)
            section_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #1976d2; margin-top: 5px;")
            content_layout.addWidget(section_title)
            
            # Descripción de la sección
            if desc_text:
                section_desc = QLabel(desc_text)
                section_desc.setWordWrap(True)
                section_desc.setStyleSheet("font-size: 14px; color: #222; margin-left: 10px; margin-bottom: 8px;")
                content_layout.addWidget(section_desc)
        
        # Nota final
        note = QLabel("🚀 <b>Ready to start?</b> Close this dialog and begin cleaning your code!")
        note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        note.setStyleSheet("font-size: 16px; color: #1976d2; margin-top: 15px; padding: 10px; background-color: #e3e6ee; border-radius: 8px; border: 1px solid #b0b0b0;")
        content_layout.addWidget(note)
        
        content_layout.addStretch()
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
        
        # Botones
        button_layout = QHBoxLayout()
        
        # Botón "Don't show again" con colores consistentes
        self.dont_show_again = QPushButton("✅ Don't show again")
        self.dont_show_again.setStyleSheet("""
            QPushButton {
                background-color: #e3e6ee;
                color: #222;
                border-radius: 8px;
                padding: 10px 22px;
                font-size: 15px;
                border: 1px solid #b0b0b0;
            }
            QPushButton:hover {
                background-color: #d0d6e0;
            }
        """)
        self.dont_show_again.clicked.connect(self.dont_show_clicked)
        
        # Botón de cerrar principal
        close_btn = QPushButton("🚀 Start Using Code Cleaner")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #e3e6ee;
                color: #222;
                border-radius: 8px;
                padding: 10px 22px;
                font-size: 15px;
                border: 1px solid #b0b0b0;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d0d6e0;
            }
        """)
        close_btn.clicked.connect(self.accept)
        
        button_layout.addWidget(self.dont_show_again)
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)
        
        self.dont_show = False
    
    def center_dialog(self):
        """Centra el diálogo en el medio de la pantalla"""
        # Obtener el tamaño de la pantalla
        screen = QApplication.primaryScreen().geometry()
        
        # Calcular la posición central
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        
        # Mover el diálogo al centro
        self.move(x, y)

    def dont_show_clicked(self):
        self.dont_show = True
        self.accept()

class CodeCleaner(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Code Cleaner V1 (PyQt6)")
        self.resize(1200, 700)
        
        # Centrar la ventana principal en la pantalla
        self.center_window()
        
        # Mostrar panel de instrucciones al inicio
        self.show_instructions_dialog()
        
        # Aplicar el estilo consistente con el diálogo de instrucciones
        self.setStyleSheet("""
            QWidget {
                background-color: #f7fafd;
            }
            QLabel {
                font-size: 16px;
                color: #222;
            }
            QPushButton {
                background-color: #e3e6ee;
                color: #222;
                border-radius: 8px;
                padding: 10px 22px;
                font-size: 15px;
                border: 1px solid #b0b0b0;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #d0d6e0;
                border: 1px solid #a0a0a0;
            }
            QPushButton:pressed {
                background-color: #c0c6d0;
            }
            QPlainTextEdit {
                background-color: #ffffff;
                color: #222;
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid #e0e0e0;
                padding: 8px;
            }
            QPlainTextEdit:focus {
                border: 2px solid #1976d2;
            }
            QLineEdit {
                background: #ffffff;
                color: #222;
                border-radius: 6px;
                border: 1px solid #e0e0e0;
                padding: 6px 12px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #1976d2;
                background: #fafbfc;
            }
            QGroupBox {
                border: 2px solid #e0e0e0;
                border-radius: 12px;
                margin-top: 8px;
                margin-bottom: 4px;
                margin-left: 2px;
                margin-right: 2px;
                background: #ffffff;
                padding-top: 20px;
                font-weight: 600;
            }
            QGroupBox:title {
                color: #1976d2;
                font-size: 18px;
                font-weight: bold;
                left: 16px;
                top: 10px;
                padding: 0 8px;
                background: #ffffff;
            }
            /* Estilo específico para grupos internos */
            QGroupBox#internal {
                border: 1.5px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 2px;
                background: #f9f9fb;
                padding-top: 8px;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(8, 8, 8, 8)

        # Título con estilo mejorado
        title = QLabel("🧹 <b>Code Cleaner V1</b>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 32px; 
            margin-bottom: 12px; 
            color: #1976d2;
            font-weight: bold;
            padding: 8px;
            background: rgba(25, 118, 210, 0.05);
            border-radius: 10px;
            border: 1px solid rgba(25, 118, 210, 0.2);
        """)
        main_layout.addWidget(title)

        editors_layout = QHBoxLayout()
        editors_layout.setSpacing(12)
        editors_layout.setContentsMargins(0, 0, 0, 0)

        # --- LEFT CARD ---
        left_card = QGroupBox("📝 Original Code")
        left_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        left_card_layout = QVBoxLayout(left_card)
        left_card_layout.setSpacing(8)
        left_card_layout.setContentsMargins(12, 12, 12, 12)

        # Inputs de selección con mejor estilo
        inputs_group = QGroupBox()
        inputs_group.setObjectName("internal")
        inputs_group.setStyleSheet("""
            QGroupBox#internal {
                border: 1px solid #e0e0e0;
                background: rgba(25, 118, 210, 0.02);
                border-radius: 8px;
                padding: 8px;
            }
        """)
        inputs_layout = QHBoxLayout(inputs_group)
        inputs_layout.setSpacing(8)
        
        # Label para los inputs
        range_label = QLabel("📍 <b>Select Range:</b>")
        range_label.setStyleSheet("color: #1976d2; font-size: 14px; font-weight: bold;")
        
        self.from_box = QLineEdit()
        self.from_box.setPlaceholderText("from")
        self.from_box.setFixedWidth(70)
        self.to_box = QLineEdit()
        self.to_box.setPlaceholderText("to")
        self.to_box.setFixedWidth(70)
        self.select_btn = QPushButton("✅ Select")
        self.select_btn.setFixedWidth(110)
        self.unselect_btn = QPushButton("❌ Unselect")
        self.unselect_btn.setFixedWidth(120)
        
        inputs_layout.addWidget(range_label)
        inputs_layout.addStretch()
        inputs_layout.addWidget(self.from_box)
        inputs_layout.addWidget(self.to_box)
        inputs_layout.addWidget(self.select_btn)
        inputs_layout.addWidget(self.unselect_btn)
        inputs_layout.addStretch()
        left_card_layout.addWidget(inputs_group)

        # Editor con números de línea
        editor_group = QGroupBox()
        editor_group.setObjectName("internal")
        editor_group_layout = QVBoxLayout(editor_group)
        editor_group_layout.setContentsMargins(4, 4, 4, 4)
        editor_group_layout.setSpacing(0)

        editor_layout = QHBoxLayout()
        editor_layout.setContentsMargins(0, 0, 0, 0)
        editor_layout.setSpacing(0)
        self.editor = QPlainTextEdit()
        self.editor.setFont(QFont("Consolas", 12))
        self.editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.editor.installEventFilter(self)
        self.editor.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.editor.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.line_numbers = LineNumberArea(self.editor, self)
        self.editor.textChanged.connect(self.update_line_numbers)
        self.editor.textChanged.connect(self.update_line_count)
        self.editor.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.line_numbers.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        editor_layout.addWidget(self.line_numbers)
        editor_layout.addWidget(self.editor)
        editor_group_layout.addLayout(editor_layout, stretch=2)

        # Estadísticas con mejor diseño
        stats_left_layout = QHBoxLayout()
        stats_left_layout.setContentsMargins(12, 8, 12, 8)
        self.line_count_label = QLabel("📊 Total Lines: 0")
        self.line_count_label.setStyleSheet("""
            color: #1976d2; 
            font-weight: bold; 
            font-size: 15px;
            padding: 4px 8px;
            background: rgba(25, 118, 210, 0.1);
            border-radius: 6px;
        """)
        self.selected_count_label = QLabel("🎯 Selected Lines: 0")
        self.selected_count_label.setStyleSheet("""
            color: #ff9800; 
            font-weight: bold; 
            font-size: 15px;
            padding: 4px 8px;
            background: rgba(255, 152, 0, 0.1);
            border-radius: 6px;
        """)
        self.empty_label = QLabel("")
        self.empty_label.setMinimumWidth(120)
        stats_left_layout.addWidget(self.line_count_label, alignment=Qt.AlignmentFlag.AlignLeft)
        stats_left_layout.addStretch()
        stats_left_layout.addWidget(self.empty_label, alignment=Qt.AlignmentFlag.AlignCenter)
        stats_left_layout.addStretch()
        stats_left_layout.addWidget(self.selected_count_label, alignment=Qt.AlignmentFlag.AlignRight)
        editor_group_layout.addLayout(stats_left_layout)

        left_card_layout.addWidget(editor_group, stretch=2)

        # Botones con mejor estilo
        buttons_group = QGroupBox()
        buttons_group.setObjectName("internal")
        buttons_group.setStyleSheet("""
            QGroupBox#internal {
                border: 1px solid #e0e0e0;
                background: rgba(233, 30, 99, 0.02);
                border-radius: 8px;
                padding: 8px;
            }
        """)
        buttons_layout = QHBoxLayout(buttons_group)
        buttons_layout.setSpacing(12)
        self.clear_btn = QPushButton("🗑️ Clear Code")
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffebee;
                color: #d32f2f;
                border: 1px solid #ffcdd2;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ffcdd2;
                border: 1px solid #ef9a9a;
            }
        """)
        self.clear_btn.clicked.connect(self.clear_editor)
        self.clean_btn = QPushButton("🧼 Clean Code")
        self.clean_btn.setStyleSheet("""
            QPushButton {
                background-color: #e8f5e8;
                color: #2e7d32;
                border: 1px solid #c8e6c9;
                font-weight: bold;
                font-size: 16px;
                padding: 12px 24px;
            }
            QPushButton:hover {
                background-color: #c8e6c9;
                border: 1px solid #a5d6a7;
            }
        """)
        self.clean_btn.clicked.connect(self.clean_code)
        buttons_layout.addWidget(self.clear_btn)
        buttons_layout.addWidget(self.clean_btn)
        left_card_layout.addWidget(buttons_group)

        left_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        editors_layout.addWidget(left_card, stretch=1)

        # --- RIGHT CARD ---
        right_card = QGroupBox("✨ Clean Code")
        right_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        right_card_layout = QVBoxLayout(right_card)
        right_card_layout.setSpacing(8)
        right_card_layout.setContentsMargins(12, 12, 12, 12)

        # Output con números de línea
        output_group = QGroupBox()
        output_group.setObjectName("internal")
        output_group_layout = QVBoxLayout(output_group)
        output_group_layout.setContentsMargins(4, 4, 4, 4)
        output_group_layout.setSpacing(0)

        output_layout = QHBoxLayout()
        output_layout.setContentsMargins(0, 0, 0, 0)
        output_layout.setSpacing(0)
        self.output = QPlainTextEdit()
        self.output.setFont(QFont("Consolas", 12))
        self.output.setReadOnly(True)
        self.output.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.output.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.output.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.output_line_numbers = LineNumberArea(self.output, self)
        self.output.textChanged.connect(self.update_output_line_numbers)
        self.output.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.output_line_numbers.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        output_layout.addWidget(self.output_line_numbers)
        output_layout.addWidget(self.output)
        output_group_layout.addLayout(output_layout, stretch=2)

        # Estadísticas del output con mejor diseño
        stats_layout = QHBoxLayout()
        stats_layout.setContentsMargins(12, 8, 12, 8)
        self.output_line_count_label = QLabel("✅ Clean Lines: 0")
        self.output_line_count_label.setStyleSheet("""
            color: #388e3c; 
            font-weight: bold; 
            font-size: 15px;
            padding: 4px 8px;
            background: rgba(56, 142, 60, 0.1);
            border-radius: 6px;
        """)
        self.deleted_lines_label = QLabel("🗑️ Deleted Lines: 0")
        self.deleted_lines_label.setStyleSheet("""
            color: #d32f2f; 
            font-weight: bold; 
            font-size: 15px;
            padding: 4px 8px;
            background: rgba(211, 47, 47, 0.1);
            border-radius: 6px;
        """)
        self.errors_label = QLabel("⚠️ Errors Found: 0")
        self.errors_label.setStyleSheet("""
            color: #ff9800; 
            font-weight: bold; 
            font-size: 15px;
            padding: 4px 8px;
            background: rgba(255, 152, 0, 0.1);
            border-radius: 6px;
        """)
        stats_layout.addWidget(self.output_line_count_label, alignment=Qt.AlignmentFlag.AlignLeft)
        stats_layout.addStretch()
        stats_layout.addWidget(self.deleted_lines_label, alignment=Qt.AlignmentFlag.AlignCenter)
        stats_layout.addStretch()
        stats_layout.addWidget(self.errors_label, alignment=Qt.AlignmentFlag.AlignRight)
        output_group_layout.addLayout(stats_layout)

        right_card_layout.addWidget(output_group, stretch=2)

        # Botón copiar con mejor estilo
        copy_button_container = QGroupBox()
        copy_button_container.setObjectName("internal")
        copy_button_container.setStyleSheet("""
            QGroupBox#internal {
                border: 1px solid #e0e0e0;
                background: rgba(25, 118, 210, 0.02);
                border-radius: 8px;
                padding: 8px;
            }
        """)
        copy_layout = QHBoxLayout(copy_button_container)
        self.copy_btn = QPushButton("📋 Copy Result")
        self.copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #e3f2fd;
                color: #1976d2;
                border: 1px solid #bbdefb;
                font-weight: bold;
                font-size: 16px;
                padding: 12px 24px;
            }
            QPushButton:hover {
                background-color: #bbdefb;
                border: 1px solid #90caf9;
            }
        """)
        self.copy_btn.clicked.connect(self.copy_result)
        copy_layout.addWidget(self.copy_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        right_card_layout.addWidget(copy_button_container)

        right_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        editors_layout.addWidget(right_card, stretch=1)

        main_layout.addLayout(editors_layout, stretch=15)

        # Inicializa los sets ANTES de llamar a cualquier método que los use
        self.highlighted_lines = set()
        self.highlighted_output_lines = set()

        self.update_line_numbers()
        self.update_line_count()
        self.update_output_line_numbers()
        self.update_output_line_count()
        self.update_deleted_lines_and_errors()

        self.select_btn.clicked.connect(self.select_lines_range)
        self.unselect_btn.clicked.connect(self.unselect_lines_range)

        # Hace que el layout principal expanda todo
        self.setLayout(main_layout)

    def update_line_numbers(self):
        self.line_numbers.update_numbers()
        self.line_numbers.verticalScrollBar().setValue(self.editor.verticalScrollBar().value())

    def update_line_count(self):
        text = self.editor.toPlainText()
        lines = text.split('\n')
        self.line_count_label.setText(f"Total Lines: {len(lines)}")
        self.selected_count_label.setText(f"Selected Lines: {len(self.highlighted_lines)}")

    def update_output_line_numbers(self):
        self.output_line_numbers.update_numbers()
        self.output_line_numbers.verticalScrollBar().setValue(self.output.verticalScrollBar().value())
        self.update_output_line_count()
        self.update_deleted_lines_and_errors()

    def update_output_line_count(self):
        text = self.output.toPlainText()
        lines = text.split('\n')
        self.output_line_count_label.setText(f"Clean Lines: {len(lines)}")

    def update_deleted_lines_and_errors(self):
        orig_lines = self.editor.toPlainText().split('\n')
        clean_lines = self.output.toPlainText().split('\n')
        eliminadas = max(0, len(orig_lines) - len(clean_lines))
        self.deleted_lines_label.setText(f"Deleted Lines: {eliminadas}")

        def is_real_code(line):
            line = line.strip()
            if not line:
                return False
            if line.startswith("//"):
                return False
            if line.startswith("/*") and line.endswith("*/"):
                return False
            return True

        errores_editor = 0
        matched_output_lines = set()
        for i in self.highlighted_lines:
            if 0 <= i < len(orig_lines) and is_real_code(orig_lines[i]):
                content = orig_lines[i].strip()
                if content == "}":
                    # Solo cuenta la llave si la línea anterior también fue mapeada
                    if i-1 in self.highlighted_lines and i-1 >= 0:
                        prev_content = orig_lines[i-1].strip()
                        # Busca la llave de cierre justo después de la línea mapeada en el output
                        for idx in range(1, len(clean_lines)):
                            if clean_lines[idx].strip() == "}" and clean_lines[idx-1].strip() == prev_content:
                                if idx in self.highlighted_output_lines and idx not in matched_output_lines:
                                    errores_editor += 1
                                    matched_output_lines.add(idx)
                                    break
                else:
                    for idx, line in enumerate(clean_lines):
                        if line.strip() == content and idx in self.highlighted_output_lines and idx not in matched_output_lines:
                            errores_editor += 1
                            matched_output_lines.add(idx)
                            break

        self.errors_label.setText(f"Errors Found: {errores_editor}")

    def clean_code(self):
        code = self.editor.toPlainText()
        orig_lines = code.split('\n')
        cleaned_lines = []
        self.mapa_limpio_a_original = []

        # Limpia los resaltados del lado derecho antes de recalcular
        self.highlighted_output_lines.clear()

        for idx, line in enumerate(orig_lines):
            line_sin_comentario = re.sub(r'//.*$', '', line)
            line_sin_comentario = re.sub(r'/\*.*?\*/', '', line_sin_comentario)
            if line_sin_comentario.strip():
                cleaned_lines.append(line_sin_comentario.strip())
                self.mapa_limpio_a_original.append(idx)

        cleaned = '\n'.join(cleaned_lines)
        self.output.setPlainText(cleaned)
        self.sync_highlight_to_output()
        self.update_output_line_numbers()
        self.update_deleted_lines_and_errors()

    def sync_highlight_to_output(self):
        # No limpiar el set, solo agregar las líneas sincronizadas
        if not hasattr(self, 'mapa_limpio_a_original'):
            return
        for idx_limpio, idx_original in enumerate(self.mapa_limpio_a_original):
            if idx_original in self.highlighted_lines:
                self.highlighted_output_lines.add(idx_limpio)
        self.highlight_output_line()

    def copy_result(self):
        result = self.output.toPlainText()
        if result:
            clipboard = QApplication.clipboard()
            clipboard.setText(result)

    def toggle_highlight_line(self, line_number):
        if line_number in self.highlighted_lines:
            self.highlighted_lines.remove(line_number)
        else:
            self.highlighted_lines.add(line_number)
        self.highlight_line()
        self.line_numbers.update()

    def toggle_highlight_output_line(self, line_number):
        # No permitir marcar/desmarcar en el lado derecho
        pass

    def highlight_line(self):
        extraSelections = []
        for line_number in self.highlighted_lines:
            selection = QTextEdit.ExtraSelection()
            line_color = QColor(255, 102, 102, 100)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextCharFormat.Property.FullWidthSelection, True)
            cursor = self.editor.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.Start)
            cursor.movePosition(QTextCursor.MoveOperation.Down, QTextCursor.MoveMode.MoveAnchor, line_number)
            cursor.select(QTextCursor.SelectionType.LineUnderCursor)
            selection.cursor = cursor
            extraSelections.append(selection)
        self.editor.setExtraSelections(extraSelections)
        # Actualiza el contador de seleccionadas cada vez que se resalta
        self.selected_count_label.setText(f"Líneas seleccionadas: {len(self.highlighted_lines)}")

    def highlight_output_line(self):
        extraSelections = []
        for line_number in self.highlighted_output_lines:
            selection = QTextEdit.ExtraSelection()
            line_color = QColor(255, 102, 102, 100)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextCharFormat.Property.FullWidthSelection, True)
            cursor = self.output.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.Start)
            cursor.movePosition(QTextCursor.MoveOperation.Down, QTextCursor.MoveMode.MoveAnchor, line_number)
            cursor.select(QTextCursor.SelectionType.LineUnderCursor)
            selection.cursor = cursor
            extraSelections.append(selection)
        self.output.setExtraSelections(extraSelections)
        self.update_deleted_lines_and_errors()

    def select_lines_range(self):
        from_line = self.from_box.text()
        to_line = self.to_box.text()
        if not from_line or not to_line:
            return
        try:
            from_line = int(from_line) - 1
            to_line = int(to_line) - 1
            if from_line < 0 or to_line < 0 or to_line < from_line:
                return
        except ValueError:
            return

        self.highlighted_lines.update(range(from_line, to_line + 1))  # <-- Cambiado aquí
        self.highlight_line()
        self.line_numbers.update()

        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Start)
        cursor.movePosition(QTextCursor.MoveOperation.Down, QTextCursor.MoveMode.MoveAnchor, from_line)
        self.editor.setTextCursor(cursor)
        self.editor.ensureCursorVisible()

    def unselect_lines_range(self):
        self.highlighted_lines.clear()
        self.highlight_line()
        self.line_numbers.update()

    def clear_editor(self):
        self.editor.setPlainText("")
        self.update_deleted_lines_and_errors()

    def eventFilter(self, obj, event):
        # Permite solo pegar en el editor izquierdo
        if obj == self.editor:
            if event.type() == event.Type.KeyPress:
                # Permitir solo Ctrl+V o Shift+Insert
                if (event.modifiers() & Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_V) or \
                   (event.modifiers() & Qt.KeyboardModifier.ShiftModifier and event.key() == Qt.Key.Key_Insert):
                    return False  # Permitir pegar
                return True  # Bloquear cualquier otra tecla
            if event.type() == event.Type.MouseButtonDblClick or event.type() == event.Type.MouseButtonPress:
                return True  # Bloquear edición con mouse
        return super().eventFilter(obj, event)

    def show_instructions_dialog(self):
        """Muestra el diálogo de instrucciones"""
        dialog = InstructionsDialog(self)
        dialog.exec()
        
        # Si el usuario eligió no mostrar de nuevo, podrías guardarlo en settings
        if dialog.dont_show:
            # Aquí podrías guardar la preferencia en un archivo de configuración
            pass

    def show_instructions_manually(self):
        """Método para mostrar instrucciones manualmente desde un menú"""
        dialog = InstructionsDialog(self)
        dialog.exec()

    def center_window(self):
        """Centra la ventana principal en el medio de la pantalla"""
        # Obtener el tamaño de la pantalla
        screen = QApplication.primaryScreen().geometry()
        
        # Calcular la posición central
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        
        # Mover la ventana al centro
        self.move(x, y)

def main():
    app = QApplication(sys.argv)
    window = CodeCleaner()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()