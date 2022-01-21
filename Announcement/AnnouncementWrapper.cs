using Newtonsoft.Json;
using System.Collections.Generic;

namespace DGP.Genshin.MiHoYoAPI.Announcement
{
    public class AnnouncementWrapper
    {
        [JsonProperty("list")] public List<AnnouncementListWrapper>? List { get; set; }
        [JsonProperty("total")] public int Total { get; set; }
        [JsonProperty("type_list")] public List<AnnouncementType>? TypeList { get; set; }
        [JsonProperty("alert")] public bool Alert { get; set; }
        [JsonProperty("alert_id")] public int AlertId { get; set; }
        [JsonProperty("timezone")] public int TimeZone { get; set; }
        [JsonProperty("t")] public long TimeStamp { get; set; }
    }
}
