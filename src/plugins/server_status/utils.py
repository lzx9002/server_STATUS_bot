# -*- coding: utf-8 -*-
# @Project : server_STATUS_bot
# @File    : utils.py
# @IDE     : PyCharm
# @Author  : lzx9002
# @Time    : 2025/4/5 14:46
import hashlib
import time

import psutil
from aiohttp import ClientSession

async def call_bt_status_api():
    api_sk="bu2DutNRkS5yFZTjlPni6sXFVh7LHkWh"
    request_time=time.time()
    def md5(s):
        return hashlib.md5(s).hexdigest()
    request_token = md5(request_time)+md5(api_sk)
    async with ClientSession() as session:
        async with session.post("http://159.138.156.179:8888/system?action=GetSystemTotal",json={"request_time": request_time, " request_token": request_token}) as response:
            res = await response.json()
            print(res)
            return res
def get_status():
    return {
        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent,
        "disk": {d.mountpoint: usage
        for d in psutil.disk_partitions()
        if (usage := psutil.disk_usage(d.mountpoint))
                 },
        "swap": psutil.swap_memory().percent,
    }