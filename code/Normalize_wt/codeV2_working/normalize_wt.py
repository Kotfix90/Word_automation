
import zipfile
from xml.etree import ElementTree as ET

from find_indexes import get_indexes
from join_wt import join
            
# ф-я открывающая файл и меняющая xml
def norm_wt(word_path, search_text):
    with zipfile.ZipFile(word_path, 'r') as docx_zip:
            # Получаем всё папки и файлы zip'a
            zip_content = docx_zip.namelist()
            if 'word/document.xml' in zip_content:
                with docx_zip.open('word/document.xml') as xml_file:
                    # Считываем в переменную весь код разметки
                    content = xml_file.read() 
                    
                    # Получаем словарь строк их кол-ва и индексов             
                    index_dict = get_indexes(search_text, content)
                           
                    print(index_dict,'\n')   
                    
                    # Обединяем элементы в один
                    content = join(content, index_dict) 
                    print()   


if __name__ == "__main__": 
    
    file_path = r'C:\Users\1\Desktop\DOC\Normalize_wt\file\КШ-L.TR.P.ФЛ.3.5.ХЛ1.МП.А 01001...01003.docx'             
    
    search_text = ['КШ-L-15-16-2026-193-01001…01018', 'Заводской (серийный) №', 'Заводской номер арматуры']
                    
    norm_wt(file_path, search_text)               