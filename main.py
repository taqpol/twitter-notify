from flask import Flask, request
from twilio.rest import Client
import os
import re
import requests
import json
import ast
import traceback

app = Flask(__name__)

@app.route('/', methods=['POST'])
def main():
	try:
		tweet = parse_post_data(request.data)
	except:
		send_text(traceback.format_exc())
		return app.make_response('')
	else:
		if tweet:
			send_text(tweet)
		return app.make_response('')


def send_text(text_body):
	account_sid = os.environ.get('account_sid')
	auth_token  = os.environ.get('auth_token')

	client = Client(account_sid, auth_token)

	message = client.messages.create(
	    to=os.environ.get('receiving_number'), 
	    from_=os.environ.get('sending_number'),
	    body=text_body)


def parse_post_data(post_data):
	tweet_url, tweet_body = post_data.replace(b'"', b'').replace(b"'", b'').decode().split(' ', 1)
	if not re.match('http:\/\/twitter.com\/vainglory\/\S*', tweet_url) or re.match('RT @\S*', tweet_body) or re.match('@\S*', tweet_body):
		return
	r = requests.get(tweet_url)
	stream_links = re.findall('twitch.tv\/\S*', r.text)
	if stream_links or check_keywords(tweet_body.lower()):
		if ast.literal_eval(os.environ.get('blacklist')) in stream_links:
			return
		else:
			return tweet_body

def check_keywords(tweet_text):
	for keyword in ast.literal_eval(os.environ.get('keywords')):
		if keyword.lower() in tweet_text:
			return True
	else:
		return False

if __name__ == '__main__':
	app.run(threaded=True)

