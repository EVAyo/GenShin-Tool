using DGP.Genshin.HutaoAPI.GetModel;
using DGP.Genshin.HutaoAPI.PostModel;
using DGP.Genshin.MiHoYoAPI.GameRole;
using DGP.Genshin.MiHoYoAPI.Record;
using DGP.Genshin.MiHoYoAPI.Record.Avatar;
using DGP.Genshin.MiHoYoAPI.Record.SpiralAbyss;
using DGP.Genshin.MiHoYoAPI.Request;
using DGP.Genshin.MiHoYoAPI.Response;
using Snap.Exception;
using Snap.Extenion.Enumerable;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace DGP.Genshin.HutaoAPI
{
    public class PlayerRecordClient
    {
        private const string HutaoAPIHost = "https://hutao-api.snapgenshin.com";
        private class Token
        {
            public string? AccessToken { get; set; }
        }
        private record AuthToken(string Appid, string Secret);
        private Requester AuthRequester { get; set; } = new();

        /// <summary>
        /// 登录获取token
        /// </summary>
        /// <returns></returns>
        public async Task InitializeAsync()
        {
            //Please contract us for new token
            AuthToken token = new("08d9e212-0cb3-4d71-8ed7-003606da7b20", "7ueWgZGn53dDhrm8L5ZRw+YWfOeSWtgQmJWquRgaygw=");
            Response<Token>? resp = await new Requester().PostWithContentTypeAsync<Token>($"{HutaoAPIHost}/Auth/Login", token , "text/json");
            AuthRequester = resp?.Data?.AccessToken is not null
                ? (new() { UseAuthToken = true, AuthToken = resp.Data.AccessToken })
                : throw new SnapGenshinInternalException("请求胡桃API权限时发生错误");
        }

        public async Task GetAllRecordsAndUploadAsync(string cookie, Func<PlayerRecord, Task<bool>> confirmAsyncFunc, Func<Response, Task> resultAsyncFunc)
        {
            RecordProvider recordProvider = new(cookie);

            List<UserGameRole> userGameRoles = await new UserGameRoleProvider(cookie).GetUserGameRolesAsync();
            foreach (UserGameRole role in userGameRoles)
            {
                _ = role.GameUid ?? throw new UnexpectedNullException("获取uid失败");
                _ = role.Region ?? throw new UnexpectedNullException("获取server失败");

                PlayerInfo? playerInfo = await recordProvider.GetPlayerInfoAsync(role.GameUid, role.Region);
                _ = playerInfo ?? throw new UnexpectedNullException("获取用户角色统计信息失败");

                DetailedAvatarWrapper? detailAvatars = await recordProvider.GetDetailAvaterInfoAsync(role.GameUid, role.Region, playerInfo);
                _ = detailAvatars ?? throw new UnexpectedNullException("获取用户角色详细信息失败");

                SpiralAbyss? spiralAbyssInfo = await recordProvider.GetSpiralAbyssAsync(role.GameUid, role.Region, SpiralAbyssType.Current);
                _ = spiralAbyssInfo ?? throw new UnexpectedNullException("获取用户深境螺旋信息失败");

                PlayerRecord playerRecord = PlayerRecordBuilder.BuildPlayerRecord(role.GameUid, detailAvatars, spiralAbyssInfo);
                if (await confirmAsyncFunc.Invoke(playerRecord))
                {
                    Response<string>? resp = null;
                    Response<string>? itemResp = await UploadItemsAsync(detailAvatars);
                    if (itemResp?.ReturnCode == 0)
                    {
                        resp = await AuthRequester.PostWithContentTypeAsync<string>($"{HutaoAPIHost}/Record/Upload", playerRecord, "text/json");
                    }
                    await resultAsyncFunc.Invoke(resp ?? new Response()
                    {
                        ReturnCode = (int)KnownReturnCode.InternalFailure,
                        Message = $"{role.GameUid}-记录提交失败。"
                    });
                }
            }
        }

        #region V1 API
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
            return resp?.Data ?? Enumerable.Empty<AvatarParticipation>();
        }
        public async Task<IEnumerable<AvatarReliquaryUsage>> GetAvatarReliquaryUsagesAsync()
        {
            Response<IEnumerable<AvatarReliquaryUsage>>? resp = await AuthRequester
                .GetAsync<IEnumerable<AvatarReliquaryUsage>>($"{HutaoAPIHost}/Statistics/AvatarReliquaryUsage");
            return resp?.Data ?? Enumerable.Empty<AvatarReliquaryUsage>();
        }
        public async Task<IEnumerable<TeamCollocation>> GetTeamCollocationsAsync()
        {
            Response<IEnumerable<TeamCollocation>>? resp = await AuthRequester
                .GetAsync<IEnumerable<TeamCollocation>>($"{HutaoAPIHost}/Statistics/TeamCollocation");
            return resp?.Data ?? Enumerable.Empty<TeamCollocation>();
        }
        public async Task<IEnumerable<WeaponUsage>> GetWeaponUsagesAsync()
        {
            Response<IEnumerable<WeaponUsage>>? resp = await AuthRequester
                .GetAsync<IEnumerable<WeaponUsage>>($"{HutaoAPIHost}/Statistics/WeaponUsage");
            return resp?.Data ?? Enumerable.Empty<WeaponUsage>();
        }
        #endregion

        #region V2 API
        public async Task<Response<string>?> UploadItemsAsync(DetailedAvatarWrapper detailedAvatar)
        {
            IEnumerable<GenshinItem>? avatars = detailedAvatar.Avatars?
                .Select(avatar => new GenshinItem(avatar.Id, avatar.Name, avatar.Icon))
                .DistinctBy(item => item.Id);
            IEnumerable<GenshinItem>? weapons = detailedAvatar.Avatars?
                .Select(avatar => avatar.Weapon)
                .NotNull()
                .Select(weapon => new GenshinItem(weapon.Id, weapon.Name, weapon.Icon))
                .DistinctBy(item => item.Id);
            IEnumerable<GenshinItem>? reliquaries = detailedAvatar.Avatars?
                .Select(avatars => avatars.Reliquaries)
                .SelectMany(reliquaries => reliquaries!)
                .Where(relic => relic.Position == 1)
                .Select(relic => new GenshinItem(relic.ReliquarySet!.Id, relic.ReliquarySet.Name, relic.Icon))
                .DistinctBy(item => item.Id);

            GenshinItemWrapper? data = new() { Avatars = avatars, Weapons = weapons, Reliquaries = reliquaries };

            return await AuthRequester
                        .PostWithContentTypeAsync<string>($"{HutaoAPIHost}​/GenshinItems/Upload", data, "text/json");
        }

        public async Task<IEnumerable<GenshinItem>> GetAvatarMapAsync()
        {
            Response<IEnumerable<GenshinItem>>? resp = await AuthRequester
                .GetAsync<IEnumerable<GenshinItem>>($"{HutaoAPIHost}/GenshinItems/Avatars");
            return resp?.Data?.DistinctBy(x => x.Id) ?? Enumerable.Empty<GenshinItem>();
        }
        public async Task<IEnumerable<GenshinItem>> GetWeaponMapAsync()
        {
            Response<IEnumerable<GenshinItem>>? resp = await AuthRequester
                .GetAsync<IEnumerable<GenshinItem>>($"{HutaoAPIHost}/GenshinItems/Weapons");
            return resp?.Data?.DistinctBy(x => x.Id) ?? Enumerable.Empty<GenshinItem>();
        }
        public async Task<IEnumerable<GenshinItem>> GetReliquaryMapAsync()
        {
            Response<IEnumerable<GenshinItem>>? resp = await AuthRequester
                .GetAsync<IEnumerable<GenshinItem>>($"{HutaoAPIHost}/GenshinItems/Reliquaries");
            return resp?.Data?.DistinctBy(x => x.Id) ?? Enumerable.Empty<GenshinItem>();
        }

        public async Task<IEnumerable<AvatarConstellationNum>> GetAvatarConstellationsAsync()
        {
            Response<IEnumerable<AvatarConstellationNum>>? resp = await AuthRequester
                .GetAsync<IEnumerable<AvatarConstellationNum>>($"{HutaoAPIHost}/Statistics/Constellation");
            return resp?.Data ?? Enumerable.Empty<AvatarConstellationNum>();
        }
        public async Task<IEnumerable<TeamCombination>> GetTeamCombinationsAsync()
        {
            Response<IEnumerable<TeamCombination>>? resp = await AuthRequester
                .GetAsync<IEnumerable<TeamCombination>>($"{HutaoAPIHost}/Statistics/TeamCombination");
            return resp?.Data ?? Enumerable.Empty<TeamCombination>();
        }
        #endregion
    }
}