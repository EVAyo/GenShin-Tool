using DGP.Genshin.Common.Exceptions;
using DGP.Genshin.Common.Request;
using DGP.Genshin.Common.Request.DynamicSecret;
using DGP.Genshin.MiHoYoAPI.Record.Avatar;
using System;
using System.Collections.Generic;
using System.Diagnostics.CodeAnalysis;
using System.Linq;
using System.Threading.Tasks;

namespace DGP.Genshin.MiHoYoAPI.Record
{
    public class RecordProvider : IApiTakumiInterop
    {
        private const string ApiTakumi = @"https://api-takumi.mihoyo.com";
        private const string BaseUrl = @"https://api-takumi.mihoyo.com/game_record/app/genshin/api";
        private const string Referer = @"https://webstatic.mihoyo.com/app/community-game-records/index.html?v=6";

        private readonly Requester requester;

        /// <summary>
        /// 使用同一个提供器可用重复请求
        /// </summary>
        /// <param name="cookie"></param>
        public RecordProvider(string cookie)
        {
            requester = new(new RequestOptions
            {
                {"Accept", RequestOptions.Json },
                {"x-rpc-app_version", DynamicSecretProvider2.AppVersion },
                {"User-Agent", RequestOptions.CommonUA2161 },
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
            return string.IsNullOrEmpty(uid)
                ? null
                : uid[0] switch
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
        public async Task<PlayerInfo?> GetPlayerInfoAsync(string uid, string server)
        {
            return await requester.GetWhileUpdateDynamicSecret2Async<PlayerInfo>(
                $@"{BaseUrl}/index?server={server}&role_id={uid}");
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="uid"></param>
        /// <param name="server"></param>
        /// <param name="type">1：当期，2：上期</param>
        /// <returns></returns>
        public async Task<SpiralAbyss.SpiralAbyss?> GetSpiralAbyssAsync(string uid, string server, int type)
        {
            return await requester.GetWhileUpdateDynamicSecret2Async<SpiralAbyss.SpiralAbyss>(
                $@"{BaseUrl}/spiralAbyss?schedule_type={type}&server={server}&role_id={uid}");
        }

        /// <summary>
        /// 获取玩家活动信息
        /// </summary>
        /// <param name="uid"></param>
        /// <param name="server"></param>
        /// <returns></returns>
        public async Task<dynamic?> GetActivitiesAsync(string uid, string server)
        {
            return await requester.GetWhileUpdateDynamicSecret2Async<dynamic>(
                $@"{BaseUrl}/activities?server={server}&role_id={uid}");
        }

        /// <summary>
        /// 获取玩家角色详细信息
        /// 经过修改后已经支持获取全角色信息
        /// </summary>
        /// <param name="uid"></param>
        /// <param name="server"></param>
        /// <param name="playerInfo">玩家的基础信息</param>
        /// <returns></returns>
        [SuppressMessage("", "IDE0037")]
        public async Task<DetailedAvatarInfo?> GetDetailAvaterInfoAsync(string uid, string server, PlayerInfo playerInfo, bool isUsingBypassMethod = false)
        {
            if (isUsingBypassMethod)
            {
                //bypass mihoyo's api limit by attemptting request all avatar at same time
                List<Task<DetailedAvatarInfo?>> tasks = new();
                Random random = new();
                foreach (int id in Enumerable.Range(10000002, 80))
                {
                    var data = new
                    {
                        character_ids = new List<int> { id },
                        role_id = uid,
                        server = server
                    };
                    Task<DetailedAvatarInfo?> task = requester.PostWhileUpdateDynamicSecret2Async<DetailedAvatarInfo>(
                        $@"{BaseUrl}/character", data);
                    tasks.Add(task);
                }
                DetailedAvatarInfo?[] result = await Task.WhenAll(tasks);
                return new() { Avatars = result.Where(info => info is not null).SelectMany(info => info!.Avatars ?? new()).ToList() };
            }
            else
            {
                //original method
                List<Avatar.Avatar>? avatars = playerInfo.Avatars;
                var data = new
                {
                    character_ids = avatars?.Select(x => x.Id).ToList() ?? throw new SnapGenshinInternalException("avatars 不应为 null"),
                    role_id = uid,
                    server = server
                };
                return await requester.PostWhileUpdateDynamicSecret2Async<DetailedAvatarInfo>(
                    $@"{BaseUrl}/character", data);
            }
        }

        /// <summary>
        /// 开关记录数据
        /// </summary>
        /// <param name="isPublic">开关状态</param>
        /// <param name="switchId">"1"：个人主页卡片 "2"：角色详情数据</param>
        /// <returns></returns>
        [UnTestedAPI]
        public async Task<dynamic?> ChangeRecordDataSwitch(bool isPublic, string switchId)
        {
            var data = new { is_public = isPublic, switch_id = switchId, game_id = "2" };
            return await requester.PostWhileUpdateDynamicSecret2Async<dynamic>(
                $"{ApiTakumi}/game_record/app/card/wapi/changeDataSwitch", data);
        }
    }
}
