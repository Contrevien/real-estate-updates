from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time
import json


#Selenium driver configs
ch = os.getcwd() + '/tools/chromedriver.exe'
options = Options()
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
options.set_headless(headless=True)
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("log-level=3")
driver = webdriver.Chrome(options=options, executable_path=ch)
wait = WebDriverWait(driver, 10)


errors = {
	"ebay": [],
	"immobilienscout24": []
}

new_ones = {
	"apartment_rent": {},
	"apartment_buy": {},
	"room_rent": {}
}


####### scrapers #####


def ebay_scraper(scraping_link, focus_link=""):
	print("Scraper let loose: ebay_scraper")
	if focus_link != "":
		final_link = scraping_link
		driver.get(final_link)

		result = []

		page = 1
		done = False
		while not done:
			ul = None
			lis = None
			try:
				ul = driver.find_element_by_id("srchrslt-adtable")
				lis = ul.find_elements_by_class_name("ad-listitem")
			except:
				errors["ebay"].append("List fetching failed at {0}".format(final_link))
				break

			for i,li in enumerate(lis):
				temp = {}		

				try:
					temp["link"] = li.find_elements_by_class_name("aditem-main")[0].find_elements_by_tag_name("a")[0].get_attribute("href")
				except:
					errors["ebay"].append("Link fetch at {0}, #{1}".format(final_link, i))
					continue

				if temp["link"] == focus_link:
					done = True
					break

				try:
					temp["name"] = li.find_elements_by_class_name("aditem-main")[0].find_elements_by_tag_name("a")[0].text
				except:
					errors["ebay"].append("Name fetch at {0}, #{1}".format(final_link, i))
					continue
					

				try:
					temp["description"] = li.find_elements_by_class_name("aditem-main")[0].find_elements_by_tag_name("p")[0].text
				except:
					errors["ebay"].append("Desc fetch at {0}, #{1}".format(final_link, i))
					continue
				
				try:
					more_det = li.find_elements_by_class_name("aditem-main")[0].find_elements_by_tag_name("p")[1].text.split()
					temp["rooms"] = more_det[0] + " rooms"
					temp["area"] = more_det[2] + " " + more_det[3]
				except:
					errors["ebay"].append("Extra fetch at {0}, #{1}".format(final_link, i))
					continue

				try:
					loc_n_price_det = li.find_elements_by_class_name("aditem-details")[0].text
					[temp["price"], ref, temp["specific_loc"]] = loc_n_price_det.split("\n")
				except:
					try:
						[temp["price"], ref, temp["specific_loc"], useless] = loc_n_price_det.split("\n")
					except:
						errors["ebay"].append("Loc n Price fetch at {0}, #{1}".format(final_link, i))					
						continue
				result.append(temp)
			try:
				final_link = driver.find_elements_by_class_name("pagination-next")[0].get_attribute("href")
				page += 1
				driver.get(final_link)
			except:
				break
		return result

	else:
		final_link = scraping_link
		driver.get(final_link)

		# the final result
		result = []

		# get the list
		page = 1
		while True:
			ul = None
			lis = None
			try:
				ul = driver.find_element_by_id("srchrslt-adtable")
				lis = ul.find_elements_by_class_name("ad-listitem")
			except:
				errors["ebay"].append("List fetching failed at {0}".format(final_link))
				break

			print("Scraping page {0}..  Errors: {1}".format(page, len(errors["ebay"])))
	
			for i,li in enumerate(lis):
				temp = {}		

				try:
					temp["link"] = li.find_elements_by_class_name("aditem-main")[0].find_elements_by_tag_name("a")[0].get_attribute("href")
				except:
					errors["ebay"].append("Link fetch at {0}, #{1}".format(final_link, i))
					continue

				try:
					temp["name"] = li.find_elements_by_class_name("aditem-main")[0].find_elements_by_tag_name("a")[0].text
				except:
					errors["ebay"].append("Name fetch at {0}, #{1}".format(final_link, i))
					continue
					

				try:
					temp["description"] = li.find_elements_by_class_name("aditem-main")[0].find_elements_by_tag_name("p")[0].text
				except:
					errors["ebay"].append("Desc fetch at {0}, #{1}".format(final_link, i))
					continue
				
				try:
					more_det = li.find_elements_by_class_name("aditem-main")[0].find_elements_by_tag_name("p")[1].text.split()
					temp["rooms"] = more_det[0] + " rooms"
					temp["area"] = more_det[2] + " " + more_det[3]
				except:
					errors["ebay"].append("Extra fetch at {0}, #{1}".format(final_link, i))
					continue

				try:
					loc_n_price_det = li.find_elements_by_class_name("aditem-details")[0].text
					[temp["price"], ref, temp["specific_loc"]] = loc_n_price_det.split("\n")
				except:
					try:
						[temp["price"], ref, temp["specific_loc"], useless] = loc_n_price_det.split("\n")
					except:
						errors["ebay"].append("Loc n Price fetch at {0}, #{1}".format(final_link, i))					
						continue
				result.append(temp)
			try:
				final_link = driver.find_elements_by_class_name("pagination-next")[0].get_attribute("href")
				page += 1
				driver.get(final_link)
			except:
				break
		return result


