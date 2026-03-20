from bs4 import BeautifulSoup
import zipfile
from xml.etree import ElementTree as ET
import os

from change_wt import change_wt, create_new_passport, nearest_image_del

# ф-я для создания нового паспорта позиции заводского номера
def proccessing(word_path, stack_serial_numb, serial_numbs, string_for_imgs, output_dir):
    try:
        with zipfile.ZipFile(word_path, 'r') as docx_zip:
            # Получаем всё папки и файлы zip'a
            zip_content = docx_zip.namelist()
            if 'word/document.xml' in zip_content:
                with docx_zip.open('word/document.xml') as xml_file:
                    # Считываем в переменную весь код разметки
                    content = xml_file.read()
                    
                    # готовим суп
                    soup = BeautifulSoup(content, 'xml')
                    
                    # заменем общий stack серийников на конкретный для каждого серийника с печатями
                    for serial_numb in serial_numbs:
                        new_soup = change_wt(soup, stack_serial_numb, serial_numb)
                        
                        # формируем путь для сохранения по количеству в позиции
                        new_file_name = f'{serial_numb}.docx'
                        
                        # путь куда сохраняются все папки
                        save_path = output_dir
                        
                        # Папка для новых паспортов с названием "для заказчика"
                        save_path = os.path.join(save_path, 'Для заказчика заверенные', new_file_name)
                        
                        create_new_passport(save_path, docx_zip, zip_content, new_soup)
                    
                        # удаляем печати в созданных ранее паспорте и создаем новый
                        # Находим ближаейшие к поисковм строкам
                        for string in string_for_imgs:
                            new_del_soup = nearest_image_del(new_soup, string)
                        
                        # Пишем путь для паспортов с удаленными изображениями
                        new_file_name = f'{serial_numb}.docx'
                        
                        # путь куда сохраняются все папки
                        save_path = output_dir
                        
                        # Папка для новых паспортов с названием "для заказчика"
                        save_path = os.path.join(save_path,'Для заказчика', new_file_name)
                        
                        create_new_passport(save_path, docx_zip, zip_content, new_del_soup)                     
                     
            else:
                raise FileNotFoundError ("Отсутвует файл word/document.xml")
            
    except FileNotFoundError:
        print(f"Проверь указанный путь: {word_path}" )
        

        