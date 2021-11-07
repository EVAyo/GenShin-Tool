using DGP.Genshin.Common.Request;
using DGP.Genshin.Common.Response;
using System.Threading.Tasks;

namespace DGP.Genshin.MiHoYoAPI.Mission
{
    public class MissionProvider
    {
        private const string Referer = @"https://webstatic.mihoyo.com/app/community-shop/index.html?bbs_presentation_style=no_header";
        private const string ApiTakumi = @"https://api-takumi.mihoyo.com";

        private readonly string cookie;
        public MissionProvider(string cookie)
        {
            this.cookie = cookie;
        }
        /// <summary>
        /// 获取米游币任务
        /// </summary>
        /// <returns></returns>
        public async Task<MissionWrapper?> GetMissionsAsync()
        {
            Requester requester = new(new RequestOptions
            {
                {"Accept", RequestOptions.Json },
                {"User-Agent", RequestOptions.CommonUA2101 },
                {"Referer",Referer },
                {"Cookie", cookie },
                {"x_Request_with",RequestOptions.Hyperion }
            });
            Response<MissionWrapper>? resp =
                await requester.GetAsync<MissionWrapper>($"{ApiTakumi}/apihub/wapi/getMissions?point_sn=myb");
            return resp?.Data;
        }
    }
}