def immobilienscout24_scraper(scraping_link, old_ones=[]):
	print("Scraper let loose: immobilienscout24_scraper")
	if old_ones != []:
		link_based = {}
		for entry in old_ones:
			link_based[entry["link"]] = entry

		final_link = scraping_link
		driver.get(final_link)

		result = []

		page = 1
		while True:
			ul = None
			lis = None
			try:
				ul = driver.find_element_by_id("resultListItems")
				lis = ul.find_elements_by_class_name("result-list__listing ")
			except:
				errors["immobilienscout24"].append("List fetching failed at {0}".format(final_link))
				break

			print("Scraping page {0}..  Errors: {1}".format(page, len(errors["immobilienscout24"])))
			
			for i,li in enumerate(lis):
				temp = {}		

				try:
					temp["link"] = li.find_elements_by_class_name("result-list-entry__brand-title-container")[0].get_attribute("href")
				except:
					errors["immobilienscout24"].append("Link fetch at {0}, #{1}".format(final_link, i))
					continue

				if temp["link"] in link_based.keys():
					continue

				try:
					temp["name"] = li.find_elements_by_class_name("result-list-entry__brand-title")[0].text
				except:
					errors["immobilienscout24"].append("Name fetch at {0}, #{1}".format(final_link, i))
					continue
					

				try:
					temp["description"] = ""
				except:
					errors["immobilienscout24"].append("Desc fetch at {0}, #{1}".format(final_link, i))
					continue
				
				try:
					more_det = li.find_elements_by_class_name("result-list-entry__primary-criterion")
					temp["price"] = more_det[0].find_elements_by_tag_name("dd")[0].text
					temp["rooms"] = more_det[2].find_elements_by_tag_name("dd")[0].text + " rooms"
					temp["area"] = more_det[1].find_elements_by_tag_name("dd")[0].text
				except:
					errors["immobilienscout24"].append("Extra fetch at {0}, #{1}".format(final_link, i))
					continue

				try:
					temp["specific_loc"] = li.find_elements_by_class_name("result-list-entry__address")[0].text
				except:
					errors["immobilienscout24"].append("Loc fetch at {0}, #{1}".format(final_link, i))					
					continue
				result.append(temp)
			try:
				final_link = driver.find_element_by_xpath("//a[@data-is24-qa='paging_bottom_next']").get_attribute("href")
				page += 1
				driver.get(final_link)
			except:
				break

		return result


	else:
		final_link = scraping_link
		driver.get(final_link)

		result = []

		page = 1
		while True:
			ul = None
			lis = None
			try:
				ul = driver.find_element_by_id("resultListItems")
				lis = ul.find_elements_by_class_name("result-list__listing ")
			except:
				errors["immobilienscout24"].append("List fetching failed at {0}".format(final_link))
				break

			print("Scraping page {0}..  Errors: {1}".format(page, len(errors["immobilienscout24"])))
			
			for i,li in enumerate(lis):
				temp = {}		

				try:
					temp["link"] = li.find_elements_by_class_name("result-list-entry__brand-title-container")[0].get_attribute("href")
				except:
					errors["immobilienscout24"].append("Link fetch at {0}, #{1}".format(final_link, i))
					continue

				try:
					temp["name"] = li.find_elements_by_class_name("result-list-entry__brand-title")[0].text
				except:
					errors["immobilienscout24"].append("Name fetch at {0}, #{1}".format(final_link, i))
					continue
					

				try:
					temp["description"] = ""
				except:
					errors["immobilienscout24"].append("Desc fetch at {0}, #{1}".format(final_link, i))
					continue
				
				try:
					more_det = li.find_elements_by_class_name("result-list-entry__primary-criterion")
					temp["price"] = more_det[0].find_elements_by_tag_name("dd")[0].text
					temp["rooms"] = more_det[2].find_elements_by_tag_name("dd")[0].text + " rooms"
					temp["area"] = more_det[1].find_elements_by_tag_name("dd")[0].text
				except:
					errors["immobilienscout24"].append("Extra fetch at {0}, #{1}".format(final_link, i))
					continue

				try:
					temp["specific_loc"] = li.find_elements_by_class_name("result-list-entry__address")[0].text
				except:
					errors["immobilienscout24"].append("Loc fetch at {0}, #{1}".format(final_link, i))					
					continue
				result.append(temp)
			try:
				final_link = driver.find_element_by_xpath("//a[@data-is24-qa='paging_bottom_next']").get_attribute("href")
				page += 1
				driver.get(final_link)
			except:
				break
		return result


