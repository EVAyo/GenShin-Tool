using System.Collections.Generic;

namespace DGP.Genshin.HutaoAPI.PostModel
{
    public class AvatarReliquarySet
    {
        public AvatarReliquarySet(int id, int count)
        {
            Id = id;
            Count = count;
        }

        public AvatarReliquarySet(KeyValuePair<int,int> kvp) : this(kvp.Key, kvp.Value) { }

        public int Id { get; set; }
        public int Count { get; set; }
    }
}