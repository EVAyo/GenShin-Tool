import json
import math
import os
import random
import sqlite3
import threading
import time
import urllib
from io import BytesIO
from typing import Optional, Tuple

import numpy as np
from httpx import get
from wordcloud import WordCloud
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pyrogram.types import Message

from defs.db import GetAward, MysSign, GetSignInfo, GetSignList, GetDaily, cacheDB, GetMysInfo, \
    errorDB, GetCharacter, GetInfo, GetSpiralAbyssInfo, MybSign, get_spiral_abyss_info
from defs.event import ys_font

WEAPON_PATH = os.path.join("assets", 'weapon')
BG_PATH = os.path.join("assets", "bg")
CHAR_DONE_PATH = os.path.join("assets", 'char_done')
BG2_PATH = os.path.join("assets", "bg2")
CHAR_PATH = os.path.join("assets", "characters")
CHAR_IMG_PATH = os.path.join("assets", 'char_img')
CHAR_NAMECARD_PATH = os.path.join("assets", 'char_namecard')
REL_PATH = os.path.join("assets", "reliquaries")
avatar_json = {
    "Albedo": "阿贝多",
    "Ambor": "安柏",
    "Barbara": "芭芭拉",
    "Beidou": "北斗",
    "Bennett": "班尼特",
    "Chongyun": "重云",
    "Diluc": "迪卢克",
    "Diona": "迪奥娜",
    "Eula": "优菈",
    "Fischl": "菲谢尔",
    "Ganyu": "甘雨",
    "Hutao": "胡桃",
    "Jean": "琴",
    "Kazuha": "枫原万叶",
    "Kaeya": "凯亚",
    "Ayaka": "神里绫华",
    "Keqing": "刻晴",
    "Klee": "可莉",
    "Lisa": "丽莎",
    "Mona": "莫娜",
    "Ningguang": "凝光",
    "Noel": "诺艾尔",
    "Qiqi": "七七",
    "Razor": "雷泽",
    "Rosaria": "罗莎莉亚",
    "Sucrose": "砂糖",
    "Tartaglia": "达达利亚",
    "Venti": "温迪",
    "Xiangling": "香菱",
    "Xiao": "魈",
    "Xingqiu": "行秋",
    "Xinyan": "辛焱",
    "Yanfei": "烟绯",
    "Zhongli": "钟离",
    "Yoimiya": "宵宫",
    "Sayu": "早柚",
    "Shogun": "雷电将军",
    "Aloy": "埃洛伊",
    "Sara": "九条裟罗",
    "Kokomi": "珊瑚宫心海",
    "Shenhe": "申鹤"
}
daily_im = '''
*数据刷新可能存在一定延迟，请以当前游戏实际数据为准{}
==============
原粹树脂：{}/{}{}
每日委托：{}/{} 奖励{}领取
周本减半：{}/{}
洞天宝钱：{}
探索派遣：
总数/完成/上限：{}/{}/{}
{}'''
month_im = '''
==============
{}
UID：{}
==============
本日获取原石：{}
本日获取摩拉：{}
==============
昨日获取原石：{}
昨日获取摩拉：{}
==============
本月获取原石：{}
本月获取摩拉：{}
==============
上月获取原石：{}
上月获取摩拉：{}
==============
原石收入组成：
{}=============='''


def genshin_font(size):
    return ImageFont.truetype(f"assets{os.sep}fonts{os.sep}yuan_shen.ttf", size=size, encoding="utf-8")


def get_char_img_pic(url: str):
    with open(os.path.join(CHAR_IMG_PATH, url.split(os.sep)[-1]), 'wb') as f:
        f.write(get(url).content)


async def award(uid):
    data = await GetAward(uid)
    nickname = data['data']['nickname']
    day_stone = data['data']['day_data']['current_primogems']
    day_mora = data['data']['day_data']['current_mora']
    lastday_stone = data['data']['day_data']['last_primogems']
    lastday_mora = data['data']['day_data']['last_mora']
    month_stone = data['data']['month_data']['current_primogems']
    month_mora = data['data']['month_data']['current_mora']
    lastmonth_stone = data['data']['month_data']['last_primogems']
    lastmonth_mora = data['data']['month_data']['last_mora']
    group_str = ''
    for i in data['data']['month_data']['group_by']:
        group_str = group_str + \
                    i['action'] + "：" + str(i['num']) + \
                    "（" + str(i['percent']) + "%）" + '\n'

    im = month_im.format(nickname, uid, day_stone, day_mora, lastday_stone, lastday_mora,
                         month_stone, month_mora, lastmonth_stone, lastmonth_mora, group_str)
    return im


# 签到函数
async def sign(uid):
    try:
        # 任务签到
        sign_data = await MysSign(uid)
        sign_info = await GetSignInfo(uid)
        sign_info = sign_info['data']
        sign_list = await GetSignList()
        status = sign_data['message']
        getitem = sign_list['data']['awards'][int(
            sign_info['total_sign_day']) - 1]['name']
        getnum = sign_list['data']['awards'][int(
            sign_info['total_sign_day']) - 1]['cnt']
        get_im = f"本次签到获得{getitem}x{getnum}"
        if status == "OK" and sign_info['is_sign']:
            mes_im = "签到成功"
        else:
            mes_im = status
        sign_missed = sign_info['sign_cnt_missed']
        im = mes_im + "!" + "\n" + get_im + "\n" + f"本月漏签次数：{sign_missed}"
        # 米游币
        im += "\n<code>============</code>\n" + await MybSign(uid)
    except:
        im = "签到失败，请检查Cookies是否失效。"
    return im


