using System.Collections.Generic;

namespace DGP.Genshin.HutaoAPI.GetModel
{
    public record TeamCombination
    {
        public Level Level { get; set; } = null!;
        public IEnumerable<Rate<Team>> Teams { get; set; } = null!;
    }
}
