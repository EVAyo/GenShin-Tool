##

import numpy as np
import pandas as pd
import json

if __name__ == '__main__':
    print('reading.')
    pd = pd.read_excel(
        "20211122_120727.xlsx",
        sheet_name=['角色活动祈愿', '武器活动祈愿', '常驻祈愿', '新手祈愿']
    )

    for item in [('角色活动祈愿', '301'), ('武器活动祈愿', '302'), ('常驻祈愿', '200'), ('新手祈愿', '100')]:
        all_data = []
        for lable, gacha in pd[item[0]].iterrows():
            all_data.append({
                "uid": "100266228",
                "gacha_type": item[1],
                "item_id": "",
                "count": "1",
                "time": gacha[0],
                "name": gacha[1],
                "lang": "zh-cn",
                "item_type": gacha[2],
                "rank_type": str(gacha[3]),
                "id": "0"
            })
        all_data.reverse()
        with open(item[1]+'_export.json', 'w', encoding='utf-8') as file:
            json.dump(all_data, fp=file, ensure_ascii=False, indent=4)
