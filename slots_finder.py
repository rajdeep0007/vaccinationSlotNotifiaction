import json
import time
import requests
from datetime import datetime
from playsound import playsound
import schedule

# PLEASE CHANGE THE DATE HERE
monday_date = '17-05-2021'
#PLEASE ADD THE RESPECTIVE PIN CODE
pin_codes = ['831001']


def find_slots():
    """Hit API and find the slots, If available Play Alarm - """
    print(f'Running at time: {datetime.now()}', end=' ')
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    for pin_code in pin_codes:
        response = requests.get(
            f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pin_code}&date={monday_date}',
            headers=headers)
        data = json.loads(response.text)
        centers = data.get('centers', [])
        print(centers)
        if len(centers):
            centers_age_18 = [center for center in centers for session in center.get('sessions', []) if
                              session.get('min_age_limit') == 18 and
                              session.get('available_capacity', 0)]
            if len(centers_age_18):
                print('Slots Available for 18+' )
                playsound('Alert Ringtone.mp3')
            else:
                print('No Slots Available for 18+')
        else:
            print('No Slots Available')


schedule.every(10).seconds.do(find_slots)

while True:
    schedule.run_pending()
    time.sleep(1)
