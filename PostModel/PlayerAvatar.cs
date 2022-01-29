using System.Collections.Generic;

namespace DGP.Genshin.HutaoAPI.PostModel
{
    public class PlayerAvatar
    {
        public PlayerAvatar(int id, int level, int activedConstellationNum, AvatarWeapon weapon, List<AvatarReliquarySet> reliquarySets)
        {
            Id = id;
            Level = level;
            ActivedConstellationNum = activedConstellationNum;
            Weapon = weapon;
            ReliquarySets = reliquarySets;
        }

        public int Id { get; set; }
        public int Level { get; set; }
        public int ActivedConstellationNum { get; set; }
        public AvatarWeapon Weapon { get; set; }
        public List<AvatarReliquarySet> ReliquarySets { get; set; }
    }
}