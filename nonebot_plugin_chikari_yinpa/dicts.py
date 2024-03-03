
class dicts():
    """银趴常量字典
    """
    
    yinpa_help_dict = {
        "":"Chikari_yinpa 模块帮助\n加入银趴：/yinpa_join <银趴昵称> <银趴种族>\n种族列表：/yinpa_help 种族\n技能列表：/yinpa_help 技能\n状态列表：/yinpa_help 状态\n查询个人信息：/info\n签到：/sign_in\n商店：/shop\n工作：/work",
        "help":"help\n命令：/help [参数]\n命令别称：/银趴帮助\n查询Chikari_yinpa的帮助",
        "sign_in":"sign_in\n命令：/sign_in\n命令别称：/签到 /打卡\n每日打卡，每天可使用一次，增加长度、深度、金钱",
        "yinpa_join":"join_yinpa\n命令：/yinpa_join <银趴昵称> <银趴种族>\n命令别称：/加入银趴\n加入银趴！\n种族列表参照： /yinpa_help 种族",
        "yinpa_leave":"yinpa_leave\n命令：/yinpa_leave [key]\n命令别称：/离开银趴\n离开银趴！\n首次输入时会返回一个key码，需再次发送带key的命令才能离开",
        "yinpa_control":"yinpa_control\n命令：/yinpa_control <enable/disable>\n命令别称：/银趴控制\n控制本群银趴的开启/关闭",
        "info":"info\n命令：/info [@某人]\n命令别称：/信息 /查询\n查询自己或某人的银趴信息",
        "tou":"tou\n命令：/tou <@某人 或 银趴昵称>\n命令别称：/透 /插入\n透某人",
        "zha":"zha\n命令：/zha <@某人 或 银趴昵称>\n命令别称：/榨 /榨精\n榨某人",
        "chong":"chong\n命令：/chong\n命令别称：/冲 /打胶 /手冲 /撸 /导\n冲一发，能够增加或减少一定长度",
        "kou":"kou\n命令：/kou\n命令别称：/扣 /扣扣 /自慰 /紫薇\n扣一次，能够增加少量深度",
        "shop":"shop\n命令：/shop\n命令别称：/商店 /买 /买东西 /店\n花费金钱购买商品\n参见：/yinpa_help shop",
        "work":"work\n命令：/work\n命令别称：/工作 /打工\n工作，获得金钱及其他东西\n参见：/yinpa_help work",
    }
    """帮助表
    """

    help_aliases = {
        "银趴帮助":"help",
        "签到":"sign_in",
        "打卡":"sign_in",
        "信息":"info",
        "查询":"info",
        "加入银趴":"yinpa_join",
        "离开银趴":"yinpa_leave",
        "银趴控制":"yinpa_control",
        "种族":"species",
        "技能":"skill",
        "状态":"state",
        "银趴种族":"species",
        "插入":"tou",
        "榨精":"zha",
        "透":"tou",
        "榨":"zha",
        "打胶":"chong",
        "手冲":"chong",
        "撸":"chong",
        "导":"chong",
        "冲":"chong",
        "扣":"kou",
        "扣扣":"kou",
        "自慰":"kou",
        "紫薇":"kou",
        "商店":"shop",
        "买":"shop",
        "买东西":"shop",
        "店":"shop",
        "工作":"work",
        "打工":"work",
    }
    """帮助别称
    """

    species_dict = {
        0:"NULL",
        1:"人类",
        2:"猫娘",
        3:"精灵",
        4:"天使",
        5:"魅魔",
        6:"舰娘",
        7:"吸血鬼",
    }
    """种族表
    """

    species_help = {
        "NULL":"NULL（ID：0）\n……？\n一个不存在的种族\n如果你的种族变成了这个，请尝试联系bot主或重新加入银趴",
        "人类":"人类（ID：1）\n最为平凡的种族\n力量：1d100\n体质：1d100\n技巧：1d100\n意志：1d100\n智力：1d100\n魅力：1d100\n无额外技能",
        "猫娘":"猫娘（ID：2）\n可爱的猫猫，柔软而可爱\n力量：1d100\n体质：20+1d80\n技巧：20+1d80\n意志：1d100\n智力：1d90\n魅力：10+1d90\n额外技能：猫化（ID：2）",
        "精灵":"精灵（ID：3）\n诞生于自然中的精灵，能够导引自然之力\n力量：20+1d80\n体质：10+1d80\n技巧：10+1d90\n意志：1d100\n智力：1d100\n魅力：20+1d80\n额外技能：自然之心（ID：3）",
        "天使":"天使（ID：4）\n自天堂降临的天使，身体素质十分强大，但是性爱方面嘛……\n力量：40+1d60\n体质：40+1d60\n技巧：1d60\n意志：1d60\n智力：30+1d70\n魅力：20+1d80\n额外技能：圣体（ID：4）",
        "魅魔":"魅魔（ID：5）\n自地狱降临的恶魔，拥有无与伦比的性爱技巧，但是身体素质十分薄弱，一旦晕倒……\n力量：1d60\n体质：1d60\n技巧：40+1d60\n意志：40+1d60\n智力：20+1d80\n魅力：30+1d70\n额外技能：淫纹（ID：5）",
        "舰娘":"舰娘（ID：6）\n拥有舰装的特殊存在，舰装为其提供了强大的承受能力，但相对的，失去舰装的舰娘十分脆弱\n力量：1d50\n体质：1d50\n技巧：1d100\n意志：1d50\n智力：40+1d60\n魅力：40+1d60\n额外技能：舰装（ID：6）",
        "吸血鬼":"吸血鬼（ID：7）\n潜伏于黑暗的种族，在晚上极为强大，白天极为弱小\n力量：1d100\n体质：1d100\n技巧：1d100\n意志：1d100\n智力：1d100\n魅力：1d100\n额外技能：猩红之影（ID：7）",
    }
    """种族帮助
    """

    species_initial_ability = {
        0:[[0,100],[0,100],[0,100],[0,100],[0,100],[0,100],[]],
        1:[[0,100],[0,100],[0,100],[0,100],[0,100],[0,100],[]],
        2:[[0,100],[20,80],[20,80],[0,100],[0,90],[10,90],[2]],
        3:[[20,80],[10,80],[10,90],[0,100],[0,100],[20,80],[3]],
        4:[[40,60],[40,60],[0,60],[0,60],[30,70],[20,80],[4]],
        5:[[0,60],[0,60],[40,60],[40,60],[20,80],[30,70],[5]],
        6:[[0,50],[0,50],[0,100],[0,50],[40,60],[40,60],[6]],
        7:[[0,100],[0,100],[0,100],[0,100],[0,100],[0,100],[7]],
    }
    """种族初始数据
    """

    skill_dict = {
        2:"猫化",
        3:"自然之心",
        4:"圣体",
        5:"淫纹",
        6:"舰装",
        7:"猩红之影",
        8:"自然蕴息宝珠",
        9:"屹立不倒",
        10:"呓语",
        11:"亡命疯徒",
        12:"黑暗恐惧",
        13:"造血障碍",
        14:"敏感",
        15:"弱点",
    }
    """技能表
    """

    skill_help = {
        "猫化":"猫化（ID：2）\n猫科动物的共性。\n造成的伤害增加1d(30×√(等级))，受到的伤害减少1d(30×√(等级))。",
        "自然之心":"自然之心（ID：3）\n自然之力的运用。\n造成的伤害增加1d(智力×√(等级)/2)，受到的伤害减少1d(智力×√(等级)/2)。",
        "圣体":"圣体（ID：4）\n至高天堂的回响。\n受到的伤害减少1d(80×√(等级))。",
        "淫纹":"淫纹（ID：5）\n无尽地狱的欲望。\n造成的伤害增加1d(80×√(等级))。",
        "舰装":"舰装（ID：6）\n科技树的巅峰结晶。\n拥有舰装的时候力量、体质、意志增加(智力×√(等级))。\n因被透而昏迷时，舰装进入3天的冷却。",
        "猩红之影":"猩红之影（ID：7）\n行走于黑暗的存在。\n白天（6：00~18：00）力量、体质、技巧、意志减少(50÷√(等级))，夜晚（18：00~次日6：00）力量、体质、技巧、意志增加(50×√(等级))。",
        "自然蕴息宝珠":"自然蕴息宝珠（ID：8）\n自然之力的结晶。\n自然回复血量增加(5×等级)/分钟。",
        "屹立不倒":"屹立不倒（ID：9）\n屹（弟）立（弟）不倒！\n在失神状态下也能行动，但其他技能仍然失效。",
        "呓语":"呓语（ID：10）\n【诅咒】\n你听到了什么……你的大脑开始变得混乱\n造成的伤害减少1d(50×等级)。",
        "亡命疯徒":"亡命疯徒（ID：11）\n【诅咒】\n疯狂占据了你的大脑，你开始不择手段地伤害他人……和自己\n造成和受到的伤害增加1d(60×等级)。",
        "黑暗恐惧":"黑暗恐惧（ID：12）\n【诅咒】\n你感觉到黑暗中有什么东西在蠢蠢欲动，你开始感到害怕\n夜晚（18：00~次日6：00）技巧、意志减少(20×等级)。",
        "造血障碍":"造血障碍（ID：13）\n【诅咒】\n血细胞凋亡加速，骨髓造血机能受抑制\n自然回复血量减少(5×等级)（不会低于0）。",
        "敏感":"敏感（ID：14）\n【诅咒】\n你的所有感受都被放大了\n受到的伤害增加1d(50×等级)。",
        "弱点":"弱点（ID：15）\n【诅咒】\n万物都有弱点，你也一样\n受到伤害时，如果1d100 <= (等级)，则受到1000点伤害。",
    }
    """技能帮助
    """

    state_dict = {
        1:"失神",
        2:"昏迷",
        3:"伟哥",
    }
    """状态表
    """

    state_help = {
        "失神":"失神（ID：1）\n失神检定失败的后果，在1d10分钟内无法行动，技能失效。如果失神期间受到攻击，每次受到攻击失神状态将延长一分钟。",
        "昏迷":"昏迷（ID：2）\n昏迷检定失败的后果，在1d10小时内无法行动，无法被透，技能失效。",
        "伟哥":"伟哥（ID：3）\n一小时内造成的伤害增加1d(30×等级)。",
    }
    """状态帮助
    """

    shop_dict = {
        1:"伟哥",
        2:"伟哥 max mix pro",
        3:"精力药水",
        4:"神奇猫耳",
        5:"自然之种",
        6:"金色光环",
        7:"纹身贴纸",
        8:"心智魔方（去核）",
        9:"嗜血注射器",
        10:"自然蕴息宝珠",
        11:"屹立不倒",
        12:"潘多拉魔盒",
    }
    """商店物品表
    """

    shop_help = {
        "伟哥":"伟哥（ID：1）\n标签上写着：“味道好极了”\n购买后获得/升级状态：伟哥（ID：3）（一小时内造成的伤害增加1d30）",
        "伟哥 max mix pro":"伟哥 max mix pro（ID：2）\n金色瓶装的伟哥\n购买后长度、深度永久增加2cm",
        "精力药水":"精力药水（ID：3）\n一瓶奇怪的乳白色浊液\n购买后回复100HP",
        "神奇猫耳":"神奇猫耳（ID：4）\n柔软的猫耳头饰\n据说带上这个猫耳的顾客都长出了尾巴\n购买后获得/升级技能：猫化（ID：2）",
        "自然之种":"自然之种（ID：5）\n看上去是个果子\n据说吃下去后会在肚子里发芽\n购买后获得/升级技能：自然之心（ID：3）",
        "金色光环":"金色光环（ID：6）\n金色的光环，会漂浮在头上，让人变强\n但是晚上睡觉的时候关不了灯\n购买后获得/升级技能：圣体（ID：4）",
        "纹身贴纸":"纹身贴纸（ID：7）\n和某个器官形状相近的贴纸\n贴在小腹会全身发热，并长出桃心尖尾巴\n购买后获得/升级技能：淫纹（ID：5）",
        "心智魔方（去核）":"心智魔方（去核）（ID：8）\n心智魔方，但是中间的核心不见了\n只能大建出舰装而不是舰娘\n购买后获得/升级技能：舰装（ID：6）",
        "嗜血注射器":"嗜血注射器（ID：9）\n装满红色液体的注射器，打一针就能变成吸血鬼\n但是你以后出门看漫展都得写遗书了\n购买后获得/升级技能：猩红之影（ID：7）",
        "自然蕴息宝珠":"自然蕴息宝珠（ID：10）\n发光的绿色珠子\n看着就让人感到安心\n购买后获得/升级技能：自然蕴息宝珠（ID：8）",
        "屹立不倒":"屹立不倒（ID：11）\n屹（弟）立（弟）不倒！\n使你在失神状态下也能行动\n购买后获得/升级技能：屹立不倒（ID：9）",
        "潘多拉魔盒":"潘多拉魔盒（ID：12）\n收纳诅咒之物\n如果适当地使用，也许并不会带来负面效果\n购买后失去所有【诅咒】技能",
    }
    """商店帮助
    """

    shop_price_dict = {
        1:100,
        2:500,
        3:100,
        4:1000,
        5:1000,
        6:3000,
        7:3000,
        8:9000,
        9:5000,
        10:6666,
        11:8888,
        12:10000,
    }
    """商店价格表
    """
    
    work_dict = {
        1:"搬砖",
        2:"援交",
        3:"直播",
        4:"写文",
        5:"打架",
        6:"探险",
    }
    """工作表
    """
    
    work_help_dict = {
        "搬砖":"搬砖（ID：1）\n需求属性：力量、体质\n普通的工地搬砖\n体力活，不需要太多能力\n虽然赚的不多，但胜在稳定",
        "援交":"援交（ID：2）\n需求属性：技巧、魅力\n又名卖春\n来钱快，但是需要良好的能力，否则顾客是不会满意的\n如果意志较低，可能会进入1d10分钟的失神",
        "直播":"直播（ID：3）\n需求属性：智力、魅力\n网络直播\n把自己的能力展现在网友面前，有可能突然爆火\n会根据属性追加收益",
        "写文":"写文（ID：4）\n需求属性：技巧、智力\n写文，包括H文\n文学的魅力是无穷的，但是得看是谁写的\n需要较高的属性，否则作品将无人问津",
        "打架":"打架（ID：5）\n需求属性：力量、体质\n打架，比如地下擂台\n需要的能力极高，否则是赚不到钱的\n如果体质较低，可能会昏迷",
        "探险":"探险（ID：6）\n需求属性：无\n前往一些奇怪的地方探索\n可能大赚一笔，可能空手而归\n也可能得到一些奇怪的东西,或者提升属性",
    }
    """工作帮助
    """
    
    attribute_dict = {
        "name":"昵称",
        "species":"种族",
        "sex_value":"性别倾向 （暂无作用）",
        "hp_v":"意志HP",
        "hp_c":"体质HP",
        "penis_length":"长度",
        "vagina_depth":"深度",
        "strength":"力量",
        "constitution":"体质",
        "technique":"技巧",
        "volition":"意志",
        "intelligence":"智力",
        "charm":"魅力",
        "money":"金钱",
        "skill":"技能[ID,附加数据]",
        "state":"状态[ID,结束时间]",
        "passive_times":"被动次数",
        "active_times":"主动次数",
        "last_sign_in_time":"上次签到时间",
        "last_operation_time":"上次操作时间",
        "last_refresh_time":"上次数据更新时间",
        "next_work_time":"下次可工作时间",
    }
    """属性表
    """
