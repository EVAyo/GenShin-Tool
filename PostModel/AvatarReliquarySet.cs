namespace DGP.Genshin.HutaoAPI.PostModel
{
    public class AvatarReliquarySet
    {
        public AvatarReliquarySet(int id, int count)
        {
            Id = id;
            Count = count;
        }

        public int Id { get; set; }
        public int Count { get; set; }
    }
}