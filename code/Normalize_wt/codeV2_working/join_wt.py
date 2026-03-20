from bs4 import BeautifulSoup

def join(content, idx_dict):
    soup = BeautifulSoup(content, 'xml')  
    all_wt = soup.find_all('w:t') 
    
    for string in idx_dict:
        #print(string)
        for k,v in idx_dict[string].items():
            #print("№ шт. ",k)
            
            max_length = 0
            for wt_idx in v:

                curr_length = len(all_wt[wt_idx].text)
                if curr_length > max_length:
                    max_length = curr_length
                    max_idx = wt_idx  
                else:
                    continue
            
            # удаляем эклемент из списка в словаре 
            del v[v.index(max_idx)]
            
            # перезаписываем элемент с наибольшей длиной
            all_wt[max_idx].string = string
            
            # удаляем остальные w:t
            for wt_idx in v:
                all_wt[wt_idx].decompose()
                #print(f"удаление w:t по индексу, {wt_idx}\n")
    
    #return all_wt
    
    # Возвращаем как байты с правильной кодировкой
    #return soup.prettify(formatter=None).encode('utf-8')

    # Возвращаем как строку с XML декларацией
    return str(soup)
                
             