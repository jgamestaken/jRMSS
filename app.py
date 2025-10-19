

# jgamestaken ready-to-use mail sending service - jRMSS

##
# Quick Doc
##

## HOW TO SEND MAIL
# * Required option
# 1. Send a request as a JSON - {to*=str, subject*=str, content*=[{data=str, type="html" OR "text"},...}} @ port 7979(or self-defined)
# 2. Mail will be sent internally

## HOW TO EDIT VARIABLES
# 1. Don't edit things here, go into .env and edit the values there

## CHECK GITHUB FOR MORE DOCUMENTATION

##
# Module start
##

from fastapi import FastAPI, Request # Import the API service

import smtplib, ssl # Import required mail (and mail formatting) services
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv # Import dotenv and os to read environment values
import os

load_dotenv() # Load the dotenv file

# Get dotenv variables

EMAIL_SERVER = os.getenv("EMAIL_SERVER")
EMAIL_PORT = int(os.getenv("EMAIL_PORT")) # INT IS REQUIRED
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

API_IP = os.getenv("API_IP") # This probably should be 127.0.0.1
API_PORT = int(os.getenv("API_PORT")) # INT IS REQUIRED

##
# Mail class
##

class Mail():
	def __init__(self, json):
		# Initialize the MAIL class

		self.mail_deliverable = True # Indicator to show whether the mail is deliverable, default is True but changes if there's an issue.
		self.mail_delivery_status = "Delivered normally" # String to send back to the requesting client showing whether the mail was delivered correctly.

		 # Copy the values given into self
		self.json = json

		self._prepare_mail() # Prepare the email.

	def _get_json_property(self, property, required=False, default=""):
		# Check a json property in self.json and validate it

		if property in self.json: # If the property is there, return it
			return self.json[property]
		elif not required: # If it's not, but it's not required, return the default
			return default
		else: # If it's not, and it's required, stop the mail delivery, return the default so nothing breaks
			self.mail_deliverable = False
			self.mail_delivery_status = f"Couldn't deliver, critical variable ${str(property)} wasn't provided or valid"
			return default

	def _prepare_mail(self):
		# Prepare an email for sending

		self.mail = MIMEMultipart("alternative") # Create the multipart message.

		self.mail["From"] = EMAIL_ADDRESS # Set the sender to the sending email address

		self.mail["To"] = self._get_json_property("to", required=True) # Set the json-set variables aswell
		self.mail["Subject"] = self._get_json_property("subject", required=False)

		# From here, set the contents of the email
		# Notes:
		# - The list gets reversed so that the content still shows in the correct order(mime will show the last-added message first)
		# - If one item attachment failes the entire mail fails, until a better solution is met.

		content = self._get_json_property("content", required=True, default=[]) # Get the variables
		content.reverse() # Reverse the content

		for item in content: # Go through all content
			try:
				content = MIMEText(item["data"], item["type"]) # Create the element with the correct type and attach it
				self.mail.attach(content)
			except Exception as error: # If something goes wrong, do not deliver the mail and notify user.
				self.mail_deliverable = False
				self.mail_delivery_status = f"Couldn't deliver, content attachment failed - ${error}"

		# Mail is ready, tada!!

	def send_mail(self):
		# Send the email, to be ran manually

		if self.mail_deliverable: # Check if the mail can be delivered
			try:
				ssl_context = ssl.create_default_context() # Create an SSL context for a secure connection

				with smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT) as server: # Connect with the smtp server
					server.ehlo()
					server.starttls(context=ssl_context) # Start the SSL/TLS context
					server.login(EMAIL_ADDRESS, EMAIL_PASSWORD) # Log into the server with the sender email address
					server.ehlo()
					server.sendmail(EMAIL_ADDRESS, self._get_json_property("to", required=True), self.mail.as_string()) # Send mail

			except Exception as error: # If an error occurs, notify the user
				self.mail_deliverable = False
				self.mail_delivery_status = f"Couldn't deliver, mail sending failed - ${error}"

		return self.mail_deliverable, self.mail_delivery_status # Relay information to the user

##
# API Section
##

app = FastAPI( # Start the API
	docs_url=None, # Disable all docs
	redoc_url=None,
	openapi_url=None
)

@app.post("/")
async def send_an_email(request: Request):
#	try:
	info = await request.json() # Convert the request into a json
	mail_object = Mail(info) # Create the Mail object that formats the mail correctly

	success, status = mail_object.send_mail()

#	except Exception as error: # If it fails, set the success to false and reset the status.
#		success = False
#		status = f"Couldn't deliver, Mail object failure - ${error}"

	return {"sent": success, "message": status}

##
# Execute App Section
##

if __name__ == "__main__":
	import uvicorn

	uvicorn.run("app:app", host=API_IP, port=API_PORT, reload=True)
