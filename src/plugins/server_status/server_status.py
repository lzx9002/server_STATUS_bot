# -*- coding: utf-8 -*-
# @Project : server_STATUS_bot
# @File    : server_status.py
# @IDE     : PyCharm
# @Author  : lzx9002
# @Time    : 2025/4/5 14:29
import json

from nonebot.adapters.onebot.v11 import Bot as V11Bot, MessageEvent, PokeNotifyEvent, Event
from nonebot.permission import SUPERUSER
from nonebot.plugin.on import on_message, on_command, on_notice

from src.plugins.server_status.utils import call_bt_status_api, get_status, formatted

status = on_command("状态", aliases={"status"})
status_Poke = on_notice()

@status.handle()
@status_Poke.handle()
async def _(event: MessageEvent | PokeNotifyEvent, bot: V11Bot):
    data =get_status()
    disk = ''
    for key, i in data["disk"].items():
        disk += f"\t{key}:{i}%\n"
    await status.send(f"cpu占用:{data["cpu"]}%\n内存占用:{data["memory"]}%\n虚拟内存:{data["swap"]}%\n磁盘占用:\n{disk}")
    bt_data = call_bt_status_api()
    if bt_data.get('status', True):
        await status.finish(formatted(call_bt_status_api()))
    else:
        await status.finish(bt_data['msg'].encode('utf-8').decode('unicode_escape'))