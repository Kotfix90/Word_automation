import os
import zipfile

from find_indexes import get_indexes
from join_wt import join
            

def norm_wt(word_path, search_text):
    # Сначала создаем временный файл
    temp_docx = word_path + '.tmp'
    
    # Открываем оригинальный файл
    with zipfile.ZipFile(word_path, 'r') as docx_zip:
        # Получаем всё папки и файлы zip'a
        zip_content = docx_zip.namelist()
        
        if 'word/document.xml' in zip_content:
            # Читаем XML файл
            with docx_zip.open('word/document.xml') as xml_file:
                # Считываем в переменную весь код разметки
                content = xml_file.read() 
                
                # Получаем словарь строк их кол-ва и индексов             
                index_dict = get_indexes(search_text, content)
                       
                print(index_dict,'\n')   
                
                # Объединяем элементы в один
                new_content = join(content, index_dict)
                
                # Создаем новый ZIP с изменениями
                with zipfile.ZipFile(temp_docx, 'w', zipfile.ZIP_DEFLATED) as new_docx_zip:
                    # Копируем все файлы из оригинального ZIP
                    for item in zip_content:
                        if item == 'word/document.xml':
                            # Записываем измененный XML как байты
                            new_docx_zip.writestr(item, new_content.encode('utf-8'))
                        else:
                            # Копируем остальные файлы без изменений
                            new_docx_zip.writestr(item, docx_zip.read(item))
    
    # Закрываем все файлы и заменяем оригинал
    # Важно: закрываем оригинальный файл перед заменой
    docx_zip.close()
    
    # Заменяем оригинальный файл временным
    os.remove(word_path)  # Удаляем оригинал
    os.rename(temp_docx, word_path)  # Переименовываем временный
    
    print(f"Файл {word_path} успешно обновлен")
    
if __name__ == "__main__": 
    
    # сделать получаемым через интерфейс
    file_path = r'C:\Users\1\Desktop\Passports Hydra(fix)\code\Normalize_wt\file\КШ-L-15-16-2026-193-01001…01018.docx'             
    # подавать сюда строки из таблицы с шильдами (для паспортов)
    search_text = ['КШ-L-15-16-2026-193-01001…01018', 'Заводской (серийный) №', 'Заводской номер арматуры']
                    
    norm_wt(file_path, search_text)  