using System.Collections.Generic;

namespace DGP.Genshin.MiHoYoAPI.Gacha
{
    /// <summary>
    /// 包装了包含Uid与抽卡记录的字典
    /// </summary>
    public class GachaDataCollection : Dictionary<string, GachaData>
    {
        /// <summary>
        /// 获取最新的时间戳id
        /// </summary>
        /// <returns>default 0</returns>
        public long GetNewestTimeId(ConfigType type, string? uid)
        {
            //有uid有卡池记录就读取最新物品的id,否则返回0
            if (uid is not null && ContainsKey(uid))
            {
                if (type.Key is not null)
                {
                    if (this[uid] is GachaData one)
                    {
                        if (one.ContainsKey(type.Key))
                        {
                            var item = one[type.Key];
                            if (item is not null)
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
