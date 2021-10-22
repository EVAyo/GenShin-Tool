using DGP.Genshin.MiHoYoAPI.Request;
using DGP.Genshin.MiHoYoAPI.Request.DynamicSecret;
using DGP.Genshin.MiHoYoAPI.Response;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DGP.Genshin.MiHoYoAPI.Record
{
    public class RecordProvider
    {
        private const string QueryHistoryFile = "history.dat";
        private const string BaseUrl = @"https://api-takumi.mihoyo.com/game_record/app/genshin/api";
        private const string Referer = @"https://webstatic.mihoyo.com/app/community-game-records/index.html?v=6";

        private readonly Requester requester;
        
        private readonly string cookie;
        public RecordProvider(string cookie)
        {
            this.cookie = cookie;
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

        public async Task<Record> GetRecordAsync(string? uid)
        {
            if (uid is null)
            {
                return new Record("请输入Uid");
            }
            
            //figure out the server
            if (!this.TryEvaluateUidRegion(uid, out string? server))
            {
                return new Record("不支持查询此UID");
            }

            Response<PlayerInfo>? playerInfo = null;
            if (!await Task.Run(() => this.TryGetWhileChangeDS(
                $@"{BaseUrl}/index?server={server}&role_id={uid}", requester, out playerInfo)))
            {
                return new Record($"获取玩家基本信息失败：\n{playerInfo?.Message}");
            }
            Response<SpiralAbyss>? spiralAbyss = null;
            if (!await Task.Run(() => this.TryGetWhileChangeDS(
                $@"{BaseUrl}/spiralAbyss?schedule_type=1&server={server}&role_id={uid}", requester, out spiralAbyss)))
            {
                return new Record($"获取本期深境螺旋信息失败：\n{spiralAbyss?.Message}");
            }
            Response<SpiralAbyss>? lastSpiralAbyss = null;
            if (!await Task.Run(() => this.TryGetWhileChangeDS(
                $@"{BaseUrl}/spiralAbyss?schedule_type=2&server={server}&role_id={uid}", requester, out lastSpiralAbyss)))
            {
                return new Record($"获取上期深境螺旋信息失败：\n{lastSpiralAbyss?.Message}");
            }
            Response<dynamic>? activitiesInfo = null;
            if (!await Task.Run(() => this.TryGetWhileChangeDS(
                $@"{BaseUrl}/activities?server={server}&role_id={uid}", requester, out activitiesInfo)))
            {
                return new Record($"获取活动信息失败：\n{activitiesInfo?.Message}");
            }
            //prepare for character
            requester.Headers.Remove("x-rpc-device_id");
            var data = new
            {
                character_ids = playerInfo?.Data?.Avatars?.Select(x => x.Id).ToList(),
                role_id = uid,
                server = server
            };
            Response<DetailedAvatarInfo>? roles = null;
            if (!await Task.Run(() => this.TryPostWhileChangeDS(
                $@"{BaseUrl}/character", data, requester, out roles)))
            {
                RecordProgressed?.Invoke(null);
                return new Record($"获取详细角色信息失败：\n{roles?.Message}");
            }

            RecordProgressed?.Invoke(null);
            //return
            return roles?.ReturnCode != 0 ? new Record(roles?.Message) : new Record
            {
                Success = true,
                UserId = uid,
                Server = server,
                PlayerInfo = playerInfo?.Data,
                SpiralAbyss = spiralAbyss?.Data,
                LastSpiralAbyss = lastSpiralAbyss?.Data,
                DetailedAvatars = roles.Data?.Avatars,
                Activities = activitiesInfo?.Data
            };
        }

        private bool TryEvaluateUidRegion(string? uid, out string? result)
        {
            if (string.IsNullOrEmpty(uid))
            {
                result = null;
                return false;
            }
            result = uid[0] switch
            {
                >= '1' and <= '4' => "cn_gf01",
                '5' => "cn_qd01",
                '6' => "os_usa",
                '7' => "os_euro",
                '8' => "os_asia",
                '9' => "os_cht",
                _ => null
            };
            return result is not null;    
        }
        private bool TryGetWhileChangeDS<T>(string url, Requester requester, out Response<T>? response)
        {
            requester.Headers["DS"] = DynamicSecretProvider2.Create(url);
            response = requester.Get<T>(url);
            return response?.ReturnCode == 0;
        }
        private bool TryPostWhileChangeDS<T>(string url, object data, Requester requester, out Response<T>? response)
        {
            requester.Headers["DS"] = DynamicSecretProvider2.Create(url, data);
            response = requester.Post<T>(url, data);
            return response?.ReturnCode == 0;
        }
    }
}
