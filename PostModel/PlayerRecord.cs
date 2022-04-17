using System.Collections.Generic;

namespace DGP.Genshin.HutaoAPI.PostModel
{
    /// <summary>
    /// 玩家记录
    /// </summary>
    public class PlayerRecord
    {
        /// <summary>
        /// 构造一个新的玩家记录
        /// </summary>
        /// <param name="uid">uid</param>
        /// <param name="playerAvatars">玩家角色</param>
        /// <param name="playerSpiralAbyssesLevels">玩家深渊信息</param>
        public PlayerRecord(string uid, List<PlayerAvatar> playerAvatars, List<PlayerSpiralAbyssLevel> playerSpiralAbyssesLevels)
        {
            Uid = uid;
            PlayerAvatars = playerAvatars;
            PlayerSpiralAbyssesLevels = playerSpiralAbyssesLevels;
        }

        /// <summary>
        /// uid
        /// </summary>
        public string Uid { get; }

        /// <summary>
        /// 玩家角色
        /// </summary>
        public List<PlayerAvatar> PlayerAvatars { get; }

        /// <summary>
        /// 玩家深渊信息
        /// </summary>
        public List<PlayerSpiralAbyssLevel> PlayerSpiralAbyssesLevels { get; }
    }
}