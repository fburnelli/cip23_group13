import mechanicalsoup
browser = mechanicalsoup.StatefulBrowser()
url = "https://www.intersportrent.ch/en/rent-shop/products/"

browser.open(url)
#print(browser.get_url())


#get HTML
input_id = "searchbox"
text_to_fill = "Arosa"
browser.get_current_page().find('input', {'id': input_id})['value'] = text_to_fill

# Select the form by its ID
form = browser.select_form("#portal-search")

# Fill in the form fields with your data
#form["field_name2"] = "value2"
# Add more fields as needed

# Submit the form
browser.submit_selected()
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

