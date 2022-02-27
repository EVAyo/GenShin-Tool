# ?pageSize=5&pageNum=12&channelId=10

import wget
from bs4 import BeautifulSoup
from kokomi.miHoYo.HoYoLAB import api


def GetAllNews():
    param = {
        "pageSize": 200,
        "pageNum": 1,
        "channelId": 10
    }
    data = api.getConntentList(params=param)
    return data


def getImgLink(contentId: int):
    resp = api.getContent({'contentId': contentId, 'around': 1})
    bs = BeautifulSoup(resp['content'], features="lxml")
    return bs.find('img').attrs['src']


if __name__ == "__main__":
    data = GetAllNews()
    for item in data['list']:
        try:
            if '生日' in item['title']:
                u = getImgLink(item['contentId'])
                wget.download(u, bar=None)
        except Exception as e:
            print(e)
