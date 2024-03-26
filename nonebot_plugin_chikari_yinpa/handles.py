from nonebot.adapters.onebot.v11 import GroupMessageEvent,Message,MessageSegment
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot import get_driver,get_plugin_config
from time import time
from hashlib import md5
from math import sqrt

from .data_handles import data,configdata,DHandles
from .config import Config
from .utils import Utils
from .dicts import dicts

plugin_config = get_plugin_config(Config)

class yinpa_Handles():
    """消息处理
    """
    
    async def module_enable(
            matcher: Matcher,event: GroupMessageEvent,args: Message = CommandArg()
    ):
        """处理银趴的开关
        """
        
        command: str = args.extract_plain_text()
        if "enable" in command and not Utils.group_enable_check(event.group_id):
            DHandles.configdata_set("yinpa_enabled_group",configdata["yinpa_enabled_group"] + [event.group_id])
            await matcher.finish("本群银趴已开启")
        elif "disable" in command and Utils.group_enable_check(event.group_id):
            DHandles.group_remove(event.group_id)
            await matcher.finish("本群银趴已禁用")
        else:
            await matcher.finish("错误：参数错误！\n命令：/yinpa_control <enable/disable>")

    async def sign_in(
            matcher: Matcher,event: GroupMessageEvent
    ):
        """处理签到
        """
        
        if not Utils.group_enable_check(event.group_id):
            await matcher.finish("本群银趴已禁用")
        if not Utils.yinpa_user_presence_check(event.get_user_id()):
            await matcher.finish("您还未加入银趴！\ntips：请使用 /yinpa_join 或 /加入银趴 加入银趴")
        uid: str=event.get_user_id()
        if data[uid]["last_sign_in_time"] < (int)(time() / 86400):
            DHandles.data_set(uid,"last_sign_in_time",(int)(time() / 86400))
            d_pl = Utils.dice(100,(int)(data[uid]['penis_length']) ^ 1)
            d_vd = Utils.dice(100,(int)(data[uid]['vagina_depth']) ^ 2)
            d_m = Utils.dice(100,(int)(data[uid]['money']) ^ 3)
            await matcher.send(f"{data[uid]['name']}签到成功\n长度增加：{data[uid]['penis_length']} + (1d100 / 100) = {data[uid]['penis_length']} + ({d_pl} / 100) = {round(data[uid]['penis_length'] + d_pl / 100,2)}\n深度增加：{data[uid]['vagina_depth']} + (1d100 / 100) = {data[uid]['vagina_depth']} + ({d_vd} / 100) = {round(data[uid]['vagina_depth'] + d_vd / 100,2)}\n金钱增加：{data[uid]['money']} + 1d100 = {data[uid]['money']} + {d_m} = {data[uid]['money'] + d_m}\nps：签到于早上8点刷新")
            DHandles.data_set(uid,'penis_length',round(data[uid]['penis_length'] + d_pl / 100,2))
            DHandles.data_set(uid,'vagina_depth',round(data[uid]['vagina_depth'] + d_vd / 100,2))
            DHandles.data_set(uid,'money',data[uid]['money'] + d_m)
            await matcher.finish()
        else:
            await matcher.finish("你今天已经打过卡了呢~\nps：签到于早上8点刷新，别问我为什么")

    async def yinpa_join(
            matcher: Matcher,event: GroupMessageEvent,args: Message = CommandArg()
    ):
        """处理加入银趴
        """
        
        if not Utils.group_enable_check(event.group_id):
            await matcher.finish("本群银趴已禁用，你不准参加银趴！")
        if Utils.yinpa_user_presence_check(event.get_user_id()):
            await matcher.finish("您已加入银趴！\n如果想要重置银趴数据，请使用 /leave_yinpa 或 /离开银趴 离开银趴后再加入")
        uid: str=event.get_user_id()
        command: str = args.extract_plain_text()
        arg_list: list = command.split()
        if not len(arg_list) == 2:
            await matcher.finish("参数错误！\n格式： /yinpa_join <银趴昵称> <银趴种族> \n种族列表参照： /yinpa_help 种族 ")
        if not arg_list[1].isdigit() or (int)(arg_list[1]) <= 0:
            await matcher.finish("参数错误！\n种族应为一个正整数（种族编号）\n种族列表参照： /yinpa_help 种族 ")
        name: str = arg_list[0]
        species: int = (int)(arg_list[1])
        if not dicts.species_dict.get(species):
            await matcher.finish("参数错误！\n不存在指定的种族\n种族列表参照： /yinpa_help 种族 ")
        if Utils.find_user_name(name):
            await matcher.finish("已经有人使用这个昵称了！")
        DHandles.user_add(uid,{
            'name':name,
            'species':species,
            'sex_value':plugin_config.chikari_yinpa_initial_sex_value,
            'penis_length':plugin_config.chikari_yinpa_initial_penis_length,
            'vagina_depth':plugin_config.chikari_yinpa_initial_vagina_depth,
            'strength':dicts.species_initial_ability[species][0][0] + Utils.dice(dicts.species_initial_ability[species][0][1],species ^ 4),
            'constitution':dicts.species_initial_ability[species][1][0] + Utils.dice(dicts.species_initial_ability[species][1][1],species ^ 5),
            'technique':dicts.species_initial_ability[species][2][0] + Utils.dice(dicts.species_initial_ability[species][2][1],species ^ 6),
            'volition':dicts.species_initial_ability[species][3][0] + Utils.dice(dicts.species_initial_ability[species][3][1],species ^ 7),
            'intelligence':dicts.species_initial_ability[species][4][0] + Utils.dice(dicts.species_initial_ability[species][4][1],species ^ 8),
            'charm':dicts.species_initial_ability[species][5][0] + Utils.dice(dicts.species_initial_ability[species][5][1],species ^ 9),
            'money':plugin_config.chikari_yinpa_initial_money,
            'state':[],
            "passive_times":0,
            "active_times":0,
            "last_sign_in_time":0,
            "last_operation_time":0,
            "last_refresh_time":time(),
            "next_work_time":0,
        })
        skill = []
        for i in dicts.species_initial_ability[species][6]:
            skill.append([i,0,1])
        DHandles.data_set(uid,"skill",skill)
        obj = md5("Chikari`s salt".encode("utf-8"))
        obj.update(f"{uid}".encode("utf-8"))
        DHandles.data_set(uid,"md5",obj.hexdigest())
        await matcher.send("成功加入银趴！")
        await matcher.finish(MessageSegment.image(Utils.get_user_info_image(uid)))

    async def yinpa_leave(
            matcher: Matcher,event: GroupMessageEvent,args: Message = CommandArg()
    ):
        """处理离开银趴
        """
        
        if not Utils.group_enable_check(event.group_id):
            await matcher.finish("本群银趴已禁用")
        if not Utils.yinpa_user_presence_check(event.get_user_id()):
            await matcher.finish("您还未加入银趴！\n请使用 /join_yinpa 或 /加入银趴 加入银趴")
        uid: str=event.get_user_id()
        command: str = args.extract_plain_text()
        if not command or not data[uid]["md5"] or command != data[uid]["md5"]:
            obj = md5("Chikari`s salt".encode("utf-8"))
            obj.update(f"{uid}".encode("utf-8"))
            DHandles.data_set(uid,"md5",obj.hexdigest())
            await matcher.finish(f"警告：这将清除你的所有银趴数据！\n请输入 /yinpa_leave {obj.hexdigest()} 以完成操作")
        else:
            name = data[uid]['name']
            DHandles.user_remove(uid)
            await matcher.finish(f"离开银趴成功。\n大家会记住你的，{name}")

    async def yinpa_help(
            matcher: Matcher,args: Message = CommandArg()
    ):
        """处理银趴帮助
        """
        
        command = args.extract_plain_text()
        help_key = command.split()
        if not help_key:
            await matcher.finish(MessageSegment.image(Utils.text_to_image(dicts.yinpa_help_dict[""])))
        if dicts.help_aliases.get(help_key[0]):
            help_key[0] = dicts.help_aliases[help_key[0]]
        if help_key[0] == "all":
            await matcher.finish(MessageSegment.image(Utils.text_to_image("可用帮助：\n" + "\n".join(list(dicts.yinpa_help_dict.keys())))))
        elif help_key[0] == 'species':
            if len(help_key) >= 2 and dicts.species_help.get(help_key[1]):
                await matcher.finish(MessageSegment.image(Utils.text_to_image(dicts.species_help[help_key[1]])))
            elif len(help_key) >= 2 and dicts.species_dict.get(int(help_key[1])):
                await matcher.finish(MessageSegment.image(Utils.text_to_image(dicts.species_help[dicts.species_dict[int(help_key[1])]])))
            else:
                str = ""
                for i in list(dicts.species_dict.keys()):
                    str += f"{i}：{dicts.species_dict[i]}\n"
                await matcher.finish("错误：该种族不存在\n可用种族：\n" + str + "\n输入/yinpa_help species [种族名或种族ID] 以查看种族描述")
        elif help_key[0] == "skill":
            if len(help_key) >= 2 and dicts.skill_help.get(help_key[1]):
                await matcher.finish(MessageSegment.image(Utils.text_to_image(dicts.skill_help[help_key[1]])))
            elif len(help_key) >= 2 and dicts.skill_dict.get(int(help_key[1])):
                await matcher.finish(MessageSegment.image(Utils.text_to_image(dicts.skill_help[dicts.skill_dict[int(help_key[1])]])))
            else:
                str = ""
                for i in list(dicts.skill_dict.keys()):
                    str += f"{i}：{dicts.skill_dict[i]}\n"
                await matcher.finish("错误：该技能不存在\n可用技能：\n" + str + "\n输入/yinpa_help skill [技能名或技能ID] 以查看技能描述")
        elif help_key[0] == 'state':
            if len(help_key) >= 2 and dicts.state_help.get(help_key[1]):
                await matcher.finish(MessageSegment.image(Utils.text_to_image(dicts.state_help[help_key[1]])))
            elif len(help_key) >= 2 and dicts.state_dict.get(int(help_key[1])):
                await matcher.finish(MessageSegment.image(Utils.text_to_image(dicts.state_help[dicts.state_dict[int(help_key[1])]])))
            else:
                str = ""
                for i in list(dicts.state_dict.keys()):
                    str += f"{i}：{dicts.state_dict[i]}\n"
                await matcher.finish("错误：该状态不存在\n可用状态：\n" + str + "\n输入/yinpa_help state [状态名或状态ID] 以查看状态描述")
        elif help_key[0] == "shop":
            if len(help_key) >= 2 and dicts.shop_help.get(help_key[1]):
                await matcher.finish(MessageSegment.image(Utils.text_to_image(dicts.shop_help[help_key[1]])))
            elif len(help_key) >= 2 and dicts.shop_dict.get(int(help_key[1])):
                await matcher.finish(MessageSegment.image(Utils.text_to_image(dicts.shop_help[dicts.shop_dict[int(help_key[1])]])))
            else:
                str = ""
                for i in list(dicts.shop_dict.keys()):
                    str += f"{i}：{dicts.shop_dict[i]} 售价：{dicts.shop_price_dict[i]}\n"
                await matcher.finish("错误：该商品不存在\n可用商品：\n" + str + "\n输入/yinpa_help shop [商品名或商品ID] 以查看商品描述")
        elif help_key[0] == "work":
            if len(help_key) >= 2 and dicts.work_dict.get(help_key[1]):
                await matcher.finish(MessageSegment.image(Utils.text_to_image(dicts.work_help_dict[help_key[1]])))
            elif len(help_key) >= 2 and dicts.work_dict.get(int(help_key[1])):
                await matcher.finish(MessageSegment.image(Utils.text_to_image(dicts.work_help_dict[dicts.work_dict[int(help_key[1])]])))
            else:
                str = ""
                for i in list(dicts.work_dict.keys()):
                    str += f"{i}：{dicts.work_dict[i]}\n"
                await matcher.finish("错误：该工作不存在\n可用工作：\n" + str + "\n输入/yinpa_help work [工作名或工作ID] 以查看工作描述")
        elif dicts.yinpa_help_dict.get(help_key[0]):
            await matcher.finish(MessageSegment.image(Utils.text_to_image(dicts.yinpa_help_dict[help_key[0]])))
        else:
            await matcher.finish(MessageSegment.image(Utils.text_to_image("错误：不存在对应的帮助\n可用帮助：\n" + "\n".join(list(dicts.yinpa_help_dict.keys())))))

    async def yinpa_info(
            matcher: Matcher,event: GroupMessageEvent,args: Message = CommandArg()
    ):
        """处理查询信息
        """
        
        at:list = Utils.get_at(event)
        if not at:
            arg_list = (args.extract_plain_text()).split()
            if arg_list:
                f_uid = None
                for i in arg_list:
                    f_uid = Utils.find_user_name(i)
                    if f_uid:
                        at = [f_uid]
                        break
                if not f_uid:
                    await matcher.finish("错误：未找到目标！")
        else:
            at = [at[0]]
        uid: str = event.get_user_id()
        if not at or at == ['all']:
            if not data.get(uid):
                await matcher.finish("错误：你还没加入银趴！")
            await matcher.finish(MessageSegment.image(Utils.get_user_info_image(uid)))
        else:
            at = at[0]
            if not data.get(at):
                await matcher.finish("错误：目标还没加入银趴！")
            await matcher.finish(MessageSegment.image(Utils.get_user_info_image(at)))

    async def yinpa_tou(
            matcher: Matcher,event: GroupMessageEvent,args: Message = CommandArg()
    ):
        """处理透人
        """
        
        at:list = Utils.get_at(event)
        if not at:
            arg_list = (args.extract_plain_text()).split()
            if arg_list:
                f_uid = None
                for i in arg_list:
                    f_uid = Utils.find_user_name(i)
                    if f_uid:
                        at = f_uid
                        break
                if not f_uid:
                    await matcher.finish("错误：未找到目标！")
            else:
                await matcher.finish("错误：未指定目标！")
        elif at == ['all']:
            await matcher.finish("错误：未指定目标！")
        else:
            at = at[0]
        uid: str = event.get_user_id()
        if not Utils.yinpa_user_presence_check(uid):
            await matcher.finish("您还未加入银趴！\ntips：请使用 /yinpa_join 或 /加入银趴 加入银趴")
        if not Utils.yinpa_user_presence_check(at):
            await matcher.finish("对方还未加入银趴！")
        if uid == at:
            await matcher.finish("你想透自己？请使用 /冲 或 /扣")
        Utils.refresh_data(uid)
        Utils.refresh_data(at)
        oc = Utils.operation_check(uid)
        if oc:
            await matcher.finish(f"错误：操作失败！\n原因：{oc}")
        if Utils.get_state(at,2):
            await matcher.finish(f"错误：操作失败！\n原因：你连昏迷的{data[at]['name']}都不放过吗？")
        pl = (int)(data[uid]['penis_length']) * 4
        if pl >= 80:
            pl = 80 + sqrt(pl - 80)
        atk_u = Utils.get_attack_list(uid,at) + [[pl,f"{data[uid]['name']}：长度",False]]
        str_u = f"{data[at]['name']}受到的伤害：1d50"
        for i in atk_u:
            if i[2]:
                if i[0] > 0:
                    str_u += f" + {int(i[0])}（{i[1]}）"
                elif i[0] < 0:
                    str_u += f" - {-int(i[0])}（{i[1]}）"
            else:
                if i[0] > 0:
                    str_u += f" + 1d{int(i[0])}（{i[1]}）"
                elif i[0] < 0:
                    str_u += f" - 1d{-int(i[0])}（{i[1]}）"
        res_u = Utils.dice(50,uid)
        str_u += f" = {res_u}"
        for i in atk_u:
            if i[2]:
                if i[0] > 0:
                    str_u += f" + {int(i[0])}"
                    res_u += int(i[0])
                elif i[0] < 0:
                    str_u += f" - {int(i[0])}"
                    res_u -= int(i[0])
            else:
                if i[0] > 0:
                    d = Utils.dice(int(i[0]),(int)(uid) ^ int(i[0]) ^ 101)
                    str_u += f" + {d}"
                    res_u += d
                elif i[0] < 0:
                    d = Utils.dice(-int(i[0]),(int)(uid) ^ int(i[0]) ^ 102)
                    str_u += f" - {d}"
                    res_u -= d
        str_u += f" = {res_u}\n"
        if res_u <= 0:
            res_u = 0
            str_u += " = 0"
        vd = (int)(data[at]['vagina_depth']) * 4
        if vd >= 80:
            vd = 80 + sqrt(vd - 80)
        atk_t = Utils.get_attack_list(at,uid) + [[vd,f"{data[at]['name']}：深度",False]]
        str_t = f"{data[uid]['name']}受到的伤害：1d50"
        for i in atk_t:
            if i[2]:
                if i[0] > 0:
                    str_t += f" + {int(i[0])}（{i[1]}）"
                elif i[0] < 0:
                    str_t += f" - {-int(i[0])}（{i[1]}）"
            else:
                if i[0] > 0:
                    str_t += f" + 1d{int(i[0])}（{i[1]}）"
                elif i[0] < 0:
                    str_t += f" - 1d{-int(i[0])}（{i[1]}）"
        res_t = Utils.dice(50,at)
        str_t += f" = {res_t}"
        for i in atk_t:
            if i[2]:
                if i[0] > 0:
                    str_t += f" + {int(i[0])}"
                    res_t += int(i[0])
                elif i[0] < 0:
                    str_t += f" - {int(i[0])}"
                    res_t -= int(i[0])
            else:
                if i[0] > 0:
                    d = Utils.dice(int(i[0]),(int)(at) ^ int(i[0]) ^ 103)
                    str_t += f" + {d}"
                    res_t += d
                elif i[0] < 0:
                    d = Utils.dice(-int(i[0]),(int)(at) ^ int(i[0]) ^ 104)
                    str_t += f" - {d}"
                    res_t -= d
        str_t += f" = {res_t}"
        if res_t <= 0:
            res_t = 0
            str_t += " = 0"
        hp_u = Utils.get_value(uid,"hp")
        hp_t = Utils.get_value(at,"hp")
        hp_str = f"HP： {hp_u[0]} → {hp_u[0] - res_t} "
        if hp_u[1]:
            hp_str += "（体质）"
        hp_str += f" | {hp_t[0]} → {hp_t[0] - res_u} "
        if hp_t[1]:
            hp_str += "（体质）"
        rh_str_u = Utils.reduce_hp(uid,res_t)
        rh_str_t = Utils.reduce_hp(at,res_u)
        DHandles.data_set(uid,"active_times",data[uid]["active_times"] + 1)
        DHandles.data_set(at,"passive_times",data[at]["passive_times"] + 1)
        await matcher.finish(f"{data[uid]['name']}透了{data[at]['name']}\n" + str_t + "\n" + str_u + hp_str +  rh_str_u +  rh_str_t)
        
    async def yinpa_zha(
            matcher: Matcher,event: GroupMessageEvent,args: Message = CommandArg()
    ):
        """处理榨人
        """
        
        at:list = Utils.get_at(event)
        if not at:
            arg_list = (args.extract_plain_text()).split()
            if arg_list:
                f_uid = None
                for i in arg_list:
                    f_uid = Utils.find_user_name(i)
                    if f_uid:
                        at = f_uid
                        break
                if not f_uid:
                    await matcher.finish("错误：未找到目标！")
            else:
                await matcher.finish("错误：未指定目标！")
        elif at == ['all']:
            await matcher.finish("错误：未指定目标！")
        else:
            at = at[0]
        uid: str = event.get_user_id()
        if not Utils.yinpa_user_presence_check(uid):
            await matcher.finish("您还未加入银趴！\ntips：请使用 /yinpa_join 或 /加入银趴 加入银趴")
        if not Utils.yinpa_user_presence_check(at):
            await matcher.finish("对方还未加入银趴！")
        if uid == at:
            await matcher.finish("你想榨自己？请使用 /冲 或 /扣")
        oc = Utils.operation_check(uid)
        Utils.refresh_data(uid)
        Utils.refresh_data(at)
        if oc:
            await matcher.finish(f"错误：操作失败！\n原因：{oc}")
        if Utils.get_state(at,2):
            await matcher.finish(f"错误：操作失败！\n原因：你连昏迷的{data[at]['name']}都不放过吗？")
        vd = (int)(data[uid]['vagina_depth']) * 4
        if vd >= 80:
            vd = 80 + sqrt(vd - 80)
        atk_u = Utils.get_attack_list(uid,at) + [[vd,f"{data[uid]['name']}：深度",False]]
        str_u = f"{data[at]['name']}受到的伤害：1d50"
        for i in atk_u:
            if i[2]:
                if i[0] > 0:
                    str_u += f" + {int(i[0])}（{i[1]}）"
                elif i[0] < 0:
                    str_u += f" - {-int(i[0])}（{i[1]}）"
            else:
                if i[0] > 0:
                    str_u += f" + 1d{int(i[0])}（{i[1]}）"
                elif i[0] < 0:
                    str_u += f" - 1d{-int(i[0])}（{i[1]}）"
        res_u = Utils.dice(50,uid)
        str_u += f" = {res_u}"
        for i in atk_u:
            if i[2]:
                if i[0] > 0:
                    str_u += f" + {int(i[0])}"
                    res_u += int(i[0])
                elif i[0] < 0:
                    str_u += f" - {int(i[0])}"
                    res_u -= int(i[0])
            else:
                if i[0] > 0:
                    d = Utils.dice(int(i[0]),(int)(uid) ^ int(i[0]) ^ 101)
                    str_u += f" + {d}"
                    res_u += d
                elif i[0] < 0:
                    d = Utils.dice(-int(i[0]),(int)(uid) ^ int(i[0]) ^ 102)
                    str_u += f" - {d}"
                    res_u -= d
        str_u += f" = {res_u}\n"
        if res_u <= 0:
            res_u = 0
            str_u += " = 0"
        pl = (int)(data[at]['penis_length']) * 4
        if pl >= 80:
            pl = 80 + sqrt(pl - 80)
        atk_t = Utils.get_attack_list(at,uid) + [[pl,f"{data[at]['name']}：长度",False]]
        str_t = f"{data[uid]['name']}受到的伤害：1d50"
        for i in atk_t:
            if i[2]:
                if i[0] > 0:
                    str_t += f" + {int(i[0])}（{i[1]}）"
                elif i[0] < 0:
                    str_t += f" - {-int(i[0])}（{i[1]}）"
            else:
                if i[0] > 0:
                    str_t += f" + 1d{int(i[0])}（{i[1]}）"
                elif i[0] < 0:
                    str_t += f" - 1d{-int(i[0])}（{i[1]}）"
        res_t = Utils.dice(50,at)
        str_t += f" = {res_t}"
        for i in atk_t:
            if i[2]:
                if i[0] > 0:
                    str_t += f" + {int(i[0])}"
                    res_t += int(i[0])
                elif i[0] < 0:
                    str_t += f" - {int(i[0])}"
                    res_t -= int(i[0])
            else:
                if i[0] > 0:
                    d = Utils.dice(int(i[0]),(int)(at) ^ int(i[0]) ^ 103)
                    str_t += f" + {d}"
                    res_t += d
                elif i[0] < 0:
                    d = Utils.dice(-int(i[0]),(int)(at) ^ int(i[0]) ^ 104)
                    str_t += f" - {d}"
                    res_t -= d
        str_t += f" = {res_t}"
        if res_t <= 0:
            res_t = 0
            str_t += " = 0"
        hp_u = Utils.get_value(uid,"hp")
        hp_t = Utils.get_value(at,"hp")
        hp_str = f"HP： {hp_u[0]} → {hp_u[0] - res_t}"
        if hp_u[1]:
            hp_str += "（体质）"
        hp_str += f" | {hp_t[0]} → {hp_t[0] - res_u}"
        if hp_t[1]:
            hp_str += "（体质）"
        rh_str_u = Utils.reduce_hp(uid,res_t)
        rh_str_t = Utils.reduce_hp(at,res_u)
        DHandles.data_set(uid,"active_times",data[uid]["active_times"] + 1)
        DHandles.data_set(at,"passive_times",data[at]["passive_times"] + 1)
        await matcher.finish(f"{data[uid]['name']}榨了{data[at]['name']}\n" + str_t  + "\n" + str_u + hp_str + rh_str_u + rh_str_t)
        
    async def yinpa_chong(
            matcher: Matcher,event: GroupMessageEvent
    ):
        """处理冲
        """
        
        uid: str = event.get_user_id()
        if not Utils.yinpa_user_presence_check(event.get_user_id()):
            await matcher.finish("您还未加入银趴！\ntips：请使用 /yinpa_join 或 /加入银趴 加入银趴")
        oc = Utils.operation_check(uid)
        if oc:
            await matcher.finish(f"错误：操作失败！\n原因：{oc}")
        Utils.refresh_data(uid)
        d = Utils.dice(100,uid)
        hp = Utils.get_value(uid,"hp")
        pl_str = f"长度： {data[uid]['penis_length']} → {round(data[uid]['penis_length'] + d / 100 - 0.5,2)}"
        DHandles.data_set(uid,'penis_length',round(data[uid]['penis_length'] + d / 100 - 0.5,2))
        hp_str = f"HP： {hp[0]} → {hp[0] - d}"
        rh_str = Utils.reduce_hp(uid,d)
        await matcher.finish(f"{data[uid]['name']}冲了一发\n" + pl_str + "\n" + hp_str + rh_str)
        
    async def yinpa_kou(
            matcher: Matcher,event: GroupMessageEvent
    ):
        """处理扣
        """
        
        uid: str = event.get_user_id()
        if not Utils.yinpa_user_presence_check(event.get_user_id()):
            await matcher.finish("您还未加入银趴！\ntips：请使用 /yinpa_join 或 /加入银趴 加入银趴")
        oc = Utils.operation_check(uid)
        if oc:
            await matcher.finish(f"错误：操作失败！\n原因：{oc}")
        Utils.refresh_data(uid)
        d = Utils.dice(40,uid)
        hp = Utils.get_value(uid,"hp")
        vd_str = f"深度： {data[uid]['vagina_depth']} → {round(data[uid]['vagina_depth'] + d / 100,2)}"
        DHandles.data_set(uid,'vagina_depth',round(data[uid]['vagina_depth'] + d / 100,2))
        hp_str = f"HP： {hp[0]} → {hp[0] - d}"
        rh_str = Utils.reduce_hp(uid,d)
        await matcher.finish(f"{data[uid]['name']}扣了一次\n" + vd_str + "\n" + hp_str + rh_str)

    async def yinpa_shop(
            matcher: Matcher,event: GroupMessageEvent,args: Message = CommandArg()
    ):
        """处理商店
        """
        
        uid = event.get_user_id()
        command = args.extract_plain_text()
        shop_key = command.split()
        if not shop_key:
            str = ""
            for i in list(dicts.shop_dict.keys()):
                str += f"{i}：{dicts.shop_dict[i]} 售价：{dicts.shop_price_dict[i]}\n"
            await matcher.finish("可用商品：\n" + str + "\n输入/yinpa_help shop [商品名或商品ID] 以查看商品描述")
        else:
            goods = shop_key
            price = 0
            for i in goods:
                if not dicts.shop_dict.get(i) and not dicts.shop_help.get(i) and not dicts.shop_dict.get(int(i)):
                    str = ""
                    for j in list(dicts.shop_dict.keys()):
                        str += f"{j}：{dicts.shop_dict[j]} 售价：{dicts.shop_price_dict[j]}\n"
                    await matcher.finish("错误：该商品不存在\n可用商品：\n" + str + "\n输入/yinpa_help shop [商品名或商品ID] 以查看商品描述")
                if i in list(dicts.shop_dict.values()):
                    i = (list(dicts.shop_dict.keys()))[(list(dicts.shop_dict.values())).index(i)]
                i = int(i)
                price += dicts.shop_price_dict[i]
            if data[uid]['money'] < price:
                await matcher.finish(f"错误：你的金钱并不够买这些商品！\n这些商品的总售价：{price}\n你的金钱：{data[uid]['money']}")
            DHandles.data_set(uid,'money',data[uid]['money'] - price)
            str = ""
            for i in goods:
                i = int(i)
                str += Utils.gain_item(uid,i)
            await matcher.finish(MessageSegment.image(Utils.text_to_image(str)))

    async def yinpa_work(
            matcher: Matcher,event: GroupMessageEvent,args: Message = CommandArg()
    ):
        """处理工作
        """
        
        uid = event.get_user_id()
        if not Utils.yinpa_user_presence_check(event.get_user_id()):
            await matcher.finish("您还未加入银趴！\ntips：请使用 /yinpa_join 或 /加入银趴 加入银趴")
        Utils.refresh_data(uid)
        command = args.extract_plain_text()
        work_key = command.split()
        if not work_key:
            str = ""
            for i in list(dicts.work_dict.keys()):
                str += f"{i}：{dicts.work_dict[i]}\n"
            await matcher.finish("可用工作：\n" + str + "\n输入/yinpa_help work [工作名或工作ID] 以查看工作描述")
        work_key = work_key[0]
        if not dicts.work_dict.get(work_key) and not dicts.work_help_dict.get(work_key) and not dicts.work_dict.get(int(work_key)):
            str = ""
            for i in list(dicts.work_dict.keys()):
                str += f"{i}：{dicts.work_dict[i]}"
            await matcher.finish("错误：该工作不存在\n可用工作：\n" + str + "\n输入/yinpa_help work [工作名或工作ID] 以查看工作描述")
        oc = Utils.operation_check(uid)
        if oc:
            await matcher.finish(f"错误：操作失败！\n原因：{oc}")
        if data[uid]["next_work_time"] >= time():
            await matcher.finish("你现在正在工作冷却中！")
        if work_key in list(dicts.work_dict.values()):
            work_key = (list(dicts.work_dict.keys()))[(list(dicts.work_dict.values())).index(work_key)]
        work_key = int(work_key)
        str = ""
        money = 0
        if work_key == 1:
            money += (Utils.get_value(uid,'strength')[0] + Utils.get_value(uid,'constitution')[0]) * Utils.dice(200,(Utils.get_value(uid,'strength')[0] + Utils.get_value(uid,'constitution')[0])) / 100
            if money < 0:
                money = 0
            str += f"你进行了工作：{dicts.work_dict[work_key]}\n收益：{money}\n"
        elif work_key == 2:
            money += (Utils.get_value(uid,'technique')[0] * 0.7 + Utils.get_value(uid,'charm')[0] * 0.9) * Utils.dice(260,(Utils.get_value(uid,'technique')[0] + Utils.get_value(uid,'charm')[0])) / 100
            if money < 0:
                money = 0
            str += f"你进行了工作：{dicts.work_dict[work_key]}\n收益：{money}\n"
            d = Utils.dice(100,Utils.get_value(uid,'volition')[0])
            str += f"意志检定：1d100 = {d} "
            if d >= Utils.get_value(uid,'volition')[0]:
                DHandles.data_set(uid,"hp_v",0)
                d = Utils.dice(10,(int)(uid) ^ 100)
                DHandles.state_refresh(uid,1,time() + d * 60)
                str += f" >= {data[uid]['volition']}\n{data[uid]['name']}失神了！失神状态将持续1d10 = {d}分钟。（期间无法行动，技能失效。如果失神期间受到攻击，失神状态将延长一分钟。）"
            else:
                str += f" < {data[uid]['volition']}\n"
        elif work_key == 3:
            money += (Utils.get_value(uid,'intelligence')[0] + Utils.get_value(uid,'charm')[0] - 60) * Utils.dice(200,(Utils.get_value(uid,'intelligence')[0] + Utils.get_value(uid,'charm')[0])) / 100
            if money < 0:
                money = 0
            str += f"你进行了工作：{dicts.work_dict[work_key]}\n收益：{money}\n"
            d = Utils.dice(100,Utils.get_value(uid,'volition')[0])
            str += f"智力检定：1d100 = {d} "
            if d >= Utils.get_value(uid,'intelligence')[0]:
                str += f" >= {data[uid]['intelligence']}\n"
            else:
                money += 3 * d
                str += f" < {data[uid]['intelligence']}\n追加收益：{3 * d}\n"
        elif work_key == 4:
            money += (Utils.get_value(uid,'technique')[0] + Utils.get_value(uid,'intelligence')[0] - 100) * Utils.dice(300,(Utils.get_value(uid,'technique')[0] + Utils.get_value(uid,'intelligence')[0])) / 100
            if money < 0:
                money = 0
            str += f"你进行了工作：{dicts.work_dict[work_key]}\n收益：{money}\n"
        elif work_key == 5:
            money += (Utils.get_value(uid,'strength')[0] * 0.9 + Utils.get_value(uid,'constitution')[0] * 0.8) * Utils.dice(200,(Utils.get_value(uid,'strength')[0] + Utils.get_value(uid,'constitution')[0])) / 120
            if money < 0:
                money = 0
            str += f"你进行了工作：{dicts.work_dict[work_key]}\n收益：{money}\n"
            d = Utils.dice(100,Utils.get_value(uid,'constitution')[0])
            str += f"体质检定：1d100 = {d} "
            if d >= Utils.get_value(uid,'constitution')[0]:
                DHandles.data_set(uid,"hp_v",0)
                d = Utils.dice(10,(int)(uid) ^ 101)
                DHandles.state_refresh(uid,1,time() + d * 3600)
                str += f" >= {data[uid]['constitution']}\n{data[uid]['name']}昏迷了！失神状态将持续1d10 = {d}小时。（期间无法行动，无法被透，技能失效。）"
            else:
                str += f" < {data[uid]['constitution']}\n"
        elif work_key == 6:
            d = Utils.dice(100,(int)(uid) ^ 102)
            money += (d - 80) * 500
            if money < 0:
                money = 0
            str += f"你进行了工作：{dicts.work_dict[work_key]}\n收益：{money}\n"
            d = Utils.dice(10,(int)(uid) ^ 103)
            if d == 1:
                d = Utils.dice(10,(int)(uid) ^ 104)
                if d >= 1 and d <= 1:
                    l = list(dicts.shop_dict.keys())
                    i = Utils.dice(len(l),(int)(uid) ^ 105)
                    str += Utils.gain_item(uid,l[i - 1])
                elif d >= 2 and d <= 4:
                    l = list(dicts.state_dict.keys())
                    i = Utils.dice(len(l),(int)(uid) ^ 106)
                    d = Utils.dice(86400,(int)(uid) ^ 107)
                    str += DHandles.state_refresh(uid,i,time() + d,level = 1,mode = 'add')
                elif d >= 5 and d <= 7:
                    i = Utils.dice(8,(int)(uid) ^ 108)
                    d = Utils.dice(100,(int)(uid) ^ 109) / 20
                    if i == 1:
                        i = 'strength'
                    elif i == 2:
                        i = 'constitution'
                    elif i == 3:
                        i = 'technique'
                    elif i == 4:
                        i = 'volition'
                    elif i == 5:
                        i = 'intelligence'
                    elif i == 6:
                        i = 'charm'
                    elif i == 7:
                        i = 'penis_length'
                    elif i == 8:
                        i = 'vagina_depth'
                    str += f"你的{dicts.attribute_dict[i]}： {data[uid][i]} → {data[uid][i] + d}\n"
                    DHandles.data_set(uid,i,(data[uid][i] + d))
                elif d >= 8 and d <= 10:
                    l = [10,11,12,13,14,15,]
                    i = Utils.dice(len(l),(int)(uid) ^ 106)
                    d = Utils.dice(86400,(int)(uid) ^ 107)
                    str += DHandles.skill_refresh(uid,l[i - 1],level = 1,mode = 'add')
        DHandles.data_set(uid,"next_work_time",(time() + 3600))
        DHandles.data_set(uid,"money",data[uid]["money"] + money)
        str += "一小时内你将无法继续工作"
        await matcher.finish(MessageSegment.image(Utils.text_to_image(str)))

    # async def test(
    #     matcher: Matcher,event: GroupMessageEvent,args: Message = CommandArg()
    # ):
    #     """测试用
    #     """
        
    #     uid = event.get_user_id()
    #     #await matcher.finish(await Utils.get_group_yinpa_list((str)(event.self_id),event.group_id))
    #     await matcher.finish(MessageSegment.image(Utils.draw_rank_image(event.group_id,uid,(str)(event.self_id))))