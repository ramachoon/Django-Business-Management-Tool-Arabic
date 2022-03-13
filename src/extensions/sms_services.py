import json

import requests
from django.conf import settings

api_address = settings.SMS_PANEL_SAMPLE_API
phone_number = settings.SMS_PANEL_PHONE_NUMBER
request_header = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}


def send_otp_sms(to, code):
    send_sms_data = {
        'to': to,
        'from': phone_number,
        'text': f'کدتائید: {code} \nگروه فلزکاری برادران عبدی'
    }
    send_sms_req = requests.post(
        url=api_address, data=json.dumps(send_sms_data), headers=request_header
    )
    if send_sms_req.json()['status'] == 'ارسال موفق بود':
        return True
