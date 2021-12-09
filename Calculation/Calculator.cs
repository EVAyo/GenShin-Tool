using DGP.Genshin.Common.Request;
using DGP.Genshin.Common.Response;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace DGP.Genshin.MiHoYoAPI.Calculation
{
    public class Calculator
    {
        private const string ApiTakumi = @"https://api-takumi.mihoyo.com";
        private const string ReferBaseUrl = @"https://webstatic.mihoyo.com/ys/event/e20200923adopt_calculator/index.html";

        private static readonly string Referer =
            $"{ReferBaseUrl}?bbs_presentation_style=fullscreen&bbs_auth_required=true&mys_source=GameRecord";

        private readonly string cookie;

        public Calculator(string cookie)
        {
            this.cookie = cookie;
        }

        /// <summary>
        /// 同步当前cookie的角色
        /// </summary>
        /// <param name="uid"></param>
        /// <param name="server"></param>
        /// <param name="isSync">是否同步玩家角色信息</param>
        /// <param name="isRandomDelayEnabled"></param>
        /// <returns></returns>
        public async Task<List<Avatar>> GetAvatarListAsync(string uid, string server, bool isSync, bool isRandomDelayEnabled = false)
        {
            int currentPage = 1;
            Random random = new();
            Requester requester = new(new RequestOptions
            {
                {"Accept", RequestOptions.Json },
                {"User-Agent", RequestOptions.CommonUA2101 },
                {"Referer", Referer },
                {"Cookie", cookie },
                {"X-Requested-With", RequestOptions.Hyperion }
            });
            List<Avatar> syncedAvatars = new();
            Response<ListWrapper<Avatar>>? resp;
            do
            {
                AvatarFilterData data = new() { Page = currentPage, Size = 20, Uid = uid, Region = server };
                resp = await requester.PostAsync<ListWrapper<Avatar>>
                    ($"{ApiTakumi}/event/e20200928calculate/v1{(isSync ? "/sync" : "")}/avatar/list", data);
                //add to cached list
                if (resp?.Data?.List is not null)
                {
                    syncedAvatars.AddRange(resp.Data.List);
                }

                if (currentPage != 1 && isRandomDelayEnabled)
                {
                    await Task.Delay(random.Next(0, 1000));
                }
                currentPage++;
            }
            while (resp?.Data?.List?.Count == 20);

            return syncedAvatars;
        }

        /// <summary>
        /// 获取角色详细计算信息
        /// </summary>
        /// <param name="avatarId">角色id</param>
        /// <param name="uid">游戏内uid</param>
        /// <param name="region">服务器名称</param>
        /// <returns></returns>
        public async Task<AvatarDetailData?> GetAvatarDetailDataAsync(int avatarId, string uid, string region)
        {
            Requester requester = new(new RequestOptions
            {
                {"Accept", RequestOptions.Json },
                {"User-Agent", RequestOptions.CommonUA2101 },
                {"Referer", Referer },
                {"Cookie", cookie },
                {"X-Requested-With", RequestOptions.Hyperion }
            });
            //https://api-takumi.mihoyo.com
            Response<AvatarDetailData>? resp = await requester.GetAsync<AvatarDetailData>
                ($"{ApiTakumi}/event/e20200928calculate/v1/sync/avatar/detail?avatar_id={avatarId}&uid={uid}&region={region}");
            return resp?.Data;
        }

        /// <summary>
        /// 计算所需的材料
        /// </summary>
        /// <param name="promotion">提升的增量</param>
        /// <returns>所需的材料</returns>
        public async Task<Consumption?> ComputeAsync(AvatarPromotionDelta promotion)
        {
            Requester requester = new(new RequestOptions
            {
                {"Accept", RequestOptions.Json },
                {"User-Agent", RequestOptions.CommonUA2101 },
                {"Referer", Referer },
                {"Cookie", cookie },
                {"X-Requested-With", RequestOptions.Hyperion }
            });
            Response<Consumption>? resp = await requester.PostAsync<Consumption>
                ($"{ApiTakumi}/event/e20200928calculate/v2/compute", promotion);
            return resp?.Data;
        }
        //获取未拥有的角色的技能
        //https://api-takumi.mihoyo.com/event/e20200928calculate/v1/avatarSkill/list?avatar_id=10000054&element_attr_id=6
    }
}
