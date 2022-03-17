import json
import os
import time

from defs.db import GetInfo, cacheDB, GetMysInfo, get_spiral_abyss_info, errorDB
from pydantic import BaseModel
from typing import List


class GenshinUserCharacher(BaseModel):
    id: int
    image: str  # 角色头图url
    name: str  # 角色名
    element: str  # 属性
    fetter: int  # 好感等级
    level: int
    rarity: int  # 稀有度
    actived_constellation_num: int  # 命之座


class GenshinUserStats(BaseModel):
    active_day_number: int  # 活跃天数
    achievement_number: int  # 成就数
    win_rate: int
    anemoculus_number: int  # 风神瞳数量
    geoculus_number: int  # 岩神瞳数
    electroculus_number: int  # 雷神瞳数量
    avatar_number: int  # 角色数量
    way_point_number: int  # 传送点解锁数
    domain_number: int  # 秘境解锁数
    spiral_abyss: str  # 深渊进度
    common_chest_number: int  # 普通宝箱数量
    exquisite_chest_number: int  # 精致宝箱数量
    precious_chest_number: int  # 珍贵宝箱数量
    luxurious_chest_number: int  # 华丽宝箱数量
    magic_chest_number: int  # 奇馈宝箱数量


class GenshinWorldOfferings(BaseModel):
    name: str
    level: int


class GenshinWorldInfo(BaseModel):
    level: int  # 声望等级
    exploration_percentage: int  # 探索度
    icon: str  # 区域图标url
    name: str
    type: str
    id: int
    offerings: List[GenshinWorldOfferings]  # 供奉信息


class GenshinHomeInfo(BaseModel):
    level: int  # 信任等级
    visit_num: int  # 访客数
    comfort_num: int  # 洞天仙力
    item_num: int  # 摆件数量
    name: str
    icon: str  # 背景图
    comfort_level_name: str  # 洞天仙力对应名称
    comfort_level_icon: str  # 等级图标


class GenshinUserData(BaseModel):
    avatars: List[GenshinUserCharacher]  # 角色列表
    stats: GenshinUserStats
    city_explorations: List  # 不知道是啥玩意, 都是空的
    world_explorations: List[GenshinWorldInfo]  # 区域探索信息
    homes: List[GenshinHomeInfo]  # 家园信息


class GenshinAbyssRankInfo(BaseModel):
    avatar_id: int
    avatar_icon: str
    value: int
    rarity: int


class GenshinAbyssFloorInfoBattlesAvatars(BaseModel):
    id: int
    icon: str
    level: int
    rarity: int


class GenshinAbyssFloorInfoBattles(BaseModel):
    index: int  # 战斗场次
    timestamp: str
    avatars: List[GenshinAbyssFloorInfoBattlesAvatars]


class GenshinAbyssFloorInfo(BaseModel):
    index: int  # 间号
    star: int
    max_star: int
    battles: List[GenshinAbyssFloorInfoBattles]


class GenshinAbyssFloors(BaseModel):
    index: int  # 层数
    icon: str  # 空的
    is_unlock: bool
    settle_time: str
    star: int
    max_star: int
    levels: List[GenshinAbyssFloorInfo]


class GenshinAbyss(BaseModel):
    schedule_id: int
    start_time: int  # 10位
    end_time: int  # 10位
    total_battle_times: int
    total_win_times: int
    max_floor: str
    reveal_rank: List[GenshinAbyssRankInfo]  # 出战次数Rank
    defeat_rank: List[GenshinAbyssRankInfo]  # 击破数Rank
    damage_rank: List[GenshinAbyssRankInfo]  # 最强一击
    take_damage_rank: List[GenshinAbyssRankInfo]  # 承伤Rank
    normal_skill_rank: List[GenshinAbyssRankInfo]  # 元素战技释放数
    energy_skill_rank: List[GenshinAbyssRankInfo]  # 元素爆发次数
    floors: List[GenshinAbyssFloors]
    total_star: int
    is_unlock: bool


