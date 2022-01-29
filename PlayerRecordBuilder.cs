using DGP.Genshin.HutaoAPI.PostModel;
using DGP.Genshin.MiHoYoAPI.Record.Avatar;
using DGP.Genshin.MiHoYoAPI.Record.SpiralAbyss;
using Snap.Exception;
using System.Collections.Generic;
using System.Linq;

namespace DGP.Genshin.HutaoAPI
{
    internal static class PlayerRecordBuilder
    {
        /// <summary>
        /// 表示一个对 <see cref="T"/> 类型的计数器
        /// </summary>
        /// <typeparam name="T"></typeparam>
        private class CounterOf<T> : Dictionary<int, T> { }
        private class FloorIndexedLevel
        {
            public FloorIndexedLevel(int floorIndex, Level level)
            {
                FloorIndex = floorIndex;
                Level = level;
            }

            public int FloorIndex { get; set; }
            public Level Level { get; set; }
        }

        internal static PlayerRecord BuildPlayerRecord(string uid, DetailedAvatarWrapper detailAvatars, SpiralAbyss spiralAbyss)
        {
            _ = detailAvatars.Avatars ?? throw new UnexceptedNullException("角色信息不应为 null");
            List<PlayerAvatar> playerAvatars = detailAvatars.Avatars
                .Select(avatar => new PlayerAvatar(
                    avatar.Id,
                    avatar.Level,
                    avatar.ActivedConstellationNum,
                    BuildAvatarWeapon(avatar.Weapon),
                    BuildAvatarReliquarySets(avatar.Reliquaries)))
                .ToList();

            _ = spiralAbyss.Floors ?? throw new UnexceptedNullException("层信息不应为 null");
            List<PlayerSpiralAbyssLevel> playerSpiralAbyssLevels = spiralAbyss.Floors
                .SelectMany(f => f.Levels!, (f, level) => new FloorIndexedLevel(f.Index, level))
                .Select(indexedLevel => new PlayerSpiralAbyssLevel(
                    indexedLevel.FloorIndex,
                    indexedLevel.Level.Index,
                    indexedLevel.Level.Star,
                    indexedLevel.Level.Battles!
                    .Select(b => new PlayerSpiralAbyssBattle(
                        b.Index,
                        b.Avatars!.Select(a => a.Id).ToList()))
                    .ToList()))
                .ToList();

            PlayerRecord playerRecord = new(uid, playerAvatars, playerSpiralAbyssLevels);
            return playerRecord;
        }
        private static AvatarWeapon BuildAvatarWeapon(Weapon? weapon)
        {
            _ = weapon ?? throw new UnexceptedNullException("weapon 不应为 null");
            return new(weapon.Id, weapon.Level, weapon.AffixLevel);
        }
        private static List<AvatarReliquarySet> BuildAvatarReliquarySets(List<Reliquary>? reliquaries)
        {
            _ = reliquaries ?? throw new UnexceptedNullException("reliquaries 不应为 null");
            CounterOf<int> reliquarySetId = new();
            foreach (Reliquary reliquary in reliquaries)
            {
                if (reliquary.ReliquarySet is not null)
                {
                    reliquarySetId[reliquary.ReliquarySet.Id] = reliquarySetId.ContainsKey(reliquary.ReliquarySet.Id)
                        ? reliquarySetId[reliquary.ReliquarySet.Id] + 1
                        : 1;
                }
            }
            //含有2件套以上的套装
            return reliquarySetId.Keys.Any(k => k >= 2)
                ? reliquarySetId.Select(kvp => new AvatarReliquarySet(kvp.Key, kvp.Value)).ToList()
                : (new());
        }
    }

}