namespace DGP.Genshin.HutaoAPI.PostModel
{
    public class HutaoItem
    {
        /// <summary>
        /// 需要默认构造器以执行json反序列化
        /// </summary>
        public HutaoItem()
        {

        }

        public HutaoItem(int id, string? name, string? url)
        {
            this.Id = id;
            this.Name = name;
            this.Url = url;
        }

        public int Id { get; set; }
        public string? Name { get; set; }
        public string? Url { get; set; }
    }
}