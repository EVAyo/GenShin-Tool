using DGP.Genshin.Common.Request;
using DGP.Genshin.Common.Response;
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
        /// 获取角色详细计算信息
        /// </summary>
        /// <param name="avatarId">角色id</param>
        /// <param name="uid">游戏内uid</param>
        /// <param name="region">服务器名称</param>
        /// <returns></returns>
        public async Task<DetailedAvatar?> GetDetailedAvatarAsync(string avatarId,string uid,string region)
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
            Response<DetailedAvatar>? resp = await requester.GetAsync<DetailedAvatar>
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
                ($"{ApiTakumi}/event/e20200928calculate/v2/compute",promotion);
            return resp?.Data;
        }
    }
}
