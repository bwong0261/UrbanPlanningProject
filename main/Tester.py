import requests
import certifi
import pandas as pd

url = "https://en.wikipedia.org/wiki/List_of_cities_proper_by_population_density"

# Fetch the page content using requests with certificate verification
response = requests.get(url, verify=certifi.where())
html_content = response.text

# Now parse the HTML with pandas
tables = pd.read_html(html_content)
df = tables[3]
df.to_csv("Cities_and_Density", index=False ,encoding='utf-8')

print(df.head())