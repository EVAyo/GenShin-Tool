using Newtonsoft.Json;

namespace DGP.Genshin.MiHoYoAPI.Sign
{
    [JsonModel]
    public class SignInAward : Observable
    {
        private readonly double opacity = 1;

        [JsonProperty("icon")] public string? Icon { get; set; }
        [JsonProperty("name")] public string? Name { get; set; }
        [JsonProperty("cnt")] public string? Count { get; set; }
        public double Opacity { get => opacity; set => this.Set(ref opacity, value); }
    }
}
