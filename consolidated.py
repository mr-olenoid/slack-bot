from flask import Flask, request, make_response, Response
import os
import json

from slack import WebClient
from slackeventsapi import SlackEventAdapter

# Your app's Slack bot user token
SLACK_BOT_TOKEN = "xoxb-1255022124497-1262254771092-h1QhPerdXBKDgWLdzhvwSQHh"
SLACK_VERIFICATION_TOKEN = "4v91KH2NgfG9QAXcP62wUmzN"
SLACK_SIGNING_SECRET = "0af6322b563ff0e37ab0b6f41975cae2"

slack_client = WebClient(SLACK_BOT_TOKEN)
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events", app)

import coctails

@slack_events_adapter.on("app_mention")
def reaction_added(event_data):
    event = event_data["event"]
    print(event)
    channel = event["channel"]
    text_data = event['text'].split()
    print(text_data)
    if text_data[1] == "how" and text_data[2] == "to":
        drink_name = ' '.join(map(str, text_data[3:]))
        drink_name = drink_name.replace('*', '')
        slack_client.chat_postMessage(channel=channel, blocks=coctails.get_named_cocktail(drink_name), text=drink_name)   
    if text_data[1] == "random" and text_data[2] == "drink":
        slack_client.chat_postMessage(channel=channel, blocks=coctails.get_random_drink(), text="random")   


# Helper for verifying that requests came from Slack
def verify_slack_token(request_token):
    if SLACK_VERIFICATION_TOKEN != request_token:
        print("Error: invalid verification token!")
        print("Received {} but was expecting {}".format(request_token, SLACK_VERIFICATION_TOKEN))
        return make_response("Request contains invalid Slack verification token", 403)


@app.route("/slack/message_options", methods=["POST"])
def message_options():
    # Parse the request payload
    form_json = json.loads(request.form["payload"])

    # Verify that the request came from Slack
    verify_slack_token(form_json["token"])

    # Dictionary of menu options which will be sent as JSON
    menu_options = {
        "options": [
            {
                "text": "Cappuccino",
                "value": "cappuccino"
            },
            {
                "text": "Latte",
                "value": "latte"
            }
        ]
    }

    # Load options dict as JSON and respond to Slack
    return Response(json.dumps(menu_options), mimetype='application/json')


# The endpoint Slack will send the user's menu selection to
@app.route("/slack/message_actions", methods=["POST"])
def message_actions():

    # Parse the request payload
    form_json = json.loads(request.form["payload"])

    # Verify that the request came from Slack
    verify_slack_token(form_json["token"])

    # Check to see what the user's selection was and update the message accordingly
    selection = form_json["actions"][0]["selected_options"][0]["value"]

    if selection == "cappuccino":
        message_text = "cappuccino"
    else:
        message_text = "latte"

    response = slack_client.chat_update(
      channel=form_json["channel"]["id"],
      ts=form_json["message_ts"],
      text="One {}, right coming up! :coffee:".format(message_text),
      attachments=[] # empty `attachments` to clear the existing massage attachments
    )

    # Send an HTTP 200 response with empty body so Slack knows we're done here
    return make_response("", 200)

# Send a Slack message on load. This needs to be _before_ the Flask server is started

# A Dictionary of message attachment options
attachments_json = [
    {
        "fallback": "Upgrade your Slack client to use messages like these.",
        "color": "#3AA3E3",
        "attachment_type": "default",
        "callback_id": "menu_options_2319",
        "actions": [
            {
                "name": "bev_list",
                "text": "Pick a beverage...",
                "type": "select",
                "data_source": "external"
            }
        ]
    }
]

# Send a message with the above attachment, asking the user if they want coffee
#slack_client.chat_postMessage(
#  channel="#general",
#  text="Would you like some coffee? :coffee:",
#  attachments=attachments_json
#)

# Start the Flask server
if __name__ == "__main__":
    app.run(ssl_context=('cert.pem', 'key.pem'), host='0.0.0.0', port=443)
