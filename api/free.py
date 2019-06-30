import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

	html = """<html><body><h1>Hello</h1></body></html>"""

	message = MIMEMultipart("alternative")
	message["Subject"] = "Hello"
	message["From"] = sender_email
	message["To"] = "sanzerinf@gmail.com"
	part1 = MIMEText(html, "html")
	message.attach(part1)
	server.sendmail(sender_email, "sanzerinf@gmail.com", message.as_string())
except: 
	pass