namespace DGP.Genshin.HutaoAPI.PostModel
{
    public class GenshinItem
    {
        public GenshinItem()
        {

        }

        public GenshinItem(int id, string? name, string? url)
        {
            Id = id;
            Name = name;
            Url = url;
        }

        public int Id { get; set; }
        public string? Name { get; set; }
        public string? Url { get; set; }
    }
}