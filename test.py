# -*- coding: utf-8 -*-
# @Project : server_STATUS_bot
# @File    : test.py
# @IDE     : PyCharm
# @Author  : lzx9002
# @Time    : 2025/4/5 17:29
import hashlib
import time

import psutil
import requests

def call_bt_status_api():
    api_sk="bu2DutNRkS5yFZTjlPni6sXFVh7LHkWh"
    request_time=int(time.time())
    def md5(s:str):
        return hashlib.md5(s.encode()).hexdigest()
    request_token = md5(str(request_time))+md5(api_sk)
    x = requests.post("http://159.138.156.179:8888/system?action=GetSystemTotal",params={"request_time": request_time, " request_token": request_token})
    res = x.text
    return res
print(call_bt_status_api())