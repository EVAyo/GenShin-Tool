using Newtonsoft.Json;
using System.Collections.Generic;

namespace DGP.Genshin.MiHoYoAPI.Calculation
{
    public class Consumption
    {
        [JsonProperty("avatar_comsume")] public List<ConsumeItem>? AvatarConsume { get; set; }
        [JsonProperty("avatar_skill_comsume")] public List<ConsumeItem>? AvatarSkillConsume { get; set; }
        [JsonProperty("weapon_comsume")] public List<ConsumeItem>? WeaponConsume { get; set; }
        [JsonProperty("reliquary_comsume")] public List<ReliquaryConsumeItem>? ReliquaryConsume { get; set; }
    }
}
