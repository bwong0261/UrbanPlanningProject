from selenium import webdriver
from selenium.webdriver.common.by import By

# Initialize WebDriver

def setup_driver():

    driver = webdriver.Chrome()
    # Open the webpage
    url = "https://en.wikipedia.org/wiki/List_of_cities_proper_by_population"
    driver.get(url)

    return driver


# Find all <tr> elements inside the table

def get_cities(driver):
    # Extract city names from the 'id' attributes
    rows = driver.find_elements(By.XPATH, "//tbody/tr")

    city_names = []

    for row in rows:
        if row.get_attribute("id"):
            city_names.append(row.get_attribute("id"))

    return city_names

def main():
    driver = setup_driver()
    cities = get_cities(driver)
    print(cities)

if __name__ == "__main__":
    main()
