from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config
from ..server_status import server_status

__plugin_meta__ = PluginMetadata(
    name="server_status",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

