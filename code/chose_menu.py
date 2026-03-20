import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QVBoxLayout, QWidget

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QWidget, 
                             QVBoxLayout, QCheckBox, QLabel, QHBoxLayout, QButtonGroup, QMessageBox)
from PyQt5.QtCore import Qt

from manual_window import ManualMenu
from auto_window import AutoMenu

# меню для выбора метода создания паспортов
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Атрибуты класса для хранения состояний чекбоксов
        self.checkbox1_state = False
        self.checkbox2_state = False
        
        # Значение выбранного метода
        self.selected_method = None
        
        # Настройка главного окна
        self.setWindowTitle("Пример с чекбоксами")
        self.setGeometry(100, 100, 400, 300)
        
        # Создание меню
        self.create_menu()
        
        # Создание центрального виджета
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Создание layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Создание чекбоксов
        self.checkbox1 = QCheckBox("Авто-копия")
        self.checkbox2 = QCheckBox("Ручная настройка")
        
        # СОЗДАНИЕ ГРУППЫ ДЛЯ ЧЕКБОКСОВ
        self.checkbox_group = QButtonGroup(self)
        self.checkbox_group.addButton(self.checkbox1)
        self.checkbox_group.addButton(self.checkbox2)
        self.checkbox_group.setExclusive(True) 
        
        # Подключение сигналов к слотам
        self.checkbox1.stateChanged.connect(self.on_checkbox1_changed)
        self.checkbox2.stateChanged.connect(self.on_checkbox2_changed)
        
        # Метка для отображения текущих состояний
        self.status_label = QLabel("Состояния чекбоксов: ")
        self.update_status_label()
        
        # Кнопка далее
        self.continue_button = QPushButton('Далее')
        self.continue_button.clicked.connect(self.click_continue)
        
        # Добавление виджетов в layout
        layout.addWidget(self.checkbox1)
        layout.addWidget(self.checkbox2)
        layout.addWidget(self.status_label)
        layout.addWidget(self.continue_button)
        layout.addStretch()
    
    def create_menu(self):
        # Создание строки меню
        menubar = self.menuBar()
        
        # Создание меню "Файл"
        file_menu = menubar.addMenu("Файл")
        
        # Создание действия для выхода
        exit_action = QAction("Выход", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        
        # Добавление действия в меню
        file_menu.addAction(exit_action)
        
        # Создание меню "Настройки"
        settings_menu = menubar.addMenu("Настройки")
        
        # Создание действия для сброса чекбоксов
        reset_action = QAction("Сбросить чекбоксы", self)
        reset_action.triggered.connect(self.reset_checkboxes)
        
        # Добавление действия в меню
        settings_menu.addAction(reset_action)
    
    def on_checkbox1_changed(self, state):
        # Сохранение значения в атрибут класса
        self.checkbox1_state = (state == Qt.Checked)
        self.update_status_label()
        #print(f"Чекбокс 1 изменен: {self.checkbox1_state}")
    
    def on_checkbox2_changed(self, state):
        # Сохранение значения в атрибут класса
        self.checkbox2_state = (state == Qt.Checked)
        self.update_status_label()
        #print(f"Чекбокс 2 изменен: {self.checkbox2_state}")
    
    def update_status_label(self):
        self.status_label.setText(
            f"Описание работы режимов: \n"
            f"{'Копии паспортов будут сделаны строго по таблице с шильдами.\nНеобходимо сверить что кол-во шаблонов паспортов совпадает с кол-ом позиций в спецификации' if self.checkbox1_state else ''}"
            f"{'В данном режиме необходимо задать собственные настроки' if self.checkbox2_state else ''}"
        )
    
    def reset_checkboxes(self):
        self.checkbox1.setChecked(False)
        self.checkbox2.setChecked(False)
        print("Чекбоксы сброшены")
        
    def click_continue(self):
        if self.checkbox1.isChecked():
            self.selected_method = "auto_method"
        elif self.checkbox2.isChecked():
            self.selected_method = "manual_method"
        else:
            self.selected_method = None
            QMessageBox.warning(self, "Внимание", "Выберите метод создания паспортов!")
            return
        self.open_selected_method()
    
    # Определение нужного метода
    def open_selected_method(self):
        if self.selected_method == "manual_method":
            self.open_manual_menu()
        elif self.selected_method == "auto_method":
            self.open_auto_menu()
    
    # Запуск ручного метода 
    def open_manual_menu(self):
        try:
            # Вызываем функцию, которая покажет модальное окно
            self.window = ManualMenu(self)  
            # Деалем коно модальным (пока оно не будет закрыто с другими окнами нельзя ничего делать)
            self.window.setWindowModality(Qt.ApplicationModal)
            self.window.show()
            #print("Ручной метод завершён успешно")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка при выполнении ручного метода:\n{str(e)}")
            
    # Запуск автоматического метода 
    def open_auto_menu(self):
        try:
            # Вызываем функцию, которая покажет модальное окно
            self.window = AutoMenu(self)
            self.window.setWindowModality(Qt.ApplicationModal)
            self.window.show()
            #print("Авто-метод завершён успешно")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка при выполнении авто-метода:\n{str(e)}")
        
        