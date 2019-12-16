import json
import requests
import time
import base64
import hmac
import hashlib
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
import random


class QCloudSMS(object):
    def __init__(self, appid, appkey):
        self.appid = appid
        self.appkey = appkey
        self.sign = '梁量我的学习展示'

    def make_code(self):
        """
        :return: code 6位随机数
        """
        code = ''
        for item in range(6):
            code += str(random.randint(0, 9))
        return code

    def send_msg(self, phone_num):
        ssender = SmsSingleSender(self.appid, self.appkey)
        try:
            # parms参数类型为list
            rzb = ssender.send_with_param(nationcode=86, phone_number=phone_num, template_id="499312",
                                          params=["123321"], sign="梁量我的学习展示")
            print(rzb)
        except HTTPError as http:
            print("HTTPError", http)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app_id = ""
    app_key = ""

    sendmsg = QCloudSMS(app_id, app_key)
    sendmsg.send_msg("18190800121")



# if __name__ == "__main__":
#
#     secretid = "AKID7B28z3CVxDF2NSvT8fx1pLcswlW3HRAf"
#     secretkey = "f5GDuOL6hKiqjMmzxm7KH1XptkNwHMDp"
#     app_key = "97e597cf421647506e3d03bc96024a5f"
#     sms_verify = SMSVerify(app_id="1400296997", template_id="499312", secretid=secretid,)  #  signature=secretkey
#     sms_verify.send_sms(code="2019", phone_number="+8618190800121", way=2)



