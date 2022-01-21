using Newtonsoft.Json;

namespace DGP.Genshin.MiHoYoAPI.Announcement
{
    public class AnnouncementType
    {
        [JsonProperty("id")] public int Id { get; set; }
        [JsonProperty("name")] public string? Name { get; set; }
        [JsonProperty("mi18n_name")] public string? MI18NName { get; set; }
    }
}
