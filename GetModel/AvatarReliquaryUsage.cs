using System.Collections.Generic;

namespace DGP.Genshin.HutaoAPI.GetModel
{
    /// <summary>
    /// 圣遗物配置数据
    /// </summary>
    public class AvatarReliquaryUsage
    {
        public int Avatar { get; set; }
        public IEnumerable<Rate<string>> ReliquaryUsage { get; set; } = null!;
    }
}
