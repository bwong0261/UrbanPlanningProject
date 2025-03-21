import requests
import certifi
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

def remove_parentheses(text):
    for i in range(len(text)):
        if text[i] == "(" or text[i] == "[":
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

def remove_greater(text):
    for i in range(len(text) - 6):
        if (text[i] == "G" and
            text[i + 1] == "r" and
            text[i + 2] == "e" and
            text[i + 3] == "a" and
            text[i + 4] == "t" and
            text[i + 5] == "e" and
            text[i + 6] == "r"):
                text = text[i + 7:].strip()
                break
    return text

def remove_area(text):
    for i in range(len(text) - 3):
        if (text[i].lower() == "a" and
            text[i + 1] == "r" and
            text[i + 2] == "e" and
            text[i + 3] == "a"):
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
    renamed_df_pop['Density (/km2)'] = renamed_df_pop['Density (/km2)'].apply(remove_parentheses)


    df_gdp = get_table("https://en.wikipedia.org/wiki/List_of_cities_by_GDP", 2)
    turn_to_csv(df_gdp, "cities_and_gdp.csv")
    selected_df_gdp = df_gdp[['City proper/metropolitan area', 'Official est. GDP up to date (billion US$)']]
    renamed_df_gdp = selected_df_gdp.rename(columns = {'City proper/metropolitan area' : 'City',
                                                       'Official est. GDP up to date (billion US$)' : 'GDP (billion US$)'})
    renamed_df_gdp['GDP (billion US$)'] = renamed_df_gdp['GDP (billion US$)'].apply(remove_parentheses)
    renamed_df_gdp['City'] = renamed_df_gdp['City'].apply(remove_metropolitan)
    renamed_df_gdp['City'] = renamed_df_gdp['City'].apply(remove_comma)
    renamed_df_gdp['City'] = renamed_df_gdp['City'].apply(remove_greater)
    renamed_df_gdp['City'] = renamed_df_gdp['City'].apply(remove_area)

    merged_df = pd.merge(renamed_df_pop, renamed_df_gdp, on = 'City', how = 'inner')
    turn_to_csv(merged_df, "cities_and_gdp_and_pop.csv")
    print(merged_df.head())


if __name__ == "__main__":
    main()