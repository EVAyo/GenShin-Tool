using Newtonsoft.Json;
using Snap.Data.Primitive;

namespace DGP.Genshin.MiHoYoAPI.Calculation
{
    /// <summary>
    /// 要消耗的物品信息
    /// </summary>
    public class ConsumeItem : Observable, ICloneable<ConsumeItem>
    {
        private bool isCompleted = false;

        [JsonProperty("id")] public int Id { get; set; }
        [JsonProperty("name")] public string? Name { get; set; }
        [JsonProperty("icon")] public string? Icon { get; set; }
        [JsonProperty("num")] public double Num { get; set; }
        [JsonProperty("wiki_url")] public string? WikiUrl { get; set; }
        public bool IsCompleted { get => isCompleted; set => Set(ref isCompleted, value); }

        public ConsumeItem Clone()
        {
            return new()
            {
                Id = Id,
                Name = Name,
                Icon = Icon,
                Num = Num,
                WikiUrl = WikiUrl,
                IsCompleted = false
            };
        }
    }
}
