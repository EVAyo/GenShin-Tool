using System.Collections.Generic;

namespace DGP.Genshin.HutaoAPI.GetModel
{
    /// <summary>
    /// 命座比例
    /// </summary>
    public class AvatarConstellationNum
    {
        public int Avatar { get; set; }
        public double HoldingRate { get; set; }
        public IEnumerable<Rate<int>> Rate { get; set; } = null!;
    }
}