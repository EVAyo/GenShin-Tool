using Newtonsoft.Json;
using System.Collections.Generic;

namespace DGP.Genshin.MiHoYoAPI.Gacha
{
    /// <summary>
    /// 奖池类型信息
    /// </summary>
    public class ConfigType
    {
        [JsonProperty("id")] public string? Id { get; set; }
        [JsonProperty("key")] public string? Key { get; set; }
        [JsonProperty("name")] public string? Name { get; set; }

        public const string PermanentWish = "200";
        public const string NoviceWish = "100";
        public const string CharacterEventWish = "301";
        public const string CharacterEventWish2 = "400";
        public const string WeaponEventWish = "302";

        public static readonly Dictionary<string, string> Known = new()
        {
            { NoviceWish, "新手祈愿" },
            { PermanentWish, "常驻祈愿" },
            { CharacterEventWish, "角色活动祈愿" },
            { CharacterEventWish2, "角色活动祈愿-2" },
            { WeaponEventWish, "武器活动祈愿" }
        };

        public static readonly Dictionary<string, int> Order = new()
        {
            { NoviceWish, 0 },
            { PermanentWish, 1 },
            { CharacterEventWish, 4 },
            { CharacterEventWish2, 3 },
            { WeaponEventWish, 2 }
        };

        public static readonly Dictionary<string, string> UIGFGachaTypeMap = new()
        {
            { NoviceWish, NoviceWish },
            { PermanentWish, PermanentWish },
            { CharacterEventWish, CharacterEventWish },
            { CharacterEventWish2, CharacterEventWish },
            { WeaponEventWish, WeaponEventWish }
        };
    }
}
