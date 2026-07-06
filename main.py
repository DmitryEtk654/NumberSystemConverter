import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from ui_main import MainWindow

def main():
    app = QApplication(sys.argv) #создание приложения
    app.setApplicationName("NumberSystemConverter")
    app.setFont(QFont("Segoe UI", 10))

    try:
        with open("assets/style.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        pass
    
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__=="__main__":
    main()
