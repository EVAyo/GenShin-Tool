using DGP.Genshin.Common.Request;
using DGP.Genshin.Common.Response;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace DGP.Genshin.MiHoYoAPI.Blackboard
{
    public class BlackboardProvider
    {
        private const string ApiStatic = @"https://api-static.mihoyo.com";
        public async Task<List<BlackboardEvent>?> GetBlackboardEventsAsync()
        {
            Requester requester = new();
            Response<ListWrapper<BlackboardEvent>>? resp =
                await requester.GetAsync<ListWrapper<BlackboardEvent>>($"{ApiStatic}/common/blackboard/ys_obc/v1/get_activity_calendar?app_sn=ys_obc");
            return resp?.Data?.List;
        }
    }
}
