import io
import json

fp = open('scraped.json', encoding="utf-8")
data = json.load(fp)

with io.open('scraped.json', 'w', encoding="utf-8") as fp:
	json.dump(data, fp, ensure_ascii=False)