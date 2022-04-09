import asyncio
import random
import re
import sqlite3
import traceback
from genshin import ChineseClient

from typing import Union

from pyrogram import Client, ContinuePropagation, filters
from pyrogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from defs.db import deal_ck, selectDB, OpenPush, CheckDB, connectDB, deletecache
from defs.event import generate_event
from defs.mys2 import award, sign, daily, draw_pic, draw_wordcloud, draw_info_pic
from defs.mihoyo import draw_pic as draw_pic_2

from ci import scheduler, app, admin_id
from defs.redis_load import redis
from defs.spiral_abyss import draw_abyss_pic, draw_abyss0_pic
from defs.spiral_abyss_text import get_user_abyss

SUPERUSERS = [admin_id]
Cookie_Right_Text = """
Cookie 有效，请在 30 秒内选择您要绑定的账号：
"""
Bind_Right_Text = """
账号绑定成功，欢迎使用！
"""
No_Account_Text = """
暂无账号信息，请先前往 APP 绑定账号！
"""

def is_chinese(x: Union[int, str]) -> bool:
    """Recognizes whether the server/uid is chinese."""
    return str(x).startswith(("1", "2", "5"))


async def choose_account(message: Message, results: list,
                         client: Union[ChineseClient] = None):
    # 选择账号
    if results:
        keyboard = []
        data = {}
        for i in results:
            data[str(i.uid)] = i
            keyboard.append(KeyboardButton(text=f"{i.uid} - {i.nickname} - lv.{i.level}"))
        msg = await message.reply(Cookie_Right_Text,
                                  reply_to_message_id=message.message_id,
                                  reply_markup=ReplyKeyboardMarkup([keyboard]))
        try:
            ask = await app.listen(message.from_user.id, filters=filters.text, timeout=30)  # noqa
        except asyncio.TimeoutError:
            await msg.delete()
            await message.reply("您的操作超时，请重试。", reply_markup=ReplyKeyboardRemove())
            raise ContinuePropagation
        except Exception as e:
            await msg.delete()
            await message.reply(f"出现错误：{e}", reply_markup=ReplyKeyboardRemove())
            raise ContinuePropagation
        try:
            data = data[ask.text.split(" - ")[0]]
        except (AttributeError, IndexError, KeyError):
            await ask.reply("您的操作错误，请重试。", quote=True)
            raise ContinuePropagation
        except Exception as e:
            await ask.reply_text(f"出现错误：{e}", quote=True)
            raise ContinuePropagation
        # 写入数据
        await connectDB(message.from_user.id, data.uid)
        await connectDB(message.from_user.id, None, client.hoyolab_uid)


