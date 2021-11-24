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
        public const string NoviceWishes = "100";
        public const string CharacterEventWish = "301";
        public const string CharacterEventWish2 = "400";
        public const string WeaponEventWish = "302";

        public static readonly Dictionary<string, string> Known = new()
        {
            { "100", "新手祈愿" },
            { "200", "奔行世间" },
            { "301", "角色活动" },
            { "400", "角色活动-2" },
            { "302", "神铸赋形" }
        };
    }
}