# 统计状态函数
async def daily(mode="push", uid=None):
    def seconds2hours(seconds: int) -> str:
        m, s = divmod(int(seconds), 60)
        h, m = divmod(m, 60)
        return "%02d:%02d:%02d" % (h, m, s)

    temp_list = []
    conn = sqlite3.connect('ID_DATA.db')
    c = conn.cursor()
    if mode == "ask":
        c_data = ([uid, 0, 0, 0, 0, 0, 0],)
    else:
        cursor = c.execute(
            "SELECT *  FROM NewCookiesTable WHERE StatusA != ?", ("off",))
        c_data = cursor.fetchall()

    for row in c_data:
        raw_data = await GetDaily(str(row[0]))
        if raw_data["retcode"] != 0:
            temp_list.append(
                {"qid": row[2], "gid": row[3], "message": "你的推送状态有误；可能是uid绑定错误或没有在米游社打开“实时便筏”功能。"})
        else:
            dailydata = raw_data["data"]
            current_resin = dailydata['current_resin']

            current_expedition_num = dailydata['current_expedition_num']
            max_expedition_num = dailydata['max_expedition_num']
            finished_expedition_num = 0
            expedition_info: list[str] = []
            for expedition in dailydata['expeditions']:
                avatar: str = expedition['avatar_side_icon'][89:-4]
                try:
                    avatar_name: str = avatar_json[avatar]
                except KeyError:
                    avatar_name: str = avatar

                if expedition['status'] == 'Finished':
                    expedition_info.append(f"{avatar_name} 探索完成")
                    finished_expedition_num += 1
                else:
                    remained_timed: str = seconds2hours(
                        expedition['remained_time'])
                    expedition_info.append(
                        f"{avatar_name} 剩余时间{remained_timed}")

            if current_resin >= row[6] or dailydata["max_home_coin"] - dailydata[
                "current_home_coin"] <= 100 or finished_expedition_num > 0:
                tip = ''

                if current_resin >= row[6] != 0:
                    tip += "\n==============\n你的树脂快满了！"
                if dailydata["max_home_coin"] - dailydata["current_home_coin"] <= 100:
                    tip += "\n==============\n你的洞天宝钱快满了！"
                if finished_expedition_num > 0:
                    tip += "\n==============\n你有探索派遣完成了！"
                max_resin = dailydata['max_resin']
                rec_time = ''
                # print(dailydata)
                if current_resin < 160:
                    resin_recovery_time = seconds2hours(
                        dailydata['resin_recovery_time'])
                    next_resin_rec_time = seconds2hours(
                        8 * 60 - ((dailydata['max_resin'] - dailydata['current_resin']) * 8 * 60 - int(
                            dailydata['resin_recovery_time'])))
                    rec_time = f' ({next_resin_rec_time}/{resin_recovery_time})'

                finished_task_num = dailydata['finished_task_num']
                total_task_num = dailydata['total_task_num']
                is_extra_got = '已' if dailydata['is_extra_task_reward_received'] else '未'

                resin_discount_num_limit = dailydata['resin_discount_num_limit']
                used_resin_discount_num = resin_discount_num_limit - \
                                          dailydata['remain_resin_discount_num']

                coin = f'{dailydata["current_home_coin"]}/{dailydata["max_home_coin"]}'
                if dailydata["current_home_coin"] < dailydata["max_home_coin"]:
                    coin_rec_time = seconds2hours(int(dailydata["home_coin_recovery_time"]))
                    coin_add_speed = math.ceil((dailydata["max_home_coin"] - dailydata["current_home_coin"]) / (
                            int(dailydata["home_coin_recovery_time"]) / 60 / 60))
                    coin += f'（{coin_rec_time} 约{coin_add_speed}/h）'

                expedition_data = "\n".join(expedition_info)
                send_mes = daily_im.format(tip, current_resin, max_resin, rec_time, finished_task_num, total_task_num,
                                           is_extra_got, used_resin_discount_num,
                                           resin_discount_num_limit, coin, current_expedition_num,
                                           finished_expedition_num, max_expedition_num, expedition_data)

                temp_list.append(
                    {"qid": row[2], "gid": row[3], "message": send_mes})
    return temp_list


def create_rounded_rectangle_mask(rectangle, radius):
    solid_fill = (50, 50, 50, 255)
    i = Image.new("RGBA", rectangle.size, (0, 0, 0, 0))

    corner = Image.new('RGBA', (radius, radius), (0, 0, 0, 0))
    draw = ImageDraw.Draw(corner)
    draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=solid_fill)

    mx, my = rectangle.size

    i.paste(corner, (0, 0), corner)
    i.paste(corner.rotate(90), (0, my - radius), corner.rotate(90))
    i.paste(corner.rotate(180), (mx - radius, my - radius), corner.rotate(180))
    i.paste(corner.rotate(270), (mx - radius, 0), corner.rotate(270))

    draw = ImageDraw.Draw(i)
    draw.rectangle([(radius, 0), (mx - radius, my)], fill=solid_fill)
    draw.rectangle([(0, radius), (mx, my - radius)], fill=solid_fill)

    return i


def get_weapon_pic(url):
    urllib.request.urlretrieve(url, os.path.join(WEAPON_PATH, url.split('/')[-1]))


def get_char_pic(id, url):
    urllib.request.urlretrieve(f'{url}', os.path.join(CHAR_PATH, f'{id}.png'))


def get_charimg_pic(url):
    urllib.request.urlretrieve(url, os.path.join(CHAR_IMG_PATH, url.split('/')[-1]))


def get_rel_pic(url):
    urllib.request.urlretrieve(url, os.path.join(REL_PATH, url.split('/')[-1]))


