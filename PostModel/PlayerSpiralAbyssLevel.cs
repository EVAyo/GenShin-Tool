using System.Collections.Generic;

namespace DGP.Genshin.HutaoAPI.PostModel
{
    public class PlayerSpiralAbyssLevel
    {
        public PlayerSpiralAbyssLevel(int floorIndex, int levelIndex, int star, List<PlayerSpiralAbyssBattle> battles)
        {
            this.FloorIndex = floorIndex;
            this.LevelIndex = levelIndex;
            this.Star = star;
            this.Battles = battles;
        }

        public int FloorIndex { get; set; }
        public int LevelIndex { get; set; }
        public int Star { get; set; }
        public List<PlayerSpiralAbyssBattle> Battles { get; set; }
    }
}