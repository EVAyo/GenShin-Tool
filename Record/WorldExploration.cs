﻿using Newtonsoft.Json;
using System.Collections.Generic;

namespace DGP.Genshin.MiHoYoAPI.Record
{
    /// <summary>
    /// 世界探索
    /// </summary>
    public class WorldExploration
    {
        [JsonProperty("level")] public int Level { get; set; }
        /// <summary>
        /// Maxmium is 1000
        /// </summary>
        [JsonProperty("exploration_percentage")] public int ExplorationPercentage { get; set; }
        [JsonProperty("icon")] public string? Icon { get; set; }
        [JsonProperty("name")] public string? Name { get; set; }
        [JsonProperty("type")] public string? Type { get; set; }
        [JsonProperty("offerings")] public List<Offering>? Offerings { get; set; }
        [JsonProperty("id")] public string? Id { get; set; }

        #region Snap Genshin Extensions
        public double ExplorationPercentageBy10
        {
            get => ExplorationPercentage / 10.0;
        }

        public bool IsReputation
        {
            get => Type == "Reputation";
        }

        public string ConvertedType
        {
            get => IsReputation ? "声望等级" : "供奉等级";
        }
        #endregion
    }
}
