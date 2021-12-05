using Newtonsoft.Json;
using System.Collections.Generic;

namespace DGP.Genshin.MiHoYoAPI.Gacha
{
    /// <summary>
    /// 更多信息详见 https://github.com/DGP-Studio/Snap.Genshin/wiki/StandardFormat
    /// </summary>
    public class UIGF
    {
        [JsonProperty("info")] public UIGFInfo? Info { get; set; }
        [JsonProperty("list")] public IEnumerable<UIGFItem?>? List { get; set; }
    }
}
