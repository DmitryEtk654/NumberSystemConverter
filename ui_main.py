from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence
from logic import convert
from database import HistoryManager
from logic import detect_base
import json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NumberSystemConventer")
        self.resize(1100, 900)
        self.setMinimumSize(1000, 800)
        
        self.db = HistoryManager()
        
        central = QWidget()
        self.setCentralWidget(central)
        
        self._setup_ui()
        self._bind_signals()
        self._refresh_history()

        self.shortcut_convert = QShortcut(QKeySequence("Ctrl+Enter"), self)
        self.shortcut_convert.activated.connect(self._on_convert)

        self.shortcut_clear = QShortcut(QKeySequence("Ctrl+Shift+C"), self)
        self.shortcut_clear.activated.connect(self._clear_fields)

        self.shortcut_copy = QShortcut(QKeySequence("Ctrl+C"), self)
        self.shortcut_copy.activated.connect(self._copy_result)
    
    def _setup_ui(self):
        main_layout = QHBoxLayout()
        self.centralWidget().setLayout(main_layout)
        
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        title = QLabel("Конвертер систем счисления")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        left_layout.addWidget(title)
        
        left_layout.addSpacing(10)
        
        left_layout.addWidget(QLabel("Введите число:"))
        self.input_num = QLineEdit()
        self.input_num.setPlaceholderText("Например: 1010, FF, 255")
        self.input_num.setMinimumHeight(30)
        left_layout.addWidget(self.input_num)
        
        left_layout.addSpacing(10)
        
        form_layout = QFormLayout()
        
        self.base_from = QComboBox()
        self.base_from.addItems(["2 (Двоичная)", "8 (Восьмеричная)", "10 (Десятичная)", "16 (Шестнадцатеричная)"])
        self.base_from.setCurrentIndex(2)
        form_layout.addRow("Из системы:", self.base_from)
        
        self.base_to = QComboBox()
        self.base_to.addItems(["2 (Двоичная)", "8 (Восьмеричная)", "10 (Десятичная)", "16 (Шестнадцатеричная)"])
        self.base_to.setCurrentIndex(0)
        form_layout.addRow("В систему:", self.base_to)
        
        left_layout.addLayout(form_layout)
        
        left_layout.addSpacing(10)
        
        self.btn_convert = QPushButton("Конвертировать")
        self.btn_convert.setMinimumHeight(40)
        left_layout.addWidget(self.btn_convert)
        
        left_layout.addSpacing(10)
        
        left_layout.addWidget(QLabel("Результат:"))
        self.output = QLineEdit()
        self.output.setReadOnly(True)
        self.output.setMinimumHeight(35)
        left_layout.addWidget(self.output)
        
        left_layout.addSpacing(10)
        
        self.btn_clear = QPushButton("Очистить")

        self.btn_detect = QPushButton("Определить систему")
        self.btn_detect.setMinimumHeight(30)
        left_layout.addWidget(self.btn_detect)
        
        self.btn_copy = QPushButton("Копировать результат")
        self.btn_copy.setMinimumHeight(30)
        left_layout.addWidget(self.btn_copy)
        left_layout.addWidget(self.btn_clear)
        
        left_layout.addSpacing(10)
        
        left_layout.addWidget(QLabel("Изображение:"))
        self.image_label = QLabel("Нет изображения")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumHeight(150)
        self.image_label.setStyleSheet("background-color: #f5f5f5; border: 2px dashed #bbb; border-radius: 8px;")
        left_layout.addWidget(self.image_label)
        
        self.btn_load_image = QPushButton("Загрузить изображение")
        left_layout.addWidget(self.btn_load_image)
        
        left_layout.addStretch()
        
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        right_layout.addWidget(QLabel("История конвертаций"))
        
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["Дата", "Число", "Из", "В", "Результат"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.history_table.setEditTriggers(QTableWidget.NoEditTriggers)
        right_layout.addWidget(self.history_table)
        
        btn_layout = QHBoxLayout()
        self.btn_export = QPushButton("Экспорт CSV")
        self.btn_export_json = QPushButton("Экспорт JSON")
        btn_layout.addWidget(self.btn_export_json)
        self.btn_clear_history = QPushButton("Очистить историю")
        btn_layout.addWidget(self.btn_export)
        btn_layout.addWidget(self.btn_clear_history)
        right_layout.addLayout(btn_layout)
        
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([450, 450])
        
        main_layout.addWidget(splitter)
    
    def _bind_signals(self):
        self.btn_convert.clicked.connect(self._on_convert)
        self.btn_clear.clicked.connect(self._clear_fields)
        self.btn_load_image.clicked.connect(self._load_image)
        self.btn_export.clicked.connect(self._export_csv)
        self.btn_export_json.clicked.connect(self._export_json)
        self.btn_clear_history.clicked.connect(self._clear_history)
        self.input_num.returnPressed.connect(self._on_convert)

        self.btn_detect.clicked.connect(self._detect_system)
        self.btn_copy.clicked.connect(self._copy_result)

        
    def _detect_system(self):
        value = self.input_num.text().strip()
        if not value:
            QMessageBox.information(self, "Информация", "Введите число для определения системы")
            return
        
        detected = detect_base(value)
        
        for i in range(self.base_from.count()):
            if str(detected) == self.base_from.itemText(i).split()[0]:
                self.base_from.setCurrentIndex(i)
                break
        
        QMessageBox.information(
            self, "Определена система",
            f"Число '{value}' определено как {detected}-ичная система"
        )
    
    def _copy_result(self):
        result = self.output.text()
        if result:
            clipboard = QApplication.clipboard()
            clipboard.setText(result)
            QMessageBox.information(self, "Успех", "Результат скопирован в буфер обмена")
        else:
            QMessageBox.warning(self, "Ошибка", "Нет результата для копирования")
    
    def _on_convert(self):
        value = self.input_num.text().strip()
        if not value:
            QMessageBox.warning(self, "Ошибка", "Введите число!")
            return
        
        base_from = int(self.base_from.currentText().split()[0])
        base_to = int(self.base_to.currentText().split()[0])
        
        try:
            result = convert(value, base_from, base_to)
            self.output.setText(result)
            self.db.add_record(value, base_from, base_to, result)
            self._refresh_history()
        except ValueError as e:
            QMessageBox.critical(self, "Ошибка", str(e))
            self.output.clear()
    
    def _clear_fields(self):
        self.input_num.clear()
        self.output.clear()
        self.input_num.setFocus()
    
    def _load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите изображение", "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if not file_path:
            return
        
        try:
            from PIL import Image
            img = Image.open(file_path).convert("RGBA")
            img.thumbnail((200, 200), Image.LANCZOS)
            
            data = img.tobytes("raw", "RGBA")
            qimage = QImage(data, img.width, img.height, QImage.Format_RGBA8888)
            pixmap = QPixmap.fromImage(qimage)
            
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить:\n{e}")

    def _export_json(self):
        path, _ = QFileDialog.getSaveFileName(
        self,
        "Сохранить JSON",
        "history.json",
        "JSON files (*.json)"
        )

        if not path:
            return

        records = self.db.get_all()
        if not records:
            QMessageBox.information(self, "Информация", "История пуста")
            return

        try:
            data = []
            for rec in records:
                data.append({
                    "timestamp": rec["timestamp"],
                    "input_value": rec["input_value"],
                    "base_from": rec["base_from"],
                    "base_to": rec["base_to"],
                    "result": rec["result"]
                })

            with open(path, 'w') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            QMessageBox.information(
                self,
                "Успех",
                f"Экспортировано в:\n{path}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
    
    def _refresh_history(self):
        self.history_table.setRowCount(0)
        records = self.db.get_all()
        for i, rec in enumerate(records):
            self.history_table.insertRow(i)
            self.history_table.setItem(i, 0, QTableWidgetItem(rec["timestamp"][:19]))
            self.history_table.setItem(i, 1, QTableWidgetItem(rec["input_value"]))
            self.history_table.setItem(i, 2, QTableWidgetItem(str(rec["base_from"])))
            self.history_table.setItem(i, 3, QTableWidgetItem(str(rec["base_to"])))
            self.history_table.setItem(i, 4, QTableWidgetItem(rec["result"]))
    
    def _export_csv(self):
        import csv
        path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить CSV", "history.csv", "CSV files (*.csv)"
        )
        if not path:
            return
        
        records = self.db.get_all()
        if not records:
            QMessageBox.information(self, "Инфо", "История пуста")
            return
        
        try:
            with open(path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(["Дата", "Число", "Из", "В", "Результат"])
                for rec in records:
                    writer.writerow([
                        rec["timestamp"], rec["input_value"],
                        rec["base_from"], rec["base_to"], rec["result"]
                    ])
            QMessageBox.information(self, "Успех", f"Сохранено в {path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
    
    def _clear_history(self):
        if QMessageBox.question(
            self, "Подтверждение",
            "Удалить всю историю?",
            QMessageBox.Yes | QMessageBox.No
        ) == QMessageBox.Yes:
            self.db.clear()
            self._refresh_history()
    
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, "Выход",
            "Закрыть приложение?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.db.close()
            event.accept()
        else:
            event.ignore()
