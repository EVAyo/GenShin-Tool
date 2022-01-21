using Newtonsoft.Json;

namespace DGP.Genshin.MiHoYoAPI.Announcement
{
    public class AnnouncementContent
    {
        [JsonProperty("ann_id")] public int AnnId { get; set; }
        [JsonProperty("title")] public string? Title { get; set; }
        [JsonProperty("subtitle")] public string? Subtitle { get; set; }
        [JsonProperty("banner")] public string? Banner { get; set; }
        [JsonProperty("content")] public string? Content { get; set; }
        [JsonProperty("lang")] public string? Lang { get; set; }
    }
}
