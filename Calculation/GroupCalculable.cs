using Newtonsoft.Json;

namespace DGP.Genshin.MiHoYoAPI.Calculation
{
    public abstract class GroupCalculable : Calculable
    {
        [JsonProperty("group_id")] public int GroupId { get; set; }
        public override PromotionDelta ToPromotionDelta()
        {
            return new()
            {
                LevelCurrent = this.LevelCurrent,
                LevelTarget = this.LevelTarget,
                Id = this.GroupId
            };
        }
    }
}
