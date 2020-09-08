from flask import Flask, request, render_template
import logging
import os
import config as cf
from src import utils

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = cf.imgs_path


@app.route("/", methods=['GET'])
def get_homepage():
    logo_path = os.path.join(cf.imgs_path, "logo_flatfinder.png")
    return render_template("index.html", logo=logo_path)


@app.route("/message", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return utils.verify_fb_token(token_sent)
    # if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    # Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        response_sent_text = utils.get_message(message['message'].get('text'), recipient_id)

    return "Message Processed"


@app.route("/process_text", methods=["POST"])
def process_text():
    output = request.get_json()
    utils.extract_information(output["query"])
    return "done"


if __name__ == "__main__":
    logging.info('App is running successfully')
    app.run()