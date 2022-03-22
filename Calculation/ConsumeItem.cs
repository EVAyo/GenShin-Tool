﻿using Microsoft;
using Newtonsoft.Json;
using Snap.Data.Primitive;
using System;

namespace DGP.Genshin.MiHoYoAPI.Calculation
{
    /// <summary>
    /// 要消耗的物品信息
    /// </summary>
    public class ConsumeItem : Observable, ICloneable<ConsumeItem>
    {
        private bool isCompleted = false;

        [JsonProperty("id")] public int Id { get; set; }
        [JsonProperty("name")] public string? Name { get; set; }
        [JsonProperty("icon")] public string? Icon { get; set; }
        [JsonProperty("num")] public double Num { get; set; }
        [JsonProperty("wiki_url")] public string? WikiUrl { get; set; }
        public bool IsCompleted { get => isCompleted; set => Set(ref isCompleted, value); }

        private bool? isTodaysMaterial;
        [JsonIgnore]
        public bool IsTodaysMaterial
        {
            get
            {
                if (isTodaysMaterial == null)
                {
                    DateTime day = DateTime.UtcNow + TimeSpan.FromHours(4);
                    DayOfWeek currntDayOfWeek = day.DayOfWeek;
                    isTodaysMaterial = DetermineIsTodaysMaterial(Id, currntDayOfWeek);
                }
                return isTodaysMaterial.Value;
            }
        }

        private bool DetermineIsTodaysMaterial(int id, DayOfWeek currntDayOfWeek)
        {
            Requires.Defined(currntDayOfWeek, nameof(currntDayOfWeek));
            return currntDayOfWeek switch
            {
                DayOfWeek.Monday or DayOfWeek.Thursday => id switch
                {
                    >= 104301 and <= 104303 => true,//自由
                    >= 104310 and <= 104312 => true,//繁荣
                    >= 104320 and <= 104322 => true,//浮世

                    >= 114001 and <= 114004 => true,//高塔孤王
                    >= 114013 and <= 114016 => true,//孤云寒林
                    >= 114025 and <= 114028 => true,//远海夷地
                    _ => false,
                },
                DayOfWeek.Tuesday or DayOfWeek.Friday => id switch
                {
                    >= 104304 and <= 104306 => true,//抗争
                    >= 104313 and <= 104315 => true,//勤劳
                    >= 104323 and <= 104325 => true,//风雅

                    >= 114005 and <= 114008 => true,
                    >= 114017 and <= 114020 => true,
                    >= 114029 and <= 114032 => true,
                    _ => false,
                },
                DayOfWeek.Wednesday or DayOfWeek.Saturday => id switch
                {
                    >= 104307 and <= 104309 => true,//诗文
                    >= 104316 and <= 104318 => true,//黄金
                    >= 104326 and <= 104328 => true,//天光

                    >= 114009 and <= 114012 => true,
                    >= 114021 and <= 114024 => true,
                    >= 114033 and <= 114036 => true,
                    _ => false,
                },
                _ => true,
            };
        }

        public ConsumeItem Clone()
        {
            return new()
            {
                Id = Id,
                Name = Name,
                Icon = Icon,
                Num = Num,
                WikiUrl = WikiUrl,
                IsCompleted = false
            };
        }
    }
}
