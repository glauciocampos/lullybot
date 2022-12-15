import logging
import os
import requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

TOKEN = os.environ.get("TOKEN")
chat_id = os.environ.get("CHAT_ID")
f_file = os.environ.get("F_PATH")
f_path = Path(f_file)

s_file = os.environ.get("S_PATH")
s_path = Path(s_file)

if f_path.is_file():
 print(f'The file {f_file} exists')
else:
 message = os.environ.get("F_MESSAGE_ERR")
 url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
 print(requests.get(url).json())


if s_path.is_file():
        print(f'The file {s_file} exists')
else:
        message = os.environ.get("S_MESSAGE_ERR")
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
        print(requests.get(url).json())
        
