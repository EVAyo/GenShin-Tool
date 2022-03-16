using DGP.Genshin.HutaoAPI.PostModel;
using DGP.Genshin.MiHoYoAPI.Record.Avatar;
using DGP.Genshin.MiHoYoAPI.Record.SpiralAbyss;
using Microsoft;
using Snap.Data.Utility;
using System.Collections.Generic;
using System.Linq;

namespace DGP.Genshin.HutaoAPI
{
    internal static class PlayerRecordBuilder
    {
        private record FloorIndexedLevel(int FloorIndex, Level Level);

        internal static PlayerRecord BuildPlayerRecord(string uid, DetailedAvatarWrapper detailAvatars, SpiralAbyss spiralAbyss)
        {
            Requires.NotNull(detailAvatars.Avatars!, nameof(detailAvatars.Avatars));
            List<PlayerAvatar> playerAvatars = detailAvatars.Avatars
                .Select(avatar => new PlayerAvatar(
                    avatar.Id,
                    avatar.Level,
                    avatar.ActivedConstellationNum,
                    BuildAvatarWeapon(avatar.Weapon),
                    BuildAvatarReliquarySets(avatar.Reliquaries)))
                .ToList();

            Requires.NotNull(spiralAbyss.Floors!, nameof(spiralAbyss.Floors));
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
            Requires.NotNull(weapon!, nameof(weapon));
            return new(weapon.Id, weapon.Level, weapon.AffixLevel);
        }
        private static List<AvatarReliquarySet> BuildAvatarReliquarySets(List<Reliquary>? reliquaries)
        {
            Requires.NotNull(reliquaries!, nameof(reliquaries));
            CounterInt32<int> reliquarySetCounter = new();
            foreach (Reliquary reliquary in reliquaries)
            {
                if (reliquary.ReliquarySet is not null)
                {
                    reliquarySetCounter.Increase(reliquary.ReliquarySet.Id);
                }
            }
            //含有2件套以上的套装
            return reliquarySetCounter.Keys.Any(k => k >= 2)
                ? reliquarySetCounter.Select(kvp => new AvatarReliquarySet(kvp)).ToList()
                : new();
        }
    }
}