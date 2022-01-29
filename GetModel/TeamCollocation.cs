using System.Collections.Generic;

namespace DGP.Genshin.HutaoAPI.GetModel
{
    /// <summary>
    /// 组队数据
    /// </summary>
    public class TeamCollocation
    {
        public int Avater { get; set; }
        public IEnumerable<Rate<int>> Collocations { get; set; } = null!;
    }
}
