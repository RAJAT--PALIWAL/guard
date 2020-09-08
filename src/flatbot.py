from pymessenger.bot import Bot


class FlatBot(Bot):

    def __init__(self, *args, **kwargs):
        super(Bot, self).__init__(*args, **kwargs)

    def send_quick_message(self, recipient_id, message, buttons):
        '''Send quick message to the specified recipient.
                https://developers.facebook.com/docs/messenger-platform/send-messages/quick-replies
                Input:
                    recipient_id: recipient id to send to
                    message: message to send
                    buttons: list of buttons
                Output:
                    Response from API as <dict>
                '''
        quick_replies_list = []
        for button in buttons:
            quick_replies_list.append({
                "content_type": "text",
                "title": button,
                "payload": button
            })
        payload = {
            'recipient': {
                'id': recipient_id
            },
            "messaging_type": "RESPONSE",
            'message': {
                'text': message,
                'quick_replies': quick_replies_list
            }
        }
        print(payload)
        return self.send_raw(payload)
