from flask import Flask, request, Response
import os
from flask_restful import Resource, Api
import json

app = Flask(__name__)
api = Api(app)

class Locations(Resource):
    def get(self, type):
        fp = None
        if type == "apartment_rent":
            fp = open('apartment_rent_locations.json', encoding="utf8")
        elif type == "apartment_buy":
            fp = open('apartment_buy_locations.json', encoding="utf8")
        elif type == "room_rent":
            fp = open('room_rent_locations.json', encoding="utf8")
        data = json.load(fp)
        locations = []
        for provinces in data.keys():
            for cities in data[provinces].keys():
                locations.append(cities + ", " + provinces)
        return locations
        

api.add_resource(Locations, '/location/<type>')

if __name__ == '__main__':
     app.run(host="0.0.0.0", port=5000)