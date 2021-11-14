using Newtonsoft.Json;

namespace DGP.Genshin.MiHoYoAPI.Calculation
{
    /// <summary>
    /// 要消耗的物品信息
    /// </summary>
    public class ConsumeItem
    {
        [JsonProperty("id")] public int Id { get; set; }
        [JsonProperty("name")] public string? Name { get; set; }
        [JsonProperty("icon")] public string? Icon { get; set; }
        [JsonProperty("num")] public int Num { get; set; }
    }
}
