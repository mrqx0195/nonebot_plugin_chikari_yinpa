import json
import os

from pathlib import Path
from time import time
from .dicts import dicts
import nonebot_plugin_localstore as store

plugin_data_file: Path = store.get_data_file("chikari_yinpa", "data.json")
plugin_config_file: Path = store.get_config_file("chikari_yinpa", "config.json")

#用户数据文件初始化及载入

with open(plugin_data_file,encoding='utf-8')as datafile:
    datastr = datafile.read()
    if not os.path.exists(plugin_data_file) or not datastr:
        f = open(plugin_data_file,'w')
        init_data = {}
        json.dump(init_data,f,indent=4)
        f.close
        data = init_data
    else:
        data = json.loads(datastr,strict=False)
        
#配置数据文件初始化及载入

with open(plugin_config_file,encoding='utf-8')as configfile:
    configstr = configfile.read()
    if not os.path.exists(plugin_config_file) or not configstr:
        f = open(plugin_config_file,'w')
        init_data = {
            "yinpa_enabled_group":[],
        }
        json.dump(init_data,f,indent=4)
        f.close
        configdata = init_data
    else:
        configdata = json.loads(configstr,strict=False)


class DHandles():
    """数据处理"""
    
    def file_save():
        """将内存中的数据保存至文件
        """
        
        global data
        global configdata
        f = open(plugin_data_file,'w')
        json.dump(data,f,indent=4)
        f.close
        f = open(plugin_config_file,'w')
        json.dump(configdata,f,indent=4)
        f.close

    def data_set(uid: str,key: str,value):
        """设置特定用户的特定数值

        Args:
            uid (str): 用户id
            key (str): 数据键值
            value (_type_): 数据
        """
        
        global data
        data[uid][key] = value
        DHandles.file_save()
        return
    
    def configdata_set(key: str,value):
        """设置配置文件

        Args:
            key (str): 配置键值
            value (_type_): 数据
        """
        
        global configdata
        configdata[key] = value
        DHandles.file_save()
        return
    
    def group_remove(group_id: int):
        """将群组移出银趴

        Args:
            group_id (int): 群组id
        """
        
        global configdata
        configdata["yinpa_enabled_group"].remove(group_id)
        DHandles.file_save()
        return
    
    def user_add(uid: str,dict: dict):
        """将用户加入银趴

        Args:
            uid (str): 用户id
            dict (dict): 用户初始数据
        """
        
        global data
        data[uid] = dict
        data[uid]["hp_v"] = (data[uid]["volition"] + 10) * 5
        data[uid]["hp_c"] = (data[uid]["constitution"] + 10) * 10
        DHandles.file_save()
        return
        
    def user_remove(uid: str):
        """将用户移出银趴

        Args:
            uid (str): 用户id
        """
        
        global data
        del data[uid]
        DHandles.file_save()
        return
    
    def skill_refresh(uid: str,id: int,value = None,level: int = 1,mode: str = ''):
        """更新技能

        Args:
            uid (str): 用户id
            id (int): 技能id
            value (_type_, optional): 技能附加数据
            level (int): 技能等级
            mode (str): 若为'add'则为增加等级，否则为修改等级（如果未拥有该技能，则固定为修改等级）

        Returns:
            str: 描述文本
        """
        
        global data
        b = False
        for i in range(len(data[uid]["skill"])):
            if data[uid]["skill"][i][0] == id:
                data[uid]["skill"][i][1] = value
                if len(data[uid]["skill"][i]) >= 3:
                    if mode == 'add':
                        level += data[uid]["skill"][i][2]
                    data[uid]["skill"][i][2] = level
                else:
                    data[uid]["skill"][i].insert(2,level)
                b = True
                break
        if not b:
            data[uid]["skill"].append([id,value,level])
        return f"获得技能：{dicts.skill_dict[id]}（等级：{level}）（ID：{id}）\n"
    
    def state_refresh(uid: str,id: int,value = time(),level: int = 1,mode: str = ''):
        """更新状态

        Args:
            uid (str): 用户id
            id (int): 状态id
            value (_type_, optional): 状态结束时间
            level (int): 状态等级
            mode (str): 若为'add'则为增加等级，否则为修改等级（如果未拥有该状态，则固定为修改等级）

        Returns:
            str: 描述文本
        """
        
        global data
        b = False
        for i in range(len(data[uid]["state"])):
            if data[uid]["state"][i][0] == id:
                data[uid]["state"][i][1] = value
                if len(data[uid]["state"][i]) >= 3:
                    if mode == 'add':
                        level += data[uid]["state"][i][2]
                    data[uid]["state"][i][2] = level
                else:
                    data[uid]["state"][i].insert(2,level)
                b = True
                break
        if not b:
            data[uid]["state"].append([id,value,level])
        return f"获得状态：{dicts.state_dict[id]}（等级：{level}）（ID：{id}）\n"
