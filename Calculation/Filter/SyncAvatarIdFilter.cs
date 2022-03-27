using Newtonsoft.Json;

namespace DGP.Genshin.MiHoYoAPI.Calculation.Filter
{
    /// <summary>
    /// 必须提供 uid 与 region
    /// </summary>
    public class SyncAvatarIdFilter : AvatarIdFilter
    {
        public SyncAvatarIdFilter(string uid, string region)
        {
            this.Uid = uid;
            this.Region = region;
        }

        [JsonProperty("uid")] public string Uid { get; set; }
        [JsonProperty("region")] public string Region { get; set; }
    }
}
