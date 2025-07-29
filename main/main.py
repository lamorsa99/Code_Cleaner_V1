import sys
import re
from PyQt6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPlainTextEdit, QPushButton, QLabel
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class LineNumberArea(QPlainTextEdit):
    def __init__(self, editor):
        super().__init__()
        self.editor = editor
        self.setReadOnly(True)
        self.setMaximumWidth(45)
        self.setFont(QFont("Courier", 10))
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
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
        self.resize(800, 600)
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Ingresa tu código aquí:"))

        code_layout = QHBoxLayout()
        self.editor = QPlainTextEdit()
        self.editor.setFont(QFont("Courier", 10))
        self.line_numbers = LineNumberArea(self.editor)
        self.editor.textChanged.connect(self.update_line_numbers)
        self.editor.textChanged.connect(self.update_line_count)  # Nueva conexión
        code_layout.addWidget(self.line_numbers)
        code_layout.addWidget(self.editor)
        layout.addLayout(code_layout)

        # Etiqueta para mostrar la cantidad de líneas
        self.line_count_label = QLabel("Líneas totales: 0")
        layout.addWidget(self.line_count_label)

        self.clean_btn = QPushButton("Clean Code")
        self.clean_btn.clicked.connect(self.clean_code)
        layout.addWidget(self.clean_btn)

        layout.addWidget(QLabel("Código limpio:"))
        self.output = QPlainTextEdit()
        self.output.setFont(QFont("Courier", 10))
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.copy_btn = QPushButton("Copiar Resultado")
        self.copy_btn.clicked.connect(self.copy_result)
        layout.addWidget(self.copy_btn)

        self.update_line_numbers()
        self.update_line_count()  # Inicializa el contador

    def update_line_numbers(self):
        self.line_numbers.update_numbers()
        self.line_numbers.verticalScrollBar().setValue(self.editor.verticalScrollBar().value())

    def update_line_count(self):
        text = self.editor.toPlainText()
        lines = text.split('\n')
        self.line_count_label.setText(f"Líneas totales: {len(lines)}")

    def clean_code(self):
        code = self.editor.toPlainText()
        code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        lines = [line.strip() for line in code.split('\n') if line.strip()]
        self.output.setPlainText('\n'.join(lines))

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