# Библиотеки, которые могут вам понадобиться
# При необходимости расширяйте список
import time
from datetime import datetime, timedelta  
import requests
import schedule
from bs4 import BeautifulSoup

from tqdm.notebook import tqdm  
import json

def get_book_data(book_url: str) -> dict:
    """
    Функция парсит страницу с данными по книге.

    Args:
       book_url (str): Ссылка на страницу.
       
    Returns:
       res (dict): Словарь с полученной информацией.
    """
    # НАЧАЛО ВАШЕГО РЕШЕНИЯ
    resp = requests.get(book_url, timeout=10)
    soup = BeautifulSoup(resp.text, 'html.parser')

    d_1 = {
        "site name": soup.find('title').text.strip().split(' | ')[1],
        
        "title": soup.find('title').text.strip().split(' | ')[0]
    }

    d_2 = {}
    # парсинг метаданных
    for tag in soup.find_all("meta"):
        keys = tag.attrs.keys()
        for k in keys:
            if k != 'content':
                d_2[tag[k]] = tag['content'].strip()
            else:
                continue

    d_3 = {}
    # парсинг таблицы
    for t in soup.find_all("tr"):
        d_3[t.find('th').get_text()] = t.find('td').get_text()

     
    res = {**d_1, **d_2, **d_3}

     
    return res
    # КОНЕЦ ВАШЕГО РЕШЕНИЯ

def scrape_books(is_save : bool = True, paige_count : int = None) -> list:
    """
    Функция парсит все страницы с книгами.

    Args:
       is_save (bool): флаг на сохранение в books_data.txt.
       paige_count (int)
       
    Returns:
       res (list): Список словарей по каждой книге со всех страниц.
    """

    # НАЧАЛО ВАШЕГО РЕШЕНИЯ
    print(f"ВЫПОЛНЯЮ ПАРСИНГ! {datetime.now().strftime('%H:%M:%S')}")
    
    if paige_count:
        print ("paige count: ", paige_count)
    else:
        main = "https://books.toscrape.com/index.html"
        r = requests.get(main, timeout=10)
        s = BeautifulSoup(r.text, 'html.parser')
        paige_count = int(s.find_all("li", {"class":"current"})[0].text.strip().split(' ')[-1])
        print ("paige count: ", paige_count)

    lst = []
    for paige in tqdm(range(1, paige_count + 1)):
        paige = f"http://books.toscrape.com/catalogue/page-{paige}.html"
        response = requests.get(paige, timeout=10)
        sp = BeautifulSoup(response.text, 'html.parser')
        
        for h in sp.find_all("h3"):
            book = h.find('a')['href']
            book_url = f"https://books.toscrape.com/catalogue/{book}"
            lst.append(get_book_data(book_url))

    if is_save:
        with open('../artifacts/books.txt', 'w', encoding='utf-8') as f:
            for book in lst:
                f.write(json.dumps(book, ensure_ascii=False) + '\n')

    return lst
    # КОНЕЦ ВАШЕГО РЕШЕНИЯ