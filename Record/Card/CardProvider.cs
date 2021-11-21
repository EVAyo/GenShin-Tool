using DGP.Genshin.Common.Request;
using DGP.Genshin.Common.Request.DynamicSecret;
using DGP.Genshin.Common.Response;
using System.Threading.Tasks;

namespace DGP.Genshin.MiHoYoAPI.Record.Card
{
    public class CardProvider
    {
        private const string ApiTakumi = @"https://api-takumi.mihoyo.com";
        private const string Referer = "https://webstatic.mihoyo.com/app/community-game-records/index.html?bbs_presentation_style=fullscreen";
        private readonly string cookie;

        /// <summary>
        /// 初始化 <see cref="CardProvider"/> 的实例
        /// </summary>
        /// <param name="cookie"></param>
        public CardProvider(string cookie)
        {
            this.cookie = cookie;
        }

        /// <summary>
        /// 获取游戏展示卡片信息
        /// </summary>
        /// <param name="uid">米游社uid，可以是别人的uid</param>
        /// <returns></returns>
        public async Task<ListWrapper<Card>?> GetGameRecordCardAsync(string uid)
        {
            Requester requester = new(new RequestOptions
            {
                {"Accept", RequestOptions.Json },
                {"x-rpc-app_version", DynamicSecretProvider.AppVersion },
                {"User-Agent",RequestOptions.CommonUA2161 },
                {"x_rpc_client_type", "5" },
                {"Referer", Referer },
                {"Cookie", cookie },
                {"X-Requested-With", RequestOptions.Hyperion }
            });
            ListWrapper<Card>? resp = await requester.GetWhileUpdateDynamicSecret2Async<ListWrapper<Card>>(
                $"{ApiTakumi}/game_record/app/card/wapi/getGameRecordCard?uid={uid}");
            return resp;
        }

        /// <summary>
        /// 开关米游社数据
        /// </summary>
        /// <param name="isPublic">开关状态</param>
        /// <param name="id">开关的id</param>
        /// <returns></returns>
        public async Task<dynamic?> ChangeDataSwitch(bool isPublic, string id)
        {
            var data = new { is_public = isPublic, switch_id = id, game_id = "2" };
            Requester requester = new(new RequestOptions
            {
                {"Accept", RequestOptions.Json },
                {"x-rpc-app_version", DynamicSecretProvider2.AppVersion },
                {"User-Agent", RequestOptions.CommonUA2161 },
                {"x-rpc-client_type", "5" },
                {"Referer",Referer },
                {"Cookie", cookie },
                {"X-Requested-With", RequestOptions.Hyperion }
            });
            return await requester.PostWhileUpdateDynamicSecret2Async<dynamic>(
                $"{ApiTakumi}/game_record/app/card/wapi/changeDataSwitch", data);
        }
    }
}
