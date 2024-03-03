from nonebot.adapters.onebot.v11 import GroupMessageEvent,bot
from nonebot import get_plugin_config,get_bots

import json
from random import randint,seed
from time import time,localtime
from PIL import Image,ImageDraw,ImageFont
from io import BytesIO
from math import sqrt

from .data_handles import data,configdata,DHandles
from .dicts import dicts
from .config import Config

plugin_config = get_plugin_config(Config)

class Utils:
    def group_enable_check(groupid: int):
        """检查群组是否在银趴列表中

        Args:
            groupid (int): 群组id

        Returns:
            int: 是否出现
        """
        
        return configdata["yinpa_enabled_group"].count(groupid)
    
    def last_operation_time_check(uid: str):
        """检测上次行动时间

        Args:
            uid (str): 用户id

        Returns:
            bool: 是否到时
        """
        
        minutes=(int)(time()/60)
        if data[uid]["last_operation_time"] < minutes:
            return True
        return False
    
    def set_last_operation_time(uid: str):
        """设置上次行动时间

        Args:
            uid (str): 用户id
        """
        
        DHandles.data_set(uid,"last_operation_time",(int)(time()/60))
        return
    
    def dice(d:int,_seed):
        """骰子

        Args:
            d (int): 上限
            _seed (_type_): 随机数种子

        Returns:
            int: 值
        """
        
        seed((int)(time()) ^ (int)(d) ^ (int)(_seed))
        return randint(1,(int)(d))
    
    def get_at(event: GroupMessageEvent):
        """获取消息中的at

        Args:
            event (GroupMessageEvent): 消息

        Returns:
            list: at列表
        """
        
        try:
            qq_list = []
            msg = json.loads(event.json())
            for i in msg['message']:
                if i['type'] == 'at':
                    if 'all' not in str(i):
                        qq_list.append((str)(int(i['data']['qq'])))
                    else:
                        return ['all']
            if event.to_me:
                qq_list += [(str)(event.self_id)]
            return qq_list
        except KeyError:
            return []

    def yinpa_user_presence_check(uid: str):
        """检查用户是否存在

        Args:
            uid (str): 用户id

        Returns:
            bool: 用户是否存在
        """
        
        if data.get(uid):
            return True
        return False
    
    def text_to_image(text: str):
        """文字转图片

        Args:
            text (str): 要转换的文字

        Returns:
            bytes: 图片
        """
        
        fontSize = 20
        liens = text.split('\n')
        max_len = 0
        for str in liens:
            max_len = max(len(str),max_len)
        image = Image.new("RGB", ((fontSize * max_len), len(liens) * (fontSize + 5)), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(plugin_config.chikari_yinpa_font, fontSize)
        draw.text((0, 0), text, font=font, fill="#000000", stroke_width = 0)
        img = image.convert("RGB")
        img_byte = BytesIO()
        img.save(img_byte,"PNG")
        return img_byte.getvalue()

    def get_user_info_image(uid: str):
        """获取用户的信息图

        Args:
            uid (str): 用户id

        Returns:
            bytes: 图片
        """
        
        Utils.refresh_data(uid)
        user_data = data[uid]
        skill_text = ""
        state_text = ""
        for i in user_data["skill"]:
            if i[0] == 6 and i[1] and i[1] >= time():
                skill_text += "\n    " + dicts.skill_dict[i[0]] + f'（等级：{i[2]}）（舰装损坏，{(int)(i[1] - time())}秒后修复）' + '；'
            else:
                skill_text += "\n    " + dicts.skill_dict[i[0]] + f'（等级：{i[2]}）' + '；'
        if not skill_text:
            skill_text = '无'
        for i in user_data["state"]:
            state_text += dicts.state_dict[i[0]] + f'（等级：{i[2]}）（剩余时间：{(int)(i[1] - time())}秒）' + '；'
        if not state_text:
            state_text = '无'
        text = f"    ID：{uid}\n"\
        f"    昵称：{user_data['name']}\n"\
        f"    种族：{user_data['species']}\n"\
        f"    意志HP：{user_data['hp_v']}\n"\
        f"    体质HP：{user_data['hp_c']}\n"\
        f"    长度：{user_data['penis_length']}\n"\
        f"    深度：{user_data['vagina_depth']}\n"\
        f"    力量：{user_data['strength']}（当前：{Utils.get_value(uid,"strength")}）\n"\
        f"    体质：{user_data['constitution']}（当前：{Utils.get_value(uid,"constitution")}）\n"\
        f"    技巧：{user_data['technique']}（当前：{Utils.get_value(uid,"technique")}）\n"\
        f"    意志：{user_data['volition']}（当前：{Utils.get_value(uid,"volition")}）\n"\
        f"    智力：{user_data['intelligence']}\n"\
        f"    魅力：{user_data['charm']}\n"\
        f"    金钱：{user_data['money']}\n"\
        f"    技能：{skill_text}\n"\
        f"    状态：{state_text}\n"\
        f"    被动次数：{user_data['passive_times']}\n"\
        f"    主动次数：{user_data['active_times']}"\
        
        return Utils.text_to_image(text)
    
    def refresh_data(uid: str):
        """更新用户数据

        Args:
            uid (str): 用户id
        """
        
        b = False
        for i in data[uid]["skill"]:
            if len(i) <= 2:
                DHandles.skill_refresh(uid,i[0],i[1])
        for i in data[uid]["state"]:
            if len(i) <= 2:
                DHandles.state_refresh(uid,i[0],i[1])
        new_state = data[uid]["state"]
        for i in data[uid]["state"]:
            if i[1] <= time():
                new_state.remove(i)
            if i[0] == 1:
                if i[1] > time():
                    b = True
                else:
                    DHandles.data_set(uid,'hp_v',(Utils.get_value(uid,'volition')[0] + 10) * 5)
            elif i[0] == 2 and i[1] <= time():
                DHandles.data_set(uid,'hp_v',(Utils.get_value(uid,'volition')[0] + 10) * 5)
                DHandles.data_set(uid,'hp_c',(Utils.get_value(uid,'constitution')[0] + 10) * 10)
        DHandles.data_set(uid,"state",new_state)
        if b :
            if data[uid]['hp_c'] + (int)(((int)(time()) - (int)(data[uid]["last_refresh_time"])) / 60) >= (Utils.get_value(uid,'constitution')[0] + 10) * 10:
                DHandles.data_set(uid,'hp_c',(Utils.get_value(uid,'constitution')[0] + 10) * 10)
            else:
                DHandles.data_set(uid,'hp_c',data[uid]['hp_c'] + ((int)(((int)(time()) - (int)(data[uid]["last_refresh_time"])) / 60)) * Utils.get_regeneration_rate(uid))
        else:
            DHandles.data_set(uid,'hp_c',(Utils.get_value(uid,'constitution')[0] + 10) * 10)
            if data[uid]['hp_v'] + (int)(((int)(time()) - (int)(data[uid]["last_refresh_time"])) / 60) >= (Utils.get_value(uid,'volition')[0] + 10) * 5:
                DHandles.data_set(uid,'hp_v',(Utils.get_value(uid,'volition')[0] + 10) * 5)
            else:
                DHandles.data_set(uid,'hp_v',data[uid]['hp_v'] + ((int)(((int)(time()) - (int)(data[uid]["last_refresh_time"])) / 60)) * Utils.get_regeneration_rate(uid))
        DHandles.data_set(uid,"last_refresh_time",time())
        return

    def get_skill(uid: str,id: int):
        """获取技能

        Args:
            uid (str): 用户id
            id (int): 技能id

        Returns:
            list: [技能id,附加数据,等级]
        """
        
        s = []
        for i in data[uid]["skill"]:
            if i[0] == id:
                s = i
            if len(i) <= 2:
                DHandles.skill_refresh(uid,i[0],i[1])
        if s and s[0] not in [9,10,11,12,13,14,15,] and Utils.get_state(uid,1):
            s = []
        return s

    def get_state(uid: str,id: int):
        """获取状态

        Args:
            uid (str): 用户id
            id (int): 状态id

        Returns:
            list: [状态id,结束时间,等级]
        """
        
        s = []
        for i in data[uid]["state"]:
            if i[0] == id:
                s = i
            if len(i) <= 2:
                DHandles.state_refresh(uid,i[0],i[1])
        return s

    def is_night():
        """判断是否为晚上

        Returns:
            bool: 是否为晚上
        """
        
        b = True
        hour = localtime().tm_hour
        if hour >= 6 and hour < 18:
            b = False
        return b

    def boat(uid: str):
        """判断舰装是否生效

        Args:
            uid (str): 用户id

        Returns:
            int: 舰装等级
        """
        
        b = 0
        s = Utils.get_skill(uid,6)
        if s and s[1] and s[1] <= time():
            b = s[2]
        return b

    def vampire(uid: str):
        """判断吸血鬼技能是否生效

        Args:
            uid (str): 用户id

        Returns:
            int: 加成值，无吸血鬼技能时返回0
        """
        
        if  i := Utils.get_skill(uid,7):
            if Utils.is_night():
                return 50 * sqrt(i[2])
            else:
                return -50 / sqrt(i[2])
        return 0

    def get_value(uid: str,key: str):
        """获取用户当前状态下的某一数值

        Args:
            uid (str): 用户id
            key (str): 数值名

        Returns:
            list: [数值,附加信息]
        """
        
        b = False
        value = 0
        if key == "hp":
            if Utils.get_state(uid,1):
                b = True
            if b:
                hp = data[uid]['hp_c']
            else:
                hp = data[uid]['hp_v']
            value = hp
        elif key == 'penis_length':
            value = data[uid]['penis_length']
        elif key == 'vagina_depth':
            value = data[uid]['vagina_depth']
        elif key == 'strength':
            value = data[uid]['strength']
            if i := Utils.boat(uid):
                value += Utils.get_value(uid,'intelligence')[0] * sqrt(i[2])
            value += Utils.vampire(uid)
        elif key == 'constitution':
            value = data[uid]['constitution']
            if i := Utils.boat(uid):
                value += Utils.get_value(uid,'intelligence')[0] * sqrt(i[2])
            value += Utils.vampire(uid)
        elif key == 'technique':
            value = data[uid]['technique']
            value += Utils.vampire(uid)
            if i := Utils.get_skill(uid,12) and Utils.is_night():
                value += -20 * i[2]
        elif key == 'volition':
            value = data[uid]['volition']
            if i := Utils.boat(uid):
                value += Utils.get_value(uid,'intelligence')[0] * sqrt(i[2])
            value += Utils.vampire(uid)
            if i := Utils.get_skill(uid,12) and Utils.is_night():
                value += -20 * i[2]
        elif key == 'intelligence':
            value = data[uid]['intelligence']
        elif key == 'charm':
            value = data[uid]['charm']
        if value < 0:
            value = 0
        return [value,b]

    def get_attack_list(uid: str,target: str):
        """获取用户对目标造成的伤害

        Args:
            uid (str): 用户id
            target (str): 目标id

        Returns:
            list: 伤害列表
        """
        
        Utils.refresh_data(uid)
        Utils.refresh_data(target)
        atk = [[Utils.get_value(uid,'technique')[0],f"{data[uid]['name']}：技巧",False]]
        if i := Utils.get_skill(uid,2):
            atk.append([30 * sqrt(i[2]),f"{data[uid]['name']}：猫化",False])
        if i := Utils.get_skill(uid,3):
            atk.append([Utils.get_value(uid,'intelligence')[0] / 2 * sqrt(i[2]),f"{data[uid]['name']}：自然之心",False])
        if i := Utils.get_skill(uid,5):
            atk.append([80 * sqrt(i[2]),f"{data[uid]['name']}：淫纹",False])
        if i := Utils.get_state(uid,3):
            atk.append([30 * sqrt(i[2]),f"{data[uid]['name']}：伟哥",False])
        if i := Utils.get_skill(uid,11):
            atk.append([60 * i[2],f"{data[uid]['name']}：亡命疯徒",False])
        if i := Utils.get_skill(target,11):
            atk.append([60 * i[2],f"{data[target]['name']}：亡命疯徒",False])
        if i := Utils.get_skill(target,15):
            if Utils.dice(100,i[2] * 15) <= i[2]:
                atk.append([1000,f"{data[target]['name']}：弱点",True])
        
        if i := Utils.get_skill(target,2):
            atk.append([-30 * sqrt(i[2]),f"{data[target]['name']}：猫化",False])
        if i := Utils.get_skill(target,3):
            atk.append([-Utils.get_value(uid,'intelligence')[0] / 2 * sqrt(i[2]),f"{data[target]['name']}：自然之心",False])
        if i := Utils.get_skill(target,4):
            atk.append([-80 * sqrt(i[2]),f"{data[target]['name']}：圣体",False])
        if i := Utils.get_skill(uid,10):
            atk.append([-50 * i[2],f"{data[uid]['name']}：呓语",False])
        if i := Utils.get_skill(target,14):
            atk.append([-50 * i[2],f"{data[target]['name']}：敏感",False])
        return atk
    
    def reduce_hp(uid: str,hp: int):
        """减少hp并返回描述文本

        Args:
            uid (str): 用户id
            hp (int): 减少的hp

        Returns:
            str: 若有高潮/失神/昏迷，则返回相关描述文本
        """
        
        str = ""
        if not Utils.get_state(uid,1):
            DHandles.data_set(uid,'hp_v',(int)(Utils.get_value(uid,"hp")[0] - hp))
            if data[uid]['hp_v'] <= 0:
                d = Utils.dice(100,(int)(uid) ^ 10)
                str += f"\n{data[uid]['name']}高潮了！\n意志检定：1d100 = {d}"
                if d >= data[uid]['volition']:
                    DHandles.data_set(uid,'hp_v',0)
                    d = Utils.dice(10,(int)(uid) ^ 11)
                    DHandles.state_refresh(uid,1,time() + d * 60)
                    str += f" >= {data[uid]['volition']}\n{data[uid]['name']}失神了！失神状态将持续1d10 = {d}分钟。（期间无法行动，技能失效。如果失神期间受到攻击，失神状态将延长一分钟。）"
                else:
                    d = Utils.dice(data[uid]['volition'],(int)(uid) ^ 12)
                    DHandles.data_set(uid,'hp_v',(d + 10) * 5)
                    str += f" < {data[uid]['volition']}\n{data[uid]['name']}的意志HP回复至{data[uid]['hp_v']}"
        else:
            DHandles.data_set(uid,'hp_c',(int)(Utils.get_value(uid,"hp")[0] - hp))
            DHandles.state_refresh(uid,1,Utils.get_state(uid,1)[1] + 60)
            if data[uid]['hp_c'] <= 0:
                d = Utils.dice(100,(int)(uid) ^ 13)
                str += f"\n{data[uid]['name']}高潮了！\n体质检定：1d100 = {d}"
                if d >= data[uid]['constitution']:
                    DHandles.data_set(uid,'hp_c',0)
                    d = Utils.dice(10,(int)(uid) ^ 14)
                    DHandles.state_refresh(uid,2,time() + d * 3600)
                    str += f" >= {data[uid]['constitution']}\n{data[uid]['name']}昏迷了！昏迷状态将持续1d10 = {d}小时。（期间无法行动，无法被透，技能失效。）"
                    if Utils.boat(uid):
                        DHandles.skill_refresh(uid,6,time() + 259200)
                        str += f"\n{data[uid]['name']}的舰装破损了！将进入三天的冷却。"
                else:
                    d = Utils.dice(data[uid]['constitution'],(int)(uid) ^ 15)
                    DHandles.data_set(uid,'hp_c',(d + 10) * 5)
                    str += f" < {data[uid]['constitution']}\n{data[uid]['name']}的体质HP回复至{data[uid]['hp_c']}"
        if str:
            str = "\n" + str
        return str
    
    def operation_check(uid: str):
        """检测用户是否能够行动

        Args:
            uid (str): 用户id

        Returns:
            str: 不能行动的理由，可以行动时返回""
        """
        
        oc = ""
        Utils.refresh_data(uid)
        if not Utils.last_operation_time_check(uid):
            oc += "你操作太快了！"
        if Utils.get_state(uid,1) and not Utils.get_skill(uid,9):
            oc += "你失神了！"
        if Utils.get_state(uid,2):
            oc += "你昏迷了！"
        if not oc:
            Utils.set_last_operation_time(uid)
        return oc
    
    def find_user_name(name: str):
        """从昵称查找至用户id

        Args:
            name (str): 银趴昵称

        Returns:
            str: 用户id，未找到时返回None
        """
        
        for i in data.keys():
            if data[i]['name'] == name:
                return i
        return None
    
    def get_regeneration_rate(uid: str):
        """获取hp自然恢复速度

        Args:
            uid (str): 用户id

        Returns:
            int: 每分钟自然恢复hp
        """
        
        rr = 1
        if i := Utils.get_skill(uid,8):
            rr += 5 * i[2]
        if i := Utils.get_skill(uid,13):
            rr += -5 * i[2]
        if rr < 0:
            rr = 0
        return rr
    
    def gain_item(uid: str,id: int):
        """用户获得物品

        Args:
            uid (str): 用户id
            id (int): 物品id

        Returns:
            str: 描述文本
        """
        
        str = ''
        str += f"你获得了物品：{dicts.shop_dict[id]}\n"
        if id == 1:
            str += DHandles.state_refresh(uid,3,time() + 3600,level = 1,mode = 'add')
        elif id == 2:
            DHandles.data_set(uid,'penis_length',data[uid]['penis_length'] + 2)
            DHandles.data_set(uid,'vagina_depth',data[uid]['vagina_depth'] + 2)
            str += "长度增加了2cm，深度增加了2cm\n"
        elif id == 3:
            hp = Utils.get_value(uid,"hp")
            if hp[1]:
                DHandles.data_set(uid,"hp_c",data[uid]["hp_c"] + 100)
                str += "体质HP增加了100\n"
            else:
                DHandles.data_set(uid,"hp_v",data[uid]["hp_v"] + 100)
                str += "意志HP增加了100\n"
        elif id == 4:
            str += DHandles.skill_refresh(uid,2,level = 1,mode = 'add')
        elif id == 5:
            str += DHandles.skill_refresh(uid,3,level = 1,mode = 'add')
        elif id == 6:
            str += DHandles.skill_refresh(uid,4,level = 1,mode = 'add')
        elif id == 7:
            str += DHandles.skill_refresh(uid,5,level = 1,mode = 'add')
        elif id == 8:
            str += DHandles.skill_refresh(uid,6,level = 1,mode = 'add')
        elif id == 9:
            str += DHandles.skill_refresh(uid,7,level = 1,mode = 'add')
        elif id == 10:
            str += DHandles.skill_refresh(uid,8,level = 1,mode = 'add')
        elif id == 11:
            str += DHandles.skill_refresh(uid,9,level = 1,mode = 'add')
        elif id == 12:
            l = [10,11,12,13,14,15,]
            for i in l:
                DHandles.skill_refresh(uid,i,level = 0)
            str += "已清除所有诅咒"
        return str
    
    async def get_group_yinpa_list(bid: str,gid: int):
        """获取群内加入银趴的成员

        Args:
            bid (str): bot的id
            gid (int): 群的id

        Returns:
            list: 一个由群员id组成的列表
        """
        bot = get_bots()[bid]
        gmdlist = await bot.call_api('get_group_member_list',group_id = gid)
        gymlist = []
        for i in gmdlist:
            if data.get(i["user_id"]):
                gymlist.append(i["user_id"])
        return gymlist
    
    # def draw_rank_image(gid: int,uid: str):
    #     image = Image.new("RGB",(512,1024),(255,255,255))
    #     draw = ImageDraw.Draw(image)
    #     linewidth = 24
    #     for k in range(2):
    #         for j in range(2):
    #             tx = 28 + j * 256
    #             ty = 28 + k * 512
    #             for i in range(20):
    #                 draw.line([(tx,ty + i * linewidth),(tx + 200,ty + i * linewidth)],(0,0,0),1)
    #                 draw.line([(tx,ty + 512 + i * linewidth),(tx + 200,ty + 512 + i * linewidth)],(0,0,0),1)
    #             for i in range(2):
    #                 draw.line([(tx,ty + i * 512),(tx,ty + 456 + i * 512)],(0,0,0),1)
    #                 draw.line([(tx + 100,ty + i * 512 + linewidth),(tx + 100,ty + 456 + i * 512)],(0,0,0),1)
    #                 draw.line([(tx + 200,ty + i * 512),(tx + 200,ty + 456 + i * 512)],(0,0,0),1)
    #     img = image.convert("RGB")
    #     img_byte = BytesIO()
    #     img.save(img_byte,"PNG")
    #     return img_byte.getvalue()