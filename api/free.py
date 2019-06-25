import io
import json

fp = open('apartment_buy_locations.json', encoding="utf-8")
data = json.load(fp)

newdata = {}

for province in data.keys():
	newdata[province] = {}
	for city in data[province].keys():
		if len(data[province][city].keys()) == 0:
			continue
		newdata[province][city] = data[province][city]


with io.open('apartment_buy_locations.json', 'w', encoding="utf-8") as fp:
	json.dump(newdata, fp, ensure_ascii=False)