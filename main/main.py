import sys
import re
from PyQt6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPlainTextEdit, QPushButton, QLabel, QFrame, QSizePolicy
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class LineNumberArea(QPlainTextEdit):
    def __init__(self, editor):
        super().__init__()
        self.editor = editor
        self.setReadOnly(True)
        self.setMaximumWidth(55)
        self.setFont(QFont("Consolas", 11))
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setStyleSheet("background-color: #f5f5f5; color: #888; border: none;")
        self.editor.verticalScrollBar().valueChanged.connect(self.sync_scroll)

    def sync_scroll(self, value):
        self.verticalScrollBar().setValue(value)

    def update_numbers(self):
        block_count = self.editor.blockCount()
        numbers = "\n".join(str(i+1) for i in range(block_count))
        self.setPlainText(numbers)

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
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(14)
        main_layout.setContentsMargins(30, 20, 30, 20)

        title = QLabel("🧹 <b>Code Cleaner V1</b>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; margin-bottom: 10px; color: #1976d2;")
        main_layout.addWidget(title)

        # Layout horizontal para los dos cuadros principales
        editors_layout = QHBoxLayout()
        editors_layout.setSpacing(18)

        # --- Cuadro izquierdo: Código sucio ---
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Código original:"))

        code_frame = QFrame()
        code_frame.setFrameShape(QFrame.Shape.StyledPanel)
        code_frame.setStyleSheet("background: #f5f7fa; border-radius: 8px;")
        code_layout = QHBoxLayout(code_frame)
        code_layout.setContentsMargins(8, 8, 8, 8)
        code_layout.setSpacing(0)

        self.editor = QPlainTextEdit()
        self.editor.setFont(QFont("Consolas", 11))
        self.editor.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.line_numbers = LineNumberArea(self.editor)
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
        self.output_line_numbers = LineNumberArea(self.output)
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

def main():
    app = QApplication(sys.argv)
    window = CodeCleaner()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()