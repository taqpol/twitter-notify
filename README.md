# twitter-notify

notifies via sms when certain twitch streams come online by monitoring the vainglory twitter account via IFTTT webhooks

written with flask and twilio, running on gunicorn, deployed on heroku, and listening to twitter via IFTTT.

## instructions for spinning up your own instance:

* clone and deploy via heroku and add the following environment vars: 
  * sending_number (your twilio number)
  * receiving_number (the number that you want to receive text messages)
  * account_sid (your twilio sid)
  * auth_token (your twilio auth token)
  * keywords: use the following structure: \["keyword1", "keyword2"...\]. leave as an empty list if you don't plan on further filtering by keyword.
  * blacklist: use the following structure: \["blacklisted_twitch_stream_link1", "blacklisted_twitch_stream_link2"...\]. leave as an empty list if you want to be notified of all twitch streams.

* set up IFTTT trigger with maker webhooks to respond to the vainglory twitter and send a request to your heroku application

* use the following options when setting up the trigger: 
  * username to watch: vainglory
  * method: POST
  * content type: application/json
  * body: {{LinkToTweet}} {{Text}}
