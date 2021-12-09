using DGP.Genshin.Common.Data.Behavior;
using Newtonsoft.Json;

namespace DGP.Genshin.MiHoYoAPI.Calculation
{
    public abstract class Calculable : Observable
    {
        private int levelTarget;

        [JsonProperty("id")] public int Id { get; set; }
        [JsonProperty("name")] public string? Name { get; set; }
        [JsonProperty("icon")] public string? Icon { get; set; }
        [JsonProperty("level_current")] public int LevelCurrent { get; set; } = 1;
        public int LevelTarget { get => levelTarget; set => Set(ref levelTarget, value); }
        [JsonProperty("max_level")] public int MaxLevel { get; set; }

        public virtual PromotionDelta ToPromotionDelta()
        {
            return new()
            {
                LevelCurrent = this.LevelCurrent,
                LevelTarget = this.LevelTarget,
                Id = this.Id
            };
        }
    }
}
