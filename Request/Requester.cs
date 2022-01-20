using DGP.Genshin.Common.Response;
using Snap.Core.Logging;
using Snap.Data.Json;
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Threading;
using System.Threading.Tasks;

namespace DGP.Genshin.Common.Request
{
    /// <summary>
    /// MiHoYo API 专用请求器
    /// 同一个 <see cref="Requester"/> 若使用一代动态密钥不能长时间使用
    /// </summary>
    public class Requester
    {
        // HttpClient is intended to be instantiated once per application, rather than per-use.
        private static readonly Lazy<HttpClient> LazyHttpClient = new(() => new() { Timeout = Timeout.InfiniteTimeSpan });

        public static Action<Exception, string, string>? ResponseFailedAction { get; set; }
        public RequestOptions Headers { get; set; } = new RequestOptions();

        /// <summary>
        /// 构造一个新的 <see cref="Requester"/> 对象
        /// </summary>
        public Requester() { }

        /// <summary>
        /// 构造一个新的 <see cref="Requester"/> 对象
        /// </summary>
        /// <param name="headers">请求头</param>
        public Requester(RequestOptions headers)
        {
            Headers = headers;
        }

        private async Task<Response<T>?> Request<T>(Func<HttpClient, RequestInfo> requestFunc)
        {
            RequestInfo? info = null;

            HttpClient client = LazyHttpClient.Value;
            client.DefaultRequestHeaders.Clear();
            foreach (KeyValuePair<string, string> entry in Headers)
            {
                client.DefaultRequestHeaders.Add(entry.Key, entry.Value);
            }
            info = requestFunc(client);
            try
            {
                HttpResponseMessage response = await info.RequestAsyncFunc.Invoke();
                HttpContent content = response.Content;
                return Json.ToObject<Response<T>>(await content.ReadAsStringAsync());
            }
            catch (Exception ex)
            {
                string? httpMethod = $"[{info?.Method} {info?.Url[..48]}]";
                ResponseFailedAction?.Invoke(ex, httpMethod, "failed");

                return new Response<T>
                {
                    ReturnCode = (int)KnownReturnCode.InternalFailure,
                    Message = $"{ex.GetType()}:{ex.Message}"
                };
            }
        }

        /// <summary>
        /// GET 操作
        /// </summary>
        /// <typeparam name="T">返回的类类型</typeparam>
        /// <param name="url">地址</param>
        /// <returns>响应</returns>
        public async Task<Response<T>?> GetAsync<T>(string? url)
        {
            this.Log($"GET {url?.Split('?')[0]}");
            return url is null ? null : await Request<T>(client =>
           new RequestInfo("GET", url, () => client.GetAsync(url)));
        }

        /// <summary>
        /// POST 操作
        /// </summary>
        /// <typeparam name="T">返回的类类型</typeparam>
        /// <param name="url">地址</param>
        /// <param name="data">要发送的.NET（匿名）对象</param>
        /// <returns>响应</returns>
        public async Task<Response<T>?> PostAsync<T>(string? url, object data)
        {
            string dataString = Json.Stringify(data);
            this.Log($"POST {url?.Split('?')[0]} with\n{dataString}");
            return url is null ? null : await Request<T>(client =>
            new RequestInfo("POST", url, () => client.PostAsync(url, new StringContent(dataString))));
        }
    }
}