namespace DGP.Genshin.HutaoAPI.Model
{
    public class AvatarWeapon
    {
        public AvatarWeapon(int id, int level, int affixLevel)
        {
            Id = id;
            Level = level;
            AffixLevel = affixLevel;
        }

        public int Id { get; set; }
        public int Level { get; set; }
        /// <summary>
        /// 精炼
        /// </summary>
        public int AffixLevel { get; set; }
    }
}