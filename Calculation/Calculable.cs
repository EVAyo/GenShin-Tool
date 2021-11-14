using Newtonsoft.Json;

namespace DGP.Genshin.MiHoYoAPI.Calculation
{
    public abstract class Calculable
    {
        [JsonProperty("id")] public int Id { get; set; }
        [JsonProperty("name")] public string? Name { get; set; }
        [JsonProperty("icon")] public string? Icon { get; set; }
        [JsonProperty("level_current")] public int LevelCurrent { get; set; }
        [JsonProperty("max_level")] public int MaxLevel { get; set; }
    }
}
