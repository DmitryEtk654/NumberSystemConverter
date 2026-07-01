from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("number converter system")
        self.resize(800, 600)
        self.setMinimumSize(700, 500)

        central = QWidget()
        self.setCentralWidget(central)
