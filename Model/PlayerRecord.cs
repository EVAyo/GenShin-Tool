using System.Collections.Generic;

namespace DGP.Genshin.HutaoAPI.Model
{
    public class PlayerRecord
    {
        public PlayerRecord(string uid, List<PlayerAvatar> playerAvatars, List<PlayerSpiralAbyssLevel> playerSpiralAbyssesLevels)
        {
            Uid = uid;
            PlayerAvatars = playerAvatars;
            PlayerSpiralAbyssesLevels = playerSpiralAbyssesLevels;
        }

        public string Uid { get; set; }
        public List<PlayerAvatar> PlayerAvatars { get; set; }
        public List<PlayerSpiralAbyssLevel> PlayerSpiralAbyssesLevels { get; set; }
    }
}