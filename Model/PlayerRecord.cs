using System.Collections.Generic;

namespace DGP.Genshin.HutaoAPI.Model
{
    public class PlayerRecord
    {
        public List<PlayerAvatar> PlayerAvatars { get; set; }
        public List<PlayerSpiralAbyssLevel> PlayerSpiralAbyssesLevels { get; set; }
    }
}