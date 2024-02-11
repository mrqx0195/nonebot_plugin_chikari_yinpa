import json
import os

from pathlib import Path
from time import time
import nonebot_plugin_localstore as store

plugin_data_file: Path = store.get_data_file("chikari_yinpa", "data.json")
plugin_config_file: Path = store.get_config_file("chikari_yinpa", "config.json")

if not os.path.exists(plugin_data_file):
    f = open(plugin_data_file,'w')
    init_data = {}
    json.dump(init_data,f,indent=4)
    f.close
    data = init_data
else:
    with open(plugin_data_file,encoding='utf-8')as datafile:
        data = json.load(datafile,strict=False)

if not os.path.exists(plugin_config_file):
    f = open(plugin_config_file,'w')
    init_data = {
        "yinpa_enabled_group":[],
    }
    json.dump(init_data,f,indent=4)
    f.close
    configdata = init_data
else:
    with open(plugin_config_file,encoding='utf-8')as configfile:
        configdata = json.load(configfile,strict=False)


class DHandles():
    def file_save():
        global data
        global configdata
        f = open(plugin_data_file,'w')
        json.dump(data,f,indent=4)
        f.close
        f = open(plugin_config_file,'w')
        json.dump(configdata,f,indent=4)
        f.close

    def data_set(uid: str,key: str,value):
        global data
        data[uid][key] = value
        DHandles.file_save()
        return
    
    def configdata_set(key: str,value):
        global configdata
        configdata[key] = value
        DHandles.file_save()
        return
    
    def group_remove(group_id: int):
        global configdata
        configdata["yinpa_enabled_group"].remove(group_id)
        DHandles.file_save()
        return
    
    def user_add(uid: str,dict: dict):
        global data
        data[uid] = dict
        data[uid]["hp_v"] = (data[uid]["volition"] + 10) * 5
        data[uid]["hp_c"] = (data[uid]["constitution"] + 10) * 10
        DHandles.file_save()
        return
        
    def user_remove(uid: str):
        global data
        del data[uid]
        DHandles.file_save()
        return
    
    def skill_refresh(uid: str,id: int,value = None):
        global data
        b = False
        for i in range(len(data[uid]["skill"])):
            if data[uid]["skill"][i][0] == id:
                data[uid]["skill"][i][1] = value
                b = True
                break
        if not b:
            data[uid]["skill"].append([id,value])
        return
    
    def state_refresh(uid: str,id: int,value = time()):
        global data
        b = False
        for i in range(len(data[uid]["state"])):
            if data[uid]["state"][i][0] == id:
                data[uid]["state"][i][1] = value
                b = True
                break
        if not b:
            data[uid]["state"].append([id,value])
        return