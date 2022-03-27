using Newtonsoft.Json;
using Snap.Data.Primitive;
using System.Collections.Generic;

namespace DGP.Genshin.MiHoYoAPI.Calculation
{
    public class Consumption : Observable
    {
        private List<ConsumeItem>? avatarConsume;
        private List<ConsumeItem>? avatarSkillConsume;
        private List<ConsumeItem>? weaponConsume;
        private List<ReliquaryConsumeItem>? reliquaryConsume;

        [JsonProperty("avatar_consume")]
        public List<ConsumeItem>? AvatarConsume
        {
            get => this.avatarConsume;

            set => this.Set(ref this.avatarConsume, value);
        }
        [JsonProperty("avatar_skill_consume")]
        public List<ConsumeItem>? AvatarSkillConsume
        {
            get => this.avatarSkillConsume;

            set => this.Set(ref this.avatarSkillConsume, value);
        }
        [JsonProperty("weapon_consume")]
        public List<ConsumeItem>? WeaponConsume
        {
            get => this.weaponConsume;

            set => this.Set(ref this.weaponConsume, value);
        }
        [JsonProperty("reliquary_consume")]
        public List<ReliquaryConsumeItem>? ReliquaryConsume
        {
            get => this.reliquaryConsume;

            set => this.Set(ref this.reliquaryConsume, value);
        }
    }
}
