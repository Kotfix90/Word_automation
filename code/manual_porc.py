import sys

# Подключаем нормализацию w:t
# Путь к папке с модулем
sys.path.insert(0, r'C:\Users\1\Desktop\DOC\Passports Hydra\code\Normalize_wt\codeV2_working')
from main_norm_wt import norm_wt

from create_pass import proccessing

# метод создания новых серийников по позициям
def pos_count_new_sn(serial_numb, pos_count):
    # список для новых серийников
    pos_serial_numbs = []

    # если шаблон был выбран с диапазоном
    if '...' in serial_numb:
        serial_numb = serial_numb.split('...')
    serial_numb = [el for el in serial_numb if el != '...'][0] 
    
    serial_numb = serial_numb.split('-')
    right_part = serial_numb[-1]
    serial_numb = serial_numb[:-1]
    
    for numb in range(1, int(pos_count)+1):
        
        # если число текщуей позиции менее 10 тогда строка будет 0+(число)
        if numb < 10: 
            numb = '0' + str(numb)
        elif numb >= 10 :
            numb = str(numb)
            
        # делаем замену в правой части
        right_part = numb + right_part[(len(numb)):len(right_part)+1]
        
        #собираем все в одну строку
        new_serial_numb = '-'.join(serial_numb)
        new_serial_numb += '-'+right_part 

        pos_serial_numbs.append(new_serial_numb)
        
    return pos_serial_numbs
    
# метод для создания списка серийных номеров по количеству шт
def count_new_sn(pos_serial_numbs, count):
    # список для новых серийников
    all_serial_numbs = []
    
    for serial_numb in pos_serial_numbs:
        # если шаблон был выбран с диапазоном
        if '...' in serial_numb:
            serial_numb = serial_numb.split('...')
            serial_numb = [el for el in serial_numb if el != '...']
        
        serial_numb = serial_numb.split('-')
        right_part = serial_numb[-1]
        serial_numb = serial_numb[:-1]
        
        for numb in range(1, int(count)+1):
            
            # делаем замену в правой части
            right_part = right_part[:-1*(len(str(numb)))] + str(numb)
            
            #собираем все в одну строку
            new_serial_numb = '-'.join(serial_numb)
            new_serial_numb += '-'+right_part 

            all_serial_numbs.append(new_serial_numb)
        
    print(all_serial_numbs)
    return all_serial_numbs

# Ф-я для запуска копирования по заданным настройкам   
def manual_copy(input_data):
    
    # Получаем путь к файлу на основе которого будет делать копии
    file_path = input_data['file_path']
    
    # путь для сохранения всех готовых документов (выбиремый путь)
    output_dir = input_data['directory_path']
    
    # Получаем серийник в паспорте
    serial_numb = input_data['inp_ser_numb'].strip()
    
    # Получаем список новых серийников по количеству в одной позиции
    pos_serial_numbs = pos_count_new_sn(serial_numb, input_data['inp_copy_pos_count'])
     
    # Получаем все серийники дляновых паспортов
    all_serial_numbs = count_new_sn(pos_serial_numbs, input_data['inp_copy_count'])
     
    # массив строк для нормализации
    norm_strings = input_data['norm_strings']
    # убираем лишние данные в массив и строках  
    norm_strings = [el for el in norm_strings if el != '' and el != ' ']
    norm_strings = [el.strip() for el in norm_strings]
    
    norm_strings.append(serial_numb)
    
    # Нормальизуем w:t, чтобы в его было легко искать и работать
    norm_wt(file_path, norm_strings)
    
        # работа с файлом
    str_for_imgs = norm_strings [1:] 
    proccessing(file_path, serial_numb, all_serial_numbs, str_for_imgs, output_dir)