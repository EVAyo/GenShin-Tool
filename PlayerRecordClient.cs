using DGP.Genshin.HutaoAPI.Model;
using DGP.Genshin.MiHoYoAPI.GameRole;
using DGP.Genshin.MiHoYoAPI.Record;
using DGP.Genshin.MiHoYoAPI.Record.Avatar;
using DGP.Genshin.MiHoYoAPI.Record.SpiralAbyss;
using DGP.Genshin.MiHoYoAPI.Request;
using DGP.Genshin.MiHoYoAPI.Response;
using Snap.Exception;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace DGP.Genshin.HutaoAPI
{
    public class PlayerRecordClient
    {
        public const string HutaoAPIHost = "";
        public async Task<List<Response?>> GetAllRecordsAndPostAsync(string cookie)
        {
            RecordProvider recordProvider = new(cookie);
            Requester requester = new();
            List<Response?> results = new();

            List<UserGameRole> userGameRoles = await new UserGameRoleProvider(cookie).GetUserGameRolesAsync();
            foreach(UserGameRole role in userGameRoles)
            {
                _ = role.GameUid ?? throw new UnexceptedNullException("获取uid失败");
                _ = role.Region ?? throw new UnexceptedNullException("获取server失败");

                PlayerInfo? playerInfo = await recordProvider.GetPlayerInfoAsync(role.GameUid, role.Region);
                _ = playerInfo ?? throw new UnexceptedNullException("获取用户角色统计信息失败");

                DetailedAvatarInfo? detailAvatars = await recordProvider.GetDetailAvaterInfoAsync(role.GameUid, role.Region, playerInfo);
                _ = detailAvatars ?? throw new UnexceptedNullException("获取用户角色详细信息失败");

                SpiralAbyss? spiralAbyssInfo = await recordProvider.GetSpiralAbyssAsync(role.GameUid, role.Region, SpiralAbyssType.Current);
                _ = spiralAbyssInfo ?? throw new UnexceptedNullException("获取用户深境螺旋信息失败");

                PlayerRecord playerRecord = BuildPlayerRecord(detailAvatars, spiralAbyssInfo);
                Response<string>? resp = await requester.PostAsync<string>($"{HutaoAPIHost}/statistic/post", playerRecord);
                results.Add(resp);
            }
            return results;
        }

        private PlayerRecord BuildPlayerRecord(DetailedAvatarInfo detailAvatars, SpiralAbyss spiralAbyssInfo)
        {
            throw new NotImplementedException();
        }
    }
}