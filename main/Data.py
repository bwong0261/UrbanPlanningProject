import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

# Initialize WebDriver

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in background
    driver = webdriver.Chrome(options = options)
    # Open the webpage
    url = "https://en.wikipedia.org/wiki/List_of_cities_proper_by_population"
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

def turn_to_csv(column, name, name_2):
    df = pd.DataFrame(column, columns =[name, name_2])
    df.to_csv("Cities_and_Pop.csv", index=False ,encoding='utf-8')
    print(df)

def main():
    driver = setup_driver()
    cities = get_cities_and_pop(driver)
    turn_to_csv(cities, "City Name", "Population")
    driver.quit()

if __name__ == "__main__":
    main()
