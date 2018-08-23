from flask import Flask, request
from twilio.rest import Client
import os
import re
import requests
import json

app = Flask(__name__)

@app.route('/', methods=['POST'])
def main():
	import pdb; pdb.set_trace()
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
	tweet_data = json.loads(post_data.decode())
	tweet_url = tweet_data['tweet_link']
	tweet_body = tweet_data['tweet_body']
	if not re.search('https:\/\/twitter.com\/vainglory\/\S*', tweet_url):
		return
	r = requests.get(tweet_url)
	match_obj = re.findall('twitch.tv\/\S*', r.text)
	if match_obj:
		if ['twitch.tv/vainglory', 'twitch.tv/excoundrel', 'twitch.tv/qlash_eng'] in match_obj:
			return
		else:
			return tweet_body


if __name__ == '__main__':
	app.run()