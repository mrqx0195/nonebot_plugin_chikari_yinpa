from pydantic import BaseModel
from typing import Optional

class Config(BaseModel):
    #初始性别倾向。默认：50
    chikari_yinpa_initial_sex_value: Optional[int] = 50
    #初始长度。默认：10
    chikari_yinpa_initial_penis_length: Optional[int] = 10
    #初始深度。默认：10
    chikari_yinpa_initial_vagina_depth: Optional[int] = 10
    #初始金钱。默认：100
    chikari_yinpa_initial_money: Optional[int] = 100