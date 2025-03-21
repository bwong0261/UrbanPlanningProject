# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
import requests
import certifi
import pandas as pd
from io import StringIO

# Initialize WebDriver

# def setup_driver(url):
#     options = webdriver.ChromeOptions()
#     options.add_argument("--headless")  # Run in background
#     driver = webdriver.Chrome(options = options)
#     # Open the webpage
#     driver.get(url)
#
#     return driver
#
#
# def remove_parentheses(text):
#     for i in range(len(text)):
#         if text[i] == "(":
#             text = text[:i - 1].strip()
#             break
#     return text
#
# def get_cities_and_pop(driver):
#     # Find rows that have an 'id' attribute
#     rows = driver.find_elements(By.XPATH, "//tbody/tr[@id]")
#     data = []
#     for row in rows:
#         # City name from <tr id="Tokyo">, for example
#         city_name = row.get_attribute("id")
#
#         # Attempt to grab the first <td style="text-align:right"> in that row
#         # This is typically the population cell
#         population_cells = row.find_elements(By.XPATH, ".//td[@style='text-align:right']")
#
#         if population_cells:
#             population = population_cells[0].text
#         else:
#             population = None
#
#         data.append([city_name, population])
#
#     return data
#
# def get_cities_and_gdp(driver):
#     table_ = driver.find_element(By.XPATH, "//table[contains(@class, 'static-row-numbers sortable wikitable jquery-tablesorter')]")
#     rows = table_.find_elements(By.TAG_NAME, "tr")
#     data = []
#     for row in rows[1:]:
#         cells = row.find_elements(By.TAG_NAME, "td")
#         # Make sure the row has enough cells to extract
#         if len(cells) >= 3:
#             # 1st cell:  City name
#             city_name = cells[0].text.strip()
#             # 3rd cell: GDP
#             gdp = cells[2].text.strip()
#             gdp = remove_parentheses(gdp)
#             data.append([city_name, gdp])
#     return data
#
#
# def turn_to_csv(column, name, name_2, file_name):
#     df = pd.DataFrame(column, columns =[name, name_2])
#     df.to_csv(file_name, index=False ,encoding='utf-8')
#     return df

# def main():
#     driver_cap = setup_driver("https://en.wikipedia.org/wiki/List_of_largest_cities")
#     cities_and_pop = get_cities_and_pop(driver_cap)
#     df = turn_to_csv(cities_and_pop, "City Name", "Population", "Cities_and_Population.csv")
#     driver_cap.quit()
#
#     driver_cag = setup_driver("https://en.wikipedia.org/wiki/List_of_cities_by_GDP")
#     cities_and_gdp = get_cities_and_gdp(driver_cag)
#     df = turn_to_csv(cities_and_gdp, "City Name", "GDP", "Cities_and_GDP.csv")
#     driver_cag.quit()
#
# if __name__ == "__main__":
#     main()


# Now parse the HTML with pandas

def remove_parentheses(text):
    for i in range(len(text)):
        if text[i] == "(":
            text = text[:i - 1].strip()
            break
    return text

def remove_comma(text):
    for i in range(len(text)):
        if text[i] == ",":
            text = text[:i].strip()
            break
    return text

def remove_metropolitan(text):
    for i in range(len(text) - 4):
        if (text[i].lower() == "m" and
            text[i + 1] == "e" and
            text[i + 2] == "t" and
            text[i + 3] == "r" and
            text[i + 4] == 'o'):
                text = text[:i].strip()
                break
    return text

def get_table(url, i):
    # Fetch the page content using requests with certificate verification
    response = requests.get(url, verify=certifi.where())
    html_content = response.text
    tables = pd.read_html(StringIO(html_content))
    df = tables[i]
    return df

def get_cities_and_gdp(url):
    # Fetch the page content using requests with certificate verification
    response = requests.get(url, verify=certifi.where())
    html_content = response.text
    tables = pd.read_html(html_content)
    # Make sure that tables[1] is the table you want
    df = tables[1]
    return df

def turn_to_csv(df, file_name):
    df.to_csv(file_name, index=False, encoding='utf-8')

def main():
    df_pop = get_table("https://en.wikipedia.org/wiki/List_of_largest_cities", 1)
    turn_to_csv(df_pop, "cities_and_population.csv")
    selected_df_pop = df_pop[[('City[a]', 'City[a]'),
                   ('City proper[c]', 'Population'),
                   ('City proper[c]', 'Density (/km2)')]]
    renamed_df_pop = selected_df_pop.rename(columns = {'City[a]' : 'City'})
    renamed_df_pop.columns = [' '.join(col).strip() if isinstance(col, tuple) else col for col in
                              renamed_df_pop.columns]
    renamed_df_pop = renamed_df_pop.rename(columns={
        "City City": "City",
        "City proper[c] Population": "Population",
        "City proper[c] Density (/km2)" : "Density (/km2)"
    })


    df_gdp = get_table("https://en.wikipedia.org/wiki/List_of_cities_by_GDP", 2)
    turn_to_csv(df_gdp, "cities_and_gdp.csv")
    selected_df_gdp = df_gdp[['City proper/metropolitan area', 'Official est. GDP up to date (billion US$)']]
    renamed_df_gdp = selected_df_gdp.rename(columns = {'City proper/metropolitan area' : 'City',
                                                       'Official est. GDP up to date (billion US$)' : 'GDP (billion US$)'})
    renamed_df_gdp['GDP (billion US$)'] = renamed_df_gdp['GDP (billion US$)'].apply(remove_parentheses)
    renamed_df_gdp['City'] = renamed_df_gdp['City'].apply(remove_metropolitan)
    renamed_df_gdp['City'] = renamed_df_gdp['City'].apply(remove_comma)

    merged_df = pd.merge(renamed_df_pop, renamed_df_gdp, on = 'City', how = 'inner')
    print(merged_df.head())



if __name__ == "__main__":
    main()