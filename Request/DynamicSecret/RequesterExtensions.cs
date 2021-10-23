namespace DGP.Genshin.MiHoYoAPI.Request.DynamicSecret
{
    public static class RequesterExtensions
    {
        /// <summary>
        /// 使用2代动态密钥需要调用此扩展方法
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="requester"></param>
        /// <param name="url"></param>
        /// <returns></returns>
        public static T? GetWhileUpdateDynamicSecret2<T>(this Requester requester, string url) where T : class
        {
            requester.Headers["DS"] = DynamicSecretProvider2.Create(url);
            return requester.Get<T>(url)?.Data;
        }
        /// <summary>
        /// 使用2代动态密钥需要调用此扩展方法
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="requester"></param>
        /// <param name="url"></param>
        /// <param name="data"></param>
        /// <returns></returns>
        public static T? PostWhileUpdateDynamicSecret2<T>(this Requester requester, string url, object data) where T : class
        {
            requester.Headers["DS"] = DynamicSecretProvider2.Create(url, data);
            return requester.Post<T>(url, data)?.Data;
        }
    }
}
