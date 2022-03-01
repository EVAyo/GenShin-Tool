# 胡桃 API
由 DGP Studio 开发部署的一套深渊数据统计API

## 注意
首先请务必加入 [此页面上的开发群](https://github.com/DGP-Studio/Snap.Genshin) 取得唯一的Id与Token  
在取得appid与secret后才能正常的请求API  
胡桃 API 的主机名称为 `https://hutao-api.snapgenshin.com`,下文将做出省略

## 开始接入

```
POST /Auth/Login
Content-Type: text/json; charset=utf-8

{
  "Appid": "your appid",
  "Secret": "your secret"
}
```

``` json
{
    "retcode":0,
    "message":"\u767B\u5F55\u6210\u529F",
    "data":{
        "accessToken":"returned access token"
    }
}
```
此处返回的access token 将用来请求后续的数据接口

## 物品列表

### 角色

```
GET /GenshinItems/Avatars
Authorization: Bearer your access token
```

``` json
{
    "retcode":0,
    "message":"\u89D2\u8272\u6570\u636E\u67E5\u8BE2\u6210\u529F",
    "data":[
        {
            "id":10000016,
            "name":"\u8FEA\u5362\u514B",
            "url":"https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Diluc.png"
        }
    ]
}
```

### 武器

```
GET /GenshinItems/Weapons
Authorization: Bearer your access token
```

``` json
{
    "retcode":0,
    "message":"\u6B66\u5668\u6570\u636E\u67E5\u8BE2\u6210\u529F",
    "data":[
        {
            "id":12502,
            "name":"\u72FC\u7684\u672B\u8DEF",
            "url":"https://upload-bbs.mihoyo.com/game_record/genshin/equip/UI_EquipIcon_Claymore_Wolfmound.png"
        }
    ]
}
```

### 圣遗物套装

```
GET /GenshinItems/Reliquaries
Authorization: Bearer your access token
```

``` json
{
    "retcode":0,
    "message":"\u5723\u9057\u7269\u6570\u636E\u67E5\u8BE2\u6210\u529F",
    "data":[
        {
            "id":2150061,
            "name":"\u70BD\u70C8\u7684\u708E\u4E4B\u9B54\u5973",
            "url":"https://upload-bbs.mihoyo.com/game_record/genshin/equip/UI_RelicIcon_15006_4.png"
        }
    ]
}
```

## 统计

### 角色出场率

```
GET /Statistics/AvatarParticipation
Authorization: Bearer your access token
```

``` json
{
    "retcode":0,
    "message":"\u51FA\u573A\u7387\u6570\u636E\u83B7\u53D6\u6210\u529F",
    "data":[
        {
            "floor":9,
            "avatarUsage":[
                {
                    "id":10000046,
                    "value":0.06097560975609756
                }
            ]
        }
    ]
}
```

### 角色命座持有

```
GET /Statistics/Constellation
Authorization: Bearer your access token
```

``` json
{
    "retcode":0,
    "message":"\u547D\u5EA7\u6570\u636E\u83B7\u53D6\u6210\u529F",
    "data":[
        {
            "avatar":10000022,
            "holdingRate":0.486024486024486,
            "rate":[
                {
                    "id":0,
                    "value":0.8578897338403042
                }
            ]
        }
    ]
}
```

### 角色搭配

```
GET /Statistics/TeamCollocation
Authorization: Bearer your access token
```

``` json
{
    "retcode":0,
    "message":"\u7EC4\u961F\u6570\u636E\u83B7\u53D6\u6210\u529F",
    "data":[
        {
            "avater":10000046,
            "collocations":[
                {
                    "id":10000030,
                    "value":0.30357142857142855
                }
            ]
        }
    ]
}
```

### 武器搭配

```
GET /Statistics/WeaponUsage
Authorization: Bearer your access token
```

``` json
{
    "retcode":0,
    "message":"\u6B66\u5668\u6570\u636E\u83B7\u53D6\u6210\u529F",
    "data":[
        {
            "avatar":10000022,
            "weapons":[
                {
                    "id":15402,
                    "value":0.29990494296577946
                }
            ]
        }
    ]
}
```

### 圣遗物搭配

```
GET /Statistics/AvatarReliquaryUsage
Authorization: Bearer your access token
```

``` json
{
    "retcode":0,
    "message":"\u5723\u9057\u7269\u6570\u636E\u83B7\u53D6\u6210\u529F",
    "data":[
        {
            "avatar":10000022,
            "reliquaryUsage":[
                {
                    "id":"2150021-4",
                    "value":0.8710152035311427
                }
            ]
        }
    ]
}
```

### 队伍上场次数

```
GET /Statistics/TeamCombination
Authorization: Bearer your access token
```

``` json
{
    "retcode":0,
    "message":"\u961F\u4F0D\u4F7F\u7528\u6570\u636E\u83B7\u53D6\u6210\u529F",
    "data":[
        {
            "level":{
                "floor":9,
                "index":1
            },
            "teams":[
                {
                    "id":{
                        "upHalf":"10000025,10000030,10000043,10000046",
                        "downHalf":"10000022,10000023,10000032,10000037"
                    },
                    "value":1
                }
            ]
        }
    ]
}
```

### 人数统计

```
GET /Statistics/Overview
Authorization: Bearer your access token
```

``` json
{
    "retcode":0,
    "message":"\u603B\u89C8\u6570\u636E\u83B7\u53D6\u6210\u529F",
    "data":{
        "totalPlayerCount":4329,
        "collectedPlayerCount":29,
        "fullStarPlayerCount":8
    }
}
```

## 上传

为了确保上传数据的有效性，请联系我们进一步确认