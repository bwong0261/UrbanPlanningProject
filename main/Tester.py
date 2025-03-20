import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in background
driver = webdriver.Chrome(options=options)
# Open the webpage
url = "https://en.wikipedia.org/wiki/List_of_cities_proper_by_population"
driver.get(url)

rows = driver.find_elements(By.XPATH, "//tbody/tr[@id]")

data = []
for row in rows:
    # City name from <tr id="Tokyo">, for example
    city_name = row.get_attribute("id")

    # Attempt to grab the first <td style="text-align:right"> in that row
    # This is typically the population cell
    population_cells = row.find_elements(By.XPATH, ".//td[@style='text-align:right']")

    if population_cells:
        population = population_cells[0].text
    else:
        population = None

    data.append([city_name, population])

print(data)