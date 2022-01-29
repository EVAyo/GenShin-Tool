using System.Collections.Generic;

namespace DGP.Genshin.HutaoAPI.PostModel
{
    public class PlayerSpiralAbyssBattle
    {
        public PlayerSpiralAbyssBattle(int battleIndex, List<int> avatarIds)
        {
            BattleIndex = battleIndex;
            AvatarIds = avatarIds;
        }

        public int BattleIndex { get; set; }
        public List<int> AvatarIds { get; set; }
    }
}