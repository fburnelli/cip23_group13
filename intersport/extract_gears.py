import mechanicalsoup

### CONFIGURATION
#Intersport Main page
url = "https://www.intersportrent.ch/en/rent-shop/products/"
#Chosen Dates for scraping 
rent_dates = [{'first_rental_day':'2023-12-15', 'return_date':'2023-12-15'},
         {'first_rental_day':'2023-12-15', 'return_date':'2023-12-16'},
         {'first_rental_day':'2023-12-15', 'return_date':'2023-12-17'},
         ]

#helper functions for debug
def to_file(browser):
   with open('o.html','w') as f:
      f.write(str(browser.page))
   input(1111)


def extract_gear_data(location,first_rental_day,return_date):
   """" For the given configuration ectract gear data from intersport shops
        Where: location
        When:  first_rental_day,return_date
   """
   
   browser = mechanicalsoup.StatefulBrowser()
   browser.open(url)
   
   # get rhe searchin critaria form
   browser.select_form('form[id="portal-search"]' )
   #print(browser.form.print_summary())
   #set relevant parameters
   browser["q"] = location
   browser["from"] = first_rental_day
   browser["till"] = return_date

   # Submit the form
   response = browser.submit_selected()
   to_file(browser)
   
   # Iterste each gear resulr
   results = browser.page.find(class_="row gy-4 product-grid")
   
   gears = [] # all gears for the query
   for result in results:
      try:
         gear = {}
         #gear name
         gear['gear_name'] = result.a.get_text().strip()
         
         #gear description: append all free text relativer to gear
         description = ""
         li_elements = result.find(class_="product-item__list").find_all('li')
         for li in li_elements:
            description = f"{description};{li.text}"
         gear['description'] = description+";"
         
         #gear price
         price = result.find(class_="fz13 me-1").text 
         gear['price'] = price
      except Exception as e:
         print(e)

   input(9999)
   #browser.select("autocomplete_suggestion_selector")  # Replace with the actual selector for the suggestion
   #browser.click()

   #element = browser.select('a.btn.btn-primary-outline')
   #element[0].click()
   elements = browser.page.find('a', class_='btn btn-primary-outline')
   browser.follow_link(elements)

   #for element in elements:
   #    print(element.text)


   spans = browser.page.find_all('span')
   for span in spans:
      print(span)
   #print(browser.get_current_page())

def get_locations():
   return ['Arosa','Verbier']
   

if __name__ == "__main__":
   # what to scrape from confuguration
   locations = get_locations()
   rent_dates
   #Extract process
   for location in locations:
      for rent_date in rent_dates:
         #print(location,rent_date.get('first_rental_day'),rent_date.get('return_date') ) 
         extract_gear_data(location,rent_date.get('first_rental_day'),rent_date.get('return_date'))
         input("next>>>")




