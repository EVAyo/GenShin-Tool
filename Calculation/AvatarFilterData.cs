using Newtonsoft.Json;
using System.Collections.Generic;

namespace DGP.Genshin.MiHoYoAPI.Calculation
{
    public class AvatarFilterData
    {
        [JsonProperty("element_attr_ids")] public List<int>? ElementAttrIds { get; set; }
        [JsonProperty("weapon_cat_ids")] public List<int>? WeaponCatIds { get; set; }
        [JsonProperty("page")] public int Page { get; set; }
        [JsonProperty("size")] public int Size { get; set; }
        [JsonProperty("uid")] public string? Uid { get; set; }
        [JsonProperty("region")] public string? Region { get; set; }
    }
}
