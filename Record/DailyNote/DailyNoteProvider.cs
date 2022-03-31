using DGP.Genshin.MiHoYoAPI.GameRole;
using DGP.Genshin.MiHoYoAPI.Request;
using DGP.Genshin.MiHoYoAPI.Request.DynamicSecret;
using System.Threading;
using System.Threading.Tasks;

namespace DGP.Genshin.MiHoYoAPI.Record.DailyNote
{
    public class DailyNoteProvider
    {
        private const string ApiTakumiRecord = @"https://api-takumi-record.mihoyo.com/game_record/app/genshin/api";
        private const string Referer = @"https://webstatic.mihoyo.com/app/community-game-records/index.html?v=6";

        private readonly Requester requester;

        public DailyNoteProvider(string cookie)
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
        /// 获取实时便笺信息
        /// </summary>
        /// <param name="server"></param>
        /// <param name="uid"></param>
        /// <returns></returns>
        public async Task<DailyNote?> GetDailyNoteAsync(string server, string uid, CancellationToken cancellationToken = default)
        {
            return await requester.GetWhileUpdateDynamicSecret2Async<DailyNote>(
                $"{ApiTakumiRecord}/dailyNote?server={server}&role_id={uid}", cancellationToken)
                .ConfigureAwait(false);
        }

        public async Task<DailyNote?> GetDailyNoteAsync(UserGameRole role, CancellationToken cancellationToken = default)
        {
            return role?.Region is null || role.GameUid is null
                ? null
                : await GetDailyNoteAsync(role.Region, role.GameUid, cancellationToken)
                .ConfigureAwait(false);
        }
    }
}
