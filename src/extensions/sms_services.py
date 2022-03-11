import json

import requests
from django.conf import settings

username = settings.SMS_PANEL_USERNAME
password = settings.SMS_PANEL_PASSWORD
phone_number = settings.SMS_PANEL_PHONE_NUMBER
send_sms_url = 'https://rest.payamak-panel.com/api/SendSMS/SendSMS'
deliveries_sms_url = 'https://rest.payamak-panel.com/api/SendSMS/GetDeliveries2'
request_header = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}


def send_otp_sms(to, code):
    send_sms_data = {
        'username': username,
        'password': password,
        'to': to,
        'from': phone_number,
        'text': f'کدتائید: {code} \nگروه فلزکاری برادران عبدی'
    }
    send_sms_req = requests.post(
        url=send_sms_url, data=json.dumps(send_sms_data), headers=request_header
    )
    ret_status = send_sms_req.json()['RetStatus']
    str_ret_status = send_sms_req.json()['StrRetStatus']
    if ret_status == 1 and str_ret_status == "Ok":
        return True
    else:
        return False
