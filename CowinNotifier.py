# import required module
import requests
import json
import time
from cowin_api import CoWinAPI


def getAvailability(PINCODE, DATE, AGE=18):
    cowin = CoWinAPI()
    available_centers = cowin.get_availability_by_pincode(PINCODE, DATE, AGE)
    # filtered = filter(lambda k: k['center_id'] == "604866",available_centers['centers'])
    av_2 = []
    for i in available_centers['centers']:
        try:
            if i['sessions'][0]['available_capacity'] > 0:
                av_2.append(i)
        except:
            pass
    return av_2
    # return filtered


def sendMessage(PIN, DATE, AVAILABILITY):
    text = f'Alert guys!!\n Covaxin {AVAILABILITY} slots available at Pin:{PIN},\nLink: https://selfregistration.cowin.gov.in/ '
    URL = "https://www.fast2sms.com/dev/bulk"
    # create a dictionary
    my_data = {
        'sender_id': 'FSTSMS',
        'message': text,
        'language': 'english',
        'route': 'p',
        # You can send sms to multiple numbers
        # # separated by comma.
        'numbers': '9932562754,9932581232,8942052445,8431904356'
    }
    # create a dictionary
    headers = {
        'authorization': 'XptUabyTPQFJrSxCdLGkVHvIeMgnY4sR5lwzhNWB2O6D03imo1dZci9zqhgEk7CbmyUrAx1vnuLIF6Mp',
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache"
    }
    response = requests.request("POST", URL, data=my_data, headers=headers)
    # load json data from source
    returned_msg = json.loads(response.text)
    # print the send message
    print(returned_msg['message'])


while True:
    try:
        pin = "560020"
        date = "23-05-2021"
        response = getAvailability(pin, date)
        availability = len(response)
        if availability > 0:
            sendMessage(pin, date, availability)
            print("message sent")
            print(availability)
            time.sleep(7)

    except Exception as e:
        print("error in the while loop!")
        print(str(e))
    finally:
        print("script is runnning")
        time.sleep(2)
