from typing import Tuple, Optional
from os.path import exists, sep
from assets.data.pokedex import roleId, weapon


def roleIdToName(keyword) -> Tuple[int, str]:
    if not keyword:
        return 0, ""
    for key, value in roleId.items():
        for i in value:
            if i == keyword:
                return key, value[0]
    return 0, ""


def weaponToName(keyword) -> str:
    for key, value in weapon.items():
        if keyword == key or keyword in value:
            return key
    return ""


async def get_pokedex(name: str) -> Tuple[str, Optional[str]]:
    if name not in ["风主", "岩主", "雷主"]:
        cid, cname = roleIdToName(name)
        if cid in [10000005, 10000007, 20000000]:
            return "请选择：风主图鉴、岩主图鉴、雷主图鉴", None
        if not cid:
            # 武器图鉴
            wid = weaponToName(name)
            if not wid:
                return "请输入正确的角色/武器名称", None
            if exists(f"assets{sep}pokedex{sep}weaponInfo_xiaoyao{sep}{wid}.png"):
                return "", f"assets{sep}pokedex{sep}weaponInfo_xiaoyao{sep}{wid}.png"
            return "未找到资源文件", None
    else:
        cname = name
    if exists(f"assets{sep}pokedex{sep}rolesInfo_xiaoyao{sep}{cname}.png"):
        return "", f"assets{sep}pokedex{sep}rolesInfo_xiaoyao{sep}{cname}.png"
    return "未找到资源文件", None


async def get_strategy(name: str) -> Tuple[str, Optional[str]]:
    cid, cname = roleIdToName(name)
    if not cid:
        return "请输入正确的角色名称", None
    if exists(f"assets{sep}pokedex{sep}strategy_xf{sep}{cname}.jpg"):
        return "", f"assets{sep}pokedex{sep}strategy_xf{sep}{cname}.jpg"
    return f"暂无 {cname} 的攻略", None
