using System.Collections.Generic;

namespace DGP.Genshin.HutaoAPI.Model
{
    public class PlayerAvatar
    {
        public int Id { get; set; }
        public int Level { get; set; }
        public int ActivedConstellationNum { get; set; }
        public AvatarWeapon Weapon { get; set; }
        public List<AvatarReliquarySet> ReliquarySets { get; set; }
    }
}