from flask import Flask, request
from twilio.rest import Client
import json
import os

app = Flask(__name__)

@app.route('/', methods=['POST'])
def main():
	return request.data
	# parse_post_data(request.data)

def send_text():
	account_sid = os.environ.get('account_sid')
	auth_token  = os.environ.get('auth_token')

	client = Client(account_sid, auth_token)

	message = client.messages.create(
	    to=os.environ.get('receiving_number'), 
	    from_=os.environ.get('sending_number'),
	    body="Hello from Python!")

	print(message.sid)

def parse_post_data(post_data):
	print(post_data)

if __name__ == '__main__':
	app.run()