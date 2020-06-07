from selenium import webdriver

driver = webdriver.Chrome(executable_path=r'C:\Testy\chromedriver.exe')
driver.get('localhost:8000/')  # otwiera stronę podstawową w przeglądarce
# driver.get('https://demobank.jaktestowac.pl/logowanie_prod.html')
title = driver.title  # to co wyświetla się na karcie przeglądarki
print(title)
assert 'Budżet domowy' == title  # sprawdza czy tytuł strony to 'Budżet domowy'
driver.quit()  # zamyka przeglądarkę
