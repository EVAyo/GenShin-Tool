using DGP.Genshin.MiHoYoAPI.Request;
using DGP.Genshin.MiHoYoAPI.Request.DynamicSecret;
using DGP.Genshin.MiHoYoAPI.Response;

namespace DGP.Genshin.MiHoYoAPI.UserInfo
{
    public class UserInfoProvider
    {
        public const string Referer = @"https://bbs.mihoyo.com/";
        public const string BaseUrl = @"https://bbs-api.mihoyo.com/user/wapi";

        private readonly string cookie;
        public UserInfoProvider(string cookie)
        {
            this.cookie = cookie;
        }

        public UserInfo? GetUserInfo()
        {
            Requester requester = new(new RequestOptions
            {
                {"DS", DynamicSecretProvider.Create() },
                {"x-rpc-app_version", DynamicSecretProvider.AppVersion },
                {"User-Agent", RequestOptions.CommonUA2101 },
                {"x-rpc-device_id", RequestOptions.DeviceId },
                {"Accept", RequestOptions.Json },
                {"x-rpc-client_type", "4" },
                {"Referer",Referer },
                {"Cookie", cookie }
            });
            Response<UserInfoWrapper>? resp = requester.Get<UserInfoWrapper>($"{BaseUrl}/getUserFullInfo?gids=2");
            return resp?.Data?.UserInfo;
        }
    }
}
