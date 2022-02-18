using System.Collections.Generic;

namespace DGP.Genshin.HutaoAPI.PostModel
{
    public class GenshinItemWrapper
    {
        public IEnumerable<HutaoItem>? Avatars { get; set; }
        public IEnumerable<HutaoItem>? Weapons { get; set; }
        public IEnumerable<HutaoItem>? Reliquaries { get; set; }
    }
}