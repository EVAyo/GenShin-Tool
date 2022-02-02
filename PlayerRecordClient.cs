using DGP.Genshin.HutaoAPI.GetModel;
using DGP.Genshin.HutaoAPI.PostModel;
using DGP.Genshin.MiHoYoAPI.GameRole;
using DGP.Genshin.MiHoYoAPI.Record;
using DGP.Genshin.MiHoYoAPI.Record.Avatar;
using DGP.Genshin.MiHoYoAPI.Record.SpiralAbyss;
using DGP.Genshin.MiHoYoAPI.Request;
using DGP.Genshin.MiHoYoAPI.Response;
using Snap.Exception;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace DGP.Genshin.HutaoAPI
{
    public class PlayerRecordClient
    {
        //snapgenshin.com is coming soon
        private const string HutaoAPIHost = "https://snapgenshin-hutao-api2.irain.in";
        public async Task GetAllRecordsAndUploadAsync(string cookie,
            Func<PlayerRecord, Task<bool>> confirmAsyncFunc, Func<Response, Task> resultAsyncFunc)
        {
            RecordProvider recordProvider = new(cookie);

            List<UserGameRole> userGameRoles = await new UserGameRoleProvider(cookie).GetUserGameRolesAsync();
            foreach (UserGameRole role in userGameRoles)
            {
                _ = role.GameUid ?? throw new UnexceptedNullException("获取uid失败");
                _ = role.Region ?? throw new UnexceptedNullException("获取server失败");

                PlayerInfo? playerInfo = await recordProvider.GetPlayerInfoAsync(role.GameUid, role.Region);
                _ = playerInfo ?? throw new UnexceptedNullException("获取用户角色统计信息失败");

                DetailedAvatarWrapper? detailAvatars = await recordProvider.GetDetailAvaterInfoAsync(role.GameUid, role.Region, playerInfo);
                _ = detailAvatars ?? throw new UnexceptedNullException("获取用户角色详细信息失败");

                SpiralAbyss? spiralAbyssInfo = await recordProvider.GetSpiralAbyssAsync(role.GameUid, role.Region, SpiralAbyssType.Current);
                _ = spiralAbyssInfo ?? throw new UnexceptedNullException("获取用户深境螺旋信息失败");

                PlayerRecord playerRecord = PlayerRecordBuilder.BuildPlayerRecord(role.GameUid, detailAvatars, spiralAbyssInfo);
                if (await confirmAsyncFunc.Invoke(playerRecord))
                {
                    Response<string>? resp = await AuthRequester
                        .PostWithContentTypeAsync<string>($"{HutaoAPIHost}/Record/Upload", playerRecord, "text/json");
                    await resultAsyncFunc.Invoke(resp ?? new Response()
                    {
                        ReturnCode = (int)KnownReturnCode.InternalFailure,
                        Message = $"UID:{role.GameUid} 的记录提交失败。"
                    });
                }
            }
        }

        private Requester AuthRequester { get; set; } = new();

        private class Token
        {
            public string? AccessToken { get; set; }
        }
        /// <summary>
        /// 登录获取token
        /// </summary>
        /// <returns></returns>
        public async Task InitializeAsync()
        {
            Response<Token>? resp = await new Requester()
                .PostWithContentTypeAsync<Token>($"{HutaoAPIHost}/Auth/Login",
                //registered from /Auth/Register
                new
                {
                    appid = "08d9e212-0cb3-4d71-8ed7-003606da7b20",
                    secret = "7ueWgZGn53dDhrm8L5ZRw+YWfOeSWtgQmJWquRgaygw="
                }, "text/json");
            if (resp?.Data?.AccessToken is not null)
            {
                AuthRequester = new() { UseAuthToken = true, AuthToken = resp.Data.AccessToken };
            }
            else
            {
                throw new SnapGenshinInternalException("请求胡桃API访问权限时发生错误");
            }
        }
        public async Task<Overview?> GetOverviewAsync()
        {
            Response<Overview>? resp = await AuthRequester
                .GetAsync<Overview>($"{HutaoAPIHost}/Statistics/Overview");
            return resp?.Data;
        }
        public async Task<IEnumerable<AvatarParticipation>> GetAvatarParticipationsAsync()
        {
            Response<IEnumerable<AvatarParticipation>>? resp = await AuthRequester
                .GetAsync<IEnumerable<AvatarParticipation>>($"{HutaoAPIHost}/Statistics/AvatarParticipation");
            return resp?.Data ?? new List<AvatarParticipation>();
        }
        public async Task<IEnumerable<AvatarReliquaryUsage>> GetAvatarReliquaryUsagesAsync()
        {
            Response<IEnumerable<AvatarReliquaryUsage>>? resp = await AuthRequester
                .GetAsync<IEnumerable<AvatarReliquaryUsage>>($"{HutaoAPIHost}/Statistics/AvatarReliquaryUsage");
            return resp?.Data ?? new List<AvatarReliquaryUsage>();
        }
        public async Task<IEnumerable<TeamCollocation>> GetTeamCollocationsAsync()
        {
            Response<IEnumerable<TeamCollocation>>? resp = await AuthRequester
                .GetAsync<IEnumerable<TeamCollocation>>($"{HutaoAPIHost}/Statistics/TeamCollocation");
            return resp?.Data ?? new List<TeamCollocation>();
        }
        public async Task<IEnumerable<WeaponUsage>> GetWeaponUsagesAsync()
        {
            Response<IEnumerable<WeaponUsage>>? resp = await AuthRequester
                .GetAsync<IEnumerable<WeaponUsage>>($"{HutaoAPIHost}/Statistics/WeaponUsage");
            return resp?.Data ?? new List<WeaponUsage>();
        }
    }
}