def char_id_to_name(udata: GenshinUserData, charid: int):  # id2name.json数据不全, 我也懒得去搜集了, 故采用此邪道方法(
    chars = udata.avatars
    for char in chars:
        if charid == char.id:
            return char.name
    with open(f"assets{os.sep}data{os.sep}id2name.json", "r", encoding="utf-8") as f:
        id2name = json.load(f)
    if str(charid) in id2name:
        return id2name[str(charid)]
    return f"{charid}"


def timestamp_to_text(timestamp: int, _format="%Y-%m-%d %H:%M:%S"):
    """
    :param timestamp: 时间戳,若输入13位时间戳则自动转为10位
    :param _format: 格式,默认"%Y-%m-%d %H:%M:%S"
    :return: %Y-%m-%d %H:%M:%S -> str
    """
    if timestamp > 9999999999:  # 13位时间戳转10位
        timestamp = timestamp / 1000
    ret = time.strftime(_format, time.localtime(timestamp))
    return ret


async def get_user_abyss(uid, mode=2, date="1"):  # 深境螺旋
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
    udata = GenshinUserData(**raw_char_data["data"])
    aby = GenshinAbyss(**raw_data["data"])

    if not aby.floors:  # 没打
        return ""
    rettext = f"<b>第{aby.schedule_id}期深境螺旋信息</b>\n\n" \
              f"\t开始时间: {timestamp_to_text(aby.start_time)}\n" \
              f"\t结束时间: {timestamp_to_text(aby.end_time)}\n" \
              f"\t最深抵达:{aby.max_floor}\n" \
              f"\t胜利场次/总场次: {aby.total_win_times}/{aby.total_battle_times}\n"
    if aby.reveal_rank:
        rettext += f"\t出战最多: {char_id_to_name(udata, aby.reveal_rank[0].avatar_id)} - {aby.reveal_rank[0].value}\n"
    if aby.defeat_rank:
        rettext += f"\t击破最多: {char_id_to_name(udata, aby.defeat_rank[0].avatar_id)} - {aby.defeat_rank[0].value}\n"
    if aby.damage_rank:
        rettext += f"\t最强一击: {char_id_to_name(udata, aby.damage_rank[0].avatar_id)} - {aby.damage_rank[0].value}\n"
    if aby.take_damage_rank:
        rettext += f"\t最高承伤: {char_id_to_name(udata, aby.take_damage_rank[0].avatar_id)} - {aby.take_damage_rank[0].value}\n"
    if aby.normal_skill_rank:
        rettext += f"\t元素战技: {char_id_to_name(udata, aby.normal_skill_rank[0].avatar_id)} - {aby.normal_skill_rank[0].value}\n"
    if aby.energy_skill_rank:
        rettext += f"\t元素爆发: {char_id_to_name(udata, aby.energy_skill_rank[0].avatar_id)} - {aby.energy_skill_rank[0].value}\n"
    rettext += f"\t总星数: ★ {aby.total_star}\n\t"

    floor_text = ""  # 层
    has_details = False
    if len(aby.floors) >= 0:
        if len(aby.floors[0].levels) > 0:
            has_details = True
            for floor in aby.floors:  # 层
                room_text = ""  # 间
                for room in floor.levels:  # 间
                    battle_text = ""  # 场
                    for battle in room.battles:  # 场次
                        character_text = ""  # 角色
                        for char in battle.avatars:  # 角色列表
                            character_text += f"/{char_id_to_name(udata, char.id)}"
                        battle_text += f"\n\t\t\t\t第 {battle.index} 场: {character_text[1:]}"

                    room_text += f"\n\t\t\t第 {room.index} 间 (★ {room.star}/{room.max_star}):{battle_text}"

                floor_text += f"\n\n\t\t第 {floor.index} 层:\t{room_text}"
    rettext = f"{rettext}楼层信息:{floor_text}" if has_details else f"{rettext}未获取到详细楼层信息"
    return rettext
