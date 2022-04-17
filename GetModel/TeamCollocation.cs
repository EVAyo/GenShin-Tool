using Newtonsoft.Json;
using System.Collections.Generic;

namespace DGP.Genshin.HutaoAPI.GetModel
{
    /// <summary>
    /// 组队数据
    /// </summary>
    public class TeamCollocation
    {
        /// <summary>
        /// 角色Id
        /// </summary>
        [JsonProperty("Avater")]
        public int Avatar { get; set; }

        /// <summary>
        /// 角色搭配比率
        /// </summary>
        public IEnumerable<Rate<int>> Collocations { get; set; } = null!;
    }
}