###### end scrapers ######

#scrapers mapping functions
def compare_scrape(website, scraping_link, focus_link):
	print("Using compare scraper")
	if website == "ebay":
		return ebay_scraper(scraping_link, focus_link[0]["link"])
	if website == "immobilienscout24" or website == "immobilienscout24-kreis":
		return immobilienscout24_scraper(scraping_link, focus_link)
	return []


def normal_scrape(website, scraping_link):
	print("Using normal scraper")
	if website == "ebay":
		return ebay_scraper(scraping_link)
	if website == "immobilienscout24" or website == "immobilienscout24-kreis":
		return immobilienscout24_scraper(scraping_link)
	return []


#the users database
print("Getting users...")
fp = open('users.json')
users = json.load(fp)
print("Success")

#the locations database
locations = {
	"apartment_rent": {},
	"room_rent": {},
	"apartment_buy": {}	
}

print("Getting locations...")
fp2 = open('apartment_rent_locations.json')
locations["apartment_rent"] = json.load(fp2)
print("Success")

#setup locations to scrape
types = {
	"apartment_rent": [],
	"room_rent": [],
	"apartment_buy": []
}

print("Reading the scrapers with the data...")
for user in users.keys():
	for t in users[user]["parameters"]["type"]:
		if users[user]["parameters"]["location"] not in types[t]:
			types[t].append(users[user]["parameters"]["location"])


#open already scraped ones
fp5 = open('scraped.json')
scraped = json.load(fp5)

print("Initiating timestamp...")
timestamp = int(time.time())

for t in types.keys():
	# types -> apartment_rent = { "City, Province" }
	for location in types[t]:
		print("Going in for {0} in {1}".format(t, location))
		# split the city and province
		[city, province] = location.split(', ')

		# scraped -> apartment_rent = { "Province": { "City": { "website": [] } } }
		# if province and city have already been scraped previously
		if province in scraped[t].keys() and city in scraped[t][province].keys():
			focus = scraped[t][province][city]
			links = locations[t][province][city]
			
			# for each website available for the city
			for website in links.keys():

				# get the link to scrape it
				scraping_link = links[website]

				# if previous results were not empty
				if focus[website] != None and len(focus[website]) > 0:
					# get the first link
					focus_link = focus[website]

					# compare scrape using that link
					result = compare_scrape(website, scraping_link, focus_link)
					print("Caching the results...")

					# if the results are more than one then add it to the result
					if len(result) > 0:
						new_ones[t][province] = {}
						new_ones[t][province][city] = {}
						new_ones[t][province][city][website] = result
						result.extend(focus[website])
						scraped[t][province][city][website] = result

				# previous result was empty, scrape normally
				else:
					result = normal_scrape(website, scraping_link)
					print("Caching the results...")
					if result != None and len(result) > 0:
						new_ones[t][province] = {}
						new_ones[t][province][city] = {}
						new_ones[t][province][city][website] = result
						scraped[t][province][city][website] = result
		
		# the province/city have not been scraped before, scrape it again!
		else:
			links = locations[t][province][city]
			for website in links.keys():
				scraping_link = links[website]
				result = normal_scrape(website, scraping_link)
				print("Caching the results...")
				if province in scraped[t].keys():
					if city in scraped[t][province].keys():
						scraped[t][province][city][website] = result
					else:
						scraped[t][province][city] = {}
						scraped[t][province][city][website] = result
				else:
					scraped[t][province] = {}
					scraped[t][province][city] = {}
					scraped[t][province][city][website] = result

print("Dumping the results")
with open('scraped.json', 'w') as f:
	json.dump(scraped, f)
with open('new_ones.json', 'w') as f:
	json.dump(new_ones, f)
print("Dumped")

to_send = {}

for user in users.keys():
	types = users[user]["parameters"]["type"]
	loc = users[user]["parameters"]["location"]
	[city, province] = loc.split(", ")
	price = users[user]["parameters"]["max_price"]
	rooms = users[user]["parameters"]["rooms"]
	for t in types:
		if len(new_ones[t]) != 0 and province in new_ones[t].keys() and city in new_ones[t][province].keys():
			for website in new_ones[t][province][city].keys():
				focus = new_ones[t][province][city][website]
				for ap in focus:
					if ap["rooms"] == rooms and ap["price"] <= price:
						to_send[user] = ap

with open("toSend.json", "w") as f:
	json.dump(to_send, f)