using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DGP.Genshin.MiHoYoAPI.Record.Card
{
    public class Card
    {
        [JsonProperty("has_role")] public bool HasRole { get; set; }
        [JsonProperty("game_id")] public int GameId { get; set; }
        [JsonProperty("game_role_id")] public string? GameRoleId { get; set; }
        [JsonProperty("nickname")] public string? NickName { get; set; }
        [JsonProperty("region")] public string? Region { get; set; }
        [JsonProperty("level")] public int Level { get; set; }
        [JsonProperty("background_image")] public string? BackgroundImage { get; set; }
        [JsonProperty("is_public")] public bool IsPublic { get; set; }
        [JsonProperty("data")] public List<CardData>? Data { get; set; }
        [JsonProperty("region_name")] public string? RegionName { get; set; }
        [JsonProperty("url")] public string? Url { get; set; }
        [JsonProperty("data_switches")] public List<DataSwitch>? DataSwitches { get; set; }
        [JsonProperty("h5_data_switches")] public List<DataSwitch>? H5DataSwitches { get; set; }
    }
    public class DataSwitch
    {
        /// <summary>
        /// 1：个人主页卡片
        /// 2：角色详情数据
        /// 3：实时便笺数据展示
        /// </summary>
        [JsonProperty("switch_id")] public int SwitchId { get; set; }
        [JsonProperty("is_public")] public bool IsPublic { get; set; }
        [JsonProperty("switch_name")] public string? SwitchName { get; set; }
    }
}
