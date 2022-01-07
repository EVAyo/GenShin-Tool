using Newtonsoft.Json;
using System;

namespace DGP.Genshin.MiHoYoAPI.GameRole
{
    public class UserGameRole : IEquatable<UserGameRole>
    {
        [JsonProperty("game_biz")] public string? GameBiz { get; set; }
        [JsonProperty("region")] public string? Region { get; set; }
        [JsonProperty("game_uid")] public string? GameUid { get; set; }
        [JsonProperty("nickname")] public string? Nickname { get; set; }
        [JsonProperty("level")] public int Level { get; set; }
        [JsonProperty("is_chosen")] public bool IsChosen { get; set; }
        [JsonProperty("region_name")] public string? RegionName { get; set; }
        [JsonProperty("is_official")] public string? IsOfficial { get; set; }

        public bool Equals(UserGameRole? other)
        {
            if(other is null)
            {
                return false;
            }
            return GameUid == other.GameUid
                && Nickname == other.Nickname
                && Level == other.Level;
        }

        /// <summary>
        /// 重写的方法
        /// </summary>
        /// <returns></returns>
        public override string ToString()
        {
            return $"{Nickname} | Lv.{Level} | {RegionName}";
        }

        public override bool Equals(object? obj)
        {
            return Equals(obj as UserGameRole);
        }

        public static bool operator ==(UserGameRole? left,UserGameRole? right)
        {
            if (left is null || right is null)
            {
                if (left is null && right is null)
                {
                    return true;
                }
                return false;
            }
            else
            {
                return left.Equals(right);
            }
        }

        public static bool operator !=(UserGameRole? left, UserGameRole? right)
        {
            if (left is null || right is null)
            {
                if (left is null && right is null)
                {
                    return false;
                }
                return true;
            }
            else
            {
                return !left.Equals(right);
            }
        }

        public override int GetHashCode()
        {
            return base.GetHashCode();
        }
    }
}
