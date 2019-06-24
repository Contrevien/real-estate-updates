from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time
import json
import io
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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
driver = webdriver.Chrome(options=options)
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


###############################
########## Scrapers ###########
###############################


def ebay_scraper(scraping_link, old_ones={}, t="apartment_rent"):
	print("Scraper let loose: ebay_scraper")
	final_link = scraping_link
	driver.get(final_link)

	result = {}
	new_ones_ebay = {}

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
			link = ""
			try:
				link = li.find_elements_by_class_name("aditem-main")[0].find_elements_by_tag_name("a")[0].get_attribute("href")
			except:
				errors["ebay"].append("Link fetch at {0}, #{1}".format(final_link, i))
				continue

			if link in old_ones.keys():
				result[link] = old_ones[link]
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
			new_ones_ebay[link] = temp
		try:
			final_link = driver.find_elements_by_class_name("pagination-next")[0].get_attribute("href")
			page += 1
			driver.get(final_link)
		except:
			break
	return [result, new_ones_ebay]

def immobilienscout24_scraper(scraping_link, old_ones={}, t="apartment_rent"):
	print("Scraper let loose: immobilienscout24_scraper")
	final_link = scraping_link
	driver.get(final_link)

	result = {}
	new_ones_immobilien = {}

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

			if link in old_ones.keys():
				result[link] = old_ones[link]
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
			new_ones_immobilien[link] = temp
		try:
			final_link = driver.find_element_by_xpath("//a[@data-is24-qa='paging_bottom_next']").get_attribute("href")
			page += 1
			driver.get(final_link)
		except:
			break

	return [result, new_ones_immobilien]


##################################
########### END SCRAPERS #########
##################################


def compare_scrape(website, scraping_link, old_ones, t):
	print("Using compare scraper")
	if website == "ebay":
		return ebay_scraper(scraping_link, old_ones, t)
	if website == "immobilienscout24" or website == "immobilienscout24-kreis":
		return immobilienscout24_scraper(scraping_link, old_ones, t)
	return [{}, {}]


#the users database
print("Getting users...")
fp = open('users.json', encoding="utf8")
users = json.load(fp)
print("Success")

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
fp5 = open('scraped.json', encoding="utf8")
scraped = json.load(fp5)

print(new_ones.keys())
for t in types.keys():
	# types -> apartment_rent = { "City, Province" }
	for location in types[t]:
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
					old_ones = focus[website]

					# compare scrape using that link
					[result, new_one] = compare_scrape(website, scraping_link, old_ones, t)
					print("Caching the results...")

					# if the results are more than one then add it to the result
					if len(result) > 0:
						if len(new_ones[t]) != 0 and province in new_ones[t].keys() and city in new_ones[t][province].keys():
							new_ones[t][province][city][website] = new_one
						else:
							new_ones[t][province] = {}
							new_ones[t][province][city] = {}
							new_ones[t][province][city][website] = new_one
						scraped[t][province][city][website] = result

print("Dumping the results")
with io.open('scraped.json', 'w', encoding="utf8") as f:
	json.dump(scraped, f, ensure_ascii=False)
with io.open('new_ones.json', 'w', encoding="utf8") as f:
	json.dump(new_ones, f, ensure_ascii=False)
print("Dumped")

print("Sending mails to users")
to_send = {}

for user in users.keys():
	types = users[user]["parameters"]["type"]
	loc = users[user]["parameters"]["location"]
	[city, province] = loc.split(", ")
	price = users[user]["parameters"]["max_price"].split()[0]
	rooms = users[user]["parameters"]["rooms"].split()[0]
	to_send[user] = {}
	for t in types:
		if len(new_ones[t]) != 0 and province in new_ones[t].keys() and city in new_ones[t][province].keys():
			for website in new_ones[t][province][city].keys():
				for link in new_ones[t][province][city][website].keys():
					focus = new_ones[t][province][city][website][link]
					if rooms in focus["rooms"] and focus["price"].split()[0] <= price:
						to_send[user][link] = focus



smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = "therealestatebotgermany@gmail.com"
password = "dontplease"

# Create a secure SSL context
context = ssl.create_default_context()

try:
	# Try to log in to server and send email
	server = smtplib.SMTP(smtp_server,port)
	server.ehlo() # Can be omitted
	server.starttls(context=context) # Secure the connection
	server.ehlo() # Can be omitted
	server.login(sender_email, password)


	for user in to_send.keys():

		filling = ""

		if(len(to_send[user]) == 0):
			continue
			
		for link in to_send[user].keys():
			el = """
				<div class="showbox">
					<h2>{0}</h2>
					<div class="details">
						<p>{1}</p>
						<p>{2}</p>
						<p>{3}</p>
						<p>{4}</p>
					</div>
					<a target="_blank" href="{5}">
						<div class="link">
							View
						</div>
					</a>
				</div>
				<hr />
			""".format(
				to_send[user][link]["name"],
				to_send[user][link]["specific_loc"],
				to_send[user][link]["rooms"],
				to_send[user][link]["price"],
				to_send[user][link]["area"],
				link
			)
			filling += el
		
		html = """
			<html>
			<head>
				<link href="https://fonts.googleapis.com/css?family=Montserrat:400,800&display=swap" rel="stylesheet"/>
				<style>
					.hai {
						font-family: "Montserrat";
						font-weight: bolder;
						margin-top: 5%;
					}
					.cover {
						text-align: center;
					}
					.goodslist {
						justify-content: center;
						width: 100%;
					}
					.showbox {
						width: 90%;
						min-height: 100px;
						margin: 10px auto;
						text-align: left;
					}
					.showbox h2 {
						font-family: "Montserrat";
						font-weight: 400;
						color: #777;
					}
					.showbox p {
						font-family: "Montserrat";
						font-weight: bolder;
						color: #eee;
						font-size: 13px;
						display: inline;
						margin-left: 10px;
					}
					.details {
						width: 100%;
						padding: 10px 0;
						background: #111;
					}
					.link {
						font-family: "Montserrat";
						font-weight: bolder;
						color: #eee;
						font-size: 13px;
						margin-top: 10px;
						margin-bottom: 15px;
						width: 20%;
						text-align: center;
						padding: 10px 0;
						background: rgba(255,0,0,0.8);
						cursor: pointer;
					}
					.link a {
						text-decoration: none;
						color: #eee;
					}
				</style>
			</head>
			<body class="cover">
				<h1 class="hai">neue postings</h1>
				<div class="goodslist">
				""" + filling + """	
				</div>
			</body>
			</html>
		"""


		message = MIMEMultipart("alternative")
		message["Subject"] = "New properties in {0}".format(users[user]["parameters"]["location"])
		message["From"] = sender_email
		message["To"] = user
		part1 = MIMEText(html, "html")
		message.attach(part1)
		server.sendmail(sender_email, user, message.as_string())
		print("sent")

except:
	errors["email"] = 1