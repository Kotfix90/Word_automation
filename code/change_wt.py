import zipfile
import os
from copy import deepcopy

# Ф-я для нахождения бложайшего к конкретноиу w:t изображения и удаления  
def nearest_image_del(soup, string_for_imgs):               
    
    deepcopy_soup = deepcopy(soup)
    
    # Находим все текстовые элементы с искомыми строками
    text_elements = []
    all_texts = deepcopy_soup.find_all('w:t')
    
    for text in all_texts:
        if text.string:
            for search_string in string_for_imgs:
                if search_string in text.string:
                    text_elements.append(text)
                    break
    
    print(f"Найдено текстовых элементов с искомыми строками: {len(text_elements)}")
    
    # Находим все рисунки
    drawings = deepcopy_soup.find_all('w:drawing')
    print(f"Всего рисунков в документе: {len(drawings)}")
    
    # Создаем множество для отслеживания уже обработанных параграфов с текстом
    processed_paragraphs = set()
    removed_count = 0
    remaining_drawings = drawings.copy()
    
    # Для каждого текстового элемента ищем рисунок для удаления
    for text_element in text_elements:
        if not remaining_drawings:
            break
            
        text_paragraph = text_element.find_parent('w:p')
        if not text_paragraph or text_paragraph in processed_paragraphs:
            continue
            
        # Ищем рисунок в этом же параграфе
        drawing_in_same_paragraph = text_paragraph.find('w:drawing')
        if drawing_in_same_paragraph and drawing_in_same_paragraph in remaining_drawings:
            drawing_in_same_paragraph.decompose()
            remaining_drawings.remove(drawing_in_same_paragraph)
            removed_count += 1
            processed_paragraphs.add(text_paragraph)
            #print(f"Удален рисунок из того же параграфа для текста '{text_element.string[:30]}...'")
            continue
        
        # Если рисунка нет в том же параграфе, ищем в соседних
        all_paragraphs = deepcopy_soup.find_all('w:p')
        try:
            text_paragraph_idx = all_paragraphs.index(text_paragraph)
        except ValueError:
            continue
        
        # Проверяем соседние параграфы (предыдущий и следующий)
        for offset in [-1, 1]:
            neighbor_idx = text_paragraph_idx + offset
            if 0 <= neighbor_idx < len(all_paragraphs):
                neighbor_paragraph = all_paragraphs[neighbor_idx]
                drawing_in_neighbor = neighbor_paragraph.find('w:drawing')
                
                if drawing_in_neighbor and drawing_in_neighbor in remaining_drawings:
                    drawing_in_neighbor.decompose()
                    remaining_drawings.remove(drawing_in_neighbor)
                    removed_count += 1
                    processed_paragraphs.add(text_paragraph)
                    #print(f"Удален рисунок из {'предыдущего' if offset == -1 else 'следующего'} параграфа для текста '{text_element.string[:30]}...'")
                    break
    
    print(f"Удалено рисунков: {removed_count}")
    print(f"Осталось рисунков: {len(deepcopy_soup.find_all('w:drawing'))}\n")
    
    return deepcopy_soup
        

def change_wt(soup, stack, string_change):
    # делаем копию так как это ссылочный объект
    soup_copy = deepcopy(soup)
    
    all_wt = soup_copy.find_all('w:t')
    
    for wt in all_wt:
        if wt.text == stack:
            # Отладка
            #print(wt.text +' -> '+string_change+'\n')
            wt.clear()  # Очищаем содержимое
            wt.append(string_change)
            
    return soup_copy


# Ф-я создания паспорта
def create_new_passport(new_word_path, org_docx_zip, zip_content, soup):  

# Создаём папку, если её нет
    os.makedirs(os.path.dirname(new_word_path), exist_ok=True)
    
 # Создаём новый .docx файл с полной структурой
    with zipfile.ZipFile(new_word_path, 'w', zipfile.ZIP_DEFLATED) as new_docx:
        # Копируем все файлы из оригинального ZIP в новый
        for file_name in zip_content:
            if file_name == 'word/document.xml':
                # Для document.xml используем модифицированный soup
                # Преобразуем soup в строку и кодируем в UTF-8
                xml_content = str(soup)
                
                # Убеждаемся, что XML декларация присутствует
                if not xml_content.startswith('<?xml'):
                    xml_content = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + xml_content
                
                # Записываем модифицированный XML
                new_docx.writestr(file_name, xml_content.encode('utf-8'))
            else:
                # Для остальных файлов копируем без изменений
                file_content = org_docx_zip.read(file_name)
                new_docx.writestr(file_name, file_content)
