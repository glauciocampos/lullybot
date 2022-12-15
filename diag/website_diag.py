import logging
import os
import requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# site to check
site = os.environ.get("P_SERVICE")
p_token = os.environ.get("P_TOKEN")
chat_id = os.environ.get("CHAT_ID")
bot_token = os.environ.get("TOKEN")
url = f"{site}{p_token}"

try:
    # check if the site is up
    r = requests.get(url)
    # if the status code is 200, then the site is up
   
    if r.status_code == 200:
        # message to send
        message = os.environ.get("WEB_MESSAGE_OK")
        print(f"{message}")        
    else:
        # send message
        message = os.environ.get("WEB_MESSAGE_ERR")
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}"
        print(requests.get(url).json())

except Exception as e:
        print(e)


