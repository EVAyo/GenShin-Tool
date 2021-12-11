using Newtonsoft.Json;
using System.Collections.Generic;

namespace DGP.Genshin.MiHoYoAPI.Calculation.Filter
{
    public class AvatarIdFilter
    {
        [JsonProperty("element_attr_ids")] public List<int>? ElementAttrIds { get; set; } = new();
        [JsonProperty("weapon_cat_ids")] public List<int>? WeaponCatIds { get; set; } = new();
        [JsonProperty("page")] public int Page { get; set; }
        /// <summary>
        /// 请求页的尺寸，默认20
        /// </summary>
        [JsonProperty("size")] public int Size { get; set; } = 20;
    }
    public class WeaponIdFilter
    {
        /// <summary>
        /// 武器稀有度
        /// </summary>
        [JsonProperty("weapon_levels")] public List<int>? WeaponLevels { get; set; } = new();
        [JsonProperty("weapon_cat_ids")] public List<int>? WeaponCatIds { get; set; } = new() { 1 };
        [JsonProperty("page")] public int Page { get; set; }
        /// <summary>
        /// 请求页的尺寸，默认20
        /// </summary>
        [JsonProperty("size")] public int Size { get; set; } = 20;
    }
    public class ReliquaryIdFilter
    {
        /// <summary>
        /// 武器稀有度
        /// </summary>
        [JsonProperty("reliquary_levels")] public List<int>? WeaponLevels { get; set; } = new();
        /// <summary>
        /// 1 代表 花
        /// </summary>
        [JsonProperty("reliquary_cat_id")] public int WeaponCatId { get; set; } = 1;
        [JsonProperty("page")] public int Page { get; set; }
        /// <summary>
        /// 请求页的尺寸，默认20
        /// </summary>
        [JsonProperty("size")] public int Size { get; set; } = 20;
    }
}
