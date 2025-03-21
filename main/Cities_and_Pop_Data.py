import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

# Initialize WebDriver

def setup_driver(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in background
    driver = webdriver.Chrome(options = options)
    # Open the webpage
    driver.get(url)

    return driver


# Find all <tr> elements inside the table

def get_cities_and_pop(driver):
    # Find rows that have an 'id' attribute
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

    return data

def get_cities_and_gdp(driver):
    table = driver.find_elements(By.XPATH, "//table[contains(@class, 'static-row-numbers sortable wikitable jquery-tablesorter')]")
    rows = table.find(By.TAG_NAME, "tr")

def turn_to_csv(column, name, name_2):
    df = pd.DataFrame(column, columns =[name, name_2])
    df.to_csv("cities.csv", index=False ,encoding='utf-8')
    return df

def main():
    driver = setup_driver("https://en.wikipedia.org/wiki/List_of_largest_cities")
    cities = get_cities_and_pop(driver)
    df = turn_to_csv(cities, "City Name", "Population")
    print(df.head())

    driver.quit()

if __name__ == "__main__":
    main()
