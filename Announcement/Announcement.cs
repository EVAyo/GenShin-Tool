using Newtonsoft.Json;
using System;
using System.Windows.Input;

namespace DGP.Genshin.MiHoYoAPI.Announcement
{
    public class Announcement : AnnouncementContent
    {
        [JsonProperty("type_label")] public string? TypeLabel { get; set; }
        [JsonProperty("tag_label")] public string? TagLabel { get; set; }
        [JsonProperty("tag_icon")] public string? TagIcon { get; set; }
        [JsonProperty("login_alert")] public int LoginAlert { get; set; }
        [JsonProperty("start_time")] public DateTime StartTime { get; set; }
        [JsonProperty("end_time")] public DateTime EndTime { get; set; }

        #region inject
        public ICommand? OpenAnnouncementUICommand { get; set; }
        public bool ShouldShowTimeDescription
        {
            get => Type == 1;
        }

        public string TimeDescription
        {
            get
            {
                DateTime now = DateTime.UtcNow;
                if (StartTime > now)//尚未开始
                {
                    TimeSpan span = StartTime - now;
                    return $"{(int)span.TotalDays} 天后开始";
                }
                else
                {
                    TimeSpan span = EndTime - now;
                    return $"{(int)span.TotalDays} 天后结束";
                }
            }
        }
        public bool ShouldShowTimePercent
        {
            get => ShouldShowTimeDescription && (TimePercent > 0 && TimePercent < 1);
        }

        private double timePercent;
        public double TimePercent
        {
            get
            {
                if (timePercent == 0)
                {
                    //UTC+8
                    DateTime currentTime = DateTime.UtcNow + TimeSpan.FromHours(8);
                    TimeSpan current = currentTime - StartTime;
                    TimeSpan total = EndTime - StartTime;
                    timePercent = current / total;
                }
                return timePercent;
            }
        }
        #endregion

        [JsonProperty("type")] public int Type { get; set; }
        [JsonProperty("remind")] public int Remind { get; set; }
        [JsonProperty("alert")] public int Alert { get; set; }
        [JsonProperty("tag_start_time")] public string? TagStartTime { get; set; }
        [JsonProperty("tag_end_time")] public string? TagEndTime { get; set; }
        [JsonProperty("remind_ver")] public int RemindVer { get; set; }
        [JsonProperty("has_content")] public bool HasContent { get; set; }
    }
}