async def mys2_msg(client: Client, message: Message):
    text = message.text.replace("米游社", "")
    userid = message.from_user.id
    if '添加' in text:
        try:
            mes = text.replace('添加', '').strip()
            if not mes:
                return await message.reply_text("获取 Cookie 请参考：[link](https://github.com/Womsxd/AutoMihoyoBBS/"
                                                "#%E8%8E%B7%E5%8F%96%E7%B1%B3%E6%B8%B8%E7%A4%BEcookie)", quote=True)
            await deal_ck(mes, userid)
            # 开始绑定 uid
            client_ = ChineseClient()
            client_.set_cookies(mes)
            results = await client_.genshin_accounts()
            await client_.close()
            await choose_account(message, results, client_)
            await message.reply(f'<code>=============</code>\n'
                                f'添加Cookies成功！\n'
                                f'Cookies属于个人重要信息，如果你是在不知情的情况下添加，'
                                f'请马上修改米游社账户密码，保护个人隐私！\n'
                                f'<code>=============</code>', reply_markup=ReplyKeyboardRemove(), quote=True)
        except ContinuePropagation:
            raise ContinuePropagation
        except Exception as e:
            traceback.print_exc()
            await message.reply(f'校验失败！请输入正确的Cookies！获取 Cookie 请参考：'
                                f'[link](https://github.com/Womsxd/AutoMihoyoBBS/'
                                f'#%E8%8E%B7%E5%8F%96%E7%B1%B3%E6%B8%B8%E7%A4%BEcookie)', quote=True)
    elif '推送' in text:
        try:
            uid = await selectDB(userid, mode="uid")
            if '开启' in text:
                im = await OpenPush(int(uid[0]), userid, "on", "StatusA")
                await message.reply(im, quote=True)
            else:
                im = await OpenPush(int(uid[0]), userid, "off", "StatusA")
                await message.reply(im, quote=True)
        except Exception as e:
            traceback.print_exc()
            await message.reply("未找到uid绑定记录。", quote=True)
    elif '自动签到' in text:
        try:
            uid = await selectDB(userid, mode="uid")
            if '开启' in text:
                im = await OpenPush(int(uid[0]), userid, "on", "StatusB")
                await message.reply(im, quote=True)
            else:
                im = await OpenPush(int(uid[0]), userid, "off", "StatusA")
                await message.reply(im, quote=True)
        except Exception as e:
            traceback.print_exc()
            await message.reply("未找到uid绑定记录。", quote=True)
    elif "每月统计" in text:
        try:
            uid = await selectDB(message.from_user.id, mode="uid")
            uid = uid[0]
            im = await award(uid)
            await message.reply(im, quote=True)
        except Exception as e:
            traceback.print_exc()
            await message.reply('未找到绑定信息', quote=True)
    elif "签到" in text:
        try:
            uid = await selectDB(message.from_user.id, mode="uid")
            uid = uid[0]
            im = await sign(uid)
            await message.reply(im, quote=True)
        except Exception as e:
            traceback.print_exc()
            await message.reply('未找到绑定信息', quote=True)
    elif "当前状态" in text:
        try:
            uid = await selectDB(message.from_user.id, mode="uid")
            uid = uid[0]
            mes = await daily("ask", uid)
            im = mes[0]['message']
        except Exception as e:
            traceback.print_exc()
            im = "没有找到绑定信息。"
        await message.reply(im, quote=True)
    elif "当前信息" in text:
        try:
            uid = await selectDB(message.from_user.id, mode="uid")
            uid = uid[0]
            im = await draw_info_pic(uid, message)
            if not im:
                await message.reply("未查找到该用户的当前信息。", quote=True)
            else:
                await message.reply_photo(im, quote=True)
        except Exception as e:
            traceback.print_exc()
            im = "没有找到绑定信息。"
            await message.reply(im)
    elif "绑定uid" in text:
        uid = text.replace("绑定uid", "")  # str
        if is_chinese(uid):
            await connectDB(message.from_user.id, uid)
            await message.reply('绑定uid成功！', quote=True)
        else:
            await message.reply("非国区uid！", quote=True)
    elif "绑定mys" in text:
        mys = text.replace("绑定mys", "")  # str
        await connectDB(message.from_user.id, None, mys)
        await message.reply('绑定米游社id成功！', quote=True)


