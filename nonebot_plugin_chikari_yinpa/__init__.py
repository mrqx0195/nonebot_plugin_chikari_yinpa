from nonebot import require,on_command
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.permission import SUPERUSER
require("nonebot_plugin_localstore")

from nonebot.plugin import PluginMetadata

from .config import Config
from .handles import yinpa_Handles

__plugin_meta__ = PluginMetadata(
    name="Chikari_yinpa",
    description="一个普通的银趴插件",
    usage="",
    config=Config,
    type="application",
    homepage="https://github.com/mrqx0195/nonebot_plugin_chikari_yinpa",
    supported_adapters={"~onebot.v11"}
)

__version__ = "1.2.8"

on_yinpa_control = on_command(
    "yinpa_control",
    aliases={"银趴控制"},
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
    priority=10,
    block=False,
    handlers=[yinpa_Handles.module_enable]
)

on_sign_in = on_command(
    "sign_in",
    aliases={"签到","打卡"},
    priority=10,
    block=False,
    handlers=[yinpa_Handles.sign_in]
)

on_info = on_command(
    "info",
    aliases={"信息","查询"},
    priority=10,
    block=False,
    handlers=[yinpa_Handles.yinpa_info]
)

on_yinpa_help = on_command(
    "yinpa_help",
    aliases={"银趴帮助"},
    priority=10,
    block=False,
    handlers=[yinpa_Handles.yinpa_help]
)

on_yinpa_join = on_command(
    "yinpa_join",
    aliases={"加入银趴"},
    priority=10,
    block=False,
    handlers=[yinpa_Handles.yinpa_join]
)

on_yinpa_leave = on_command(
    "yinpa_leave",
    aliases={"离开银趴"},
    priority=10,
    block=False,
    handlers=[yinpa_Handles.yinpa_leave]
)

on_yinpa_attack_tou = on_command(
    "tou",
    aliases={"透","插入"},
    priority=10,
    block=False,
    handlers=[yinpa_Handles.yinpa_tou]
)

on_yinpa_attack_zha = on_command(
    "zha",
    aliases={"榨","榨精"},
    priority=10,
    block=False,
    handlers=[yinpa_Handles.yinpa_zha]
)

on_yinpa_attack_chong = on_command(
    "chong",
    aliases={"冲","打胶","手冲","撸","导"},
    priority=10,
    block=False,
    handlers=[yinpa_Handles.yinpa_chong]
)

on_yinpa_attack_kou = on_command(
    "kou",
    aliases={"扣","扣扣","自慰","紫薇"},
    priority=10,
    block=False,
    handlers=[yinpa_Handles.yinpa_kou]
)

on_yinpa_shop = on_command(
    "shop",
    aliases={"商店","买","买东西","店"},
    priority=10,
    block=False,
    handlers=[yinpa_Handles.yinpa_shop]
)

on_yinpa_work = on_command(
    "work",
    aliases={"工作","打工"},
    priority=10,
    block=False,
    handlers=[yinpa_Handles.yinpa_work]
)

# on_test = on_command(
#     "test",
#     permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
#     priority=10,
#     block=False,
#     handlers=[yinpa_Handles.test]
# )

