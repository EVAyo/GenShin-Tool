import math
import os
import random
import time
from io import BytesIO
from httpx import get
from PIL import Image, ImageDraw, ImageFont

from defs.db import cacheDB, GetMysInfo, GetInfo, errorDB, get_spiral_abyss_info

FILE2_PATH = os.path.join("assets")
CHAR_DONE_PATH = os.path.join(FILE2_PATH, "char_done")
TEXT_PATH = os.path.join(FILE2_PATH, "bg2")
BG_PATH = os.path.join(FILE2_PATH, "bg")


def get_char_done_pic(_id, url, star):
    char_data = get(url).content
    if star == 4:
        star1_path = os.path.join(TEXT_PATH, '4star_1.png')
        star2_path = os.path.join(TEXT_PATH, '4star_2.png')
    else:
        star1_path = os.path.join(TEXT_PATH, '5star_1.png')
        star2_path = os.path.join(TEXT_PATH, '5star_2.png')
    star_1 = Image.open(star1_path)
    star_2 = Image.open(star2_path)
    char_img = Image.open(BytesIO(char_data)).resize((104, 104), Image.ANTIALIAS)
    star_1.paste(char_img, (12, 15), char_img)
    star_1.paste(star_2, (0, 0), star_2)
    star_1.save(os.path.join(CHAR_DONE_PATH, str(_id) + '.png'))


def genshin_font(size):
    return ImageFont.truetype(f"assets{os.sep}fonts{os.sep}yuan_shen.ttf", size=size, encoding="utf-8")


