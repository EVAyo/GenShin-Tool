using DGP.Genshin.Common.Request;
using DGP.Genshin.Common.Request.DynamicSecret;
using DGP.Genshin.MiHoYoAPI.User;

namespace DGP.Genshin.MiHoYoAPI.Sign
{
    public class SignInProvider
    {
        private const string ApiTakumi = @"https://api-takumi.mihoyo.com";
        private const string ReferBaseUrl = @"https://webstatic.mihoyo.com/bbs/event/signin-ys/index.html";
        private const string ActivityId = "e202009291139501";

        private static readonly string Referer =
            $"{ReferBaseUrl}?bbs_auth_required=true&act_id={ActivityId}&utm_source=bbs&utm_medium=mys&utm_campaign=icon";

        private readonly string cookie;

        /// <summary>
        /// 初始化 <see cref="SignInProvider"/> 的实例
        /// </summary>
        /// <param name="cookie"></param>
        public SignInProvider(string cookie)
        {
            this.cookie = cookie;
        }

        /// <summary>
        /// 签到通用请求器
        /// </summary>
        private Requester SignInRequester
        {
            get
            {
                return new(new RequestOptions
                {
                    {"DS", DynamicSecretProvider.Create() },
                    {"x-rpc-app_version", DynamicSecretProvider.AppVersion },
                    {"User-Agent", RequestOptions.CommonUA2101 },
                    {"x-rpc-device_id", RequestOptions.DeviceId },
                    {"Accept", RequestOptions.Json },
                    {"x-rpc-client_type", "5" },
                    {"Referer", Referer },
                    {"Cookie", cookie },
                    {"X-Requested-With", RequestOptions.Hyperion }
                });
            }
        }

        /// <summary>
        /// 获取当前签到信息
        /// </summary>
        /// <param name="role"></param>
        /// <returns></returns>
        public SignInInfo? GetSignInInfo(UserGameRole role)
        {
            Requester requester = new(new RequestOptions
            {
                {"Accept", RequestOptions.Json },
                {"User-Agent",RequestOptions.CommonUA2101 },
                {"x-rpc-device_id", RequestOptions.DeviceId },
                {"Referer", Referer },
                {"Cookie", cookie },
                {"X-Requested-With", RequestOptions.Hyperion }
            });
            string query = $"act_id={ActivityId}&region={role.Region}&uid={role.GameUid}";
            return requester.Get<SignInInfo>($"{ApiTakumi}/event/bbs_sign_reward/info?{query}")?.Data;
        }

        /// <summary>
        /// 获取当前补签信息
        /// </summary>
        /// <param name="role"></param>
        /// <returns></returns>
        public ReSignInfo? GetReSignInfoAsync(UserGameRole role)
        {
            Requester requester = new(new RequestOptions
            {
                {"Accept", RequestOptions.Json },
                {"User-Agent",RequestOptions.CommonUA2101 },
                {"Referer", Referer },
                {"Cookie", cookie },
                {"X-Requested-With", RequestOptions.Hyperion }
            });
            string query = $"act_id={ActivityId}&region={role.Region}&uid={role.GameUid}";
            return requester.Get<ReSignInfo>($"{ApiTakumi}/event/bbs_sign_reward/resign_info?{query}")?.Data;
        }

        /// <summary>
        /// 签到
        /// </summary>
        /// <param name="role"></param>
        /// <returns></returns>
        public SignInResult? SignIn(UserGameRole role)
        {
            var data = new { act_id = ActivityId, region = role.Region, uid = role.GameUid };
            Requester requester = SignInRequester;
            return requester.Post<SignInResult>($"{ApiTakumi}/event/bbs_sign_reward/sign", data)?.Data;
        }

        /// <summary>
        /// 补签
        /// </summary>
        /// <param name="role"></param>
        /// <returns></returns>
        public SignInResult? ReSign(UserGameRole role)
        {
            var data = new { act_id = ActivityId, region = role.Region, uid = role.GameUid };
            Requester requester = SignInRequester;
            return requester.Post<SignInResult>($"{ApiTakumi}/event/bbs_sign_reward/sign", data)?.Data;
        }

        /// <summary>
        /// 获取签到奖励
        /// </summary>
        /// <returns></returns>
        public SignInReward? GetSignInReward()
        {
            Requester requester = new(new RequestOptions
            {
                {"Accept", RequestOptions.Json },
                {"User-Agent", RequestOptions.CommonUA2101 },
                {"Referer", Referer },
                {"Cookie", cookie },
                {"X-Requested-With", RequestOptions.Hyperion }
            });

            return requester.Get<SignInReward>($"{ApiTakumi}/event/bbs_sign_reward/home?act_id={ActivityId}")?.Data;
        }
    }
}
