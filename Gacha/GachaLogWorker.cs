using DGP.Genshin.MiHoYoAPI.Request;
using DGP.Genshin.MiHoYoAPI.Request.QueryString;
using DGP.Genshin.MiHoYoAPI.Response;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;

namespace DGP.Genshin.MiHoYoAPI.Gacha
{
    /// <summary>
    /// 联机抽卡记录
    /// </summary>
    public class GachaLogWorker
    {
        public GachaDataCollection WorkingGachaData { get; set; }

        private string? workingUid;

        #region Initialization
        private readonly int batchSize;
        private readonly string gachaLogUrl;

        public GachaLogWorker(string gachaLogUrl,GachaDataCollection gachaData, int batchSize = 20)
        {
            this.gachaLogUrl = gachaLogUrl;
            WorkingGachaData = gachaData;
            this.batchSize = batchSize;
        }
        #endregion

        private Config? gachaConfig;
        public Config? GachaConfig
        {
            get
            {
                if (gachaConfig == null)
                {
                    gachaConfig = GetGachaConfig();
                }

                return gachaConfig;
            }
        }

        /// <summary>
        /// 获取祈愿池信息
        /// </summary>
        /// <returns>网络问题导致的可能会返回null</returns>
        private Config? GetGachaConfig()
        {
            Requester requester = new(new RequestOptions
            {
                {"Accept", RequestOptions.Json },
                {"User-Agent", RequestOptions.CommonUA2101 }
            });
            Response<Config>? resp = requester.Get<Config>(gachaLogUrl?.Replace("getGachaLog?", "getConfigList?"));
            return resp?.Data;
        }
        /// <summary>
        /// 随机延时用
        /// </summary>
        private readonly Random random = new();

        public event Action<FetchProgress>? OnFetchProgressed;

        /// <summary>
        /// 获取单个奖池的祈愿记录增量信息
        /// </summary>
        /// <param name="type">卡池类型</param>
        public void FetchGachaLogIncrement(ConfigType type)
        {
            List<GachaLogItem> increment = new();
            int currentPage = 0;
            long endId = 0;
            do
            {
                if (TryGetBatch(out GachaLog gachaLog, type, endId, ++currentPage))
                {
                    if (gachaLog.List is not null)
                    {
                        foreach (GachaLogItem item in gachaLog.List)
                        {
                            workingUid = item.Uid;
                            Debug.Assert(workingUid is not null);
                            //this one is increment
                            if (item.TimeId > WorkingGachaData.GetNewestTimeId(type, item.Uid))
                            {
                                increment.Add(item);
                            }
                            else//already done the new item
                            {
                                MergeIncrement(type, increment);
                                return;
                            }
                        }
                        //last page
                        if (gachaLog.List.Count < batchSize)
                        {
                            break;
                        }
                        endId = gachaLog.List.Last().TimeId;
                    }
                }
                else
                {
                    //url not valid
                    break;
                }
                Task.Delay(1000 + random.Next(0, 1000)).Wait();
            } while (true);
            //first time fecth could go here
            MergeIncrement(type, increment);
        }

        /// <summary>
        /// 合并增量
        /// </summary>
        /// <param name="type">卡池类型</param>
        /// <param name="increment">增量</param>
        private void MergeIncrement(ConfigType type, List<GachaLogItem> increment)
        {
            if (workingUid is null)
            {
                throw new InvalidOperationException($"{nameof(workingUid)}不应为 null");
            }

            //简单的将老数据插入到增量后侧，最后重置数据
            GachaData? dict = WorkingGachaData[workingUid];
            string? key = type.Key;
            if (key is not null)
            {
                if (dict.ContainsKey(key))
                {
                    List<GachaLogItem>? local = dict[key];
                    if (local is not null)
                    {
                        increment.AddRange(local);
                    }
                }
                dict[key] = increment;
            }
        }

        /// <summary>
        /// 尝试获得20个奖池物品
        /// </summary>
        /// <param name="result">空列表或包含数据的列表</param>
        /// <param name="type"></param>
        /// <param name="endId"></param>
        /// <returns></returns>
        private bool TryGetBatch(out GachaLog result, ConfigType type, long endId, int currentPage)
        {
            OnFetchProgressed?.Invoke(new() { Type = type.Name, Page = currentPage });
            //modify the url
            string[]? splitedUrl = gachaLogUrl?.Split('?');
            string? baseUrl = splitedUrl?[0];

            //parse querystrings
            QueryString query = QueryString.Parse(splitedUrl?[1]);
            query.Set("gacha_type", type.Key);
            //20 is the max size the api can return
            query.Set("size", batchSize.ToString());
            query.Set("lang", "zh-cn");
            query.Set("end_id", endId.ToString());
            string finalUrl = $"{baseUrl}?{query}";

            Requester requester = new(new RequestOptions
            {
                {"Accept", RequestOptions.Json },
                {"User-Agent", RequestOptions.CommonUA2101 }
            });
            Response<GachaLog>? resp = requester.Get<GachaLog>(finalUrl);

            if (resp?.ReturnCode == 0)
            {
                result = resp.Data ?? new();
                return true;
            }
            else
            {
                result = new();
                return false;
            }
        }
    }
}
