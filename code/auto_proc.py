import pandas as pd
import numpy as np
import sys
import os

# Подключаем нормализацию w:t
# Путь к папке с модулем
sys.path.insert(0, r'C:\Users\1\Desktop\DOC\Passports Hydra\code\Normalize_wt\codeV2_working')
from main_norm_wt import norm_wt

from create_pass import proccessing

# Ф-я для считывания серийников из таблицы с шильдами
def get_serial_numbs(xls_file):
    df = pd.read_excel(xls_file, sheet_name=1, header=None, dtype=str)
    #headers = list(df.iloc[1, :])
    
    # получаем содержимое всех ячеек
    all_val = df.values
    
    # подстроки для поиска серийника
    substrings = 'Serial number'
    
    # ищем ячейку по подстроке 
    mask = df.applymap(lambda x: substrings.lower() in str(x).lower())
    rows, cols = np.where(mask)

    row = rows[0].item()
    start_col = cols[0].item() 
    
    # ищем конечный столбец 
    for idx, col,  in enumerate(df.columns, start=start_col+1):
        if not(pd.isna(df.iloc[row, idx])):
            end_col = idx
            break
    
    # список со всеми серийниками
    serial_numb_list = []
    # Кол-во всех строк в df
    num_rows = df.shape[0] - (row+1) 
    
    for row in range(num_rows):
        serial_numb_list.append(''.join(df.iloc[row+2, start_col:end_col].astype(str).tolist()))
        
    # Убираем калечные '–' 
    for idx in range(len(serial_numb_list)):
        if '–' in serial_numb_list[idx]:
            serial_numb_list[idx] = serial_numb_list[idx].replace('–', '-')
        else:continue
    
    #print(serial_numb_list)
    return serial_numb_list

# метод для получения словаря с отдельынми стэками по позициям
def get_stacks_serial_numb(serial_numbs):
    
    # Делаем словарь для для стэков
    stack_dict = {}
    
    start_idx = 0
    for idx, sn in enumerate(serial_numbs, start=0):
        try:
            right_part = sn.split('-')[-1]
            next_right_part = serial_numbs[idx+1].split('-')[-1]
            if right_part[:2] == next_right_part[:2]:
                continue
            else:
                # ключ номер позиции значение список номеров по срезу
                stack_dict[right_part[:2]] = serial_numbs[start_idx:idx+1]
                start_idx = idx+1
        except IndexError:
            # ключ номер позиции значение список номеров по срезу
            stack_dict[right_part[:2]] = serial_numbs[start_idx:idx+1]
            break
    
    return stack_dict
    
def auto_copy(input_data):
    # путь для папки с шаблонами
    tample_path = input_data['directory1_path']
    #tample_path = r'C:\Users\1\Desktop\DOC\Passports Hydra\file\Шаблоны'
    
    # лист файлов с шаблонами
    temple_file_list = os.listdir(tample_path)
    
    # Получаем серийники в список по всей спецификации (выбиремый путь)
    template_path = input_data['file_path']
    serial_numbs = get_serial_numbs(template_path)
    
    # путь для сохранения всех готовых документов (выбиремый путь)
    output_dir = input_data['directory2_path']
    #output_dir = r"C:\Users\1\Desktop\DOC\Passports Hydra\file\Готовые"

    # Получаем общий шаблон
    stack_serial_numb = get_stacks_serial_numb(serial_numbs)
    
    # проверка количества шаблонов для паспортов и стеков (должны быть одинаковы)
    if len(stack_serial_numb.keys()) == len(temple_file_list):
        
        # закидываем по одному шаблону и стеку позиций  
        for idx, stack in enumerate(stack_serial_numb.values(), start=0):
            
            # Делаем диапазон как в шаблоне
            right_part = stack[-1].split('-')[-1]
            serial_numb_range = f'{stack[0]}...{right_part}'
            
            # массив строк для нормализации w:t
            norm_strings = [serial_numb_range,
                        'Painting and delivery manager'
                            'Quality manager',
                            ' МП ']
            
            # Собираем путь до конкртеного шаблона
            file_path = os.path.join(tample_path, temple_file_list[idx])
            
            # Нормальизуем w:t, чтобы в его было легко искать и работать
            norm_wt(file_path, norm_strings)

            # работа с файлом
            str_for_imgs = norm_strings [1:] 
            proccessing(file_path, serial_numb_range, stack, str_for_imgs, output_dir)
        
    else: print('Количество шаблонов и стэков позиций не совпадает \nПроверьте таблицу с шильдами и шаблоны паспортов\n')