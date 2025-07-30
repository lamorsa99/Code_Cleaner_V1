class StyleManager:
    """Maneja todos los estilos de la aplicación"""
    
    @staticmethod
    def get_main_style():
        return """
            QWidget {
                background-color: #f8fafc;
            }
            QLabel {
                font-size: 16px;
                color: #2d3748;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QPushButton {
                background-color: #e2e8f0;
                color: #2d3748;
                border-radius: 0px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
                border: 1px solid #000000;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #cbd5e0;
            }
            QPlainTextEdit {
                background-color: #ffffff;
                color: #2d3748;
                border-radius: 0px;
                font-size: 13px;
                border: 1px solid #000000;
                font-family: 'Consolas', 'Monaco', monospace;
            }
            QLineEdit {
                background: #ffffff;
                color: #2d3748;
                border-radius: 0px;
                border: 1px solid #000000;
                padding: 8px 12px;
                font-size: 13px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QGroupBox {
                border: 1px solid #000000;
                border-radius: 0px;
                margin-top: 12px;
                margin-bottom: 6px;
                margin-left: 3px;
                margin-right: 3px;
                background: #ffffff;
                padding-top: 20px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QGroupBox:title {
                color: #1a365d;
                font-size: 16px;
                font-weight: bold;
                left: 20px;
                top: 12px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """

    @staticmethod
    def get_dialog_style():
        return """
            QDialog {
                background-color: #f7fafd;
                border-radius: 0px;
            }
            QLabel {
                color: #222;
                font-size: 14px;
                line-height: 1.5;
            }
            QPushButton {
                background-color: #1976d2;
                color: white;
                border-radius: 0px;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
                border: 1px solid #000000;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QWidget#content {
                background-color: #fff;
                border-radius: 0px;
                border: 1px solid #000000;
            }
        """