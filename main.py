import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPlainTextEdit, 
    QPushButton, QLabel, QSizePolicy, QTextEdit, QLineEdit, QGroupBox
)
from PyQt6.QtGui import QFont, QTextCursor, QTextCharFormat, QColor
from PyQt6.QtCore import Qt

# Imports locales
from components.line_number_area import LineNumberArea
from styles.style_manager import StyleManager
from dialogs.instructions_dialog import InstructionsDialog
from core.code_processor import CodeProcessor

class CodeCleaner(QWidget):
    def __init__(self):
        super().__init__()
        self._initialize_data()
        self._setup_window()
        self._setup_ui()
        self._connect_signals()
        self._update_all_counters()
        self.show_instructions_dialog()

    def _setup_window(self):
        """Configura las propiedades básicas de la ventana"""
        self.setWindowTitle("Code Cleaner V1 (PyQt6)")
        self.resize(1200, 700)
        self.setStyleSheet(StyleManager.get_main_style())

    def _initialize_data(self):
        """Inicializa las estructuras de datos"""
        self.highlighted_lines = set()
        self.highlighted_output_lines = set()

    def _create_title(self):
        """Crea el título principal"""
        title = QLabel("🧹 <b>Code Cleaner V1</b>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px; 
            margin-bottom: 15px; 
            color: #1e3a8a;
            font-weight: bold;
            padding: 12px 20px;
            background-color: #f8fafc;
            border: 1px solid #000000;
            border-radius: 0px;
            font-family: 'Segoe UI', 'Calibri', Arial, sans-serif;
        """)
        return title

    def _create_range_inputs(self):
        """Crea los inputs para selección de rango"""
        inputs_group = QGroupBox()
        inputs_group.setStyleSheet("""
            QGroupBox { 
                border: 1px solid #000000; 
                border-radius: 0px; 
                background: transparent; 
                margin: 2px;
            }
        """)
        inputs_group.setFixedHeight(90)  # Aumenté de 80 a 90 para más espacio
        inputs_layout = QHBoxLayout(inputs_group)
        inputs_layout.setContentsMargins(8, 8, 8, 8)  # Márgenes ajustados
        inputs_layout.setSpacing(10)  # Espaciado entre elementos
        
        self.from_box = QLineEdit()
        self.from_box.setPlaceholderText("from")
        self.from_box.setFixedWidth(60)
        self.from_box.setFixedHeight(35)  # Aumenté de 30 a 35 para mejor visualización
        
        self.to_box = QLineEdit()
        self.to_box.setPlaceholderText("to")
        self.to_box.setFixedWidth(60)
        self.to_box.setFixedHeight(35)  # Aumenté de 30 a 35 para mejor visualización
        
        self.select_btn = QPushButton("Select")
        self.select_btn.setFixedWidth(100)
        self.select_btn.setFixedHeight(35)  # Aumenté de 30 a 35 para mejor visualización
        self.select_btn.setStyleSheet("""
            QPushButton {
                background-color: #dbeafe;
                color: #1e40af;
                font-weight: bold;
                font-size: 12px;
                padding: 5px;
                border: 1px solid #93c5fd;
            }
            QPushButton:hover {
                background-color: #93c5fd;
            }
        """)
        
        self.unselect_btn = QPushButton("Unselect")
        self.unselect_btn.setFixedWidth(110)
        self.unselect_btn.setFixedHeight(35)  # Aumenté de 30 a 35 para mejor visualización
        self.unselect_btn.setStyleSheet("""
            QPushButton {
                background-color: #f3f4f6;
                color: #374151;
                font-weight: bold;
                font-size: 12px;
                padding: 5px;
                border: 1px solid #d1d5db;
            }
            QPushButton:hover {
                background-color: #d1d5db;
            }
        """)
        
        inputs_layout.addStretch()
        inputs_layout.addWidget(self.from_box)
        inputs_layout.addWidget(self.to_box)
        inputs_layout.addWidget(self.select_btn)
        inputs_layout.addWidget(self.unselect_btn)
        inputs_layout.addStretch()
        
        return inputs_group

    def _create_editor_with_line_numbers(self, is_readonly=False):
        """Crea un editor con números de línea"""
        editor_group = QGroupBox()
        editor_group.setStyleSheet("""
            QGroupBox { 
                border: 1px solid #000000; 
                border-radius: 0px; 
                margin-top: 0px; 
                background: #f8fafc; 
                padding: 8px;
            }
        """)
        editor_group_layout = QVBoxLayout(editor_group)
        editor_group_layout.setContentsMargins(2, 2, 2, 2)
        editor_group_layout.setSpacing(0)

        editor_layout = QHBoxLayout()
        editor_layout.setContentsMargins(0, 0, 0, 0)
        editor_layout.setSpacing(0)
        
        editor = QPlainTextEdit()
        editor.setFont(QFont("Consolas", 12))
        editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        editor.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        editor.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        editor.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        if is_readonly:
            editor.setReadOnly(True)
        else:
            editor.installEventFilter(self)
        
        line_numbers = LineNumberArea(editor, self)
        line_numbers.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        
        editor_layout.addWidget(line_numbers)
        editor_layout.addWidget(editor)
        editor_group_layout.addLayout(editor_layout, stretch=2)
        
        return editor_group, editor, line_numbers

    def _create_stats_layout(self, labels_data):
        """Crea un layout de estadísticas con labels"""
        stats_layout = QHBoxLayout()
        stats_layout.setContentsMargins(15, 12, 15, 12)  # Aumenté los márgenes para más espacio
        stats_layout.setSpacing(15)  # Aumenté el espaciado entre elementos
        
        labels = []
        for i, (text, style, alignment) in enumerate(labels_data):
            label = QLabel(text)
            label.setStyleSheet(style)
            labels.append(label)
            
            if alignment == "left":
                stats_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignLeft)
            elif alignment == "center":
                stats_layout.addStretch()
                stats_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
            elif alignment == "right":
                stats_layout.addStretch()
                stats_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignRight)
        
        return stats_layout, labels

    def _create_left_card(self):
        """Crea la tarjeta izquierda (Original Code)"""
        left_card = QGroupBox("📝 Original Code")
        left_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        left_card.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #1e40af;
                border: 1px solid #000000;
                border-radius: 0px;
                margin-top: 15px;
                padding-top: 10px;
                background-color: #fefefe;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                background-color: #dbeafe;
                border: 1px solid #000000;
                border-radius: 0px;
                color: #1e40af;
                font-weight: bold;
            }
        """)
        left_card_layout = QVBoxLayout(left_card)
        left_card_layout.setSpacing(8)  # Aumenté el espaciado de 6 a 8
        left_card_layout.setContentsMargins(8, 8, 8, 8)  # Márgenes más generosos

        # Inputs de selección
        left_card_layout.addWidget(self._create_range_inputs())

        # Editor con números de línea
        editor_group, self.editor, self.line_numbers = self._create_editor_with_line_numbers()
        
        # Estadísticas
        stats_data = [
            ("Total Lines: 0", "color: #2563eb; font-weight: bold; font-size: 14px; padding: 4px 8px; background-color: #eff6ff; border: 1px solid #bfdbfe;", "left"),
            ("", "", "center"),
            ("Selected Lines: 0", "color: #dc2626; font-weight: bold; font-size: 14px; padding: 4px 8px; background-color: #fef2f2; border: 1px solid #fecaca;", "right")
        ]
        stats_layout, stats_labels = self._create_stats_layout(stats_data)
        self.line_count_label = stats_labels[0]
        self.empty_label = stats_labels[1]
        self.selected_count_label = stats_labels[2]
        self.empty_label.setMinimumWidth(120)
        
        editor_group.layout().addLayout(stats_layout)
        left_card_layout.addWidget(editor_group, stretch=3)  # Reducido de 10 a 3

        # Botones
        buttons_group = QGroupBox()
        buttons_group.setStyleSheet("""
            QGroupBox { 
                border: 1px solid #000000; 
                border-radius: 0px; 
                background: transparent; 
                margin: 2px;
            }
        """)
        buttons_group.setFixedHeight(80)  # Aumenté de 70 a 80 para más espacio
        buttons_layout = QHBoxLayout(buttons_group)
        buttons_layout.setContentsMargins(5, 5, 5, 5)  # Márgenes más pequeños para más espacio
        buttons_layout.setSpacing(5)  # Espaciado reducido entre botones
        
        self.clear_btn = QPushButton("🗑️ Clear Code")
        self.clean_btn = QPushButton("🧼 Clean Code")
        
        # Los botones ocuparán todo el espacio disponible verticalmente
        self.clear_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.clean_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Estilos específicos para los botones
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #fee2e2;
                color: #991b1b;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #fca5a5;
            }
        """)
        
        self.clean_btn.setStyleSheet("""
            QPushButton {
                background-color: #dbeafe;
                color: #1e40af;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #93c5fd;
            }
        """)
        
        buttons_layout.addWidget(self.clear_btn)
        buttons_layout.addWidget(self.clean_btn)
        left_card_layout.addWidget(buttons_group)

        return left_card

    def _create_right_card(self):
        """Crea la tarjeta derecha (Clean Code)"""
        right_card = QGroupBox("✨ Clean Code")
        right_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        right_card.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #16a34a;
                border: 1px solid #000000;
                border-radius: 0px;
                margin-top: 15px;
                padding-top: 10px;
                background-color: #fefefe;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                background-color: #dcfce7;
                border: 1px solid #000000;
                border-radius: 0px;
                color: #16a34a;
                font-weight: bold;
            }
        """)
        right_card_layout = QVBoxLayout(right_card)
        right_card_layout.setSpacing(8)  # Aumenté el espaciado de 6 a 8
        right_card_layout.setContentsMargins(8, 8, 8, 8)  # Márgenes más generosos

        # Editor con números de línea (readonly)
        output_group, self.output, self.output_line_numbers = self._create_editor_with_line_numbers(is_readonly=True)
        
        # Estadísticas
        stats_data = [
            ("Clean Lines: 0", "color: #16a34a; font-weight: bold; font-size: 14px; padding: 4px 8px; background-color: #f0fdf4; border: 1px solid #bbf7d0;", "left"),
            ("Deleted Lines: 0", "color: #dc2626; font-weight: bold; font-size: 14px; padding: 4px 8px; background-color: #fef2f2; border: 1px solid #fecaca;", "center"),
            ("Errors Found: 0", "color: #d97706; font-weight: bold; font-size: 14px; padding: 4px 8px; background-color: #fffbeb; border: 1px solid #fed7aa;", "right")
        ]
        stats_layout, stats_labels = self._create_stats_layout(stats_data)
        self.output_line_count_label = stats_labels[0]
        self.deleted_lines_label = stats_labels[1]
        self.errors_label = stats_labels[2]
        
        output_group.layout().addLayout(stats_layout)
        right_card_layout.addWidget(output_group, stretch=3)  # Reducido de 10 a 3

        # Botón copiar
        copy_container = QGroupBox()
        copy_container.setStyleSheet("""
            QGroupBox { 
                border: 1px solid #000000; 
                border-radius: 0px; 
                background: transparent; 
                margin: 2px;
            }
        """)
        copy_container.setFixedHeight(80)  # Aumenté de 60 a 80 para más espacio
        copy_layout = QHBoxLayout(copy_container)
        copy_layout.setContentsMargins(5, 5, 5, 5)  # Márgenes más pequeños para más espacio
        copy_layout.setSpacing(5)  # Espaciado reducido
        
        self.copy_btn = QPushButton("📋 Copy Result")
        # El botón ocupará todo el espacio disponible
        self.copy_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #dcfce7;
                color: #166534;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #bbf7d0;
            }
        """)
        copy_layout.addWidget(self.copy_btn)
        right_card_layout.addWidget(copy_container)

        return right_card

    def _setup_ui(self):
        """Configura toda la interfaz de usuario"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(12)  # Aumenté el espaciado de 8 a 12
        main_layout.setContentsMargins(10, 10, 10, 10)  # Márgenes más generosos

        # Título
        main_layout.addWidget(self._create_title())

        # Editores
        editors_layout = QHBoxLayout()
        editors_layout.setSpacing(12)  # Aumenté el espaciado entre editores
        editors_layout.setContentsMargins(5, 5, 5, 5)  # Pequeños márgenes

        editors_layout.addWidget(self._create_left_card(), stretch=1)
        editors_layout.addWidget(self._create_right_card(), stretch=1)

        main_layout.addLayout(editors_layout, stretch=10)  # Reducido de 15 a 10

    def _connect_signals(self):
        """Conecta todas las señales"""
        # Editores
        self.editor.textChanged.connect(self.update_line_numbers)
        self.editor.textChanged.connect(self.update_line_count)
        self.output.textChanged.connect(self.update_output_line_numbers)

        # Botones
        self.select_btn.clicked.connect(self.select_lines_range)
        self.unselect_btn.clicked.connect(self.unselect_lines_range)
        self.clear_btn.clicked.connect(self.clear_editor)
        self.clean_btn.clicked.connect(self.clean_code)
        self.copy_btn.clicked.connect(self.copy_result)

    def _update_all_counters(self):
        """Actualiza todos los contadores"""
        self.update_line_numbers()
        self.update_line_count()
        self.update_output_line_numbers()
        self.update_output_line_count()
        self.update_deleted_lines_and_errors()

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

        errores_editor = CodeProcessor.count_errors_in_cleaned_code(
            orig_lines, clean_lines, self.highlighted_lines, self.highlighted_output_lines
        )
        self.errors_label.setText(f"Errors Found: {errores_editor}")

    def clean_code(self):
        code = self.editor.toPlainText()
        if not code.strip():
            return
            
        cleaned, self.mapa_limpio_a_original = CodeProcessor.clean_code(code)
        
        self.highlighted_output_lines.clear()
        self.output.setPlainText(cleaned)
        self.sync_highlight_to_output()
        self.update_output_line_numbers()
        self.update_deleted_lines_and_errors()

    def sync_highlight_to_output(self):
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
        self.selected_count_label.setText(f"Selected Lines: {len(self.highlighted_lines)}")

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

        self.highlighted_lines.update(range(from_line, to_line + 1))
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
        if not hasattr(self, 'editor') or obj != self.editor:
            return super().eventFilter(obj, event)
            
        if event.type() == event.Type.KeyPress:
            if (event.modifiers() & Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_V) or \
               (event.modifiers() & Qt.KeyboardModifier.ShiftModifier and event.key() == Qt.Key.Key_Insert):
                return False
            return True
        if event.type() == event.Type.MouseButtonDblClick or event.type() == event.Type.MouseButtonPress:
            return True
        return super().eventFilter(obj, event)

    def show_instructions_dialog(self):
        dialog = InstructionsDialog(self)
        dialog.exec()
        
        if dialog.dont_show:
            pass

    def show_instructions_manually(self):
        dialog = InstructionsDialog(self)
        dialog.exec()

def main():
    app = QApplication(sys.argv)
    window = CodeCleaner()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()