class StyleManager:
    """Maneja todos los estilos de la aplicación"""
    
    @staticmethod
    def get_main_style():
        return """
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
            }
            QPushButton:hover {
                background-color: #d0d6e0;
            }
            QPlainTextEdit {
                background-color: #f9f9fb;
                color: #222;
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid #b0b0b0;
            }
            QLineEdit {
                background: #fff;
                color: #222;
                border-radius: 6px;
                border: 1px solid #b0b0b0;
                padding: 4px 10px;
                font-size: 14px;
            }
            QGroupBox {
                border: 2px solid #e0e0e0;
                border-radius: 14px;
                margin-top: 8px;
                margin-bottom: 4px;
                margin-left: 2px;
                margin-right: 2px;
                background: #fff;
                padding-top: 18px;
            }
            QGroupBox:title {
                color: #1976d2;
                font-size: 18px;
                font-weight: bold;
                left: 16px;
                top: 8px;
            }
        """

    @staticmethod
    def get_dialog_style():
        return """
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
                background-color: #1976d2;
                color: white;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
                border: none;
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
                border-radius: 10px;
                border: 1px solid #e0e0e0;
            }
        """