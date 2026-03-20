import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QTextEdit, 
                             QPushButton, QMessageBox, QFileDialog, QDialog, )
from PyQt5.QtGui import QRegExpValidator, QIntValidator
from PyQt5.QtCore import Qt, QRegExp

from manual_porc import manual_copy

class ManualMenu(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        # Настройка главного окна
        self.setWindowTitle('Ручная настройка')
        self.setGeometry(300, 300, 600, 500)
        
        # Создаем центральный виджет и главный layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Создаем layout для двух небольших полей ввода
        small_fields_layout = QVBoxLayout()
        
        # Поле на ввод серийного номера
        label1 = QLabel('Серийный номер:')
        self.small_input1 = QLineEdit()
        self.small_input1.setPlaceholderText('Введите серийный номер')
        
        # Подключаем сигнал изменения текста для проверки валидности
        self.small_input1.textChanged.connect(self.check_inputs_validity)
        
        small_fields_layout.addWidget(label1)
        small_fields_layout.addWidget(self.small_input1)
        
        # Поле для количетсмва копий штук в одной позиции
        label2 = QLabel('Количество копий в позиции(включая оригинал):')
        self.small_input2 = QLineEdit()
        self.small_input2.setPlaceholderText('Введите количество копий в одной позиции')
        
        # Устанавливаем валидатор для поля количетсмва копий штук в одной позиции
        reg_ex2 = QRegExp("^[1-9][0-9]*$")
        input_validator2 = QRegExpValidator(reg_ex2, self.small_input2)
        self.small_input2.setValidator(input_validator2)
        
        # Подключаем сигнал изменения текста для проверки валидности
        self.small_input2.textChanged.connect(self.check_inputs_validity)
        
        small_fields_layout.addWidget(label2)
        small_fields_layout.addWidget(self.small_input2)
        
        # Поле на количестов копий по позициям
        label3 = QLabel('Количество копий в позиции(включая оригинал):')
        self.small_input3 = QLineEdit()
        self.small_input3.setPlaceholderText('Введите количество копий в одной позиции')
        # Количетсов ставится по умолчанию
        self.small_input3.setText('1')
        
        # Устанавливаем валидатор для поля "Количество копий"
        reg_ex3 = QRegExp("^[1-9][0-9]*$")
        input_validator3 = QRegExpValidator(reg_ex3, self.small_input3)
        self.small_input3.setValidator(input_validator3)
        
        # Подключаем сигнал изменения текста для проверки валидности
        self.small_input3.textChanged.connect(self.check_inputs_validity)
        
        small_fields_layout.addWidget(label3)
        small_fields_layout.addWidget(self.small_input3)
        
        # Добавляем небольшие поля в главный layout
        main_layout.addLayout(small_fields_layout)
        
        # ========== ПОЛЕ ДЛЯ ВЫБОРА ДИРЕКТОРИИ ==========
        dir_layout = QVBoxLayout()
        label_dir = QLabel('Путь папке для сохранения копий:')
        
        # Горизонтальный layout для поля ввода и кнопки
        dir_input_layout = QHBoxLayout()
        
        self.dir_path_input = QLineEdit()
        self.dir_path_input.setPlaceholderText('Выберите папку для сохранения копий')
        self.dir_path_input.setReadOnly(True)  # Только для чтения, так как путь выбирается через диалог
        self.dir_path_input.textChanged.connect(self.check_inputs_validity)
        
        self.dir_button = QPushButton('Обзор...')
        self.dir_button.clicked.connect(self.select_directory)
        
        dir_input_layout.addWidget(self.dir_path_input)
        dir_input_layout.addWidget(self.dir_button)
        
        dir_layout.addWidget(label_dir)
        dir_layout.addLayout(dir_input_layout)
        
        main_layout.addLayout(dir_layout)
        
        # ========== ПОЛЕ ДЛЯ ВЫБОРА ФАЙЛА ==========
        file_layout = QVBoxLayout()
        label_file = QLabel('Путь к шаблону паспорта')
        
        # Горизонтальный layout для поля ввода и кнопки
        file_input_layout = QHBoxLayout()
        
        self.file_path_input = QLineEdit()
        self.file_path_input.setPlaceholderText('Выберите docx-файл на основе которого необходимо сделать копии')
        self.file_path_input.setReadOnly(True)  # Только для чтения, так как путь выбирается через диалог
        self.file_path_input.textChanged.connect(self.check_inputs_validity)
        
        self.file_button = QPushButton('Обзор...')
        self.file_button.clicked.connect(self.select_file)
        
        file_input_layout.addWidget(self.file_path_input)
        file_input_layout.addWidget(self.file_button)
        
        file_layout.addWidget(label_file)
        file_layout.addLayout(file_input_layout)
        
        main_layout.addLayout(file_layout)
        
        # ========== БОЛЬШОЕ ПОЛЕ ДЛЯ МНОГОСТРОЧНОГО ВВОДА ==========
        label3 = QLabel('Строки для поиска изображения')
        self.big_input = QTextEdit()
        self.big_input.setPlaceholderText('Например, если нужно удалить подпись Xu Shiming.\nЕсли строк несколько указывать через запятую!!!')
        
        # Подключаем сигнал изменения текста для проверки валидности
        self.big_input.textChanged.connect(self.check_inputs_validity)
        
        main_layout.addWidget(label3)
        main_layout.addWidget(self.big_input)
        
        # Словарь для всех введённых данных
        self.input_data = {}
        
        # Создаем layout для кнопок
        buttons_layout = QHBoxLayout()
        
        # Кнопка "Принять"
        self.accept_button = QPushButton('Принять')
        self.accept_button.clicked.connect(self.accept_action)
        self.accept_button.setEnabled(False)  # Изначально кнопка заблокирована
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
    
    # ========== МЕТОДЫ ДЛЯ ВЫБОРА ДИРЕКТОРИИ И ФАЙЛА ==========
    def select_directory(self):
        """Открывает диалог выбора директории"""
        directory_path = QFileDialog.getExistingDirectory(
            self,
            "Выберите директорию",
            "",
            QFileDialog.ShowDirsOnly
        )
        
        if directory_path:
            self.dir_path_input.setText(directory_path)
    
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
    
    # Проверяет валидность всех полей ввода
    def check_inputs_validity(self):
        
        # Получаем текст из полей
        text1 = self.small_input1.text()
        text2 = self.small_input2.text()
        text3 = self.small_input3.text()
        dir_path = self.dir_path_input.text()
        file_path = self.file_path_input.text()
        text3 = self.big_input.toPlainText()
        
        # Проверяем первое поле (не должно быть пустым)
        is_valid1 = bool(text1.strip())
        
        # Проверяем второе поле
        is_valid2 = self.is_valid_number(text2)
        
        is_valid3 = self.is_valid_number(text3)
        # Проверяем поля путей (не должны быть пустыми)
        is_valid_dir = bool(dir_path.strip())
        is_valid_file = bool(file_path.strip())
        
        # Проверяем третье поле (не должно быть пустым)
        is_valid3 = bool(text3.strip())
        
        # Обновляем стиль полей в зависимости от валидности
        self.update_field_style(self.small_input1, is_valid1)
        self.update_field_style(self.small_input2, is_valid2)
        self.update_field_style(self.small_input3, is_valid3)
        self.update_field_style(self.dir_path_input, is_valid_dir)
        self.update_field_style(self.file_path_input, is_valid_file)
        self.update_field_style(self.big_input, is_valid3)
        
        # Обновляем сообщение об ошибке
        error_messages = []
        if not text1:
            error_messages.append("Серийный номер не может быть пустым")
            
        if not is_valid2 and text2:
            error_messages.append("Количество копий должно быть числом больше 0 (без ведущих нулей)")
        elif not text2:
            error_messages.append("Количество копий не может быть пустым")
        elif not text3:
            error_messages.append("Количество копий по позициям не может быть пустым")
        
        if not is_valid_dir:
            error_messages.append("Необходимо выбрать директорию")
        
        if not is_valid_file:
            error_messages.append("Необходимо выбрать файл")
            
        if not is_valid3:
            error_messages.append("Поле с текстом для поиска не может быть пустым")
        
        if error_messages:
            self.error_label.setText('\n'.join(error_messages))
        else:
            self.error_label.setText('')
        
        # Активируем кнопку только если все поля валидны
        self.accept_button.setEnabled(is_valid1 and is_valid2 and is_valid_dir and is_valid_file and is_valid3)
    
    # Проверяет, является ли строка валидным числом
    def is_valid_number(self, text):
        if not text:
            return False
        if not text.isdigit():
            return False
        if text[0] == '0':
            return False
        if int(text) <= 0:
            return False
        return True
    
    # Обновляет стиль поля в зависимости от валидности
    def update_field_style(self, field, is_valid):
        if is_valid:
            field.setStyleSheet("")
        else:
            field.setStyleSheet("border: 1px solid red;")
    
    #Метод для получения данных от пользователя
    def accept_action(self):
        # Получаем данные из полей ввода
        inp_ser_numb = self.small_input1.text()
        inp_copy_count = self.small_input2.text()
        inp_copy_pos_count = self.small_input3.text()
        dir_path = self.dir_path_input.text()
        file_path = self.file_path_input.text()
        big_text = self.big_input.toPlainText()
        
        # Дополнительная проверка перед обработкой
        if not (inp_ser_numb.strip() and 
                self.is_valid_number(inp_copy_count) and 
                dir_path.strip() and
                file_path.strip() and
                big_text.strip()):
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, исправьте ошибки в полях ввода')
            return
        
        # Обрабатываем большой текст (разделяем по запятой и удаляем лишние пробелы)
        big_text_list = [item.strip() for item in big_text.split(',') if item.strip()]
        
        # переносим все данные в словарь для дальнейшей работы
        self.input_data = {
            'inp_ser_numb': inp_ser_numb, 
            'inp_copy_count': inp_copy_count,
            'inp_copy_pos_count': inp_copy_pos_count,
            'directory_path': dir_path,
            'file_path': file_path,
            'norm_strings': big_text_list
        }
        
        # Выводим данные
        print("Ручной метод:\nДанные приняты: ", self.input_data,'\n')
        # Запускаем создание копиий
        manual_copy(self.input_data)
        
        # Можно показать сообщение об успешном принятии
        # QMessageBox.information(self, 'Успех', 'Данные успешно приняты!')
        
    def exit_action(self):
        # Закрываем приложение
        self.close()
        
    
    
    
    
    
    
    
    
    
