using Newtonsoft.Json;
using System.Collections.Generic;

namespace DGP.Genshin.MiHoYoAPI.Calculation
{
    public class DetailedAvatar
    {
        [JsonProperty("skill_list")] public List<Skill>? SkillList { get; set; }
        [JsonProperty("weapon")] public Weapon? Weapon { get; set; }
        [JsonProperty("reliquary_list")] public List<Reliquary>? ReliquaryList { get; set; }
    }
}
