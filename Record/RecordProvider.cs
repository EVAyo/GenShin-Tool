using DGP.Genshin.Common.Request;
using DGP.Genshin.Common.Request.DynamicSecret;
using System.Collections.Generic;
using System.Linq;

namespace DGP.Genshin.MiHoYoAPI.Record
{
    public class RecordProvider : IApiTakumiInterop
    {
        private const string BaseUrl = @"https://api-takumi.mihoyo.com/game_record/app/genshin/api";
        private const string Referer = @"https://webstatic.mihoyo.com/app/community-game-records/index.html?v=6";

        private readonly Requester requester;

        public RecordProvider(string cookie)
        {
            requester = new(new RequestOptions
            {
                {"Accept", RequestOptions.Json },
                {"x-rpc-app_version", DynamicSecretProvider2.AppVersion },
                {"User-Agent", RequestOptions.CommonUA2111 },
                {"x-rpc-client_type", "5" },
                {"Referer",Referer },
                {"Cookie", cookie },
                {"X-Requested-With", RequestOptions.Hyperion }
            });
        }

        /// <summary>
        /// 解析玩家服务器
        /// </summary>
        /// <param name="uid"></param>
        /// <returns></returns>
        public string? EvaluateUidRegion(string? uid)
        {
            if (string.IsNullOrEmpty(uid))
            {
                return null;
            }
            return uid[0] switch
            {
                >= '1' and <= '4' => "cn_gf01",
                '5' => "cn_qd01",
                '6' => "os_usa",
                '7' => "os_euro",
                '8' => "os_asia",
                '9' => "os_cht",
                _ => null
            };
        }

        /// <summary>
        /// 获取玩家基础信息
        /// </summary>
        /// <param name="uid"></param>
        /// <param name="server"></param>
        /// <returns></returns>
        public PlayerInfo? GetPlayerInfo(string uid, string server)
        {
            return requester.GetWhileUpdateDynamicSecret2<PlayerInfo>(
                $@"{BaseUrl}/index?server={server}&role_id={uid}");
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="uid"></param>
        /// <param name="server"></param>
        /// <param name="type">1：当期，2：上期</param>
        /// <returns></returns>
        public SpiralAbyss.SpiralAbyss? GetSpiralAbyss(string uid, string server, int type)
        {
            return requester.GetWhileUpdateDynamicSecret2<SpiralAbyss.SpiralAbyss>(
                $@"{BaseUrl}/spiralAbyss?schedule_type={type}&server={server}&role_id={uid}");
        }

        /// <summary>
        /// 获取玩家活动信息
        /// </summary>
        /// <param name="uid"></param>
        /// <param name="server"></param>
        /// <returns></returns>
        public dynamic? GetActivities(string uid, string server)
        {
            return requester.GetWhileUpdateDynamicSecret2<dynamic>(
                $@"{BaseUrl}/activities?server={server}&role_id={uid}");
        }

        /// <summary>
        /// 获取玩家角色详细信息
        /// </summary>
        /// <param name="uid"></param>
        /// <param name="server"></param>
        /// <param name="playerInfo">玩家的基础信息</param>
        /// <returns></returns>
        public Avatar.DetailedAvatarInfo? GetDetailAvaterInfo(string uid, string server, PlayerInfo playerInfo)
        {
            List<Avatar.Avatar>? avatars = playerInfo.Avatars;

            var data = new
            {
                //but normally avatars will not be null
                character_ids = avatars is null ? new() : avatars.Select(x => x.Id).ToList(),
                role_id = uid,
                server = server
            };
            return requester.PostWhileUpdateDynamicSecret2<dynamic>(
                $@"{BaseUrl}/character", data);
        }
    }
}
