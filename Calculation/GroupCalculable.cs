using Newtonsoft.Json;

namespace DGP.Genshin.MiHoYoAPI.Calculation
{
    public abstract class GroupCalculable
    {
        [JsonProperty("group_id")] public int SkillCatId { get; set; }
    }
}
