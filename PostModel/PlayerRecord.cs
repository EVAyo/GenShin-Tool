using System.Collections.Generic;

namespace DGP.Genshin.HutaoAPI.PostModel
{
    public class PlayerRecord
    {
        public PlayerRecord(string uid, List<PlayerAvatar> playerAvatars, List<PlayerSpiralAbyssLevel> playerSpiralAbyssesLevels)
        {
            this.Uid = uid;
            this.PlayerAvatars = playerAvatars;
            this.PlayerSpiralAbyssesLevels = playerSpiralAbyssesLevels;
        }

        public string Uid { get; set; }
        public List<PlayerAvatar> PlayerAvatars { get; set; }
        public List<PlayerSpiralAbyssLevel> PlayerSpiralAbyssesLevels { get; set; }
    }
}