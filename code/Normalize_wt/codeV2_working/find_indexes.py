from bs4 import BeautifulSoup

# Ищет в каждом w:t наличие первого символа из поисковой строки
def find_in_wt(idx, wt, string):
         
    # Ищем в конкретном w:t первый символ
    for word in wt.text: 
        if word == string[0]:
            return idx
        else:
            continue  
    
    return None
    
    
# ф-я для продолжения проверки потенциально подходящей строки в w:t
def next_checking(start_idx, all_wt, search_text):
    # Временная строка для проверки
    temp_string = ''
    idx_list = []
    
    # Проверка c текущего w:t
    for word in all_wt[start_idx].text:
        try:
            if word == search_text[len(temp_string)]:
                temp_string += word
            else:
                continue
        except IndexError:
            pass
    
    # Проверяем временную строку
    if temp_string != '':
        idx_list.append(start_idx)
        
        if temp_string == search_text:
            return idx_list
        
        else:
            
            for idx, _ in enumerate(all_wt, start=start_idx+1):
                # исключение для list out of index, когда заканчиваются w:t
                try:
                    for word in all_wt[idx].text:
                        if temp_string == search_text:
                            idx_list.append(idx)
                            return idx_list
                        if word == search_text[len(temp_string)]:
                            temp_string += word
                        else:
                            return None
                except IndexError:
                    break
                
                # Добавляем idx в список если функция не вернула None  
                idx_list.append(idx)
                if temp_string == search_text:
                    return idx_list
                else:
                    continue
      
    else:
        return None
       
def get_indexes(search_text, content):
#Словарь для сбора списков индексов для поисковой строки {'название поисковой строки': {'№ штуки': [лист idx_w:t]}}
    search_dict = {}
    search_dict= dict.fromkeys(search_text)
    
    soup = BeautifulSoup(content, 'xml')  
    all_wt = soup.find_all('w:t')    
    
    #print(all_wt)
    # Находим все w:t, в которых есть подходящие символы
    for string in search_text:  
        # Счётчк для количества вхождений
        conc_counter = 0
        # подсловарь, который записывает вхождения по порядковому номеру
        count_dict = {}
        
        for idx, wt in enumerate(all_wt):
            #print(wt.text)
            
            # Проверяем есть ли вообще в текущем wt первый жлемент из поисковой строки
            start_idx = find_in_wt(idx, wt, string)
            if start_idx != None :
                idx_list = next_checking(start_idx, all_wt, string)
                if idx_list != None:
                    conc_counter += 1
                    count_dict[conc_counter] = idx_list
                 
            else:
                continue
        
        search_dict[string]=count_dict 
    
    return search_dict