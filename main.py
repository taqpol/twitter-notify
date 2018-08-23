from flask import Flask, request
from twilio.rest import Client
import os
import re
import requests
import json
import ast

app = Flask(__name__)

@app.route('/', methods=['POST'])
def main():
	tweet = parse_post_data(request.data)
	if tweet:
		send_text(tweet)
	return app.make_response('')


def send_text(link):
	account_sid = os.environ.get('account_sid')
	auth_token  = os.environ.get('auth_token')

	client = Client(account_sid, auth_token)

	message = client.messages.create(
	    to=os.environ.get('receiving_number'), 
	    from_=os.environ.get('sending_number'),
	    body=link)


def parse_post_data(post_data):
	tweet_data = json.loads(post_data.decode(), strict=False)
	tweet_url = tweet_data['tweet_link']
	tweet_body = tweet_data['tweet_body']
	if not re.search('https:\/\/twitter.com\/vainglory\/\S*', tweet_url):
		return
	r = requests.get(tweet_url)
	stream_links = re.findall('twitch.tv\/\S*', r.text)
	if stream_links or os.environ.get('keywords') in tweet_body.lower():
		if ast.literal_eval(os.environ.get('blacklist')) in stream_links:
			return
		else:
			return tweet_body


if __name__ == '__main__':
	app.run()