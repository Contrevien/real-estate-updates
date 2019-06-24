from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time
import json

ch = os.getcwd() + '/tools/chromedriver.exe'
options = Options()
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
# options.set_headless(headless=True)
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("log-level=3")
driver = webdriver.Chrome(options=options, executable_path=ch)
wait = WebDriverWait(driver, 10)

driver.get('https://www.ebay-kleinanzeigen.de/s-wohnung-kaufen/c196')

containers = driver.find_elements_by_class_name('browsebox')
the_box = ""
for container in containers:
	if 'contentbox' in container.get_attribute('class'):
		the_box = container
		break

areas = {}
target = the_box.find_elements_by_tag_name('section')[-1]
names = list(map(lambda x: x.split()[0], target.text.split("\n")[1:]))
links = target.find_elements_by_tag_name('a')
for i in range(len(names)):
	areas[names[i]] = links[i].get_attribute('href')

# print(areas)

for name,link in areas.items():
	driver.get(link)
	containers = driver.find_elements_by_class_name('browsebox')
	the_box = ""
	for container in containers:
		if 'contentbox' in container.get_attribute('class'):
			the_box = container
			break
	areas[name] = {}
	target = the_box.find_elements_by_tag_name('section')[-1]
	try:
		driver.execute_script("""
				document.getElementsByClassName("j-listoverlay-viewall")[0].click()
			""")
	except:
		continue
	ul = driver.find_elements_by_class_name("listoverlay-list")[0]
	lis = ul.find_elements_by_tag_name("li")
	for li in lis:
		areas[name][li.find_elements_by_tag_name("a")[0].text] = li.find_elements_by_tag_name("a")[0].get_attribute("href")

	# names = list(map(lambda x: x.split()[0], target.text.split("\n")[2:]))
	# links = target.find_elements_by_tag_name('a')[1:]
	# for i in range(len(names)):
	# 	areas[name][names[i]] = links[i].get_attribute('href')

with open('apartment_buy_locations.json', 'w') as fp:
	json.dump(areas, fp)