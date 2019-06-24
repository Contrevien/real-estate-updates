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
driver.implicitly_wait(5)
wait = WebDriverWait(driver, 10)

import io
fp = io.open('apartment_buy_locations.json', encoding="utf8")
data = json.load(fp)

for location in data.keys():
	link_name = ""
	if "Baden" in location:
		link_name = "Baden-Wuerttemberg"
	elif "ringen" in location:
		link_name = "Thueringen"
	else:
		link_name = location
	driver.get("https://www.immobilienscout24.de/Suche/S-T/Wohnung-Kauf/" + link_name)
	value = driver.execute_script('''
			document.getElementsByClassName('drop-down-layer-container')[0].getElementsByClassName('one-half')[0].click();
		''')
	pit = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'cockpit__geo-hierarchy-selection-list')))
	labels = pit[0].find_elements_by_tag_name('label')[1:]
	names = []
	origNames = []
	for l in labels:
		temp = "-".join(l.text.split()[:-1])
		if "(" in temp:
			temp = temp.replace("(", "")
			temp = temp.replace(")", "")
			names.append(temp)
		else:
			names.append(temp)
		temp2 = "-".join(l.text.split()[:-1])
		if "(" in temp2:
			temp2 = temp2[:temp2.index("(") - 1]
		origNames.append(temp2)
		for i in range(len(names)):
			name = names[i]
			n = names[i]
			if "ü" in n:
				name = n.replace("ü", "ue")
			if "Ä" in n:
				name = n.replace("Ä", "Ae")
			if "ä" in n:
				name = n.replace("ä", "ae")
			if "." in n:
				name = n.replace(".", "-")
			if "ö" in n:
				name = n.replace("ö", "oe")
			if "Ü" in n:
				name = n.replace("Ü", "Ue")
			if "ß" in n:
				name = n.replace("ß", "ss")
			try:
				if("-kreis" in name.lower()):
					if origNames[i] in data[location].keys():
						data[location][origNames[i]]["immobilienscout24-kreis"] = driver.current_url + "/" + name
					else:
						data[location][origNames[i]] = {}
						data[location][origNames[i]]["immobilienscout24-kreis"] = driver.current_url + "/" + name
				else:
					if origNames[i] in data[location].keys():
						data[location][origNames[i]]["immobilienscout24"] = driver.current_url + "/" + name
					else:
						data[location][origNames[i]] = {}
						data[location][origNames[i]]["immobilienscout24"] = driver.current_url + "/" + name

			except:
				pass
			
with io.open('new_locations.json', 'w', encoding="utf8") as fp:
	json.dump(data, fp, ensure_ascii=False)