async def draw_abyss0_pic(uid, nickname, image=None, mode=2, date="1"):
    # 获取Cookies
    while True:
        use_cookies = cacheDB(uid, mode - 1)
        if use_cookies == '':
            return "绑定记录不存在。"
        elif use_cookies == "没有可以使用的Cookies！":
            return "没有可以使用的Cookies！"

        if mode == 3:
            mys_data = await GetMysInfo(uid, use_cookies)
            for i in mys_data['data']['list']:
                if i['game_id'] != 2:
                    mys_data['data']['list'].remove(i)
            uid = mys_data['data']['list'][0]['game_role_id']
            nickname = mys_data['data']['list'][0]['nickname']

        raw_data = await get_spiral_abyss_info(uid, use_cookies, date)
        raw_char_data = await GetInfo(uid, use_cookies)

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

    # 获取数据
    raw_data = raw_data["data"]
    raw_char_data = raw_char_data['data']["avatars"]

    # 获取查询者数据
    if not raw_data['floors']:
        return ""
    floors_data = raw_data['floors'][-1]
    levels_num = len(floors_data['levels'])

    # 获取背景图片
    bg2_path = os.path.join(BG_PATH, random.choice([x for x in os.listdir(BG_PATH)
                                                    if os.path.isfile(os.path.join(BG_PATH, x))]))

    if image:
        image_data = image.group(2)
        edit_bg = Image.open(BytesIO(get(image_data).content))
    else:
        edit_bg = Image.open(bg2_path)

    # 确定图片的长宽
    based_w = 900
    based_h = 660 + levels_num * 315
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

    # 确定贴图路径
    abyss0_path = os.path.join(TEXT_PATH, "abyss_0.png")
    abyss3_path = os.path.join(TEXT_PATH, "abyss_3.png")
    abyss_star0_path = os.path.join(TEXT_PATH, "abyss_star0.png")
    abyss_star1_path = os.path.join(TEXT_PATH, "abyss_star1.png")
    avatar_bg_path = os.path.join(TEXT_PATH, "avatar_bg.png")
    avatar_fg_path = os.path.join(TEXT_PATH, "avatar_fg.png")

    all_mask_path = os.path.join(TEXT_PATH, "All_Mask.png")

    # 转换遮罩的颜色、大小匹配，并paste上去
    all_mask = Image.open(all_mask_path).resize(bg_img.size, Image.ANTIALIAS)
    all_mask_img = Image.new("RGBA", (based_w, based_h), bg_color)
    bg_img.paste(all_mask_img, (0, 0), all_mask)

    # 开启图片
    avatar_bg = Image.open(avatar_bg_path)
    avatar_fg = Image.open(avatar_fg_path)

    # 确定主体框架
    avatar_bg_color = Image.new("RGBA", (316, 100), bg_color)
    bg_img.paste(avatar_bg_color, (113, 98), avatar_bg)
    bg_img.paste(avatar_fg, (114, 95), avatar_fg)

    """
    x1, y1 = 65, 276
    radius = 15
    cropped_img1 = bg_img.crop((x1, y1, 836, 607))
    blurred_img1 = cropped_img1.filter(ImageFilter.GaussianBlur(5),).convert("RGBA")
    bg_img.paste(blurred_img1, (x1, y1), create_rounded_rectangle_mask(cropped_img1,radius))
    for i in range(0,len(floors_data['levels'])):
        x2, y2 = 65, 630 + 315*i 
        radius = 15
        cropped_img2 = bg_img.crop((x2, y2, 836, 925+315*i))
        blurred_img2 = cropped_img2.filter(ImageFilter.GaussianBlur(5),).convert("RGBA")
        bg_img.paste(blurred_img2, (x2, y2), create_rounded_rectangle_mask(cropped_img2,radius))
    """

    abyss0_bg_color = Image.new("RGBA", (900, 620), new_color)
    abyss0 = Image.new("RGBA", (900, 620), (0, 0, 0, 0))

    abyss0_pic = Image.open(abyss0_path)
    abyss0.paste(abyss0_bg_color, (0, 0), abyss0_pic)
    abyss3 = Image.open(abyss3_path)
    abyss_star0 = Image.open(abyss_star0_path)
    abyss_star1 = Image.open(abyss_star1_path)

    for i in range(0, 4):
        if not os.path.exists(os.path.join(CHAR_DONE_PATH, str(raw_data["reveal_rank"][i]["avatar_id"]) + ".png")):
            get_char_done_pic(raw_data["reveal_rank"][i]["avatar_id"], raw_data["reveal_rank"][i]["avatar_icon"],
                              raw_data["reveal_rank"][i]["rarity"])
        char = os.path.join(CHAR_DONE_PATH, str(raw_data["reveal_rank"][i]["avatar_id"]) + ".png")
        char_img = Image.open(char)
        char_draw = ImageDraw.Draw(char_img)
        for k in raw_char_data:
            if k['id'] == raw_data["reveal_rank"][i]["avatar_id"]:
                char_draw.text((63.5, 117), f'{str(raw_data["reveal_rank"][i]["value"])}次', (21, 21, 21),
                               genshin_font(18), anchor="mm")
                char_draw.text((95.3, 19), f'{str(k["actived_constellation_num"])}', 'white', genshin_font(18))
                if str(k["fetter"]) == "10" or str(k["name"]) == "旅行者":
                    char_draw.text((93, 41.5), "♥", (21, 21, 21), genshin_font(15))
                else:
                    char_draw.text((95.3, 40.5), f'{str(k["fetter"])}', (21, 21, 21), genshin_font(18))
        char_crop = (82 + 130 * i, 300)
        abyss0.paste(char_img, char_crop, char_img)

    for i in range(0, 1):
        if not os.path.exists(os.path.join(CHAR_DONE_PATH, str(raw_data["damage_rank"][i]["avatar_id"]) + ".png")):
            get_char_done_pic(raw_data["damage_rank"][i]["avatar_id"], raw_data["damage_rank"][i]["avatar_icon"],
                              raw_data["reveal_rank"][i]["rarity"])
        char = os.path.join(CHAR_DONE_PATH, str(raw_data["damage_rank"][i]["avatar_id"]) + ".png")
        char_img = Image.open(char)
        char_draw = ImageDraw.Draw(char_img)
        for k in raw_char_data:
            if k['id'] == raw_data["damage_rank"][i]["avatar_id"]:
                char_draw.text((63.5, 117), f'{str(raw_data["damage_rank"][i]["value"])}', (21, 21, 21),
                               genshin_font(18), anchor="mm")
                char_draw.text((95.3, 19), f'{str(k["actived_constellation_num"])}', 'white', genshin_font(18))
                if str(k["fetter"]) == "10" or str(k["name"]) == "旅行者":
                    char_draw.text((93, 41.5), "♥", (21, 21, 21), genshin_font(15))
                else:
                    char_draw.text((95.3, 40.5), f'{str(k["fetter"])}', (21, 21, 21), genshin_font(18))
        char_crop = (685, 470)
        abyss0.paste(char_img, char_crop, char_img)

    for i in range(0, 1):
        if not os.path.exists(os.path.join(CHAR_DONE_PATH, str(raw_data["defeat_rank"][i]["avatar_id"]) + ".png")):
            get_char_done_pic(raw_data["defeat_rank"][i]["avatar_id"], raw_data["defeat_rank"][i]["avatar_icon"],
                              raw_data["reveal_rank"][i]["rarity"])
        char = os.path.join(CHAR_DONE_PATH, str(raw_data["defeat_rank"][i]["avatar_id"]) + ".png")
        char_img = Image.open(char)
        char_draw = ImageDraw.Draw(char_img)
        for k in raw_char_data:
            if k['id'] == raw_data["defeat_rank"][i]["avatar_id"]:
                char_draw.text((63.5, 117), f'{str(raw_data["defeat_rank"][i]["value"])}', (21, 21, 21),
                               genshin_font(18), anchor="mm")
                char_draw.text((95.3, 19), f'{str(k["actived_constellation_num"])}', 'white', genshin_font(18))
                if str(k["fetter"]) == "10" or str(k["name"]) == "旅行者":
                    char_draw.text((93, 41.5), "♥", (21, 21, 21), genshin_font(15))
                else:
                    char_draw.text((95.3, 40.5), f'{str(k["fetter"])}', (21, 21, 21), genshin_font(18))
        char_crop = (82 + 123 * i, 470)
        abyss0.paste(char_img, char_crop, char_img)

    for i in range(0, 1):
        if not os.path.exists(os.path.join(CHAR_DONE_PATH, str(raw_data["take_damage_rank"][i]["avatar_id"]) + ".png")):
            get_char_done_pic(raw_data["take_damage_rank"][i]["avatar_id"],
                              raw_data["take_damage_rank"][i]["avatar_icon"], raw_data["reveal_rank"][i]["rarity"])
        char = os.path.join(CHAR_DONE_PATH, str(raw_data["take_damage_rank"][i]["avatar_id"]) + ".png")
        char_img = Image.open(char)
        char_draw = ImageDraw.Draw(char_img)
        for k in raw_char_data:
            if k['id'] == raw_data["take_damage_rank"][i]["avatar_id"]:
                char_draw.text((63.5, 117), f'{str(raw_data["take_damage_rank"][i]["value"])}', (21, 21, 21),
                               genshin_font(18), anchor="mm")
                char_draw.text((95.3, 19), f'{str(k["actived_constellation_num"])}', 'white', genshin_font(18))
                if str(k["fetter"]) == "10" or str(k["name"]) == "旅行者":
                    char_draw.text((93, 41.5), "♥", (21, 21, 21), genshin_font(15))
                else:
                    char_draw.text((95.3, 40.5), f'{str(k["fetter"])}', (21, 21, 21), genshin_font(18))
        char_crop = (232 + 123 * i, 470)
        abyss0.paste(char_img, char_crop, char_img)

    for i in range(0, 1):
        if not os.path.exists(
                os.path.join(CHAR_DONE_PATH, str(raw_data["normal_skill_rank"][i]["avatar_id"]) + ".png")):
            get_char_done_pic(raw_data["normal_skill_rank"][i]["avatar_id"],
                              raw_data["normal_skill_rank"][i]["avatar_icon"], raw_data["reveal_rank"][i]["rarity"])
        char = os.path.join(CHAR_DONE_PATH, str(raw_data["normal_skill_rank"][i]["avatar_id"]) + ".png")
        char_img = Image.open(char)
        char_draw = ImageDraw.Draw(char_img)
        for k in raw_char_data:
            if k['id'] == raw_data["normal_skill_rank"][i]["avatar_id"]:
                char_draw.text((63.5, 117), f'{str(raw_data["normal_skill_rank"][i]["value"])}', (21, 21, 21),
                               genshin_font(18), anchor="mm")
                char_draw.text((95.3, 19), f'{str(k["actived_constellation_num"])}', 'white', genshin_font(18))
                if str(k["fetter"]) == "10" or str(k["name"]) == "旅行者":
                    char_draw.text((93, 41.5), "♥", (21, 21, 21), genshin_font(15))
                else:
                    char_draw.text((95.3, 40.5), f'{str(k["fetter"])}', (21, 21, 21), genshin_font(18))
        char_crop = (382 + 123 * i, 470)
        abyss0.paste(char_img, char_crop, char_img)

    for i in range(0, 1):
        if not os.path.exists(
                os.path.join(CHAR_DONE_PATH, str(raw_data["energy_skill_rank"][i]["avatar_id"]) + ".png")):
            get_char_done_pic(raw_data["energy_skill_rank"][i]["avatar_id"],
                              raw_data["energy_skill_rank"][i]["avatar_icon"], raw_data["reveal_rank"][i]["rarity"])
        char = os.path.join(CHAR_DONE_PATH, str(raw_data["energy_skill_rank"][i]["avatar_id"]) + ".png")
        char_img = Image.open(char)
        char_draw = ImageDraw.Draw(char_img)
        for k in raw_char_data:
            if k['id'] == raw_data["energy_skill_rank"][i]["avatar_id"]:
                char_draw.text((63.5, 118), f'{str(raw_data["energy_skill_rank"][i]["value"])}', (21, 21, 21),
                               genshin_font(18), anchor="mm")
                char_draw.text((95.3, 19), f'{str(k["actived_constellation_num"])}', 'white', genshin_font(18))
                if str(k["fetter"]) == "10" or str(k["name"]) == "旅行者":
                    char_draw.text((93, 41.5), "♥", (21, 21, 21), genshin_font(15))
                else:
                    char_draw.text((95.3, 40.5), f'{str(k["fetter"])}', (21, 21, 21), genshin_font(18))
        char_crop = (532 + 123 * i, 470)
        abyss0.paste(char_img, char_crop, char_img)

    bg_img.paste(abyss0, (0, 0), abyss0)

    for j in range(0, len(floors_data["levels"])):
        abyss2 = Image.new("RGBA", (900, 340), (0, 0, 0, 0))
        # abyss2 = Image.open(abyss2_path)
        num_1 = 0
        for i in floors_data['levels'][j]['battles'][0]['avatars']:
            if not os.path.exists(os.path.join(CHAR_DONE_PATH, str(i['id']) + ".png")):
                get_char_done_pic(i['id'], i['icon'], i['rarity'])
            char = os.path.join(CHAR_DONE_PATH, str(i['id']) + ".png")
            char_img = Image.open(char)
            char_draw = ImageDraw.Draw(char_img)
            for k in raw_char_data:
                if k['id'] == i['id']:
                    char_draw.text((40, 108), f'Lv.{str(k["level"])}', (21, 21, 21), genshin_font(18))
                    char_draw.text((95.3, 19), f'{str(k["actived_constellation_num"])}', 'white', genshin_font(18))
                    if str(k["fetter"]) == "10" or str(k["name"]) == "旅行者":
                        char_draw.text((93, 41.5), "♥", (21, 21, 21), genshin_font(15))
                    else:
                        char_draw.text((95.3, 40.5), f'{str(k["fetter"])}', (21, 21, 21), genshin_font(18))
            char_crop = (70 + 125 * (num_1 % 4), 46)
            abyss2.paste(char_img, char_crop, char_img)
            num_1 = num_1 + 1
        num_2 = 0
        for i in floors_data['levels'][j]['battles'][1]['avatars']:
            if not os.path.exists(os.path.join(CHAR_DONE_PATH, str(i['id']) + ".png")):
                get_char_done_pic(i['id'], i['icon'], i['rarity'])
            char = os.path.join(CHAR_DONE_PATH, str(i['id']) + ".png")
            char_img = Image.open(char)
            char_draw = ImageDraw.Draw(char_img)
            for k in raw_char_data:
                if k['id'] == i['id']:
                    char_draw.text((40, 108), f'Lv.{str(k["level"])}', (21, 21, 21), genshin_font(18))
                    char_draw.text((95.3, 19), f'{str(k["actived_constellation_num"])}', 'white', genshin_font(18))
                    if str(k["fetter"]) == "10" or str(k["name"]) == "旅行者":
                        char_draw.text((93, 41.5), "♥", (21, 21, 21), genshin_font(15))
                    else:
                        char_draw.text((95.3, 40.5), f'{str(k["fetter"])}', (21, 21, 21), genshin_font(18))
            char_crop = (70 + 125 * (num_2 % 4), 180)
            abyss2.paste(char_img, char_crop, char_img)
            num_2 = num_2 + 1
        star_num = floors_data['levels'][j]['star']
        if star_num == 1:
            abyss2.paste(abyss_star1, (640, 155), abyss_star1)
            abyss2.paste(abyss_star0, (685, 155), abyss_star0)
            abyss2.paste(abyss_star0, (730, 155), abyss_star0)
        elif star_num == 0:
            abyss2.paste(abyss_star0, (640, 155), abyss_star0)
            abyss2.paste(abyss_star0, (685, 155), abyss_star0)
            abyss2.paste(abyss_star0, (730, 155), abyss_star0)
        elif star_num == 2:
            abyss2.paste(abyss_star1, (640, 155), abyss_star1)
            abyss2.paste(abyss_star1, (685, 155), abyss_star1)
            abyss2.paste(abyss_star0, (730, 155), abyss_star0)
        else:
            abyss2.paste(abyss_star1, (640, 155), abyss_star1)
            abyss2.paste(abyss_star1, (685, 155), abyss_star1)
            abyss2.paste(abyss_star1, (730, 155), abyss_star1)
        abyss2_text_draw = ImageDraw.Draw(abyss2)
        abyss2_text_draw.text((87, 30), f"第{j + 1}间", new_color, genshin_font(21))
        timeStamp1 = int(floors_data['levels'][j]['battles'][0]['timestamp'])
        timeStamp2 = int(floors_data['levels'][j]['battles'][1]['timestamp'])
        timeArray1 = time.localtime(timeStamp1)
        timeArray2 = time.localtime(timeStamp2)
        otherStyleTime1 = time.strftime("%Y--%m--%d %H:%M:%S", timeArray1)
        otherStyleTime2 = time.strftime("%Y--%m--%d %H:%M:%S", timeArray2)
        abyss2_text_draw.text((167, 33), f"{otherStyleTime1}/{otherStyleTime2}", new_color, genshin_font(19))
        bg_img.paste(abyss2, (0, 605 + j * 315), abyss2)

    bg_img.paste(abyss3, (0, len(floors_data["levels"]) * 315 + 610), abyss3)

    text_draw = ImageDraw.Draw(bg_img)
    text_draw.text((220, 123), f"{nickname}", new_color, genshin_font(32))
    text_draw.text((235, 163), 'UID ' + f"{uid}", new_color, genshin_font(14))

    text_draw.text((690, 82), raw_data['max_floor'], new_color, genshin_font(26))
    text_draw.text((690, 127), str(raw_data['total_battle_times']), new_color, genshin_font(26))
    text_draw.text((690, 172), str(raw_data['total_star']), new_color, genshin_font(26))

    bg_img = bg_img.convert('RGB')
    bg_img.save(f"temp{os.sep}abyss.jpg", format='JPEG', subsampling=0, quality=90)
    # bg_img.save(result_buffer, format='PNG')
    return f"temp{os.sep}abyss.jpg"


