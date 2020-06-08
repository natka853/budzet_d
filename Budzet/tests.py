from selenium import webdriver
import unittest


class tests(unittest.TestCase):
    def test_open_main_page(self):
        driver = webdriver.Chrome(executable_path=r'C:\Testy\chromedriver.exe')
        driver.get('localhost:8000/')  # otwiera stronę podstawową w przeglądarce
        # driver.get('https://demobank.jaktestowac.pl/logowanie_prod.html')
        title = driver.title  # to co wyświetla się na karcie przeglądarki
        print(title)
        assert 'Budżet domowy' == title  # sprawdza czy tytuł strony to 'Budżet domowy'
        driver.quit()  # zamyka przeglądarkę

    def test_bad_login(self):
        driver = webdriver.Chrome(executable_path=r'C:\Testy\chromedriver.exe')
        driver.get('localhost:8000/login')  # otwiera stronę logowania w przeglądarce
        driver.find_element_by_name("Zaloguj").click()  # klika przycisk zaloguj w przeglądarce ale nie sprawdza czy nie zalogowało
        driver.quit()
