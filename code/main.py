from bs4 import BeautifulSoup
import zipfile
from xml.etree import ElementTree as ET
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QVBoxLayout, QWidget


from chose_menu import MainWindow


    
if __name__ == "__main__":
    
    # Вызываем главное окно выбора метода
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    
    
    