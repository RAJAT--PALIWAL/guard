import os
import random
import logging
import re
from flask import request

import random
from pymessenger.bot import Bot

import config as cf
from src.flatbot import FlatBot
from src import db_utils


bot = Bot(cf.ACCESS_TOKEN_MESSENGER)
fbot = FlatBot(cf.ACCESS_TOKEN_MESSENGER)
rx_num = re.compile(r"^\d{4}\s")
building_list = ["A", "B", "C", "D"]
flat_list = ["101", "102", "103", "201", "202", "203", "301", "302", "304"]


def verify_fb_token(token_sent):
    # take token sent by facebook and verify it matches the verify token you sent
    # if they match, allow the request, else return an error
    if token_sent == cf.VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


def get_message(text, idx):
    logging.info('Received NLP object for the request.')
    result = "Sorry! We are unable to answer to you right now. Please try again after some time."
    button_list = []
    try:
        if text.lower() == "display entries":
            result = db_utils.get_data(data=[idx, "0"])
            send_message(idx, result)
            pass
        elif text.lower() == "new entry":
            button_list.extend(building_list)
            fbot.send_quick_message(recipient_id=idx, message="Select Building", buttons=button_list)
        elif text in building_list:
            button_list.extend(flat_list)
            fbot.send_quick_message(recipient_id=idx, message="Select Flat", buttons=button_list)
        elif text.lower() in flat_list:
            number = random.randint(1111, 9999)
            bot.send_text_message(recipient_id=idx, message="Your OTP is: "+str(number)+". Please type <OTP>+<space>+visitor name to create entry.")
            db_utils.insert_data(data=[idx, str(number), "0"])
        elif check_otp(text) is not None:
            sid = db_utils.get_otp(data=[check_otp(text), "0"])
            OTP, name = get_otp_name(text)
            print(type(name), "0", type(sid[0]), type(OTP))
            db_utils.update_data(data=[name, "0", sid[0], OTP])
            fbot.send_quick_message(recipient_id=idx, message="Entry has been created", buttons=["Display Entries"])
        else:
            button_list.extend(["New Entry", "Display Entries"])
            fbot.send_quick_message(recipient_id=idx, message="What would you like to do", buttons=button_list)
    except Exception as error:
        print(str(error))
    return result


def check_otp(text):
    match = re.match(rx_num, text)
    if match is not None:
        return match[0].strip()
    else:
        return None


def get_otp_name(text):
    match = re.match(rx_num, text)
    if match is not None:
        return match[0].strip(), text.replace(match[0], "").strip()
    else:
        return None, None


# uses PyMessenger to send response to user
def send_message(recipient_id, response, buttons=None):
    if type(response) == list:
        for val in response:
            bot.send_text_message(recipient_id, str(val[0])+","+str(val[1]))
    # sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"


if __name__ == "__main__":
    print(get_otp_name("123456 RAJAT"))