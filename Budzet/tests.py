from time import sleep
from selenium import webdriver
import unittest


class tests(unittest.TestCase):
    def test_A_open_main_page(self):
        driver = webdriver.Chrome(executable_path=r'C:\Testy\chromedriver.exe')
        driver.get('localhost:8000/')  # otwiera stronę podstawową w przeglądarce
        title = driver.title  # to co wyświetla się na karcie przeglądarki
        assert 'Budżet domowy' == title  # sprawdza czy tytuł strony to 'Budżet domowy'
        driver.quit()  # zamyka przeglądarkę

    def test_B_bad_login(self):
        driver = webdriver.Chrome(executable_path=r'C:\Testy\chromedriver.exe')
        driver.get('localhost:8000/login')  # otwiera stronę logowania w przeglądarce
        driver.find_element_by_name("Zaloguj").click()
        sleep(1)
        assert driver.current_url == 'http://localhost:8000/login/'
        driver.quit()

    def test_C_register(self):
        driver = webdriver.Chrome(executable_path=r'C:\Testy\chromedriver.exe')
        driver.get('localhost:8000/register')  # otwiera stronę logowania w przeglądarce
        driver.find_element_by_name('username').send_keys('TestowyUzytkownik')
        driver.find_element_by_name('email').send_keys('aaaaaaa@aa.xyz')
        driver.find_element_by_name('password1').send_keys('SerotoninaA')
        driver.find_element_by_name('password2').send_keys('SerotoninaA')
        driver.find_element_by_name('Zarejestruj się').click()
        sleep(1)
        assert driver.find_element_by_name('rejestracja').is_displayed()
        driver.quit()

    def test_D_good_login(self):
        driver = webdriver.Chrome(executable_path=r'C:\Testy\chromedriver.exe')
        driver.get('localhost:8000/login')  # otwiera stronę logowania w przeglądarce
        driver.find_element_by_name('username').send_keys('TestowyUzytkownik')
        driver.find_element_by_name('password').send_keys('SerotoninaA')
        driver.find_element_by_name("Zaloguj").click()
        sleep(1)
        assert driver.current_url == 'http://localhost:8000/accounts/profile/'
        driver.quit()
