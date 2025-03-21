import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in background
driver = webdriver.Chrome(options=options)
# Open the webpage
url = "https://en.wikipedia.org/wiki/List_of_cities_by_GDP"
driver.get(url)

table_ = driver.find_element(By.XPATH, "//table[contains(@class, 'static-row-numbers sortable wikitable jquery-tablesorter')]")
rows = table_.find_elements(By.TAG_NAME, "tr")

def remove_parentheses(text):
    for i in range(len(text)):
        if text[i] == "(":
            text = text[:i - 1].strip()
            break
    return text

# data = []
# for row in rows[1:]:
#     cells = row.find_elements(By.TAG_NAME, "td")
#     # Make sure the row has enough cells to extract
#     if len(cells) >= 3:
#         # 1st cell:  City name
#         city_name = cells[0].text.strip()
#         # 3rd cell: GDP
#         gdp = cells[2].text.strip()
#         gdp = remove_parentheses(gdp)
#         data.append([city_name, gdp])



print(data)