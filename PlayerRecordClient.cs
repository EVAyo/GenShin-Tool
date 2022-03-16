using DGP.Genshin.HutaoAPI.GetModel;
using DGP.Genshin.HutaoAPI.PostModel;
using DGP.Genshin.MiHoYoAPI.GameRole;
using DGP.Genshin.MiHoYoAPI.Record;
using DGP.Genshin.MiHoYoAPI.Record.Avatar;
using DGP.Genshin.MiHoYoAPI.Record.SpiralAbyss;
using DGP.Genshin.MiHoYoAPI.Request;
using DGP.Genshin.MiHoYoAPI.Response;
using Microsoft;
using Snap.Extenion.Enumerable;
using Snap.Threading;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace DGP.Genshin.HutaoAPI
{
    public class PlayerRecordClient
    {
        private const string HutaoAPIHost = "https://hutao-api.snapgenshin.com";
        private const string ContentType = "text/json";

        private record Token
        {
            public string? AccessToken { get; set; }
        }
        private record Auth(string Appid, string Secret);
        private Requester AuthRequester { get; set; } = new();

        /// <summary>
        /// 登录获取token
        /// </summary>
        /// <returns></returns>
        public async Task InitializeAsync()
        {
            //Please contract us for your own token
            Auth token = new("08d9e212-0cb3-4d71-8ed7-003606da7b20", "7ueWgZGn53dDhrm8L5ZRw+YWfOeSWtgQmJWquRgaygw=");
            Response<Token>? resp = await new Requester()
                .PostAsync<Token>($"{HutaoAPIHost}/Auth/Login", token, ContentType)
                .ConfigureAwait(false);
            Requires.NotNull(resp?.Data?.AccessToken!, nameof(resp.Data.AccessToken));
            AuthRequester = new() { UseAuthToken = true, AuthToken = resp.Data.AccessToken };
        }

        [ExecuteOnMainThread]
        public async Task GetAllRecordsAndUploadAsync(string cookie, Func<PlayerRecord, Task<bool>> confirmAsyncFunc, Func<Response, Task> resultAsyncFunc)
        {
            RecordProvider recordProvider = new(cookie);

            List<UserGameRole> userGameRoles =
                await new UserGameRoleProvider(cookie).GetUserGameRolesAsync()
                .ConfigureAwait(true);
            foreach (UserGameRole role in userGameRoles)
            {
                Requires.NotNull(role.GameUid!, nameof(role.GameUid));
                Requires.NotNull(role.Region!, nameof(role.Region));

                PlayerInfo? playerInfo = await recordProvider.GetPlayerInfoAsync(role.GameUid, role.Region)
                    .ConfigureAwait(true);
                Requires.NotNull(playerInfo!, nameof(playerInfo));

                DetailedAvatarWrapper? detailAvatars = await recordProvider.GetDetailAvaterInfoAsync(role.GameUid, role.Region, playerInfo)
                    .ConfigureAwait(true);
                Requires.NotNull(detailAvatars!, nameof(detailAvatars));

                SpiralAbyss? spiralAbyssInfo = await recordProvider.GetSpiralAbyssAsync(role.GameUid, role.Region, SpiralAbyssType.Current)
                    .ConfigureAwait(true);
                Requires.NotNull(spiralAbyssInfo!, nameof(spiralAbyssInfo));

                PlayerRecord playerRecord = PlayerRecordBuilder.BuildPlayerRecord(role.GameUid, detailAvatars, spiralAbyssInfo);
                if (await confirmAsyncFunc.Invoke(playerRecord).ConfigureAwait(true))
                {
                    Response<string>? resp = null;
                    if (Response.IsOk(await UploadItemsAsync(detailAvatars).ConfigureAwait(true)))
                    {
                        resp = await AuthRequester.PostAsync<string>($"{HutaoAPIHost}/Record/Upload", playerRecord, ContentType)
                            .ConfigureAwait(true);
                    }
                    await resultAsyncFunc.Invoke(resp ?? Response.CreateFail($"{role.GameUid}-记录提交失败。"))
                        .ConfigureAwait(true);
                }
            }
        }

        #region V1 API
        public async Task<Overview?> GetOverviewAsync()
        {
            Response<Overview>? resp = await AuthRequester
                .GetAsync<Overview>($"{HutaoAPIHost}/Statistics/Overview")
                .ConfigureAwait(false);
            return resp?.Data;
        }

        public async Task<IEnumerable<AvatarParticipation>> GetAvatarParticipationsAsync()
        {
            Response<IEnumerable<AvatarParticipation>>? resp = await AuthRequester
                .GetAsync<IEnumerable<AvatarParticipation>>($"{HutaoAPIHost}/Statistics/AvatarParticipation")
                .ConfigureAwait(false);
            return resp?.Data ?? Enumerable.Empty<AvatarParticipation>();
        }
        public async Task<IEnumerable<AvatarReliquaryUsage>> GetAvatarReliquaryUsagesAsync()
        {
            Response<IEnumerable<AvatarReliquaryUsage>>? resp = await AuthRequester
                .GetAsync<IEnumerable<AvatarReliquaryUsage>>($"{HutaoAPIHost}/Statistics/AvatarReliquaryUsage")
                .ConfigureAwait(false);
            return resp?.Data ?? Enumerable.Empty<AvatarReliquaryUsage>();
        }
        public async Task<IEnumerable<TeamCollocation>> GetTeamCollocationsAsync()
        {
            Response<IEnumerable<TeamCollocation>>? resp = await AuthRequester
                .GetAsync<IEnumerable<TeamCollocation>>($"{HutaoAPIHost}/Statistics/TeamCollocation")
                .ConfigureAwait(false);
            return resp?.Data ?? Enumerable.Empty<TeamCollocation>();
        }
        public async Task<IEnumerable<WeaponUsage>> GetWeaponUsagesAsync()
        {
            Response<IEnumerable<WeaponUsage>>? resp = await AuthRequester
                .GetAsync<IEnumerable<WeaponUsage>>($"{HutaoAPIHost}/Statistics/WeaponUsage")
                .ConfigureAwait(false);
            return resp?.Data ?? Enumerable.Empty<WeaponUsage>();
        }
        #endregion

        #region V2 API
        public async Task<Response<string>?> UploadItemsAsync(DetailedAvatarWrapper detailedAvatar)
        {
            IEnumerable<HutaoItem>? avatars = detailedAvatar.Avatars?
                .Select(avatar => new HutaoItem(avatar.Id, avatar.Name, avatar.Icon))
                .DistinctBy(item => item.Id);
            IEnumerable<HutaoItem>? weapons = detailedAvatar.Avatars?
                .Select(avatar => avatar.Weapon)
                .NotNull()
                .Select(weapon => new HutaoItem(weapon.Id, weapon.Name, weapon.Icon))
                .DistinctBy(item => item.Id);
            IEnumerable<HutaoItem>? reliquaries = detailedAvatar.Avatars?
                .Select(avatars => avatars.Reliquaries)
                .SelectMany(reliquaries => reliquaries!)
                .Where(relic => relic.Position == 1)
                .Select(relic => new HutaoItem(relic.ReliquarySet!.Id, relic.ReliquarySet.Name, relic.Icon))
                .DistinctBy(item => item.Id);

            GenshinItemWrapper? data = new() { Avatars = avatars, Weapons = weapons, Reliquaries = reliquaries };

            return await AuthRequester
                        .PostAsync<string>($"{HutaoAPIHost}​/GenshinItems/Upload", data, ContentType)
                        .ConfigureAwait(false);
        }

        public async Task<IEnumerable<HutaoItem>> GetAvatarMapAsync()
        {
            Response<IEnumerable<HutaoItem>>? resp = await AuthRequester
                .GetAsync<IEnumerable<HutaoItem>>($"{HutaoAPIHost}/GenshinItems/Avatars")
                .ConfigureAwait(false);
            return resp?.Data?.DistinctBy(x => x.Id) ?? Enumerable.Empty<HutaoItem>();
        }
        public async Task<IEnumerable<HutaoItem>> GetWeaponMapAsync()
        {
            Response<IEnumerable<HutaoItem>>? resp = await AuthRequester
                .GetAsync<IEnumerable<HutaoItem>>($"{HutaoAPIHost}/GenshinItems/Weapons")
                .ConfigureAwait(false);
            return resp?.Data?.DistinctBy(x => x.Id) ?? Enumerable.Empty<HutaoItem>();
        }
        public async Task<IEnumerable<HutaoItem>> GetReliquaryMapAsync()
        {
            Response<IEnumerable<HutaoItem>>? resp = await AuthRequester
                .GetAsync<IEnumerable<HutaoItem>>($"{HutaoAPIHost}/GenshinItems/Reliquaries")
                .ConfigureAwait(false);
            return resp?.Data?.DistinctBy(x => x.Id) ?? Enumerable.Empty<HutaoItem>();
        }

        public async Task<IEnumerable<AvatarConstellationNum>> GetAvatarConstellationsAsync()
        {
            Response<IEnumerable<AvatarConstellationNum>>? resp = await AuthRequester
                .GetAsync<IEnumerable<AvatarConstellationNum>>($"{HutaoAPIHost}/Statistics/Constellation")
                .ConfigureAwait(false);
            return resp?.Data ?? Enumerable.Empty<AvatarConstellationNum>();
        }
        public async Task<IEnumerable<TeamCombination>> GetTeamCombinationsAsync()
        {
            Response<IEnumerable<TeamCombination>>? resp = await AuthRequester
                .GetAsync<IEnumerable<TeamCombination>>($"{HutaoAPIHost}/Statistics/TeamCombination")
                .ConfigureAwait(false);
            return resp?.Data ?? Enumerable.Empty<TeamCombination>();
        }
        #endregion
    }
}