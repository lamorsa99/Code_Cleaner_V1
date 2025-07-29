import sys
import re
from PyQt6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPlainTextEdit, QPushButton, QLabel, QFrame, QSizePolicy, QTextEdit, QLineEdit
)
from PyQt6.QtGui import QFont, QTextCursor, QTextCharFormat, QColor, QPainter
from PyQt6.QtCore import Qt

class LineNumberArea(QPlainTextEdit):
    def __init__(self, editor, parent_widget=None):
        super().__init__()
        self.editor = editor
        self.parent_widget = parent_widget
        self.setReadOnly(True)
        self.setMaximumWidth(55)
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
            y = top + font_metrics.ascent()
            highlighted = False
            if self.parent_widget:
                if self.editor is self.parent_widget.editor:
                    highlighted = block_number in self.parent_widget.highlighted_lines
                elif self.editor is self.parent_widget.output:
                    highlighted = block_number in self.parent_widget.highlighted_output_lines
            x_x = 4  # margen izquierdo
            if highlighted:
                painter.setPen(QColor(200, 0, 0))
                painter.drawText(x_x, y, "❌")
                number_x = x_x + font_metrics.horizontalAdvance("❌") + 6
            else:
                number_x = x_x
            painter.setPen(QColor(136, 136, 136))
            painter.drawText(number_x, y, str(block_number + 1))
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

