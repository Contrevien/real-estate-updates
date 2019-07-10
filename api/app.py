from flask import Flask, request, Response
import os
from flask_restful import Resource, Api
import json
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import hmac
import hashlib
import binascii

app = Flask(__name__)
api = Api(app)
cur_path = os.path.dirname(__file__)
key = "e179017a62b049968a38e91aa9f1"
key = binascii.unhexlify(key)

def hello(params):
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "therealestatebotgermany@gmail.com"
    password = "dontplease"
    fp = open("env.json")
    url = json.load(fp)["url"]

    # Create a secure SSL context
    context = ssl.create_default_context()

    try:
        # Try to log in to server and send email
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)

        email = params["email"].encode()
        encrypted = hmac.new(key, email, hashlib.sha256).hexdigest().lower()
            
        html = """
            <html>
            <head>
                <link
                href="https://fonts.googleapis.com/css?family=Montserrat:400,800&display=swap"
                rel="stylesheet"
                />
            </head>
            <style>
                body {
                text-align: center;
                font-family: "Montserrat";
                }
                h1 {
                font-weight: bolder;
                margin-top: 5%;
                }
                #goodslist {
                    display: flex;
                    align-items: center;
                    width: 100%;
                    flex-direction: column;
                }
                #goodslist a {
                    color: #555;
                }
                .showbox {
                    width: 90%;
                    min-height: 300px;
                    margin: 20px;
                    text-align: left;
                }
                .showbox ul {
                    list-style: none;
                }
                .showbox p {
                    font-weight: bold;
                    color: rgba(255, 0, 0, 0.8);
                }
                .showbox span {
                    font-weight: bold;
                    color: #555;
                }

                
            </style>
            <body>
                <h1>Hello, we hope to help you find your next property!</h1>
                <div id="goodslist">
                    <div class="showbox">
                        <p>Thank you for subscribing to our service; Here are the preferences you have chosen</p>
                        <ul>
                            <li><span>Location: </span>""" + params["location"] + """</li>
                            <li><span>Max Price: </span>""" + params["max_price"] + """</li>
                            <li><span>Rooms: </span>""" + params["rooms"] + """</li>
                            <li><span>Category: </span>""" + params["type"] + """</li>
                        </ul>
                        <p>You will receive a mail if a new property shows up for your preferences</p>
                    </div>
                    <a href='""" + url + """unsubscribe/""" + encrypted +  """'>Unsubscribe</a>
                </div>
            </body>
            </html>

        """


        message = MIMEMultipart("alternative")
        message["Subject"] = "Hello"
        message["From"] = sender_email
        message["To"] = params["email"]
        part1 = MIMEText(html, "html")
        message.attach(part1)
        server.sendmail(sender_email, params["email"], message.as_string())
        return 1

    except:
        return -1

class Locations(Resource):
    def get(self, type):
        fp = None
        try:
            if type == "apartment_rent":
                fp = open('apartment_rent_locations.json', encoding="utf8")
            elif type == "apartment_buy":
                fp = open('apartment_buy_locations.json', encoding="utf8")
            elif type == "room_rent":
                fp = open('room_rent_locations.json', encoding="utf8")
        except:
            return "Not found"
        data = json.load(fp)
        locations = []
        for provinces in data.keys():
            for cities in data[provinces].keys():
                locations.append(cities + ", " + provinces)
        return locations

class Add(Resource):
    def post(self):
        data = request.get_json()
        try:
            fp = open("users.json", encoding="utf8")
            users = json.load(fp)

            if data["email"] in users.keys() and data["email"]["subscription"] == "U":
                return "666"
            
            temp = {}
            temp["location"] = data["location"]
            temp["rooms"] = data["rooms"]
            if data["max_price"] == "":
                temp["max_price"] = "99999999"
            else:
                temp["max_price"] = data["max_price"]
            temp["type"] = [data["type"]]

            users[data["email"]] = {}
            users[data["email"]]["parameters"] = temp
            users[data["email"]]["subscription"] = "S"

            params = data
            if params["max_price"] == "":
                params["max_price"] = "None"
            
            if params["rooms"].split()[0] == "rooms":
                params["rooms"] = "None"

            if hello(params) == -1:
                return "777"
            
            with open("users.json", "w", encoding="utf8") as f:
                json.dump(users, f, ensure_ascii=False)

            return "1"
             
        except:
            return "777"

class Remove(Resource):
    def post(self):
        try:     
            data = request.get_json()           
            file_path = os.path.relpath("users.json")
            fp = open(file_path, encoding="utf8")
            users = json.load(fp)

            found = -1
            for user in users.keys():
                m = user.encode()
                c = hmac.new(key, m, hashlib.sha256).hexdigest().lower()
                if c == data["email"]:
                    found = user
                    break

            if found == -1 or users[found]["subscription"] == "U":
                return "666"
            
            users[found]["subscription"] = "U"

            with open(file_path, "w", encoding="utf8") as f:
                json.dump(users, f, ensure_ascii=False)
            return "1"
        except:
            return "777"


api.add_resource(Locations, '/location/<type>')
api.add_resource(Add, '/add')
api.add_resource(Remove, '/unsubscribe')

if __name__ == '__main__':
     app.run(host="0.0.0.0", port=5000)