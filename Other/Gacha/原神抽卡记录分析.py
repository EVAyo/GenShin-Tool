##

import json

import matplotlib.pyplot as plt
import pandas
from kokomi.miHoYo.Genshin.GetGacha import GachaException, getGachaLogs
from pandas import DataFrame as df
from tabulate import tabulate

characters = [
    "迪卢克", "琴", "莫娜", "七七", "刻晴",
    "温迪", "可莉", '达达利亚', '钟离', '阿贝多',
    '甘雨', '魈', '胡桃', '优菈',
    '万叶', '霄宫', '神里绫华', '雷电将军',  '珊瑚宫心海'
]

gacha_ty = {
    301: '角色限定祈愿',
    302: '武器限定祈愿',
    200: '奔行世间',
    100: '新手祈愿'
}


def readGachaLogs(gacha_type: int):
    '''读取本地抽卡记录'''
    with open(str(gacha_type)+'.json', 'r', encoding='utf-8') as file:
        return json.load(fp=file)


def readGachaLogsNb(gacha_type: int):
    '''读取本地抽卡记录'''
    with open(str(gacha_type)+'_nb.json', 'r', encoding='utf-8') as file:
        return json.load(fp=file)


def getEndId(gacha_type: int):
    with open(str(gacha_type)+'_nb.json', 'r', encoding='utf-8') as file:
        return json.load(fp=file)[0]['id']


class GachaLogEmptyList(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def updateNb(gacha_type: int):
    '''从祈愿记录页更新本地数据'''

    print('updating  ', gacha_ty[gacha_type], f"  {getEndId(gacha_type)}")

    all_data = getGachaLogs(gacha_type)
    if not all_data:
        # continue
        raise GachaLogEmptyList

    old_data = readGachaLogsNb(gacha_type)

    with open(str(gacha_type)+'_nb.json', 'w', encoding='utf-8') as file:
        json.dump(
            obj=all_data+old_data[len(all_data)-all_data.index(old_data[0]):],
            fp=file, ensure_ascii=False, indent=4
        )


def updateNbs():
    '''从祈愿记录页更新本地数据'''

    for ty in [('武器', 302), ('角色', 301), ('常驻', 200), ('新手', 100)]:
        try:
            updateNb(gacha_type=ty[1])
        except GachaLogEmptyList:
            continue
    print('update all done.')


def AnalysisGacha(gacha_type: int):
    '''分析抽卡记录'''

    name = gacha_ty[gacha_type]
    print(name, f"  {getEndId(gacha_type)}")
    all_data = readGachaLogsNb(gacha_type)
    all_data.reverse()

    cnt = 0
    fives = []
    for d in all_data:
        cnt += 1
        if d['rank_type'] == '5':
            fives.append((d['name'], cnt))
            #print(f"{d['name']} [{cnt}]")
            cnt = 0
    print(f'共{len(all_data)}抽，已累计{cnt}次未出五星.')

    try:
        print(f'共计{len(fives)}，平均{round((len(all_data)-cnt)/len(fives),2)}次一个五星.')
    except:
        print(f'共计{len(fives)}')

    print('')
    fives.insert(0, ('累计', cnt))
    return fives


def SeeIt(all_five: dict):
    '''可视化'''

    # 支持中文
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    # 各个池子五统计
    plt.subplot(1, 2, 1)
    plt.pie(
        [len(five)-1 for five in all_five.values()],
        labels=[f'{five[0]}[{len(five[1])-1}]' for five in all_five.items()]
    )

    # 武器和角色统计
    w = c = 0
    for v in all_five.values():
        for dv in v:
            if dv[0] == '累计':
                continue
            if dv[0] in characters:
                c += 1
            else:
                w += 1
    plt.subplot(1, 2, 2)
    plt.pie(
        [w, c],
        labels=[f'武器[{w}]', f'角色[{c}]']
    )

    plt.show()


def Pandas_DataFrame(all_five: dict):
    all_ff = {}
    max_len = max([len(five) for five in all_five.values()])
    for five in all_five.items():
        all_ff[five[0]] = [f'{f[0]}[{f[1]}]' for f in five[1]]
        all_ff[five[0]].extend([None]*(max_len-len(all_ff[five[0]])))

    #pandas.set_option('display.unicode.ambiguous_as_wide', True)
    #pandas.set_option('display.unicode.east_asian_width', True)
    #pandas.set_option('display.width', 360)
    d = df(all_ff)
    print(tabulate(d, headers=d.head(0), tablefmt='fancy_grid'))


if __name__ == '__main__':
    # updateNb()

    all_five = {}
    for ty in gacha_ty.items():
        try:
            all_five[ty[1]] = AnalysisGacha(ty[0])
        except GachaException as g:
            print(g.what())

    Pandas_DataFrame(all_five)
    # SeeIt(all_five)
