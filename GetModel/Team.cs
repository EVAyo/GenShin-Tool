using System.Collections.Generic;
using System.Linq;

namespace DGP.Genshin.HutaoAPI.GetModel
{
    public class Team
    {
        public string UpHalf { get; set; } = null!;
        public string DownHalf { get; set; } = null!;

        public IEnumerable<int> GetUp()
        {
            return UpHalf.Split(',').Select(x => int.Parse(x));
        }

        public IEnumerable<int> GetDown()
        {
            return DownHalf.Split(',').Select(x => int.Parse(x));
        }
    }
}
