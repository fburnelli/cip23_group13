import mechanicalsoup
import csv
import time 
### CONFIGURATION
#Intersport Main page

url = "https://www.intersportrent.ch/en/rent-shop/products/"
#Chosen Dates for scraping 
rent_dates = [{'first_rental_day':'2023-12-15', 'return_date':'2023-12-15'},
         {'first_rental_day':'2023-12-15', 'return_date':'2023-12-16'},
         {'first_rental_day':'2023-12-15', 'return_date':'2023-12-17'},
         ]
# location file
locations_csv = '../data/cip_snow_reports.csv'
# gear files
gears_csv = 'gears.csv'

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
   try:
      gears = [] # all gears for the query

      browser = mechanicalsoup.StatefulBrowser()
      browser.open(url)
      # get the searchin critaria form
      browser.select_form('form[id="portal-search"]' )
    
      #print(browser.form.print_summary())
      #set relevant parameters
      browser["q"] = location
      browser["from"] = first_rental_day
      browser["till"] = return_date
      # Submit the form
      response = browser.submit_selected()
      #to_file(browser)
     
      # Iterate each gear resulr
      results = browser.page.find(class_="row gy-4 product-grid")
   
   
      for result in results:
         try:
            gear = {'location' : location,
                 'first_rental_day' : first_rental_day,
                 'return_date' : return_date
                 }
            #gear name
            gear['gear_name'] = result.a.get_text().strip()
         
            #gear description: append all free text relativer to gear
            description = ""
            li_elements = result.find(class_="product-item__list").find_all('li')
            for li in li_elements:
               if len(description) > 0:
                  description = f"{description}__{li.text}"
               else:
                  description = li.text

            gear['description'] = description+";"
         
            #gear price
            price = result.find(class_="fz13 me-1").text 
            gear['price'] = price
            gears.append(gear.copy())
         except AttributeError as e:
            pass
         except Exception as e:
            print(e)
   except Exception as e:
      print(e)
      #input("skip cause of error")
      return gears

   return gears

def get_locations(locations_csv):
   locations = []
   with open(locations_csv, 'r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        location = row['location'].split('–')[0]
        locations.append(location)
   #return ['Leukerbad','Arosa','Verbier']
   return locations
   

if __name__ == "__main__":
   # what to scrape from confuguration
   locations = get_locations(locations_csv)
   rent_dates

   #Extract process
   gears = []
   process = True
   for location in locations:
      for rent_date in rent_dates:
         print(f"process: {location} {rent_date.get('first_rental_day')} {rent_date.get('return_date')}" ) 
         # looks like with too many request get an error HTTPSConnectionPool(host='www.intersportrent.ch', port=443): Max retries exceeded with url: /en/rent-shop/products/ (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x7f7d32d9ed30>: Failed to establish a new connection: [Errno 8] nodename nor servname provided, or not known'))
         
         time.sleep(5)
         if process == True:
            location_gears = extract_gear_data(location,rent_date.get('first_rental_day'),rent_date.get('return_date'))
            gears.extend(location_gears)
         elif 'Marécottes' in location:
            process = True 

   with open(gears_csv, 'w', newline='', encoding='utf-8') as file:
      fieldnames = gears[0].keys()
      writer = csv.DictWriter(file, fieldnames=fieldnames)
      writer.writeheader()
      writer.writerows(gears)
#Code structure as per
#https://elearning.hslu.ch/ilias/ilias.php?baseClass=ilwikihandlergui&cmdNode=17z:sh&cmdClass=ilobjwikigui&cmd=viewPage&ref_id=5933006&page=Project_FAQs#ilPageTocA121
# EXTARCT location and location orig  to do joi later
#       rename *_stage1.csv
# TRANSFORM  *_stage3.csv
#      Clean so dont remove ????duplicates, spelling mistakes, unsuitable types, zero values, outliers, missing values, incoherent entries, irrelevant extensions, e
#      Enrich add 3 calculated fields
# 
# LOAD
#       stage3 to maria db    
#
# ANALYS REview question