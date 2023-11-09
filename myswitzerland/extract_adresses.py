import json
import re
import csv

formatted_adresses = []
postal_codes_and_cities = []
cities = []
accomodations_file = '../data/accom_all.json'

def list_to_csv(list_data,filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        uniques = list(set(list_data))
        for item in uniques:
            writer.writerow([item])


with open(accomodations_file) as f:
    data = json.load(f)




for element in data:
    for l in element.get('results'):
        formatted_address = l.get('formatted_address')
        formatted_adresses.append(formatted_address)
        postal_code_city = formatted_address.split(',')[-2]
        postal_codes_and_cities.append(postal_code_city.strip())
        city =  re.sub(r'\d{4}', '', postal_code_city)
        cities.append(city)

        
list_to_csv(formatted_adresses,'formatted_adresses.csv')
list_to_csv(postal_codes_and_cities,'postal_codes_and_cities.csv')
list_to_csv(cities,'cities.csv')

