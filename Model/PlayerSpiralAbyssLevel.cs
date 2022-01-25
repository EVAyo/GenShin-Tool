using System.Collections.Generic;

namespace DGP.Genshin.HutaoAPI.Model
{
    public class PlayerSpiralAbyssLevel
    {
        public int FloorIndex { get; set; }
        public int LevelIndex { get; set; }
        public int Star { get; set; }
        public List<PlayerSpiralAbyssBattle> Battles { get; set; }
    }
}