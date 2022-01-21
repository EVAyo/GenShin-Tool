using Newtonsoft.Json;
using System.Collections.Generic;

namespace DGP.Genshin.MiHoYoAPI.Announcement
{
    public class AnnouncementListWrapper
    {
        [JsonProperty("list")] public List<Announcement>? List { get; set; }
        [JsonProperty("type_id")] public int TypeId { get; set; }
        [JsonProperty("type_label")] public string? TypeLabel { get; set; }
    }
}
