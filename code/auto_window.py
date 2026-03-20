import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QTextEdit, 
                             QPushButton, QMessageBox, QFileDialog, QDialog, )
from PyQt5.QtGui import QRegExpValidator, QIntValidator
from PyQt5.QtCore import Qt, QRegExp

from auto_proc import auto_copy

class AutoMenu(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        # Настройка главного окна
        self.setWindowTitle('Автоматическое копирование')
        self.setGeometry(300, 300, 600, 500)
        
        # Создаем центральный виджет и главный layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Создаем layout для двух небольших полей ввода
        small_fields_layout = QVBoxLayout()
    
        
        # Добавляем небольшие поля в главный layout
        main_layout.addLayout(small_fields_layout)
        
        # ========== ПЕРВОЕ ПОЛЕ ДЛЯ ВЫБОРА ДИРЕКТОРИИ ==========
        dir1_layout = QVBoxLayout()
        label_dir1 = QLabel('Путь к папке с шаблонами паспортов:')
        
        # Горизонтальный layout для поля ввода и кнопки
        dir1_input_layout = QHBoxLayout()
        
        self.dir1_path_input = QLineEdit()
        self.dir1_path_input.setPlaceholderText('Выберите папку с шаблонами паспортов')
        self.dir1_path_input.setReadOnly(True)
        self.dir1_path_input.textChanged.connect(self.check_inputs_validity)
        
        self.dir1_button = QPushButton('Обзор...')
        self.dir1_button.clicked.connect(self.select_directory1)
        
        dir1_input_layout.addWidget(self.dir1_path_input)
        dir1_input_layout.addWidget(self.dir1_button)
        
        dir1_layout.addWidget(label_dir1)
        dir1_layout.addLayout(dir1_input_layout)
        
        main_layout.addLayout(dir1_layout)
        
        # ========== ВТОРОЕ ПОЛЕ ДЛЯ ВЫБОРА ДИРЕКТОРИИ ==========
        dir2_layout = QVBoxLayout()
        label_dir2 = QLabel('Путь для сохранения готовых паспортов:')
        
        # Горизонтальный layout для поля ввода и кнопки
        dir2_input_layout = QHBoxLayout()
        
        self.dir2_path_input = QLineEdit()
        self.dir2_path_input.setPlaceholderText('Выберите папку для сохранения новых паспортов')
        self.dir2_path_input.setReadOnly(True)
        self.dir2_path_input.textChanged.connect(self.check_inputs_validity)
        
        self.dir2_button = QPushButton('Обзор...')
        self.dir2_button.clicked.connect(self.select_directory2)
        
        dir2_input_layout.addWidget(self.dir2_path_input)
        dir2_input_layout.addWidget(self.dir2_button)
        
        dir2_layout.addWidget(label_dir2)
        dir2_layout.addLayout(dir2_input_layout)
        
        main_layout.addLayout(dir2_layout)
        
        # ========== ПОЛЕ ДЛЯ ВЫБОРА ФАЙЛА ==========
        file_layout = QVBoxLayout()
        label_file = QLabel('Путь к файлу с шильдами:')
        
        # Горизонтальный layout для поля ввода и кнопки
        file_input_layout = QHBoxLayout()
        
        self.file_path_input = QLineEdit()
        self.file_path_input.setPlaceholderText('Выберите файл с шильдами')
        self.file_path_input.setReadOnly(True)
        self.file_path_input.textChanged.connect(self.check_inputs_validity)
        
        self.file_button = QPushButton('Обзор...')
        self.file_button.clicked.connect(self.select_file)
        
        file_input_layout.addWidget(self.file_path_input)
        file_input_layout.addWidget(self.file_button)
        
        file_layout.addWidget(label_file)
        file_layout.addLayout(file_input_layout)
        
        main_layout.addLayout(file_layout)
        
        # Словарь для всех введённых данных
        self.input_data = {}
        
        # Создаем layout для кнопок
        buttons_layout = QHBoxLayout()
        
        # Кнопка "Принять"
        self.accept_button = QPushButton('Принять')
        self.accept_button.clicked.connect(self.accept_action)
        self.accept_button.setEnabled(False)
        buttons_layout.addWidget(self.accept_button)
        
        # Кнопка "Выйти"
        exit_button = QPushButton('Выйти')
        exit_button.clicked.connect(self.exit_action)
        buttons_layout.addWidget(exit_button)
        
        # Добавляем кнопки в главный layout
        main_layout.addLayout(buttons_layout)
        
        # Добавляем метку для отображения ошибок
        self.error_label = QLabel('')
        self.error_label.setStyleSheet('color: red')
        main_layout.addWidget(self.error_label)
    
    # ========== МЕТОДЫ ДЛЯ ВЫБОРА ДИРЕКТОРИЙ И ФАЙЛА ==========
    def select_directory1(self):
        """Открывает диалог выбора первой директории"""
        directory_path = QFileDialog.getExistingDirectory(
            self,
            "Выберите первую директорию",
            "",
            QFileDialog.ShowDirsOnly
        )
        
        if directory_path:
            self.dir1_path_input.setText(directory_path)
    
    def select_directory2(self):
        """Открывает диалог выбора второй директории"""
        directory_path = QFileDialog.getExistingDirectory(
            self,
            "Выберите вторую директорию",
            "",
            QFileDialog.ShowDirsOnly
        )
        
        if directory_path:
            self.dir2_path_input.setText(directory_path)
    
    def select_file(self):
        """Открывает диалог выбора файла"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл",
            "",
            "Все файлы (*);;Текстовые файлы (*.txt);;Изображения (*.png *.jpg *.bmp)"
        )
        
        if file_path:
            self.file_path_input.setText(file_path)
    
    # Метод для проверки валидности
    def check_inputs_validity(self):
        # Получаем текст из полей
        dir1_path = self.dir1_path_input.text()
        dir2_path = self.dir2_path_input.text()
        file_path = self.file_path_input.text()
        
        # Проверяем поля (не должны быть пустыми)
        is_valid_dir1 = bool(dir1_path.strip())
        is_valid_dir2 = bool(dir2_path.strip())
        is_valid_file = bool(file_path.strip())
        
        # Обновляем стиль полей в зависимости от валидности
        self.update_field_style(self.dir1_path_input, is_valid_dir1)
        self.update_field_style(self.dir2_path_input, is_valid_dir2)
        self.update_field_style(self.file_path_input, is_valid_file)
        
        # Обновляем сообщение об ошибке
        error_messages = []
        if not is_valid_dir1:
            error_messages.append("Необходимо выбрать первую директорию")
        
        if not is_valid_dir2:
            error_messages.append("Необходимо выбрать вторую директорию")
        
        if not is_valid_file:
            error_messages.append("Необходимо выбрать файл")
        
        if error_messages:
            self.error_label.setText('\n'.join(error_messages))
        else:
            self.error_label.setText('')
        
        # Активируем кнопку только если все поля валидны
        self.accept_button.setEnabled(is_valid_dir1 and is_valid_dir2 and is_valid_file)
    
    #мтеод проверки валидности полей для путей
    def update_field_style(self, field, is_valid):

        if is_valid:
            field.setStyleSheet("")
        else:
            field.setStyleSheet("border: 1px solid red;")
    
    # методок для получения всех данных понажатию кнопки "Принять"
    def accept_action(self):
        # Получаем данные из полей ввода
        dir1_path = self.dir1_path_input.text()
        dir2_path = self.dir2_path_input.text()
        file_path = self.file_path_input.text()
        
        # Дополнительная проверка перед обработкой
        if not (dir1_path.strip() and
                dir2_path.strip() and
                file_path.strip()) :
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, исправьте ошибки в полях ввода')
            return
        
        # Переносим все данные в словарь для дальнейшей работы
        self.input_data = {
            'directory1_path': dir1_path,
            'directory2_path': dir2_path,
            'file_path': file_path,
        }
        
        # Выводим данные
        print("Авто метод:\nДанные приняты: ", self.input_data,'\n')
        # Запускаем создание копий
        auto_copy(self.input_data)
    # Закрывает окно
    def exit_action(self):
        self.close()