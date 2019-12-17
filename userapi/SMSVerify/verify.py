import json
import requests
import time
import base64
import hmac
import hashlib
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
import random
from .sms_config import *


class QCloudSMS(object):
    def __init__(self, appid=app_sdk_id, appkey=app_key):
        self.appid = appid
        self.appkey = appkey
        self.sign = '梁量我的学习展示'


    def send_msg(self, phone_num, verify_data):
        ssender = SmsSingleSender(self.appid, self.appkey)
        try:
            # parms参数类型为list
            rzb = ssender.send_with_param(nationcode=86, phone_number=phone_num, template_id=template_id,
                                          params=[verify_data], sign="梁量我的学习展示")
            print(rzb)
            return rzb
        except HTTPError as http:
            print("HTTPError", http)
        except Exception as e:
            print(e)



# if __name__ == '__main__':
#
#     sendmsg = QCloudSMS(app_sdk_id, app_key)
#     sendmsg.send_msg("18190800121")

