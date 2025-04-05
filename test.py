# -*- coding: utf-8 -*-
# @Project : server_STATUS_bot
# @File    : test.py
# @IDE     : PyCharm
# @Author  : lzx9002
# @Time    : 2025/4/5 17:29
import hashlib
import json
import time

import psutil
import requests

def call_bt_status_api():
    api_sk="bu2DutNRkS5yFZTjlPni6sXFVh7LHkWh"
    request_time=str(int(time.time()))
    def md5(s:str):
        return hashlib.md5(s.encode('utf-8')).hexdigest()

    # hashlib.md5((request_time + hashlib.md5(api_sk.encode()).hexdigest()).encode()).hexdigest()
    # request_token = md5(str(request_time)+''+md5(api_sk))
    p_data = {
        # "action": "GetNetWork",
        'request_token': md5(request_time + md5(api_sk)),
        'request_time': request_time
    }
    print(p_data)
    x = requests.post(url="https://hk.yousb.top:8888/system?action=GetNetWork",data=p_data)
    res = x.json()
    return res
print(json.dumps(call_bt_status_api()))
