from flask import Flask, request
from twilio.rest import Client
import json
import os
import re

app = Flask(__name__)

@app.route('/', methods=['POST'])
def main():
	twitch_link = parse_post_data(request.data)
	print(twitch_link)
	if twitch_link:
		send_text(twitch_link)
	return app.make_response('')


def send_text(link):
	account_sid = os.environ.get('account_sid')
	auth_token  = os.environ.get('auth_token')

	client = Client(account_sid, auth_token)

	message = client.messages.create(
	    to=os.environ.get('receiving_number'), 
	    from_=os.environ.get('sending_number'),
	    body=tweet_body_string)


def parse_post_data(post_data):
	tweet_body_string = post_data.decode()
	match_obj = re.findall('twitch.tv\/\S*', tweet_body_string)
	print(match_obj)

	if match_obj:
		if ['twitch.tv/vainglory', 'twitch.tv/excoundrel', 'twitch.tv/qlash_eng'] in match_obj:
			return
		else:
			return tweet_body_string


if __name__ == '__main__':
	app.run()