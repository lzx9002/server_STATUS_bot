# -*- coding: utf-8 -*-
# @Project : server_STATUS_bot
# @File    : server_status.py
# @IDE     : PyCharm
# @Author  : lzx9002
# @Time    : 2025/4/5 14:29
import json

from nonebot.adapters.onebot.v11 import Bot as V11Bot, MessageEvent, PokeNotifyEvent
from nonebot.permission import SUPERUSER
from nonebot.plugin.on import on_message, on_command, on_notice
from nonebot.rule import to_me

from src.plugins.server_status.utils import call_bt_status_api, get_status

status = on_command("状态", aliases={"status"}, rule=to_me())

@status.handle()
async def _(event: MessageEvent, bot: V11Bot):
    data =get_status()
    await status.finish(f"{json.dumps(data)}")