async def draw_abyss_pic(uid, nickname, floor_num, image=None, mode=2, date="1"):
    while True:
        use_cookies = cacheDB(uid, mode - 1)
        if use_cookies == '':
            return "绑定记录不存在。"
        elif use_cookies == "没有可以使用的Cookies！":
            return "没有可以使用的Cookies！"

        if mode == 3:
            mys_data = await GetMysInfo(uid, use_cookies)
            for i in mys_data['data']['list']:
                if i['game_id'] != 2:
                    mys_data['data']['list'].remove(i)
            uid = mys_data['data']['list'][0]['game_role_id']
            nickname = mys_data['data']['list'][0]['nickname']

        raw_data = await get_spiral_abyss_info(uid, use_cookies, date)
        raw_char_data = await GetInfo(uid, use_cookies)

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

    # 获取数据
    raw_data = raw_data["data"]
    raw_char_data = raw_char_data['data']["avatars"]
    floors_data = raw_data['floors']
    if not floors_data:
        return ""
    based_data = []
    for i in floors_data:
        if str(i['index']) == floor_num:
            based_data = i
    levels_num = len(based_data['levels'])

    # 获取背景图片
    bg2_path = os.path.join(BG_PATH, random.choice([x for x in os.listdir(BG_PATH)
                                                    if os.path.isfile(os.path.join(BG_PATH, x))]))

    if image:
        image_data = image.group(2)
        edit_bg = Image.open(BytesIO(get(image_data).content))
    else:
        edit_bg = Image.open(bg2_path)

    # 确定图片的长宽
    based_w = 900
    based_h = 440 + levels_num * 340
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

    # 打开图片
    abyss1_path = os.path.join(TEXT_PATH, "abyss_1.png")
    abyss3_path = os.path.join(TEXT_PATH, "abyss_3.png")
    abyss_star0_path = os.path.join(TEXT_PATH, "abyss_star0.png")
    abyss_star1_path = os.path.join(TEXT_PATH, "abyss_star1.png")
    abyss1 = Image.open(abyss1_path)
    abyss3 = Image.open(abyss3_path)
    abyss_star0 = Image.open(abyss_star0_path)
    abyss_star1 = Image.open(abyss_star1_path)
    avatar_bg_path = os.path.join(TEXT_PATH, "avatar_bg.png")
    avatar_fg_path = os.path.join(TEXT_PATH, "avatar_fg.png")

    all_mask_path = os.path.join(TEXT_PATH, "All_Mask.png")

    # 转换遮罩的颜色、大小匹配，并paste上去
    all_mask = Image.open(all_mask_path).resize(bg_img.size, Image.ANTIALIAS)
    all_mask_img = Image.new("RGBA", (based_w, based_h), bg_color)
    bg_img.paste(all_mask_img, (0, 0), all_mask)

    # 开启图片
    avatar_bg = Image.open(avatar_bg_path)
    avatar_fg = Image.open(avatar_fg_path)

    # 确定主体框架
    avatar_bg_color = Image.new("RGBA", (316, 100), bg_color)
    bg_img.paste(avatar_bg_color, (113, 145), avatar_bg)
    bg_img.paste(avatar_fg, (114, 142), avatar_fg)

    """
    for i in range(0,len(based_data['levels'])):
        x, y = 65, 220 + 340*i 
        radius = 10
        cropped_img = bg_img.crop((x, y, 836, 517+340*i))
        blurred_img = cropped_img.filter(ImageFilter.GaussianBlur(5),).convert("RGBA")
        bg_img.paste(blurred_img, (x, y), create_rounded_rectangle_mask(cropped_img,radius))
    """

    abyss1_bg_color = Image.new("RGBA", (900, 400), bg_color)
    bg_img.paste(abyss1_bg_color, (0, 0), abyss1)

    for j in range(0, len(based_data['levels'])):
        abyss2 = Image.new("RGBA", (900, 340), (0, 0, 0, 0))
        num_1 = 0
        avatars = based_data['levels'][j]['battles'][0]['avatars'] + based_data['levels'][j]['battles'][1]['avatars']
        for i in based_data['levels'][j]['battles'][0]['avatars']:
            if not os.path.exists(os.path.join(CHAR_DONE_PATH, str(i['id']) + ".png")):
                get_char_done_pic(i['id'], i['icon'], i['rarity'])
            char = os.path.join(CHAR_DONE_PATH, str(i['id']) + ".png")
            char_img = Image.open(char)
            char_draw = ImageDraw.Draw(char_img)
            for k in raw_char_data:
                if k['id'] == i['id']:
                    char_draw.text((40, 108), f'Lv.{str(k["level"])}', (21, 21, 21), genshin_font(18))
                    char_draw.text((95.3, 19), f'{str(k["actived_constellation_num"])}', 'white', genshin_font(18))
                    if str(k["fetter"]) == "10" or str(k["name"]) == "旅行者":
                        char_draw.text((93, 41.5), "♥", (21, 21, 21), genshin_font(15))
                    else:
                        char_draw.text((95.3, 40.5), f'{str(k["fetter"])}', (21, 21, 21), genshin_font(18))
            char_crop = (70 + 125 * (num_1 % 4), 46)
            abyss2.paste(char_img, char_crop, char_img)
            num_1 = num_1 + 1
        num_2 = 0
        for i in based_data['levels'][j]['battles'][1]['avatars']:
            if not os.path.exists(os.path.join(CHAR_DONE_PATH, str(i['id']) + ".png")):
                get_char_done_pic(i['id'], i['icon'], i['rarity'])
            char = os.path.join(CHAR_DONE_PATH, str(i['id']) + ".png")
            char_img = Image.open(char)
            char_draw = ImageDraw.Draw(char_img)
            for k in raw_char_data:
                if k['id'] == i['id']:
                    char_draw.text((40, 108), f'Lv.{str(k["level"])}', (21, 21, 21), genshin_font(18))
                    char_draw.text((95.3, 19), f'{str(k["actived_constellation_num"])}', 'white', genshin_font(18))
                    if str(k["fetter"]) == "10" or str(k["name"]) == "旅行者":
                        char_draw.text((93, 41.5), "♥", (21, 21, 21), genshin_font(15))
                    else:
                        char_draw.text((95.3, 40.5), f'{str(k["fetter"])}', (21, 21, 21), genshin_font(18))
            char_crop = (70 + 125 * (num_2 % 4), 180)
            abyss2.paste(char_img, char_crop, char_img)
            num_2 = num_2 + 1
        star_num = based_data['levels'][j]['star']
        if star_num == 1:
            abyss2.paste(abyss_star1, (640, 155), abyss_star1)
            abyss2.paste(abyss_star0, (685, 155), abyss_star0)
            abyss2.paste(abyss_star0, (730, 155), abyss_star0)
        elif star_num == 0:
            abyss2.paste(abyss_star0, (640, 155), abyss_star0)
            abyss2.paste(abyss_star0, (685, 155), abyss_star0)
            abyss2.paste(abyss_star0, (730, 155), abyss_star0)
        elif star_num == 2:
            abyss2.paste(abyss_star1, (640, 155), abyss_star1)
            abyss2.paste(abyss_star1, (685, 155), abyss_star1)
            abyss2.paste(abyss_star0, (730, 155), abyss_star0)
        else:
            abyss2.paste(abyss_star1, (640, 155), abyss_star1)
            abyss2.paste(abyss_star1, (685, 155), abyss_star1)
            abyss2.paste(abyss_star1, (730, 155), abyss_star1)
        abyss2_text_draw = ImageDraw.Draw(abyss2)
        abyss2_text_draw.text((87, 30), f"第{j + 1}间", new_color, genshin_font(21))
        timeStamp1 = int(based_data['levels'][j]['battles'][0]['timestamp'])
        timeStamp2 = int(based_data['levels'][j]['battles'][1]['timestamp'])
        timeArray1 = time.localtime(timeStamp1)
        timeArray2 = time.localtime(timeStamp2)
        otherStyleTime1 = time.strftime("%Y--%m--%d %H:%M:%S", timeArray1)
        otherStyleTime2 = time.strftime("%Y--%m--%d %H:%M:%S", timeArray2)
        abyss2_text_draw.text((167, 33), f"{otherStyleTime1}/{otherStyleTime2}", new_color, genshin_font(19))
        bg_img.paste(abyss2, (0, 350 + j * 340), abyss2)

    bg_img.paste(abyss3, (0, len(based_data['levels']) * 340 + 400), abyss3)

    text_draw = ImageDraw.Draw(bg_img)

    text_draw.text((220, 163), f"{nickname}", new_color, genshin_font(32))
    text_draw.text((235, 203), 'UID ' + f"{uid}", new_color, genshin_font(14))
    text_draw.text((710, 190), f"{floor_num}", new_color, genshin_font(50), anchor="mm")

    bg_img = bg_img.convert('RGB')
    result_buffer = BytesIO()
    bg_img.save(f"temp{os.sep}abyss.jpg", format='JPEG', subsampling=0, quality=90)
    # bg_img.save(result_buffer, format='PNG')
    return f"temp{os.sep}abyss.jpg"
