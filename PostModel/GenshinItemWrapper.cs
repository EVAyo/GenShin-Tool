using System.Collections.Generic;

namespace DGP.Genshin.HutaoAPI.PostModel
{
    public class GenshinItemWrapper
    {
        public IEnumerable<GenshinItem>? Avatars { get; set; }
        public IEnumerable<GenshinItem>? Weapons { get; set; }
        public IEnumerable<GenshinItem>? Reliquaries { get; set; }
    }
}