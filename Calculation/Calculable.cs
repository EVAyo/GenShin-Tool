using Newtonsoft.Json;
using Snap.Data.Primitive;

namespace DGP.Genshin.MiHoYoAPI.Calculation
{
    public class Calculable : Observable
    {
        private int levelTarget;

        [JsonProperty("id")] public int Id { get; set; }
        [JsonProperty("name")] public string? Name { get; set; }
        [JsonProperty("icon")] public string? Icon { get; set; }
        /// <summary>
        /// 默认值设为1，因为部分API不返回该字段
        /// </summary>
        [JsonProperty("level_current")] public int LevelCurrent { get; set; } = 1;
        public int LevelTarget
        {
            get => this.levelTarget;

            set => this.Set(ref this.levelTarget, value);
        }
        [JsonProperty("max_level")] public int MaxLevel { get; set; }

        public virtual PromotionDelta ToPromotionDelta()
        {
            return new()
            {
                LevelCurrent = LevelCurrent,
                LevelTarget = LevelTarget,
                Id = Id
            };
        }
    }
}