class CodeCleaner(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Code Cleaner V1 (PyQt6)")
        self.resize(1100, 650)
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
            }
            QLabel {
                font-size: 16px;
                color: #222;
            }
            QPushButton {
                background-color: #e3e6ee;
                color: #222;
                border-radius: 6px;
                padding: 8px 18px;
                font-size: 14px;
                border: 1px solid #b0b0b0;
            }
            QPushButton:hover {
                background-color: #d0d6e0;
            }
            QPlainTextEdit {
                background-color: #f9f9fb;
                color: #222;
                border-radius: 6px;
                font-size: 13px;
                border: 1px solid #b0b0b0;
            }
            QLineEdit {
                background: #fff;
                color: #222;
                border-radius: 4px;
                border: 1px solid #b0b0b0;
                padding: 2px 6px;
                font-size: 13px;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(14)
        main_layout.setContentsMargins(30, 20, 30, 20)

        title = QLabel("🧹 <b>Code Cleaner V1</b>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; margin-bottom: 10px; color: #1976d2;")
        main_layout.addWidget(title)

        editors_layout = QHBoxLayout()
        editors_layout.setSpacing(18)

        # --- Cuadro izquierdo: Código sucio ---
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Código original:"))

        range_layout = QHBoxLayout()
        self.from_box = QLineEdit()
        self.from_box.setPlaceholderText("from")
        self.from_box.setFixedWidth(50)
        self.to_box = QLineEdit()
        self.to_box.setPlaceholderText("to")
        self.to_box.setFixedWidth(50)
        self.select_btn = QPushButton("Select")
        self.select_btn.setFixedWidth(60)
        self.unselect_btn = QPushButton("Desmarcar")
        self.unselect_btn.setFixedWidth(80)
        range_layout.addWidget(self.from_box)
        range_layout.addWidget(self.to_box)
        range_layout.addWidget(self.select_btn)
        range_layout.addWidget(self.unselect_btn)
        range_layout.addStretch()
        left_layout.addLayout(range_layout)

        code_frame = QFrame()
        code_frame.setFrameShape(QFrame.Shape.StyledPanel)
        code_frame.setStyleSheet("background: #f5f7fa; border-radius: 8px;")
        code_layout = QHBoxLayout(code_frame)
        code_layout.setContentsMargins(8, 8, 8, 8)
        code_layout.setSpacing(0)

        self.editor = QPlainTextEdit()
        self.editor.setFont(QFont("Consolas", 11))
        self.editor.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.editor.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.editor.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.line_numbers = LineNumberArea(self.editor, self)
        self.editor.textChanged.connect(self.update_line_numbers)
        self.editor.textChanged.connect(self.update_line_count)
        code_layout.addWidget(self.line_numbers)
        code_layout.addWidget(self.editor)
        left_layout.addWidget(code_frame, stretch=2)

        self.line_count_label = QLabel("Líneas totales: 0")
        self.line_count_label.setStyleSheet("color: #1976d2; margin-bottom: 8px; font-weight: bold;")
        left_layout.addWidget(self.line_count_label)

        self.clean_btn = QPushButton("🧼 Limpiar Código")
        self.clean_btn.clicked.connect(self.clean_code)
        self.clean_btn.setStyleSheet("margin-bottom: 10px;")
        left_layout.addWidget(self.clean_btn)

        editors_layout.addLayout(left_layout, stretch=1)

        # --- Cuadro derecho: Código limpio ---
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Código limpio:"))

        output_frame = QFrame()
        output_frame.setFrameShape(QFrame.Shape.StyledPanel)
        output_frame.setStyleSheet("background: #f5f7fa; border-radius: 8px;")
        output_layout = QHBoxLayout(output_frame)
        output_layout.setContentsMargins(8, 8, 8, 8)
        output_layout.setSpacing(0)

        self.output = QPlainTextEdit()
        self.output.setFont(QFont("Consolas", 11))
        self.output.setReadOnly(True)
        self.output.setStyleSheet("background-color: #f5f5f5; color: #1976d2; border-radius: 6px;")
        self.output.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.output.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.output.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.output_line_numbers = LineNumberArea(self.output, self)
        self.output.textChanged.connect(self.update_output_line_numbers)
        output_layout.addWidget(self.output_line_numbers)
        output_layout.addWidget(self.output)
        right_layout.addWidget(output_frame, stretch=2)

        self.output_line_count_label = QLabel("Líneas limpias: 0")
        self.output_line_count_label.setStyleSheet("color: #388e3c; margin-bottom: 8px; font-weight: bold;")
        right_layout.addWidget(self.output_line_count_label)

        self.copy_btn = QPushButton("📋 Copiar Resultado")
        self.copy_btn.clicked.connect(self.copy_result)
        right_layout.addWidget(self.copy_btn)

        editors_layout.addLayout(right_layout, stretch=1)

        main_layout.addLayout(editors_layout)

        self.update_line_numbers()
        self.update_line_count()
        self.update_output_line_numbers()
        self.update_output_line_count()

        self.highlighted_lines = set()
        self.highlighted_output_lines = set()

        self.select_btn.clicked.connect(self.select_lines_range)
        self.unselect_btn.clicked.connect(self.unselect_lines_range)

    def update_line_numbers(self):
        self.line_numbers.update_numbers()
        self.line_numbers.verticalScrollBar().setValue(self.editor.verticalScrollBar().value())

    def update_line_count(self):
        text = self.editor.toPlainText()
        lines = text.split('\n')
        self.line_count_label.setText(f"Líneas totales: {len(lines)}")

    def update_output_line_numbers(self):
        self.output_line_numbers.update_numbers()
        self.output_line_numbers.verticalScrollBar().setValue(self.output.verticalScrollBar().value())
        self.update_output_line_count()

    def update_output_line_count(self):
        text = self.output.toPlainText()
        lines = text.split('\n')
        self.output_line_count_label.setText(f"Líneas limpias: {len(lines)}")

    def clean_code(self):
        code = self.editor.toPlainText()
        code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        lines = [line.strip() for line in code.split('\n') if line.strip()]
        cleaned = '\n'.join(lines)
        self.output.setPlainText(cleaned)
        self.update_output_line_numbers()

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
        if line_number in self.highlighted_output_lines:
            self.highlighted_output_lines.remove(line_number)
        else:
            self.highlighted_output_lines.add(line_number)
        self.highlight_output_line()
        self.output_line_numbers.update()

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

        self.highlighted_lines.update(range(from_line, to_line + 1))  # <-- Acumula rangos
        self.highlight_line()
        self.line_numbers.update()

        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Start)
        cursor.movePosition(QTextCursor.MoveOperation.Down, QTextCursor.MoveMode.MoveAnchor, from_line)
        self.editor.setTextCursor(cursor)
        self.editor.ensureCursorVisible()

    def unselect_lines_range(self):
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

        for line in range(from_line, to_line + 1):
            self.highlighted_lines.discard(line)
        self.highlight_line()
        self.line_numbers.update()

def main():
    app = QApplication(sys.argv)
    window = CodeCleaner()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()