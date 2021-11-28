using System;
using System.Collections.Generic;
using System.Linq;

namespace DGP.Genshin.MiHoYoAPI.Gacha
{
    /// <summary>
    /// 包装了包含Uid与抽卡记录的字典
    /// 所有与抽卡记录相关的服务都基于对此类的操作
    /// </summary>
    public class GachaDataCollection : Dictionary<string, GachaData>
    {
        public event Action<string>? UidAdded;

        /// <summary>
        /// 向集合添加数据
        /// 触发uid增加事件，便于前台响应
        /// </summary>
        /// <param name="uid"></param>
        /// <param name="data"></param>
        public new void Add(string uid, GachaData data)
        {
            base.Add(uid, data);
            UidAdded?.Invoke(uid);
        }

        /// <summary>
        /// 获取最新的时间戳id
        /// </summary>
        /// <returns>default 0</returns>
        public long GetNewestTimeId(ConfigType type, string? uid)
        {
            string? typeId = type.Key;
            if (uid is null || typeId is null)
            {
                return 0;
            }
            //有uid有卡池记录就读取最新物品的id,否则返回0
            if (ContainsKey(uid))
            {
                if (this[uid] is GachaData matchedData)
                {
                    if (matchedData.ContainsKey(typeId))
                    {
                        if (matchedData[typeId] is List<GachaLogItem> item)
                        {
                            if (item.Any())
                            {
                                return item[0].TimeId;
                            }
                        }
                    }
                }
            }
            return 0;
        }
    }
}
