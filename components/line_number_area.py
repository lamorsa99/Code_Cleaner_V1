from PyQt6.QtWidgets import QPlainTextEdit
from PyQt6.QtGui import QFont, QPainter, QColor
from PyQt6.QtCore import Qt

class LineNumberArea(QPlainTextEdit):
    def __init__(self, editor, parent_widget=None):
        super().__init__()
        self.editor = editor
        self.parent_widget = parent_widget
        self._setup_widget()
        self._connect_signals()
        self.clicked_line = None

    def _setup_widget(self):
        """Configura las propiedades básicas del widget"""
        self.setReadOnly(True)
        self.setMaximumWidth(55)
        self.setFont(QFont("Consolas", 11))
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setStyleSheet("background-color: #f5f5f5; color: #888; border: none;")

    def _connect_signals(self):
        """Conecta las señales necesarias"""
        self.editor.verticalScrollBar().valueChanged.connect(self.sync_scroll)
        self.editor.blockCountChanged.connect(self.update_numbers)
        self.editor.updateRequest.connect(self.update_numbers)

    def _is_line_highlighted(self, line_number):
        """Verifica si una línea está resaltada"""
        if not self.parent_widget:
            return False
        
        if self.editor is self.parent_widget.editor:
            return line_number in self.parent_widget.highlighted_lines
        elif self.editor is self.parent_widget.output:
            return line_number in self.parent_widget.highlighted_output_lines
        return False

    def _draw_line_number(self, painter, block_number, y, highlighted):
        """Dibuja el número de línea y el icono si está resaltado"""
        font_metrics = self.fontMetrics()
        number_str = str(block_number + 1)
        number_width = font_metrics.horizontalAdvance(number_str)
        area_width = self.width()
        number_x = area_width - number_width - 4
        x_x = 4

        if highlighted:
            painter.setPen(QColor(200, 200, 0))
            painter.drawText(x_x, y, "❌")
            painter.setPen(QColor(136, 136, 136))
            painter.drawText(number_x, y, number_str)
        else:
            painter.setPen(QColor(136, 136, 136))
            painter.drawText(number_x, y, number_str)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self.viewport())
        font_metrics = self.fontMetrics()
        block = self.editor.document().firstBlock()
        block_number = 0

        while block.isValid():
            rect = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset())
            top = int(rect.top())
            block_height = font_metrics.height()
            y = top + block_height // 2 + font_metrics.ascent() // 2

            highlighted = self._is_line_highlighted(block_number)
            self._draw_line_number(painter, block_number, y, highlighted)
            
            block = block.next()
            block_number += 1

    def _get_clicked_line_number(self, y):
        """Obtiene el número de línea en la posición Y del click"""
        editor = self.editor
        block = editor.firstVisibleBlock()
        block_number = block.blockNumber()
        top = editor.blockBoundingGeometry(block).translated(editor.contentOffset()).top()
        bottom = top + editor.blockBoundingRect(block).height()

        while block.isValid() and top <= y:
            if top <= y <= bottom:
                return block_number
            block = block.next()
            top = bottom
            bottom = top + editor.blockBoundingRect(block).height()
            block_number = block.blockNumber()
        
        return block_number

    def _handle_icon_click(self, event, line_number):
        """Maneja el click en el icono de error (❌)"""
        if not self.parent_widget:
            return False

        highlighted = self._is_line_highlighted(line_number)
        if not highlighted:
            return False

        font_metrics = self.fontMetrics()
        editor = self.editor
        block = editor.document().findBlockByNumber(line_number)
        rect = editor.blockBoundingGeometry(block).translated(editor.contentOffset())
        
        rect_x = 4
        rect_y = int(rect.top())
        rect_w = font_metrics.horizontalAdvance("❌") + 4
        rect_h = font_metrics.height()

        if (rect_x <= event.position().x() <= rect_x + rect_w and
            rect_y <= event.position().y() <= rect_y + rect_h):
            self._toggle_line_highlight(line_number)
            return True
        return False

    def _toggle_line_highlight(self, line_number):
        """Alterna el resaltado de una línea"""
        if not self.parent_widget:
            return

        if self.editor is self.parent_widget.editor:
            self.parent_widget.toggle_highlight_line(line_number)
        elif self.editor is self.parent_widget.output:
            self.parent_widget.toggle_highlight_output_line(line_number)

    def mousePressEvent(self, event):
        y = event.position().y()
        line_number = self._get_clicked_line_number(y)

        # Intentar click en icono primero
        if not self._handle_icon_click(event, line_number):
            # Si no fue click en icono, alternar resaltado de línea
            self._toggle_line_highlight(line_number)
        
        super().mousePressEvent(event)

    def sync_scroll(self, value):
        self.verticalScrollBar().setValue(value)

    def update_numbers(self, *args):
        self.update()
        self.setFixedHeight(self.editor.viewport().height())

    def wheelEvent(self, event):
        event.ignore()