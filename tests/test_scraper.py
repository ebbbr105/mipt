import sys
sys.path.append('..')

from scrapper import get_book_data, scrape_books 

def test_get_book_data_returns_dict():
        """Тест: get_book_data возвращает словарь"""
        # Подготовка тестовых данных
        test_url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
        
        # Вызов функции
        result = get_book_data(test_url)
        
        # Проверки
        assert isinstance(result, dict)
        assert result is not None
    
def test_get_book_data_has_required_keys():
    """Тест: словарь содержит все нужные ключи"""
    test_url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    result = get_book_data(test_url)
    
    required_keys = ['site name', 'title', 'content-type', 'created', 'description', 
                     'viewport', 'robots', 'UPC', 'Product Type', 'Price (excl. tax)', 
                     'Price (incl. tax)', 'Tax', 'Availability', 'Number of reviews']  # дополни своими ключами
    for key in required_keys:
        assert key in result, f"Ключ {key} отсутствует в результате"

def test_scrape_books_returns_list():
    """Тест: scrape_books возвращает список книг"""
    # Тестируем на маленьком количестве страниц для скорости
    result = scrape_books(paige_count=1)
    
    assert isinstance(result, list)
    assert len(result) > 0  # должен вернуть хотя бы одну книгу

def test_book_title_not_empty():
    """Тест: название книги не пустое"""
    test_url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    result = get_book_data(test_url)
    
    assert 'title' in result
    assert result['title'] != ""
    assert result['title'] is not None