async def mys2_qun_msg(client: Client, message: Message):
    text = message.text.replace("米游社", "")

    qid = message.from_user.id
    at = message.reply_to_message
    if "自动签到" in text:
        try:
            if at and qid in SUPERUSERS:
                qid = at.from_user.id
            elif at and qid not in SUPERUSERS:
                return await message.reply("你没有权限。")
            gid = message.chat.id
            uid = await selectDB(qid, mode="uid")
            if "开启" in text:
                im = await OpenPush(int(uid[0]), message.from_user.id, str(gid), "StatusB")
                await message.reply(im, quote=True)
            elif "关闭" in text:
                im = await OpenPush(int(uid[0]), message.from_user.id, "off", "StatusB")
                await message.reply(im)
        except Exception as e:
            traceback.print_exc()
            await message.reply("未绑定uid信息！")
    elif "推送" in text:
        try:
            if at and qid in SUPERUSERS:
                qid = at.from_user.id
            elif at and qid not in SUPERUSERS:
                return await message.reply("你没有权限。")
            gid = message.chat.id
            uid = await selectDB(qid, mode="uid")
            if "开启" in text:
                im = await OpenPush(int(uid[0]), message.from_user.id, str(gid), "StatusA")
                await message.reply(im, quote=True)
            elif "关闭" in text:
                im = await OpenPush(int(uid[0]), message.from_user.id, "off", "StatusA")
                await message.reply(im)
        except Exception as e:
            traceback.print_exc()
            await message.reply("未绑定uid信息！")
    elif "每月统计" in text:
        try:
            uid = await selectDB(message.from_user.id, mode="uid")
            uid = uid[0]
            im = await award(uid)
            await message.reply(im)
        except Exception as e:
            traceback.print_exc()
            await message.reply('未找到绑定信息')
    elif "签到" in text:
        try:
            uid = await selectDB(message.from_user.id, mode="uid")
            uid = uid[0]
            im = await sign(uid)
            await message.reply(im)
        except Exception as e:
            traceback.print_exc()
            await message.reply('未找到绑定信息')
    elif "效验全部" in text:
        im = await CheckDB()
        await message.reply(im)
    elif "当前状态" in text:
        try:
            uid = await selectDB(message.from_user.id, mode="uid")
            uid = uid[0]
            mes = await daily("ask", uid)
            im = mes[0]['message']
        except Exception as e:
            traceback.print_exc()
            im = "没有找到绑定信息。"
        await message.reply(im)
    elif "当前信息" in text:
        try:
            uid = await selectDB(message.from_user.id, mode="uid")
            uid = uid[0]
            im = await draw_info_pic(uid, message)
            if not im:
                await message.reply("未查找到该用户的当前信息。")
            else:
                await message.reply_photo(im)
        except Exception as e:
            traceback.print_exc()
            im = "没有找到绑定信息。"
            await message.reply(im)
    elif "绑定uid" in text:
        uid = text.replace("绑定uid", "")  # str
        if is_chinese(uid):
            await connectDB(message.from_user.id, uid)
            await message.reply('绑定uid成功！')
        else:
            await message.reply("非国区uid！")
    elif "绑定mys" in text:
        mys = text.replace("绑定mys", "")  # str
        await connectDB(message.from_user.id, None, mys)
        await message.reply('绑定米游社id成功！')
    elif "uid" in text:
        try:
            uid = re.findall(r"\d+", text)[0]  # str
            m = ''.join(re.findall('[\u4e00-\u9fa5]', text))
        except IndexError:
            return await message.reply("uid格式错误！")
        nickname = message.from_user.first_name
        nickname = nickname if len(nickname) < 10 else (nickname[:10] + "...")
        if m == "深渊":
            try:
                if len(re.findall(r"\d+", text)) == 2:
                    floor_num = re.findall(r"\d+", text)[1]
                    im = await draw_abyss_pic(uid, nickname, floor_num)
                    if not im:
                        await message.reply("未查找到该用户的深渊信息。")
                    else:
                        await message.reply_photo(im)
                else:
                    im = await draw_abyss0_pic(uid, nickname)
                    if not im:
                        await message.reply("未查找到该用户的深渊信息。")
                    else:
                        await message.reply_photo(im)
            except TypeError:
                await message.reply("获取失败，可能是Cookies失效或者未打开米游社角色详情开关。")
                print("上期深渊数据获取失败（Cookie失效/不公开信息）")
                traceback.print_exc()
            except Exception as e:
                await message.reply("获取失败，有可能是数据状态有问题,\n{}\n请检查后台输出。".format(e))
                print("上期深渊数据获取失败（数据状态问题）")
                traceback.print_exc()
        elif m == "上期深渊":
            try:
                if len(re.findall(r"\d+", text)) == 2:
                    floor_num = re.findall(r"\d+", text)[1]
                    im = await draw_abyss_pic(uid, nickname, floor_num, None, 2, "2")
                    if not im:
                        await message.reply("未查找到该用户的深渊信息。")
                    else:
                        await message.reply_photo(im)
                else:
                    im = await draw_abyss0_pic(uid, nickname, None, 2, "2")
                    if not im:
                        await message.reply("未查找到该用户的深渊信息。")
                    else:
                        await message.reply_photo(im)
            except TypeError:
                await message.reply("获取失败，可能是Cookies失效或者未打开米游社角色详情开关。")
                print("上期深渊数据获取失败（Cookie失效/不公开信息）")
                traceback.print_exc()
            except Exception as e:
                await message.reply("获取失败，有可能是数据状态有问题,\n{}\n请检查后台输出。".format(e))
                print("上期深渊数据获取失败（数据状态问题）")
                traceback.print_exc()
        elif m == "文本深渊":
            try:
                im = await get_user_abyss(uid, 2, "2")
                if not im:
                    await message.reply("未查找到该用户的深渊信息。")
                else:
                    await message.reply(im)
            except TypeError:
                await message.reply("获取失败，可能是Cookies失效或者未打开米游社角色详情开关。")
                print("上期深渊数据获取失败（Cookie失效/不公开信息）")
                traceback.print_exc()
            except Exception as e:
                await message.reply("获取失败，有可能是数据状态有问题,\n{}\n请检查后台输出。".format(e))
                print("上期深渊数据获取失败（数据状态问题）")
                traceback.print_exc()
        else:
            try:
                try:
                    if is_chinese(uid):
                        im = await draw_pic(uid, message, nickname=nickname, mode=2)
                    else:
                        im = await draw_pic_2(uid, message, nickname=nickname, mode=2)
                    if im.find(".") != -1:
                        await message.reply_photo(im)
                    else:
                        await message.reply(im)
                except Exception as e:
                    await message.reply("获取失败，有可能是数据状态有问题,\n{}\n请检查后台输出。".format(e))
                    traceback.print_exc()
            except Exception as e:
                traceback.print_exc()
                await message.reply("发生错误 {},请检查后台输出。".format(e))
    elif "查询" in text:
        try:
            at = message.reply_to_message
            if at:
                qid = at.from_user.id
                nickname = at.from_user.first_name
                uid = await selectDB(qid)
            else:
                nickname = message.from_user.first_name
                uid = await selectDB(message.from_user.id)
            nickname = nickname if len(nickname) < 10 else (nickname[:10] + "...")
            if uid:
                if "深渊" in text and "上期" not in text and "文本" not in text:
                    try:
                        if len(re.findall(r"\d+", text)) == 1:
                            floor_num = re.findall(r"\d+", text)[0]
                            im = await draw_abyss_pic(uid[0], nickname, floor_num, None, uid[1])
                            if not im:
                                await message.reply("未查找到该用户的深渊信息。")
                            else:
                                await message.reply_photo(im)
                        else:
                            im = await draw_abyss0_pic(uid[0], nickname, None, uid[1])
                            if not im:
                                await message.reply("未查找到该用户的深渊信息。")
                            else:
                                await message.reply_photo(im)
                    except TypeError:
                        await message.reply("获取失败，可能是Cookies失效或者未打开米游社角色详情开关。")
                        print("上期深渊数据获取失败（Cookie失效/不公开信息）")
                        traceback.print_exc()
                    except Exception as e:
                        await message.reply("获取失败，有可能是数据状态有问题,\n{}\n请检查后台输出。".format(e))
                        print("上期深渊数据获取失败（数据状态问题）")
                        traceback.print_exc()
                elif "深渊" in text and "文本" not in text:
                    try:
                        if len(re.findall(r"\d+", text)) == 1:
                            floor_num = re.findall(r"\d+", text)[0]
                            im = await draw_abyss_pic(uid[0], nickname, floor_num, None, uid[1], "2")
                            if not im:
                                await message.reply("未查找到该用户的深渊信息。")
                            else:
                                await message.reply_photo(im)
                        else:
                            im = await draw_abyss0_pic(uid[0], nickname, None, uid[1], "2")
                            if not im:
                                await message.reply("未查找到该用户的深渊信息。")
                            else:
                                await message.reply_photo(im)
                    except TypeError:
                        await message.reply("获取失败，可能是Cookies失效或者未打开米游社角色详情开关。")
                        print("上期深渊数据获取失败（Cookie失效/不公开信息）")
                        traceback.print_exc()
                    except Exception as e:
                        await message.reply("获取失败，有可能是数据状态有问题,\n{}\n请检查后台输出。".format(e))
                        print("上期深渊数据获取失败（数据状态问题）")
                        traceback.print_exc()
                elif "深渊" in text:
                    try:
                        im = await get_user_abyss(uid[0], uid[1], "2")
                        if not im:
                            await message.reply("未查找到该用户的深渊信息。")
                        else:
                            await message.reply(im)
                    except TypeError:
                        await message.reply("获取失败，可能是Cookies失效或者未打开米游社角色详情开关。")
                        print("上期深渊数据获取失败（Cookie失效/不公开信息）")
                        traceback.print_exc()
                    except Exception as e:
                        await message.reply("获取失败，有可能是数据状态有问题,\n{}\n请检查后台输出。".format(e))
                        print("上期深渊数据获取失败（数据状态问题）")
                        traceback.print_exc()
                elif "词云" in text:
                    try:
                        im = await draw_wordcloud(uid[0], message, uid[1])
                        if im.find(".jpg") != -1:
                            await message.reply_photo(im)
                        else:
                            await message.reply(im)
                    except Exception as e:
                        await message.reply("获取失败，有可能是数据状态有问题,\n{}\n请检查后台输出。".format(e))
                        traceback.print_exc()
                else:
                    try:
                        bg = await draw_pic(uid[0], message, nickname=nickname, mode=uid[1])
                        if bg.find(".") != -1:
                            await message.reply_photo(bg)
                        else:
                            await message.reply(bg)
                    except Exception as e:
                        await message.reply("获取失败，有可能是数据状态有问题,\n{}\n请检查后台输出。".format(e))
                        traceback.print_exc()
            else:
                await message.reply('未找到绑定记录！')
        except Exception as e:
            traceback.print_exc()
            await message.reply("发生错误 {},请检查后台输出。".format(e))
    elif "mys" in text:
        try:
            try:
                uid = re.findall(r"\d+", text)[0]  # str
            except IndexError:
                return await message.reply("米游社 id 格式错误！")
            nickname = message.from_user.first_name
            nickname = nickname if len(nickname) < 10 else (nickname[:10] + "...")
            try:
                im = await draw_pic(uid, message, nickname=nickname, mode=3)
                if im.find(".") != -1:
                    await message.reply_photo(im)
                else:
                    await message.reply(im)
            except Exception as e:
                await message.reply("获取失败，有可能是数据状态有问题,\n{}\n请检查后台输出。".format(e))
                traceback.print_exc()
        except Exception as e:
            traceback.print_exc()
            await message.reply("发生错误 {},请检查后台输出。".format(e))
    elif "全部重签" in text and message.from_user.id in SUPERUSERS:
        try:
            await message.reply("已开始执行")
            await daily_sign()
        except Exception as e:
            traceback.print_exc()
            await message.reply("发生错误 {},请检查后台输出。".format(e))


