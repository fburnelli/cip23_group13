import requests   
from bs4 import BeautifulSoup   
import re    
import os

import pandas as pd  
import numpy as np    

from datetime import datetime, timedelta

import warnings    
warnings.filterwarnings('ignore') 


page_url = "https://snow.myswitzerland.com/snow_reports/piste/?p="   
base_url = "https://snow.myswitzerland.com/"


all_data_from_url = []   
list_of_links = []


for page_number in range(1, 8):     
    url = page_url + str(page_number)     
    response = requests.get(url)    
    #print("Status code of the request:", response.status_code)  
    html_content = response.content   
    soup = BeautifulSoup(html_content, 'html.parser')   

    all_resorts_html = soup.find_all('tr', {'class': 'FilterGridTable--row'})  
    #print(f"Number of resorts listed in page {page_number}: ", len(all_resorts_html))
    
    for row in all_resorts_html:  
        all_data_from_url.append(row) 
        resort_url = soup.find_all('a', {'class': 'FilterGridTable--link'}, href=True) 
    
    for link in resort_url:
        href = link['href']
        #print(href)
        full_link = base_url + href   
        
        if full_link not in list_of_links:  
            list_of_links.append(full_link)

resort_title = []

for row in all_data_from_url:
    headers = row.find_all('div', {"class":"FilterGridTable--title"})    
    data = [header.get_text(strip=True) for header in headers]  
    resort_title.append(data)   
    
resort_df = pd.DataFrame(resort_title, columns = ["Resort"])


data_locations = []

for row in all_data_from_url:
    headers = []
    for header in row.find_all('div', {"class":"FilterGridTable--info"}):
        headers.append(header.get_text(strip=True))
    data_locations.append(headers)

resort_df["Link"] = list_of_links

data_content = []

for row in all_data_from_url:
    content = [content.get_text(strip=True) for content in row.find_all('td', {'class': 'FilterGridTable--cell'})]
    data_content.append(content)

for i, content in enumerate(data_content):
    if len(content) < 3:
        data_content[i] = content + [""] * (3 - len(content))

# Using NumPy to assign the data from data_content to specific columns in resort_df
for i, col in enumerate(["Open Pistes km", "Slope Condition", "Open Lifts"]):
    resort_df[col] = np.array([content[i] for content in data_content])

data_content = []

for row in all_data_from_url:
    content = [content.get_text(strip=True) for content in row.find_all('td', {'class': 'FilterGridTable--cell'})]
    data_content.append(content)

for i, content in enumerate(data_content):
    if len(content) < 3:
        data_content[i] = content + [""] * (3 - len(content))

# Using NumPy to assign the data from data_content to specific columns in resort_df
for i, col in enumerate(["Open Pistes km", "Slope Condition", "Open Lifts"]):
    resort_df[col] = np.array([content[i] for content in data_content])


hours_data = []

for link in resort_df["Link"]:
    response = requests.get(link)
    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")

    resort_op_hours = soup.find_all("div", {"class": "ArticleSection", "id": "articlesection-u20"})

    link_data_hours = {}

    for row in resort_op_hours:
        cont_test = row.find_all("th", {"scope": "row"})
        test_test = row.find_all("td")

        th_values = [content.get_text(strip = True) for content in cont_test]
        td_values = [con.get_text(strip = True) for con in test_test]

        link_data_hours.update(dict(zip(th_values, td_values)))

    hours_data.append(link_data_hours)

opening_hours = pd.DataFrame(hours_data)

resort_df = pd.concat([resort_df, opening_hours], axis=1)

hours_data = []

for link in resort_df["Link"]:
    response = requests.get(link)
    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")

    resort_op_hours = soup.find_all("div", {"class": "ArticleSection", "id": "articlesection-u20"})

    link_data_hours = {}

    for row in resort_op_hours:
        cont_test = row.find_all("th", {"scope": "row"})
        test_test = row.find_all("td")

        th_values = [content.get_text(strip = True) for content in cont_test]
        td_values = [con.get_text(strip = True) for con in test_test]

        link_data_hours.update(dict(zip(th_values, td_values)))

    hours_data.append(link_data_hours)

opening_hours = pd.DataFrame(hours_data)

resort_df = pd.concat([resort_df, opening_hours], axis=1)