async def draw_pic(uid, message: Message, nickname="1", mode=2, role_level=None):
    # 获取Cookies，如果没有能使用的则return
    while 1:
        use_cookies = cacheDB(uid, mode - 1)
        if use_cookies == '':
            return "绑定记录不存在。"
        elif use_cookies == "没有可以使用的Cookies！":
            return "没有可以使用的Cookies！"

        if mode == 3:
            mys_data = await GetMysInfo(uid, use_cookies)
            mysid_data = uid
            for i in mys_data['data']['list']:
                if i['game_id'] != 2:
                    mys_data['data']['list'].remove(i)
            uid = mys_data['data']['list'][0]['game_role_id']
            nickname = mys_data['data']['list'][0]['nickname']
            role_level = mys_data['data']['list'][0]['level']

        raw_data = await GetInfo(uid, use_cookies)

        if raw_data["retcode"] != 0:
            if raw_data["retcode"] == 10001:
                # return ("Cookie错误/过期，请重置Cookie")
                errorDB(use_cookies, "error")
            elif raw_data["retcode"] == 10101:
                # return ("当前cookies已达到30人上限！")
                errorDB(use_cookies, "limit30")
            elif raw_data["retcode"] == 10102:
                return "当前查询id已经设置了隐私，无法查询！"
            else:
                return (
                        "Api报错，返回内容为：\r\n"
                        + str(raw_data) + "\r\n出现这种情况可能的UID输入错误 or 不存在"
                )
        else:
            break

    # 获取背景图片
    bg2_path = os.path.join(BG_PATH, random.choice([x for x in os.listdir(BG_PATH)
                                                    if os.path.isfile(os.path.join(BG_PATH, x))]))

    if message.media:
        image_data = await message.download()
        edit_bg = Image.open(image_data)
    else:
        edit_bg = Image.open(bg2_path)

    # 获取背景主色
    q = edit_bg.quantize(colors=3, method=2)
    bg_num_temp = 0
    for i in range(0, 3):
        bg = tuple(q.getpalette()[i * 3:(i * 3) + 3])
        bg_num = bg[0] + bg[1] + bg[2]
        if bg_num >= bg_num_temp:
            bg_num_temp = bg_num
            bg_color = (bg[0], bg[1], bg[2])

    # 通过背景主色（bg_color）确定文字主色
    r = 140
    if max(*bg_color) > 255 - r:
        r *= -1
    new_color = (math.floor(bg_color[0] + r if bg_color[0] + r <= 255 else 255),
                 math.floor(bg_color[1] + r if bg_color[1] + r <= 255 else 255),
                 math.floor(bg_color[2] + r if bg_color[2] + r <= 255 else 255))

    # 确定texture2D路径
    panle1_path = os.path.join(BG2_PATH, "panle_1.png")
    panle3_path = os.path.join(BG2_PATH, "panle_3.png")

    avatar_bg_path = os.path.join(BG2_PATH, "avatar_bg.png")
    avatar_fg_path = os.path.join(BG2_PATH, "avatar_fg.png")

    all_mask_path = os.path.join(BG2_PATH, "All_Mask.png")

    # 记录数据
    raw_data = raw_data['data']
    char_data = raw_data["avatars"]

    char_datas = []
    char_ids = []
    char_rawdata = []

    for i in char_data:
        char_ids.append(i["id"])

    char_rawdata = GetCharacter(uid, char_ids, use_cookies)
    char_datas = char_rawdata["data"]["avatars"]

    # 确定角色占用行数
    char_num = len(char_datas)
    char_hang = 1 + (char_num - 1) // 6 if char_num > 8 else char_num

    # 确定整体图片的长宽
    based_w = 900
    based_h = 890 + char_hang * 130 if char_num > 8 else 890 + char_hang * 110
    based_scale = '%.3f' % (based_w / based_h)

    # 通过确定的长宽比，缩放背景图片
    w, h = edit_bg.size
    scale_f = '%.3f' % (w / h)
    new_w = math.ceil(based_h * float(scale_f))
    new_h = math.ceil(based_w / float(scale_f))
    if scale_f > based_scale:
        bg_img2 = edit_bg.resize((new_w, based_h), Image.ANTIALIAS)
    else:
        bg_img2 = edit_bg.resize((based_w, new_h), Image.ANTIALIAS)
    bg_img = bg_img2.crop((0, 0, 900, based_h))

    # 转换遮罩的颜色、大小匹配，并paste上去
    all_mask = Image.open(all_mask_path).resize(bg_img.size, Image.ANTIALIAS)
    all_mask_img = Image.new("RGBA", (based_w, based_h), bg_color)
    bg_img.paste(all_mask_img, (0, 0), all_mask)

    # 操作图片
    panle1 = Image.open(panle1_path)
    panle3 = Image.open(panle3_path)
    avatar_bg = Image.open(avatar_bg_path)
    avatar_fg = Image.open(avatar_fg_path)

    # 确定主体框架
    avatar_bg_color = Image.new("RGBA", (316, 100), bg_color)
    panle1_color = Image.new("RGBA", (900, 800), new_color)
    bg_img.paste(panle1_color, (0, 0), panle1)
    bg_img.paste(panle3, (0, char_hang * 130 + 800) if char_num > 8 else (0, char_hang * 110 + 800), panle3)
    bg_img.paste(avatar_bg_color, (113, 98), avatar_bg)
    bg_img.paste(avatar_fg, (114, 95), avatar_fg)

    # 绘制基础信息文字
    text_draw = ImageDraw.Draw(bg_img)

    if role_level:
        text_draw.text((140, 200), "冒险等级：" + f"{role_level}", new_color, ys_font(20))

    text_draw.text((220, 123), f"{nickname}", new_color, ys_font(32))
    text_draw.text((235, 163), 'UID ' + f"{uid}", new_color, ys_font(14))

    # 活跃天数/成就数量/深渊信息
    text_draw.text((640, 94.8), str(raw_data['stats']['active_day_number']), new_color, ys_font(26))
    text_draw.text((640, 139.3), str(raw_data['stats']['achievement_number']), new_color, ys_font(26))
    text_draw.text((640, 183.9), raw_data['stats']['spiral_abyss'], new_color, ys_font(26))

    # 宝箱
    text_draw.text((258, 375.4), str(raw_data['stats']['magic_chest_number']), new_color, ys_font(24))
    text_draw.text((258, 425.4), str(raw_data['stats']['common_chest_number']), new_color, ys_font(24))
    text_draw.text((258, 475.4), str(raw_data['stats']['exquisite_chest_number']), new_color, ys_font(24))
    text_draw.text((258, 525.4), str(raw_data['stats']['precious_chest_number']), new_color, ys_font(24))
    text_draw.text((258, 575.4), str(raw_data['stats']['luxurious_chest_number']), new_color, ys_font(24))

    # 已获角色
    text_draw.text((740, 547), str(raw_data['stats']['avatar_number']), new_color, ys_font(24))

    # 开启锚点和秘境数量
    text_draw.text((258, 625.4), str(raw_data['stats']['way_point_number']), new_color, ys_font(24))
    text_draw.text((258, 675.4), str(raw_data['stats']['domain_number']), new_color, ys_font(24))

    # 蒙德
    text_draw.text((490, 370), str(raw_data['world_explorations'][4]['exploration_percentage'] / 10) + '%', new_color,
                   ys_font(22))
    text_draw.text((490, 400), 'lv.' + str(raw_data['world_explorations'][4]['level']), new_color, ys_font(22))
    text_draw.text((513, 430), str(raw_data['stats']['anemoculus_number']), new_color, ys_font(22))

    # 璃月
    text_draw.text((490, 490), str(raw_data['world_explorations'][3]['exploration_percentage'] / 10) + '%', new_color,
                   ys_font(22))
    text_draw.text((490, 520), 'lv.' + str(raw_data['world_explorations'][3]['level']), new_color, ys_font(22))
    text_draw.text((513, 550), str(raw_data['stats']['geoculus_number']), new_color, ys_font(22))

    # 雪山
    text_draw.text((745, 373.5), str(raw_data['world_explorations'][2]['exploration_percentage'] / 10) + '%', new_color,
                   ys_font(22))
    text_draw.text((745, 407.1), 'lv.' + str(raw_data['world_explorations'][2]['level']), new_color, ys_font(22))

    # 稻妻
    text_draw.text((490, 608), str(raw_data['world_explorations'][1]['exploration_percentage'] / 10) + '%', new_color,
                   ys_font(22))
    text_draw.text((490, 635), 'lv.' + str(raw_data['world_explorations'][1]['level']), new_color, ys_font(22))
    text_draw.text((490, 662), 'lv.' + str(raw_data['world_explorations'][1]['offerings'][0]['level']), new_color,
                   ys_font(22))
    text_draw.text((513, 689), str(raw_data['stats']['electroculus_number']), new_color, ys_font(22))

    # 渊下宫
    text_draw.text((745, 480), str(raw_data['world_explorations'][0]['exploration_percentage'] / 10) + '%', new_color,
                   ys_font(22))

    # 家园
    if len(raw_data['homes']):
        text_draw.text((693, 582.4), 'lv.' + str(raw_data['homes'][0]['level']), new_color, ys_font(22))
        text_draw.text((693, 620.4), str(raw_data['homes'][0]['visit_num']), new_color, ys_font(22))
        text_draw.text((693, 658.4), str(raw_data['homes'][0]['item_num']), new_color, ys_font(22))
        text_draw.text((693, 696.4), str(raw_data['homes'][0]['comfort_num']), new_color, ys_font(22))
    else:
        text_draw.text((693, 582.4), "未开", new_color, ys_font(22))
        text_draw.text((693, 620.4), "未开", new_color, ys_font(22))
        text_draw.text((693, 658.4), "未开", new_color, ys_font(22))
        text_draw.text((693, 696.4), "未开", new_color, ys_font(22))

    # 确定texture2D路径
    charpic_mask_path = os.path.join(BG2_PATH, "charpic_mask.png")
    weaponpic_mask_path = os.path.join(BG2_PATH, "weaponpic_mask.png")

    def getText(star, step):
        return os.path.join(BG2_PATH, "{}s_{}.png".format(str(star), str(step)))

    charpic_mask = Image.open(charpic_mask_path)
    weaponpic_mask = Image.open(weaponpic_mask_path)
    s5s1 = Image.open(getText(5, 1))
    s5s2 = Image.open(getText(5, 2))
    s5s3 = Image.open(getText(5, 3))
    s5s4 = Image.open(getText(5, 4))
    s4s1 = Image.open(getText(4, 1))
    s4s2 = Image.open(getText(4, 2))
    s4s3 = Image.open(getText(4, 3))
    s4s4 = Image.open(getText(4, 4))
    s3s3 = Image.open(getText(3, 3))
    s2s3 = Image.open(getText(2, 3))
    s1s3 = Image.open(getText(1, 3))

    char_bg_path = os.path.join(BG2_PATH, "char_bg.png")
    char_fg_path = os.path.join(BG2_PATH, "char_fg.png")

    char_bg = Image.open(char_bg_path)
    char_fg = Image.open(char_fg_path)

    char_color = (math.floor(bg_color[0] + 10 if bg_color[0] + r <= 255 else 255),
                  math.floor(bg_color[1] + 10 if bg_color[1] + r <= 255 else 255),
                  math.floor(bg_color[2] + 10 if bg_color[2] + r <= 255 else 255))

    charset_mask = Image.new("RGBA", (900, 130), char_color)

    num = 0
    char_datas.sort(key=lambda x: (-x['rarity'], -x['level'], -x['fetter']))

    if char_num > 8:
        for i in char_datas:
            char_mingzuo = 0
            for k in i['constellations']:
                if k['is_actived']:
                    char_mingzuo += 1

            char_name = i["name"]
            char_id = i["id"]
            char_level = i["level"]
            char_fetter = i['fetter']
            char_rarity = i['rarity']

            char_weapon_star = i['weapon']['rarity']
            char_weapon_jinglian = i['weapon']['affix_level']
            char_weapon_icon = i['weapon']['icon']

            if not os.path.exists(os.path.join(WEAPON_PATH, str(char_weapon_icon.split('/')[-1]))):
                get_weapon_pic(char_weapon_icon)
            if not os.path.exists(os.path.join(CHAR_PATH, str(i['id']) + ".png")):
                get_char_pic(i['id'], i['icon'])

            char = os.path.join(CHAR_PATH, str(char_id) + ".png")
            weapon = os.path.join(WEAPON_PATH, str(char_weapon_icon.split('/')[-1]))

            char_img = Image.open(char)
            char_img = char_img.resize((100, 100), Image.ANTIALIAS)
            weapon_img = Image.open(weapon)
            weapon_img = weapon_img.resize((47, 47), Image.ANTIALIAS)

            charpic = Image.new("RGBA", (125, 140))

            if char_rarity == 5:
                charpic.paste(s5s1, (0, 0), s5s1)
                baseda = Image.new("RGBA", (100, 100))
                cc = Image.composite(char_img, baseda, charpic_mask)
                charpic.paste(cc, (6, 15), cc)
                charpic.paste(s5s2, (0, 0), s5s2)
                if char_weapon_star == 5:
                    charpic.paste(s5s3, (0, 0), s5s3)
                elif char_weapon_star == 4:
                    charpic.paste(s4s3, (0, 0), s4s3)
                elif char_weapon_star == 3:
                    charpic.paste(s3s3, (0, 0), s3s3)
                elif char_weapon_star == 2:
                    charpic.paste(s2s3, (0, 0), s2s3)
                elif char_weapon_star == 1:
                    charpic.paste(s1s3, (0, 0), s1s3)
                basedb = Image.new("RGBA", (47, 47))
                dd = Image.composite(weapon_img, basedb, weaponpic_mask)
                charpic.paste(dd, (69, 62), dd)
                charpic.paste(s5s4, (0, 0), s5s4)

            else:
                charpic.paste(s4s1, (0, 0), s4s1)
                baseda = Image.new("RGBA", (100, 100))
                cc = Image.composite(char_img, baseda, charpic_mask)
                charpic.paste(cc, (6, 15), cc)
                charpic.paste(s4s2, (0, 0), s4s2)
                if char_weapon_star == 5:
                    charpic.paste(s5s3, (0, 0), s5s3)
                elif char_weapon_star == 4:
                    charpic.paste(s4s3, (0, 0), s4s3)
                elif char_weapon_star == 3:
                    charpic.paste(s3s3, (0, 0), s3s3)
                elif char_weapon_star == 2:
                    charpic.paste(s2s3, (0, 0), s2s3)
                elif char_weapon_star == 1:
                    charpic.paste(s1s3, (0, 0), s1s3)
                basedb = Image.new("RGBA", (47, 47))
                dd = Image.composite(weapon_img, basedb, weaponpic_mask)
                charpic.paste(dd, (69, 62), dd)
                charpic.paste(s4s4, (0, 0), s4s4)

            char_draw = ImageDraw.Draw(charpic)
            char_draw.text((38, 106), f'Lv.{str(char_level)}', (21, 21, 21), ys_font(18))
            char_draw.text((104.5, 91.5), f'{str(char_weapon_jinglian)}', 'white', ys_font(10))
            char_draw.text((99, 19.5), f'{str(char_mingzuo)}', 'white', ys_font(18))
            if str(i["fetter"]) == "10" or str(char_name) == "旅行者":
                char_draw.text((98, 42), "♥", (21, 21, 21), ys_font(14))
            else:
                char_draw.text((100, 41), f'{str(char_fetter)}', (21, 21, 21), ys_font(16))

            char_crop = (68 + 129 * (num % 6), 800 + 130 * (num // 6))
            bg_img.paste(charpic, char_crop, charpic)
            num = num + 1
    else:
        for i in char_datas:
            char_mingzuo = 0
            for k in i['constellations']:
                if k['is_actived']:
                    char_mingzuo += 1

            char_name = i["name"]
            char_id = i["id"]
            char_level = i["level"]
            char_fetter = i['fetter']
            char_rarity = i['rarity']
            char_img_icon = i["image"]

            char_weapon_star = i['weapon']['rarity']
            char_weapon_level = i['weapon']['level']
            char_weapon_jinglian = i['weapon']['affix_level']
            char_weapon_icon = i['weapon']['icon']

            if not os.path.exists(os.path.join(WEAPON_PATH, str(char_weapon_icon.split('/')[-1]))):
                get_weapon_pic(char_weapon_icon)
            if not os.path.exists(os.path.join(CHAR_IMG_PATH, str(char_img_icon.split('/')[-1]))):
                get_charimg_pic(char_img_icon)
            if not os.path.exists(os.path.join(CHAR_PATH, str(i['id']) + ".png")):
                get_char_pic(i['id'], i['icon'])

            char = os.path.join(CHAR_PATH, str(char_id) + ".png")
            weapon = os.path.join(WEAPON_PATH, str(char_weapon_icon.split('/')[-1]))
            char_stand_img = os.path.join(CHAR_IMG_PATH, str(char_img_icon.split('/')[-1]))
            char_stand_mask = Image.open(os.path.join(BG2_PATH, "stand_mask.png"))

            char_stand = Image.open(char_stand_img)
            char_img = Image.open(char)
            char_img = char_img.resize((100, 100), Image.ANTIALIAS)
            weapon_img = Image.open(weapon)
            weapon_img = weapon_img.resize((47, 47), Image.ANTIALIAS)

            charpic = Image.new("RGBA", (900, 130))
            charpic_temp = Image.new("RGBA", (900, 130))

            charpic.paste(charset_mask, (0, 0), char_bg)

            weapon_bg = Image.open(getText(char_weapon_star, 3))
            charpic.paste(weapon_bg, (72, 10), weapon_bg)
            charpic_temp.paste(char_img, (81, 13), charpic_mask)
            charpic_temp.paste(char_stand, (395, -99), char_stand_mask)
            charpic_temp.paste(char_fg, (0, 0), char_fg)
            charpic_temp.paste(weapon_img, (141, 72), weaponpic_mask)
            # temp = Image.composite(weapon_img, basedb, weaponpic_mask)
            charpic.paste(charpic_temp, (0, 0), charpic_temp)

            for _, k in enumerate(i["reliquaries"]):
                if not os.path.exists(os.path.join(REL_PATH, str(k["icon"].split('/')[-1]))):
                    get_rel_pic(k["icon"])
                rel = os.path.join(REL_PATH, str(k["icon"].split('/')[-1]))
                rel_img = Image.open(rel).resize((43, 43), Image.ANTIALIAS)
                rel_bg = Image.open(getText(k["rarity"], 3))

                if k["pos_name"] == "生之花":
                    charpic.paste(rel_bg, (287 + 55 * 0, -14), rel_bg)
                    charpic.paste(rel_img, (360 + 55 * 0, 49), rel_img)
                elif k["pos_name"] == "死之羽":
                    charpic.paste(rel_bg, (287 + 55 * 1, -14), rel_bg)
                    charpic.paste(rel_img, (360 + 55 * 1, 49), rel_img)
                elif k["pos_name"] == "时之沙":
                    charpic.paste(rel_bg, (287 + 55 * 2, -14), rel_bg)
                    charpic.paste(rel_img, (360 + 55 * 2, 49), rel_img)
                elif k["pos_name"] == "空之杯":
                    charpic.paste(rel_bg, (287 + 55 * 3, -14), rel_bg)
                    charpic.paste(rel_img, (360 + 55 * 3, 49), rel_img)
                elif k["pos_name"] == "理之冠":
                    charpic.paste(rel_bg, (287 + 55 * 4, -14), rel_bg)
                    charpic.paste(rel_img, (360 + 55 * 4, 49), rel_img)

            char_draw = ImageDraw.Draw(charpic)

            char_draw.text((188, 30), i["name"] + " " + f'Lv.{str(char_level)}', new_color, ys_font(22))
            # char_draw.text((272, 45), f'Lv.{str(char_level)}', new_color, ys_font(18))

            # char_draw.text((104.5,91.5),f'{str(char_weapon_jinglian)}',new_color,ys_font(10))
            char_draw.text((267, 77), f'{str(char_mingzuo)}', new_color, ys_font(18))

            char_draw.text((222, 87), f'{str(i["fetter"])}' if str(char_name) != "旅行者" else "10", new_color,
                           ys_font(15), anchor="mm")
            char_draw.text((255, 87), f'{str(char_mingzuo)}', new_color, ys_font(15), anchor="mm")
            char_draw.text((218, 67), f'{str(char_weapon_level)}级{str(char_weapon_jinglian)}精', new_color, ys_font(15),
                           anchor="lm")
            char_crop = (0, 800 + 110 * num)
            num += 1
            bg_img.paste(charpic, char_crop, charpic)

    # 转换之后发送
    bg_img = bg_img.convert('RGB')
    bg_img.save(f"temp{os.sep}uid.jpg", format='JPEG', subsampling=0, quality=90)
    try:
        if message.media:
            os.remove(image_data)  # noqa
    except:
        pass
    return f"temp{os.sep}uid.jpg"


async def draw_wordcloud(uid, message: Message, mode=2):
    while 1:
        use_cookies = cacheDB(uid, mode - 1)
        if use_cookies == '':
            return "绑定记录不存在。"
        elif use_cookies == "没有可以使用的Cookies！":
            return "没有可以使用的Cookies！"

        if mode == 3:
            mys_data = await GetMysInfo(uid, use_cookies)
            mysid_data = uid
            for i in mys_data['data']['list']:
                if i['game_id'] != 2:
                    mys_data['data']['list'].remove(i)
            uid = mys_data['data']['list'][0]['game_role_id']
            nickname = mys_data['data']['list'][0]['nickname']
            role_level = mys_data['data']['list'][0]['level']
            raw_data = await GetInfo(uid, use_cookies)
            raw_Abyss_data = await GetSpiralAbyssInfo(uid, use_cookies)
        else:
            raw_Abyss_data = await GetSpiralAbyssInfo(uid, use_cookies)
            raw_data = await GetInfo(uid, use_cookies)

        if raw_data["retcode"] != 0:
            if raw_data["retcode"] == 10001:
                # return ("Cookie错误/过期，请重置Cookie")
                errorDB(use_cookies, "error")
            elif raw_data["retcode"] == 10101:
                # return ("当前cookies已达到30人上限！")
                errorDB(use_cookies, "limit30")
            elif raw_data["retcode"] == 10102:
                return "当前查询id已经设置了隐私，无法查询！"
            else:
                return (
                        "Api报错，返回内容为：\r\n"
                        + str(raw_data) + "\r\n出现这种情况可能的UID输入错误 or 不存在"
                )
        else:
            break

    raw_Abyss_data = raw_Abyss_data['data']
    raw_data = raw_data['data']

    char_data = raw_data["avatars"]
    char_num = len(raw_data["avatars"])

    char_datas = []

    def get_charid(start, end):
        for i in range(start, end):
            char_rawdata = GetCharacter(uid, [i], use_cookies)

            if char_rawdata["retcode"] == -1:
                pass
            else:
                char_datas.append(char_rawdata["data"]['avatars'][0])

    thread_list = []
    st = 8
    for i in range(0, 8):
        thread = threading.Thread(target=get_charid, args=(10000002 + i * st, 10000002 + (i + 1) * st))
        thread_list.append(thread)

    for t in thread_list:
        t.setDaemon(True)
        t.start()

    for t in thread_list:
        t.join()

    weapons_datas = []
    for i in char_datas:
        weapons_datas.append(i['weapon'])

    l1_size = 2
    l2_size = 4
    l3_size = 6
    l4_size = 7
    l5_size = 10

    word_str = {}

    star4weapon = 0
    star5weapon = 0
    star5weaponcon = 0
    star3weapon = 0
    for i in weapons_datas:
        if i['rarity'] == 5:
            star5weapon += 1
            star5weaponcon += i['affix_level']
        elif i['rarity'] == 4:
            star4weapon += 1
        elif i['rarity'] == 3:
            star4weapon += 1

    g3d1 = 0
    ly3c = 0
    star5num = 0
    star5numcon = 0

    for i in char_datas:
        if i["name"] in ['雷电将军', '温迪', '钟离', '枫原万叶']:
            g3d1 += 1
        if i["name"] in ['甘雨', '魈', '胡桃']:
            ly3c += 1
        if i['rarity'] == 5:
            star5num += 1
            if i['name'] != '旅行者':
                star5numcon += 1 + i['actived_constellation_num']

        if i["level"] >= 80:
            if i['name'] == "迪卢克":
                word_str["落魄了家人们"] = l3_size
            if i['name'] == "刻晴":
                word_str["斩尽牛杂"] = l3_size
            if i['name'] == "旅行者":
                word_str["旅行者真爱党"] = l3_size

        if i['actived_constellation_num'] == 6:
            if i['rarity'] == 5:
                if i['name'] == "旅行者":
                    word_str["满命{}".format(i['name'])] = l1_size
                if i['name'] == "魈":
                    word_str['魈深氪的救赎'] = l5_size
                if i['name'] == "甘雨":
                    word_str['璃月自走归终机'] = l5_size
                if i['name'] == "胡桃":
                    word_str['一波送走全送走'] = l5_size
                else:
                    word_str["满命{}".format(i['name'])] = l5_size
            else:
                word_str["满命{}".format(i['name'])] = l2_size

    game_time = time.mktime(time.strptime('20200915', '%Y%m%d'))
    now_time = time.time()
    total_s = now_time - game_time
    total_d = (((total_s) / 60) / 60) / 24

    if math.floor(total_d) - 5 <= raw_data['stats']['active_day_number']:
        word_str["开服玩家"] = l4_size

    if g3d1 >= 4:
        word_str["三神一帝"] = l3_size
    if ly3c >= 3:
        word_str["璃月3C"] = l3_size
    if star5num >= 16:
        word_str["五星众多"] = l3_size

    if len(weapons_datas) - star4weapon <= 3:
        word_str["武器基本四星"] = l3_size

    try:
        if raw_data['stats']['achievement_number'] // (star5weaponcon + star5numcon) >= 23:
            word_str["平民玩家"] = l2_size
        elif raw_data['stats']['achievement_number'] // (star5weaponcon + star5numcon) <= 15:
            word_str["氪金玩家"] = l3_size
    except ZeroDivisionError:
        # print("不存在五星武器")
        word_str["平民玩家"] = l2_size

    if raw_data['stats']['anemoculus_number'] + raw_data['stats']['geoculus_number'] + raw_data['stats'][
        'electroculus_number'] == 378:
        word_str["全神瞳"] = l2_size
    if raw_data['world_explorations'][3]['exploration_percentage'] + raw_data['world_explorations'][2][
        'exploration_percentage'] + raw_data['world_explorations'][1]['exploration_percentage'] + \
            raw_data['world_explorations'][0]['exploration_percentage'] >= 3950:
        word_str["全探索"] = l4_size
    if raw_data['stats']['achievement_number'] >= 510:
        word_str["全成就"] = l5_size
    elif raw_data['stats']['achievement_number'] >= 490:
        word_str["成就达人"] = l3_size
    if raw_data['stats']['spiral_abyss'] == '12-3':
        word_str["深境的探究者"] = l2_size
    if len(raw_data['avatars']) >= 42:
        word_str["全角色"] = l3_size

    if raw_data['stats']['active_day_number'] <= 40:
        word_str["刚入坑"] = l1_size
    elif raw_data['stats']['active_day_number'] <= 100:
        word_str["初心者"] = l2_size
    elif raw_data['stats']['active_day_number'] <= 300:
        word_str["老玩家"] = l2_size
    if raw_data['stats']['active_day_number'] >= 365 and raw_data['stats']['magic_chest_number'] + raw_data['stats'][
        'common_chest_number'] + raw_data['stats']['exquisite_chest_number'] + raw_data['stats'][
        'precious_chest_number'] + raw_data['stats']['luxurious_chest_number'] <= 2500:
        word_str["老咸鱼"] = l3_size
    if raw_data['stats']['magic_chest_number'] >= 46:
        word_str["迷失在黑夜里"] = l2_size
    if raw_data['homes'][0]['comfort_num'] >= 25000:
        word_str["团雀附体"] = l2_size

    if raw_Abyss_data["reveal_rank"] != []:
        if raw_Abyss_data['total_battle_times'] <= 12 and raw_Abyss_data['max_floor'] == '12-3':
            word_str["PVP资格证"] = l4_size
        if raw_Abyss_data["damage_rank"][0]["value"] >= 150000:
            word_str["这一击，贯穿星辰"] = l4_size
    else:
        pass

    bg_list = random.choice([x for x in os.listdir(BG_PATH)
                             if os.path.isfile(os.path.join(BG_PATH, x))])

    bg2_path = os.path.join(BG_PATH, bg_list)

    based_w = 900
    based_h = 1000
    based_scale = '%.3f' % (based_w / based_h)

    is_edit = False
    if message.media:
        is_edit = await message.download()

    if is_edit:
        bg_path_edit = is_edit
    else:
        bg_path_edit = bg2_path

    edit_bg = Image.open(bg_path_edit)
    w, h = edit_bg.size
    scale_f = '%.3f' % (w / h)
    new_w = math.ceil(based_h * float(scale_f))
    new_h = math.ceil(based_w / float(scale_f))
    if scale_f > based_scale:
        bg_img2 = edit_bg.resize((new_w, based_h), Image.ANTIALIAS)
    else:
        bg_img2 = edit_bg.resize((based_w, new_h), Image.ANTIALIAS)

    bg_img = bg_img2.crop((0, 0, based_w, based_h))

    x, y = 50, 153
    radius = 50
    cropped_img = bg_img.crop((x, y, x + 800, y + 800))
    blurred_img = cropped_img.filter(ImageFilter.GaussianBlur(5), ).convert("RGBA")
    bg_img.paste(blurred_img, (x, y), create_rounded_rectangle_mask(cropped_img, radius))

    panle = Image.open(os.path.join(BG2_PATH, 'wordcloud_0.png'))

    mask = np.array(Image.open(os.path.join(BG2_PATH, 'wordcloudmask.png')))

    wc = WordCloud(
        font_path=os.path.join("assets", "fonts", "ZhuZiAWan-2.ttc"),
        mask=mask,
        background_color="rgba(255, 255, 255, 0)",
        mode="RGBA",
        max_words=200,
        max_font_size=80
        # color_func=multi_color_func
        # color_func=similar_color_func
    ).generate_from_frequencies(word_str, max_font_size=100)

    image_produce = wc.to_image()

    bg_img.paste(panle, (0, 0), panle)
    bg_img.paste(image_produce, (0, 0), image_produce)
    bg_img = bg_img.convert('RGB')

    text_draw = ImageDraw.Draw(bg_img)
    text_draw.text((450, 105), 'UID ' + f"{uid}", (40, 136, 168), ys_font(26), anchor="mm")

    bg_img.save(f"temp{os.sep}cx.jpg", format='JPEG', subsampling=0, quality=90)
    if is_edit:
        try:
            os.remove(is_edit)
        except:
            pass
    return f"temp{os.sep}cx.jpg"


class GetCookies:
    def __init__(self) -> None:
        self.useable_cookies: Optional[str] = None
        self.uid: Optional[str] = None
        self.mode: Optional[int] = None
        self.raw_abyss_data: Optional[json] = None
        self.raw_data: Optional[json] = None
        self.nickname: Optional[int] = None
        self.schedule_type: Optional[str] = None

    async def get_useable_cookies(self, uid: str, mode: int = 2, schedule_type: str = "1"):
        self.uid = uid
        self.schedule_type = schedule_type
        while True:
            self.useable_cookies = cacheDB(uid, mode - 1)
            if self.useable_cookies == '':
                return "绑定记录不存在。"
            elif self.useable_cookies == "没有可以使用的Cookies！":
                return "没有可以使用的Cookies！"
            if mode == 3:
                await self.get_mihoyo_bbs_data()
            else:
                await self.get_uid_data()

            msg = await self.check_cookies_useable()
            if isinstance(msg, str):
                return msg
            elif isinstance(msg, bool):
                if msg:
                    return True

    async def get_mihoyo_bbs_data(self):
        mys_data = await GetMysInfo(self.uid, self.useable_cookies)
        for i in mys_data['data']['list']:
            if i['game_id'] != 2:
                mys_data['data']['list'].remove(i)
        self.uid = mys_data['data']['list'][0]['game_role_id']
        self.nickname = mys_data['data']['list'][0]['nickname']
        self.raw_data = await GetInfo(self.uid, self.useable_cookies)
        self.raw_abyss_data = await get_spiral_abyss_info(self.uid, self.useable_cookies, self.schedule_type)

    async def get_uid_data(self):
        self.raw_abyss_data = await get_spiral_abyss_info(self.uid, self.useable_cookies, self.schedule_type)
        self.raw_data = await GetInfo(self.uid, self.useable_cookies)

    async def check_cookies_useable(self):
        if self.raw_data:
            if self.raw_data["retcode"] != 0:
                if self.raw_data["retcode"] == 10001:
                    errorDB(self.useable_cookies, "error")
                    return False
                elif self.raw_data["retcode"] == 10101:
                    errorDB(self.useable_cookies, "limit30")
                    return False
                elif self.raw_data["retcode"] == 10102:
                    return "当前查询id已经设置了隐私，无法查询！"
                else:
                    return (
                            "Api报错，返回内容为：\r\n"
                            + str(self.raw_data) + "\r\n出现这种情况可能的UID输入错误 or 不存在"
                    )
            else:
                return True
        else:
            return "没有可以使用的Cookies！"


class CustomizeImage:
    def __init__(self, image: str, based_w: int, based_h: int) -> None:

        self.bg_img = self.get_image(image, based_w, based_h)
        self.bg_color = self.get_bg_color(self.bg_img)
        self.text_color = self.get_text_color(self.bg_color)
        self.highlight_color = self.get_highlight_color(self.bg_color)
        self.char_color = self.get_char_color(self.bg_color)
        self.bg_detail_color = self.get_bg_detail_color(self.bg_color)
        self.char_high_color = self.get_char_high_color(self.bg_color)

    def get_image(self, image: str, based_w: int, based_h: int) -> Image:
        # 获取背景图片
        bg2_path = os.path.join(BG_PATH, random.choice([x for x in os.listdir(BG_PATH)
                                                        if os.path.isfile(os.path.join(BG_PATH, x))]))

        if image:
            image_data = image.group(2)
            edit_bg = Image.open(BytesIO(get(image_data).content))
        else:
            edit_bg = Image.open(bg2_path)

        # 确定图片的长宽
        based_scale = '%.3f' % (based_w / based_h)

        w, h = edit_bg.size
        scale_f = '%.3f' % (w / h)
        new_w = math.ceil(based_h * float(scale_f))
        new_h = math.ceil(based_w / float(scale_f))
        if scale_f > based_scale:
            bg_img2 = edit_bg.resize((new_w, based_h), Image.ANTIALIAS)
        else:
            bg_img2 = edit_bg.resize((based_w, new_h), Image.ANTIALIAS)
        bg_img = bg_img2.crop((0, 0, based_w, based_h))

        return bg_img

    def get_bg_color(self, edit_bg: Image) -> Tuple[int, int, int]:
        # 获取背景主色
        color = 8
        q = edit_bg.quantize(colors=color, method=2)
        bg_color = None
        based_light = 195
        temp = 9999
        for i in range(0, color):
            bg = tuple(q.getpalette()[i * 3:(i * 3) + 3])
            light_value = bg[0] * 0.3 + bg[1] * 0.6 + bg[2] * 0.1
            if abs(light_value - based_light) < temp:
                bg_color = bg
                temp = abs(light_value - based_light)
            # if max(*bg) < 240 and min(*bg) > 20:
            #    bg_color = bg
        return bg_color

    def get_text_color(self, bg_color: Tuple[int, int, int]) -> Tuple[int, int, int]:
        # 通过背景主色（bg_color）确定文字主色
        r = 125
        if max(*bg_color) > 255 - r:
            r *= -1
        text_color = (math.floor(bg_color[0] + r if bg_color[0] + r <= 255 else 255),
                      math.floor(bg_color[1] + r if bg_color[1] + r <= 255 else 255),
                      math.floor(bg_color[2] + r if bg_color[2] + r <= 255 else 255))
        return text_color

    def get_char_color(self, bg_color: Tuple[int, int, int]) -> Tuple[int, int, int]:
        r = 140
        if max(*bg_color) > 255 - r:
            r *= -1
        char_color = (math.floor(bg_color[0] + 5 if bg_color[0] + r <= 255 else 255),
                      math.floor(bg_color[1] + 5 if bg_color[1] + r <= 255 else 255),
                      math.floor(bg_color[2] + 5 if bg_color[2] + r <= 255 else 255))
        return char_color

    def get_char_high_color(self, bg_color: Tuple[int, int, int]) -> Tuple[int, int, int]:
        r = 140
        d = 20
        if max(*bg_color) > 255 - r:
            r *= -1
        char_color = (math.floor(bg_color[0] + d if bg_color[0] + r <= 255 else 255),
                      math.floor(bg_color[1] + d if bg_color[1] + r <= 255 else 255),
                      math.floor(bg_color[2] + d if bg_color[2] + r <= 255 else 255))
        return char_color

    def get_bg_detail_color(self, bg_color: Tuple[int, int, int]) -> Tuple[int, int, int]:
        r = 140
        if max(*bg_color) > 255 - r:
            r *= -1
        bg_detail_color = (math.floor(bg_color[0] - 20 if bg_color[0] + r <= 255 else 255),
                           math.floor(bg_color[1] - 20 if bg_color[1] + r <= 255 else 255),
                           math.floor(bg_color[2] - 20 if bg_color[2] + r <= 255 else 255))
        return bg_detail_color

    def get_highlight_color(self, color: Tuple[int, int, int]) -> Tuple[int, int, int]:
        red_color = color[0]
        green_color = color[1]
        blue_color = color[2]

        highlight_color = {}
        highlight_color["red"] = red_color - 127 if red_color > 127 else 127
        highlight_color["green"] = green_color - 127 if green_color > 127 else 127
        highlight_color["blue"] = blue_color - 127 if blue_color > 127 else 127

        max_color = max(highlight_color.values())
        name = "red"
        for _highlight_color in highlight_color:
            if highlight_color[_highlight_color] == max_color:
                name = str(_highlight_color)

        if name == "red":
            return red_color, highlight_color["green"], highlight_color["blue"]
        elif name == "green":
            return highlight_color["red"], green_color, highlight_color["blue"]
        elif name == "blue":
            return highlight_color["red"], highlight_color["green"], blue_color
        else:
            return 0, 0, 0  # Error


async def draw_info_pic(uid: str, image=None) -> str:
    def seconds2hours(seconds: int) -> str:
        m, s = divmod(int(seconds), 60)
        h, m = divmod(m, 60)
        return "%02d:%02d:%02d" % (h, m, s)

    # 获取Cookies
    data_def = GetCookies()
    retcode = await data_def.get_useable_cookies(uid)
    if not retcode:
        return retcode
    raw_data = data_def.raw_data
    char_data = raw_data["data"]["avatars"]
    # 获取数据
    award_data = await GetAward(uid)
    daily_data = await GetDaily(uid)
    daily_data = daily_data["data"]
    nickname = award_data['data']['nickname']

    # 获取背景图片各项参数
    based_w = 900
    based_h = 1380
    image_def = CustomizeImage(image, based_w, based_h)
    bg_img = image_def.bg_img
    bg_color = image_def.bg_color
    text_color = image_def.text_color
    highlight_color = image_def.highlight_color
    char_color = image_def.char_color

    # 确定texture2D路径
    info1_path = os.path.join(BG2_PATH, "info_1.png")
    info2_path = os.path.join(BG2_PATH, "info_2.png")
    info3_path = os.path.join(BG2_PATH, "info_3.png")

    avatar_bg_path = os.path.join(BG2_PATH, "avatar_bg.png")
    avatar_fg_path = os.path.join(BG2_PATH, "avatar_fg.png")

    all_mask_path = os.path.join(BG2_PATH, "All_Mask.png")

    # 转换遮罩的颜色、大小匹配，并paste上去
    all_mask = Image.open(all_mask_path).resize(bg_img.size, Image.ANTIALIAS)
    all_mask_img = Image.new("RGBA", (based_w, based_h), bg_color)
    bg_img.paste(all_mask_img, (0, 0), all_mask)

    # 操作图片
    info1 = Image.open(info1_path)
    info2 = Image.open(info2_path)
    info3 = Image.open(info3_path)
    avatar_bg = Image.open(avatar_bg_path)
    avatar_fg = Image.open(avatar_fg_path)

    avatar_bg_color = Image.new("RGBA", (316, 100), bg_color)
    bg_img.paste(avatar_bg_color, (113, 98), avatar_bg)
    bg_img.paste(avatar_fg, (114, 95), avatar_fg)

    info1_color = Image.new("RGBA", (900, 1300), bg_color)
    bg_img.paste(info1_color, (0, 0), info1)

    info2_color = Image.new("RGBA", (900, 1300), text_color)
    bg_img.paste(info2_color, (0, 0), info2)

    bg_img.paste(info3, (0, 0), info3)

    text_draw = ImageDraw.Draw(bg_img)

    # 用户信息
    text_draw.text((220, 137), f"{nickname}", text_color, genshin_font(32), anchor="lm")
    text_draw.text((235, 170), 'UID ' + f"{uid}", text_color, genshin_font(14), anchor="lm")

    # 本日原石/摩拉
    text_draw.text((675, 148),
                   f"{award_data['data']['day_data']['current_primogems']}/{award_data['data']['day_data']['last_primogems']}",
                   text_color, genshin_font(28), anchor="lm")
    text_draw.text((675, 212),
                   f"{award_data['data']['day_data']['current_mora']}\n{award_data['data']['day_data']['last_mora']}",
                   text_color, genshin_font(28), anchor="lm")

    # 本月/上月原石
    text_draw.text((722, 287), f"{award_data['data']['month_data']['current_primogems']}", text_color, genshin_font(21),
                   anchor="lm")
    text_draw.text((722, 323), f"{award_data['data']['month_data']['last_primogems']}", text_color, genshin_font(21),
                   anchor="lm")

    # 本月/上月摩拉
    text_draw.text((722, 359), f"{award_data['data']['month_data']['current_mora']}", text_color, genshin_font(21),
                   anchor="lm")
    text_draw.text((722, 395), f"{award_data['data']['month_data']['last_mora']}", text_color, genshin_font(21),
                   anchor="lm")

    # 收入比例
    for index, i in enumerate(award_data['data']['month_data']['group_by']):
        text_draw.text((681, 445 + index * 32), f"{str(i['num'])}({str(i['percent'])}%)", text_color, genshin_font(21),
                       anchor="lm")

    # 基本四项
    text_draw.text((390, 314), f"{daily_data['current_resin']}/{daily_data['max_resin']}", text_color, genshin_font(26),
                   anchor="lm")
    text_draw.text((390, 408), f'{daily_data["current_home_coin"]}/{daily_data["max_home_coin"]}', text_color,
                   genshin_font(26), anchor="lm")
    text_draw.text((390, 503), f"{daily_data['finished_task_num']}/{daily_data['total_task_num']}", text_color,
                   genshin_font(26), anchor="lm")
    text_draw.text((390, 597),
                   f"{str(daily_data['resin_discount_num_limit'] - daily_data['remain_resin_discount_num'])}/{daily_data['resin_discount_num_limit']}",
                   text_color, genshin_font(26), anchor="lm")

    # 树脂恢复时间计算
    resin_recovery_time = seconds2hours(
        daily_data['resin_recovery_time'])
    next_resin_rec_time = seconds2hours(
        8 * 60 - ((daily_data['max_resin'] - daily_data['current_resin']) * 8 * 60 - int(
            daily_data['resin_recovery_time'])))
    text_draw.text((268, 305), f" {next_resin_rec_time}", text_color, genshin_font(18), anchor="lm")

    text_draw.text((170, 331), f"预计                  后全部恢复", text_color, genshin_font(18), anchor="lm")
    text_draw.text((208, 331), f"{resin_recovery_time}", highlight_color, genshin_font(18), anchor="lm")

    # 洞天宝钱时间计算
    coin_rec_time = seconds2hours(int(daily_data["home_coin_recovery_time"]))

    if daily_data["home_coin_recovery_time"] == "0":
        text_draw.text((170, 425), f"已满", text_color, genshin_font(18), anchor="lm")
    else:
        coin_add_speed = math.ceil((daily_data["max_home_coin"] - daily_data["current_home_coin"]) / (
                int(daily_data["home_coin_recovery_time"]) / 60 / 60))
        text_draw.text((270, 399), f"约{coin_add_speed}/h", text_color, genshin_font(18), anchor="lm")
        text_draw.text((170, 425), f"预计                  后达到上限", text_color, genshin_font(18), anchor="lm")
        text_draw.text((208, 425), f"{coin_rec_time}", highlight_color, genshin_font(18), anchor="lm")

    if daily_data['is_extra_task_reward_received']:
        daily_task_status = "「每日委托」奖励已领取"
    else:
        daily_task_status = "「每日委托」奖励未领取"

    # 详细信息
    text_draw.text((170, 518), f"{daily_task_status}", text_color, genshin_font(18), anchor="lm")
    text_draw.text((170, 614), f"本周剩余消耗减半次数", text_color, genshin_font(18), anchor="lm")

    # 派遣图片准备
    char_bg_path = os.path.join(BG2_PATH, "char_bg.png")

    char_bg = Image.open(char_bg_path)
    charset_mask = Image.new("RGBA", (900, 130), char_color)

    # 派遣
    for index, i in enumerate(daily_data["expeditions"]):
        for j in char_data:
            if i["avatar_side_icon"].split("_")[-1] == j["image"].split("_")[-1]:
                name = j["name"]
        if not os.path.exists(
                os.path.join(CHAR_IMG_PATH, f"UI_AvatarIcon_{i['avatar_side_icon'].split('_')[-1][:-4]}@2x.png")):
            get_char_img_pic(
                f"https://upload-bbs.mihoyo.com/game_record/genshin/character_image/UI_AvatarIcon_{i['avatar_side_icon'].split('_')[-1][:-4]}@2x.png")
        # char_stand_img = os.path.join(CHAR_IMG_PATH, f"UI_AvatarIcon_{i['avatar_side_icon'].split('_')[-1][:-4]}@2x.png")
        # char_stand = Image.open(char_stand_img)
        # char_stand_mask = Image.open(os.path.join(TEXT_PATH, "stand_mask.png"))

        # charpic_temp = Image.new("RGBA", (900, 130))
        # charpic_temp.paste(char_stand, (395, -99), char_stand_mask)
        charpic = Image.new("RGBA", (900, 130))
        char_icon = Image.open(BytesIO(get(i['avatar_side_icon']).content))

        char_namecard_img = Image.open(os.path.join(CHAR_NAMECARD_PATH, str(name + ".png")))
        char_namecard_img = char_namecard_img.resize((591, 81), Image.ANTIALIAS)
        char_namecard_img.putalpha(char_namecard_img.getchannel('A').point(lambda i: i * 0.8 if i > 0 else 0))

        char_icon_scale = char_icon.resize((140, 140), Image.ANTIALIAS)
        charpic.paste(charset_mask, (0, 0), char_bg)
        charpic.paste(char_icon_scale, (63, -26), char_icon_scale)
        charpic.paste(char_namecard_img, (247, 24), char_namecard_img)

        charpic_draw = ImageDraw.Draw(charpic)

        if i['status'] == 'Finished':
            charpic_draw.text((200, 65), f"探索完成", text_color, genshin_font(24), anchor="lm")
        else:
            remained_timed: str = seconds2hours(i['remained_time'])
            charpic_draw.text((200, 65), f"剩余时间 {remained_timed}", text_color, genshin_font(24), anchor="lm")

        bg_img.paste(charpic, (-15, 748 + 115 * index), charpic)

    end_pic = Image.open(os.path.join(BG2_PATH, "abyss_3.png"))
    bg_img.paste(end_pic, (0, 1340), end_pic)

    # 转换之后发送
    bg_img = bg_img.convert('RGB')
    bg_img.save(f"temp{os.sep}info.jpg", format='JPEG', subsampling=0, quality=90)
    return f"temp{os.sep}info.jpg"
