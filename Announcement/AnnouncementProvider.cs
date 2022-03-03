using DGP.Genshin.MiHoYoAPI.Request;
using DGP.Genshin.MiHoYoAPI.Response;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace DGP.Genshin.MiHoYoAPI.Announcement
{
    public class AnnouncementProvider
    {
        private const string Hk4eApi = "https://hk4e-api.mihoyo.com";
        private const string Query = "game=hk4e&game_biz=hk4e_cn&lang=zh-cn&bundle_id=hk4e_cn&platform=pc&region=cn_gf01&level=55&uid=100000000";

        public async Task<AnnouncementWrapper?> GetAnnouncementWrapperAsync()
        {
            Response<AnnouncementWrapper>? resp =
                await new Requester().GetAsync<AnnouncementWrapper>(
                    $"{Hk4eApi}/common/hk4e_cn/announcement/api/getAnnList?{Query}")
                .ConfigureAwait(false);
            return resp?.Data;
        }

        public async Task<List<AnnouncementContent>> GetAnnouncementContentsAsync()
        {
            Requester requester = new(new()
            {
                { "Accept", "*/*" },
                { "Accept-Encoding", "gzip" }
            }, useGZipCompression: true);
            Response<ListWrapper<AnnouncementContent>>? resp =
                await requester.GetAsync<ListWrapper<AnnouncementContent>>(
                    $"{Hk4eApi}/common/hk4e_cn/announcement/api/getAnnContent?{Query}")
                .ConfigureAwait(false);
            return resp?.Data?.List ?? new();
        }
    }
}