# 每隔一小时检测树脂是否超过设定值
@scheduler.scheduled_job('interval', hours=1)
async def push():
    daily_data = await daily()
    if daily_data is not None:
        for i in daily_data:
            # 过滤重复推送
            data = i['message'].split('==============')
            if len(data) > 2:
                text = "".join(data[1:-1])
                data = redis.get("daily_" + str(i['qid']))
                if data:
                    if text == data.decode():
                        continue
                redis.set("daily_" + str(i['qid']), text)

            if i['gid'] == "on":
                await app.send_message(int(i['qid']), i['message'])
            else:
                await app.send_message(int(i['gid']),
                                       f"[NOTICE {i['qid']}](tg://user?id={i['qid']})" + "\n" + i['message'])
    else:
        pass


# 每日零点半进行米游社签到
@scheduler.scheduled_job('cron', hour='0', minute="30")
async def daily_sign():
    conn = sqlite3.connect('ID_DATA.db')
    c = conn.cursor()
    cursor = c.execute(
        "SELECT *  FROM NewCookiesTable WHERE StatusB != ?", ("off",))
    c_data = cursor.fetchall()
    temp_list = []

    for row in c_data:
        if row[4] == "on":
            try:
                im = await sign(str(row[0]))
                await app.send_message(int(row[2]), im)
            except Exception as e:
                traceback.print_exc()
        else:
            im = await sign(str(row[0]))
            message = f"[NOTICE {row[2]}](tg://user?id={row[2]})\n\n{im}"
            for i in temp_list:
                if row[4] == i["push_group"]:
                    i["push_message"] = i["push_message"] + "\n" + message
                    break
            else:
                temp_list.append({"push_group": row[4], "push_message": message})
        await asyncio.sleep(6 + random.randint(0, 2))

    for i in temp_list:
        try:
            await app.send_message(int(i["push_group"]), i["push_message"])
        except Exception as e:
            traceback.print_exc()
        await asyncio.sleep(3 + random.randint(0, 2))


@scheduler.scheduled_job('cron', hour='2')
async def delete():
    await generate_event()


# 每日零点清空cookies使用缓存
@scheduler.scheduled_job('cron', hour='0')
async def delete():
    deletecache()
