from nonebot.adapters.onebot.v11 import GroupMessageEvent,bot

import os,json
from random import randint,seed
from time import time,localtime
from PIL import Image,ImageDraw,ImageFont
from io import BytesIO

from .data_handles import data,configdata,DHandles
from .dicts import dicts

class Utils:
    def group_enable_check(groupid: int):
        return configdata["yinpa_enabled_group"].count(groupid)
    
    def last_operation_time_check(uid: str):
        minutes=(int)(time()/60)
        if data[uid]["last_operation_time"] < minutes:
            return True
        return False
    
    def set_last_operation_time(uid: str):
        DHandles.data_set(uid,"last_operation_time",(int)(time()/60))
        return
    
    def dice(d:int,_seed):
        seed((int)(time()) ^ (int)(d) ^ (int)(_seed))
        return randint(1,(int)(d))
    
    def get_at(event: GroupMessageEvent):
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
        if data.get(uid):
            return True
        return False
    
    def text_to_image(text: str):
        fontSize = 30
        liens = text.split('\n')
        max_len = 0
        for str in liens:
            max_len = max(len(str),max_len)
        image = Image.new("RGB", ((fontSize * max_len), len(liens) * (fontSize)), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        fontPath = os.path.join("C:\\Windows\\Fonts\\", "simhei.ttf")
        font = ImageFont.truetype(fontPath, fontSize)
        draw.text((0, 0), text, font=font, fill="#000000")
        img = image.convert("RGB")
        img_byte = BytesIO()
        img.save(img_byte,"PNG")
        return img_byte.getvalue()

    def get_user_info_image(uid: str):
        Utils.refresh_data(uid)
        user_data = data[uid]
        skill_text = ""
        state_text = ""
        for i in user_data["skill"]:
            skill_text += dicts.skill_dict[i[0]] + ' '
        for i in user_data["state"]:
            state_text += dicts.state_dict[i[0]] + ' '
        text = f"ID：{uid}\n昵称：{user_data['name']}\n种族：{user_data['species']}\n意志HP：{user_data['hp_v']}\n体质HP：{user_data['hp_c']}\n长度：{user_data['penis_length']}\n深度：{user_data['vagina_depth']}\n力量：{user_data['strength']}\n体质：{user_data['constitution']}\n技巧：{user_data['technique']}\n意志：{user_data['volition']}\n智力：{user_data['intelligence']}\n魅力：{user_data['charm']}\n金钱：{user_data['money']}\n技能：{skill_text}\n状态：{state_text}\n被动次数：{user_data['passive_times']}\n主动次数：{user_data['active_times']}"
        return Utils.text_to_image(text)
    
    def refresh_data(uid: str):
        b = False
        new_state = data[uid]["state"]
        for i in range(len(data[uid]["state"])):
            if i >= len(data[uid]["state"]):
                break
            if data[uid]["state"][i][1] <= time():
                new_state.remove(data[uid]["state"][i])
            if data[uid]["state"][i][0] == 1:
                if data[uid]["state"][i][1] > time():
                    b = True
                else:
                    DHandles.data_set(uid,'hp_v',(Utils.get_value(uid,'volition')[0] + 10) * 5)
            elif data[uid]["state"][i][0] == 2 and data[uid]["state"][i][1] <= time():
                DHandles.data_set(uid,'hp_v',(Utils.get_value(uid,'volition')[0] + 10) * 5)
                DHandles.data_set(uid,'hp_c',(Utils.get_value(uid,'constitution')[0] + 10) * 10)
        DHandles.data_set(uid,"state",new_state)
        if b :
            if data[uid]['hp_c'] + (int)(((int)(time()) - (int)(data[uid]["last_refresh_time"])) / 60) >= (Utils.get_value(uid,'constitution')[0] + 10) * 10:
                DHandles.data_set(uid,'hp_c',(Utils.get_value(uid,'constitution')[0] + 10) * 10)
            else:
                DHandles.data_set(uid,'hp_c',data[uid]['hp_c'] + ((int)(((int)(time()) - (int)(data[uid]["last_refresh_time"])) / 60)) * Utils.get_regeneration_rate(uid))
        else:
            if data[uid]['hp_v'] + (int)(((int)(time()) - (int)(data[uid]["last_refresh_time"])) / 60) >= (Utils.get_value(uid,'volition')[0] + 10) * 5:
                DHandles.data_set(uid,'hp_v',(Utils.get_value(uid,'volition')[0] + 10) * 5)
            else:
                DHandles.data_set(uid,'hp_v',data[uid]['hp_v'] + ((int)(((int)(time()) - (int)(data[uid]["last_refresh_time"])) / 60)) * Utils.get_regeneration_rate(uid))
        DHandles.data_set(uid,"last_refresh_time",time())
        return

    def get_skill(uid: str,id: int):
        s = []
        if not Utils.get_state(uid,1):
            for i in data[uid]["skill"]:
                if i[0] == id:
                    s = i
        return s

    def get_state(uid: str,id: int):
        s = []
        for i in data[uid]["state"]:
            if i[0] == id:
                s = i
        return s

    def is_night():
        b = True
        hour = localtime().tm_hour
        if hour > 6 and hour <= 18:
            b = False
        return b

    def boat(uid: str):
        b = False
        s = Utils.get_skill(uid,6)
        if s and s[1] <= time():
            b = True
        return b

    def vampire(uid: str):
        if Utils.get_skill(uid,7):
            if Utils.is_night():
                return 50
            else:
                return -50
        return 0

    def get_value(uid: str,key: str):
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
            if Utils.boat(uid):
                value += Utils.get_value(uid,'intelligence')[0]
            value += Utils.vampire(uid)
        elif key == 'constitution':
            value = data[uid]['constitution']
            if Utils.boat(uid):
                value += Utils.get_value(uid,'intelligence')[0]
            value += Utils.vampire(uid)
        elif key == 'technique':
            value = data[uid]['technique']
            value += Utils.vampire(uid)
        elif key == 'volition':
            value = data[uid]['volition']
            if Utils.boat(uid):
                value += Utils.get_value(uid,'intelligence')[0]
            value += Utils.vampire(uid)
        elif key == 'intelligence':
            value = data[uid]['intelligence']
        elif key == 'charm':
            value = data[uid]['charm']
        if value < 0:
            value = 0
        return [value,b]

    def get_attack_list(uid: str,target: str):
        atk = [[Utils.get_value(uid,'technique')[0],f"{data[uid]['name']}：技巧"]]
        if Utils.get_skill(uid,2):
            atk.append([30,f"{data[uid]['name']}：猫化"])
        if Utils.get_skill(uid,3):
            atk.append([Utils.get_value(uid,'intelligence')[0] / 2,f"{data[uid]['name']}：自然之心"])
        if Utils.get_skill(uid,5):
            atk.append([80,f"{data[uid]['name']}：淫纹"])
        if Utils.get_state(uid,3):
            atk.append([30,f"{data[uid]['name']}：伟哥"])
        
        if Utils.get_skill(target,2):
            atk.append([-30,f"{data[target]['name']}：猫化"])
        if Utils.get_skill(target,3):
            atk.append([-Utils.get_value(uid,'intelligence')[0] / 2,f"{data[target]['name']}：自然之心"])
        if Utils.get_skill(target,4):
            atk.append([-80,f"{data[target]['name']}：圣体"])
        return atk
    
    def reduce_hp(uid: str,hp: int):
        str = ""
        if not Utils.get_state(uid,1):
            DHandles.data_set(uid,'hp_v',Utils.get_value(uid,"hp")[0] - hp)
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
            DHandles.data_set(uid,'hp_c',Utils.get_value(uid,"hp")[0] - hp)
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
        for i in data.keys():
            if data[i]['name'] == name:
                return i
        return None
    
    def get_regeneration_rate(uid: str):
        rr = 1
        if Utils.get_skill(uid,8):
            rr += 5
        return rr
    
    