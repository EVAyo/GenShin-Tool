# -*- coding:utf-8 -*-

import os
from concurrent import futures as cf
from multiprocessing import cpu_count
from enum import IntEnum

import wget
from kokomi.miHoYo.HoYoLAB import api


SAVE_DIR = 'D:/miHoYo/崩坏3官方壁纸/'


def to_ospath(path: str) -> str:
    for ch in "\\/:*?<>|\n":
        path = path.replace(ch, '')
    return path


def download(url: str, filename: str):
    if not os.path.exists(filename):
        wget.download(url=url, out=filename, bar=None)
        cp = os.getcwd().split('/')[-1]
        print(cp, ' : ', filename)
        return 1
    return 0


def GetPictures0(param: dict):
    with cf.ThreadPoolExecutor(max_workers=cpu_count()) as exec:
        all_task = []

        data = api.getContentList(params=param)
        data_list = data['list']

        # 遍历列表
        for item in data_list:
            url = item['ext'][0]['value'][0]['url'].replace("\\/", "/")

            filename = url.split('/')[-1].split('.')[0]  # id
            filename += "_" + item['title']  # 标题
            filename += "_" + str(item['ext'][0]['value'][0]['name'])  # 源名称
            filename = to_ospath(filename)

            all_task.append(
                exec.submit(download, url, filename)
            )

        # 等待线程结束
        cf.wait(all_task, return_when=cf.ALL_COMPLETED)

        return {
            "server": param['game_biz'] if "game_biz" in param else "bh3",
            "new": sum([task.result() for task in all_task]),
            "total": len(all_task)
        }


class Channel(IntEnum):
    BH3_CN = 177
    BH3_GLOBAL = 336
    BH3_OVERSEA = 383
    BH3_JAPAN = 949
    BH3_ASIA = 459
    BH3_KOREA = 475


def GetPictures(channel: Channel, save_dir: str):
    param = {
        "pageSize": 200,
        "pageNum": 1,
        "channelId": int(channel)
    }

    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    os.chdir(save_dir)

    if Channel.BH3_CN == channel:
        pass
    elif Channel.BH3_GLOBAL == channel:
        param['game_biz'] = 'bh3_global'
    elif Channel.BH3_OVERSEA == channel:
        param['game_biz'] = 'bh3_os'
    elif Channel.BH3_JAPAN == channel:
        param['game_biz'] = 'bh3_jp'
    elif Channel.BH3_ASIA == channel:
        param['game_biz'] = 'bh3_asia'
    elif Channel.BH3_KOREA == channel:
        param['game_biz'] = 'bh3_kr'
    else:
        return {
            "server": 'unknown',
            "new": 0,
            "total": -1
        }

    return GetPictures0(param=param)


def finish_task(data):
    print(f"{data['server']} 完成。新增 {data['new']} 张。共计 {data['total']} 张。")


if __name__ == "__main__":
    with cf.ProcessPoolExecutor() as pol:
        all_task = [
            pol.submit(GetPictures, Channel.BH3_CN, SAVE_DIR + 'bh3/'),
            pol.submit(GetPictures, Channel.BH3_GLOBAL, SAVE_DIR + 'global/'),
            pol.submit(GetPictures, Channel.BH3_OVERSEA, SAVE_DIR + 'oversea/'),
            pol.submit(GetPictures, Channel.BH3_JAPAN, SAVE_DIR + 'japan/'),
            pol.submit(GetPictures, Channel.BH3_ASIA, SAVE_DIR + 'asia/'),
            pol.submit(GetPictures, Channel.BH3_KOREA, SAVE_DIR + 'korea/')
        ]
        cf.wait(all_task, return_when=cf.ALL_COMPLETED)

        print('all clear.')
        [finish_task(task.result()) for task in all_task]

    os.startfile(SAVE_DIR)
