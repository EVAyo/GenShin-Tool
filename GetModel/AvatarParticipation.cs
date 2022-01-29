using System.Collections.Generic;

namespace DGP.Genshin.HutaoAPI.GetModel
{
    /// <summary>
    /// 出场数据
    /// </summary>
    public class AvatarParticipation
    {
        public int Floor { get; set; }

        public IEnumerable<Rate<int>> AvatarUsage { get; set; } = null!;
    }
}
