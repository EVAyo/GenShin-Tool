using Newtonsoft.Json;
using System;
using System.Collections.Generic;

namespace DGP.Genshin.MiHoYoAPI.Record.SpiralAbyss
{
    /// <summary>
    /// 表示一次战斗
    /// </summary>
    public class Battle
    {
        [JsonProperty("index")] public int Index { get; set; }
        [JsonProperty("timestamp")] public string? Timestamp { get; set; }
        [JsonProperty("avatars")] public List<IconAvatar>? Avatars { get; set; }
        public DateTime? Time
        {
            get
            {
                if (this.Timestamp is not null)
                {
                    DateTimeOffset dto = DateTimeOffset.FromUnixTimeSeconds(int.Parse(this.Timestamp));
                    return dto.ToLocalTime().DateTime;
                }
                return null;
            }
        }
    }
}
