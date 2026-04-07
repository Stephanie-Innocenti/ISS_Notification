#twilio 
#pythonanywhere
#open notify 

import requests
import datetime
import time
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
import notified_numbers as Notified_Numbers

# Bologne
MY_LATITUDE = 44.494190
MY_LONGITUDE = 11.346520

def iss_close_to_yoy():
    
    response = requests.get(url= "http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_lat = float(data['iss_position']['latitude'])
    iss_lon = float(data['iss_position']['longitude'])

    if MY_LATITUDE  - 3 < iss_lat < MY_LATITUDE + 3 and MY_LONGITUDE - 3 < iss_lon < MY_LONGITUDE + 3:
        return True 
    
def hours_check():
        
    if datetime.datetime.now().hour in range(21,25):
        return True

while True:
    if iss_close_to_yoy() and hours_check():
        time.sleep(60)
        proxy_client = TwilioHttpClient()
        proxy_client.session.proxies = {'https':os.environ['https_proxy']}
        client = Client(account_sid, auth_token,http_client=proxy_client)
        message = client.messages.create(
            body="The ISS station are passing now above you!",
            from_=Notified_Numbers.MESSAGE_FROM,
            to=Notified_Numbers.MESSAGE_RECEIVED,
        )