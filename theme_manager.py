from PyQt5.QtCore import QSettings

class ThemeManager:
    light = "light"
    dark = "dark"

    def __init__(self):
        self.settings = QSettings("MyCompany", "NumberConverter")
        saved = self.settings.value("theme", self.light)
        self.current_theme = saved if saved is not None else self.light

    def get_theme(self):
        return self.current_theme

    def set_theme(self, theme):
        self.current_theme = theme
        self.settings.setValue("theme", theme)

    def get_style(self):
        if self.current_theme == self.dark:
            return """
                QMainWindow { background-color: #1e1e1e; }
                QWidget { background-color: #1e1e1e; }
                QLabel { color: #e8e8e8; }

                QPushButton {
                    background-color: #3d3d3d;
                    color: #ffffff;
                    border: 1px solid #555555;
                    border-radius: 5px;
                    padding: 8px 15px;
                }
                QPushButton:hover {
                    background-color: #4d4d4d;
                    border-color: #4CAF50;
                }

                QPushButton#btn_convert {
                    background-color: #2e7d32;
                    color: #ffffff;
                    border: 2px solid #4CAF50;
                    font-weight: bold;
                }
                QPushButton#btn_convert:hover {
                    background-color: #388e3c;
                    border-color: #66bb6a;
                }

                QLineEdit {
                    background-color: #2d2d2d;
                    color: #e8e8e8;
                    border: 2px solid #444444;
                    border-radius: 5px;
                    padding: 8px;
                }
                QLineEdit:focus { border-color: #4CAF50; }

                QComboBox {
                    background-color: #2d2d2d;
                    color: #e8e8e8;
                    border: 2px solid #444444;
                    border-radius: 5px;
                    padding: 8px;
                }
                QComboBox:hover { border-color: #4CAF50; }
                QComboBox QAbstractItemView {
                    background-color: #2d2d2d;
                    color: #e8e8e8;
                }
                QComboBox QAbstractItemView::item:hover {
                    background-color: #4CAF50;
                    color: #ffffff;
                }

                QTableWidget {
                    background-color: #2d2d2d;
                    gridline-color: #444444;
                    border: 1px solid #444444;
                    border-radius: 5px;
                }
                QTableWidget::item {
                    color: #ffffff;
                    padding: 5px;
                    background-color: #2d2d2d;
                }
                QTableWidget::item:selected {
                    background-color: #4CAF50;
                    color: #ffffff;
                }
                QTableWidget::item:hover {
                    background-color: #3d3d3d;
                }
                QHeaderView::section {
                    background-color: #2c2c2c;
                    color: #ffffff;
                    padding: 8px;
                    border: none;
                    font-weight: bold;
                }
                QHeaderView::section:hover {
                    background-color: #3d3d3d;
                }

                QMessageBox {
                    background-color: #2d2d2d;
                    color: #e8e8e8;
                }
                QMessageBox QLabel { color: #e8e8e8; }
                QMessageBox QPushButton {
                    background-color: #3d3d3d;
                    color: #ffffff;
                    border: 1px solid #555555;
                    border-radius: 5px;
                    padding: 8px 15px;
                    min-width: 80px;
                }
                QMessageBox QPushButton:hover {
                    background-color: #4d4d4d;
                }

                QSplitter::handle { background-color: #444444; }
                QSplitter::handle:hover { background-color: #555555; }
                QStatusBar { background-color: #2c2c2c; color: #e8e8e8; }
            """
        else:
            return """
                QMainWindow { background-color: #f0f2f5; }
                QWidget { background-color: #f0f2f5; }
                QLabel { color: #2c3e50; }

                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 8px 15px;
                }
                QPushButton:hover { background-color: #45a049; }

                QLineEdit {
                    background-color: white;
                    color: #2c3e50;
                    border: 2px solid #bdc3c7;
                    border-radius: 5px;
                    padding: 8px;
                }
                QLineEdit:focus { border-color: #4CAF50; }

                QComboBox {
                    background-color: white;
                    color: #2c3e50;
                    border: 2px solid #bdc3c7;
                    border-radius: 5px;
                    padding: 8px;
                }
                QComboBox:hover { border-color: #4CAF50; }

                QTableWidget {
                    background-color: white;
                    gridline-color: #dee2e6;
                    border: 1px solid #dee2e6;
                    border-radius: 5px;
                }
                QTableWidget::item {
                    color: #2c3e50;
                    padding: 5px;
                }
                QTableWidget::item:selected {
                    background-color: #4CAF50;
                    color: white;
                }
                QTableWidget::item:hover {
                    background-color: #e8f5e9;
                }
                QHeaderView::section {
                    background-color: #2c3e50;
                    color: white;
                    padding: 8px;
                    border: none;
                    font-weight: bold;
                }

                QMessageBox { background-color: white; }
                QMessageBox QPushButton {
                    min-width: 80px;
                    padding: 8px 15px;
                }

                QSplitter::handle { background-color: #bdc3c7; }
                QSplitter::handle:hover { background-color: #95a5a6; }
                QStatusBar { background-color: #2c3e50; color: white; }
            """
