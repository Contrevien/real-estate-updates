from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time
import json
import sys


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



def ebay_scraper(scraping_link, t):
	final_link = scraping_link
	driver.get(final_link)

	# the final result
	result = {}

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
			link = ""
			try:
				link = li.find_elements_by_class_name("aditem-main")[0].find_elements_by_tag_name("a")[0].get_attribute("href")
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
			result[link] = temp
		try:
			final_link = driver.find_elements_by_class_name("pagination-next")[0].get_attribute("href")
			page += 1
			driver.get(final_link)
		except:
			break
	return result


def immobilienscout24_scraper(scraping_link, t):
	print("Scraper let loose: immobilienscout24_scraper")
	final_link = scraping_link
	driver.get(final_link)

	result = {}

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
			link = ""	

			try:
				link = li.find_elements_by_class_name("result-list-entry__brand-title-container")[0].get_attribute("href")
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
				if t == "room_rent":
					temp["rooms"] = "1 rooms"
				else:					
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
			result[link] = temp
		try:
			final_link = driver.find_element_by_xpath("//a[@data-is24-qa='paging_bottom_next']").get_attribute("href")
			page += 1
			driver.get(final_link)
		except:
			break
	return result


def normal_scrape(website, scraping_link, t):
	print("Using normal scraper")
	if website == "ebay":
		return ebay_scraper(scraping_link, t)
	if website == "immobilienscout24" or website == "immobilienscout24-kreis":
		return immobilienscout24_scraper(scraping_link, t)
	return {}


location = sys.argv[1]
t = sys.argv[2]

#the locations database
locations = {
	"apartment_rent": {},
	"room_rent": {},
	"apartment_buy": {}	
}

print("Getting locations...")
fp2 = open('apartment_rent_locations.json', encoding="utf8")
locations["apartment_rent"] = json.load(fp2)

fp3 = open('room_rent_locations.json', encoding="utf8")
locations["room_rent"] = json.load(fp3)

fp4 = open('apartment_buy_locations.json', encoding="utf8")
locations["apartment_buy"] = json.load(fp4)

print("Success")

#open already scraped ones
fp5 = open('scraped.json', encoding="utf8")
scraped = json.load(fp5)

[city, province] = location.split(', ')
if province in scraped[t].keys() and city in scraped[t][province].keys():
	pass
else:
	print(locations[t].keys())
	links = locations[t][province][city]
	for website in sorted(links.keys()):
		scraping_link = links[website]
		result = normal_scrape(website, scraping_link, t)
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
import io
with io.open('scraped.json', 'w', encoding="utf8") as f:
	json.dump(scraped, f, ensure_ascii=False)
print("Dumped")