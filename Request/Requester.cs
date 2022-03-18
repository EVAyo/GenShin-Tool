using DGP.Genshin.MiHoYoAPI.Response;
using Snap.Core.Logging;
using Snap.Data.Json;
using System;
using System.Net;
using System.Net.Http;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace DGP.Genshin.MiHoYoAPI.Request
{
    /// <summary>
    /// MiHoYo API 专用请求器
    /// 同一个 <see cref="Requester"/> 若使用一代动态密钥不能长时间使用
    /// </summary>
    public class Requester
    {
        // HttpClient is intended to be instantiated once per application, rather than per-use.
        private static readonly Lazy<HttpClient> LazyHttpClient = new(() => new() { Timeout = Timeout.InfiniteTimeSpan });
        private static readonly Lazy<HttpClient> LazyGZipCompressionHttpClient = new(() =>
        {
            return new(new HttpClientHandler
            { AutomaticDecompression = DecompressionMethods.GZip })
            { Timeout = Timeout.InfiniteTimeSpan };
        });

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

        /// <summary>
        /// 构造一个新的 <see cref="Requester"/> 对象
        /// </summary>
        /// <param name="headers">请求头</param>
        public Requester(RequestOptions headers, bool useGZipCompression)
        {
            Headers = headers;
            UseGZipCompression = useGZipCompression;
        }


        public bool UseGZipCompression { get; }
        public bool UseAuthToken { get; set; }
        public string? AuthToken { get; set; }

        private async Task<Response<TResult>?> RequestAsync<TResult>(Func<HttpClient, RequestInfo> requestFunc, CancellationToken cancellationToken = default)
        {
            RequestInfo? info = null;

            HttpClient client = UseGZipCompression ? LazyGZipCompressionHttpClient.Value : LazyHttpClient.Value;
            client.DefaultRequestHeaders.Clear();

            if (UseAuthToken)
            {
                client.DefaultRequestHeaders.Authorization = new("Bearer", AuthToken);
            }

            foreach ((string name, string value) in Headers)
            {
                client.DefaultRequestHeaders.Add(name, value);
            }

            info = requestFunc(client);

            try
            {
                HttpResponseMessage response = await info.RequestAsyncFunc.Invoke().ConfigureAwait(false);
                HttpContent content = response.Content;
                string contentString = await content.ReadAsStringAsync(cancellationToken).ConfigureAwait(false);
                return Json.ToObject<Response<TResult>>(contentString);
            }
            catch (Exception ex)
            {
                string? httpMethod = $"[{info?.Method} {info?.Url}]";
                ResponseFailedAction?.Invoke(ex, httpMethod, "failed");

                return Response<TResult>.CreateFail($"{ex.Message}");
            }
        }

        /// <summary>
        /// GET 操作
        /// </summary>
        /// <typeparam name="TResult">返回的类类型</typeparam>
        /// <param name="url">地址</param>
        /// <returns>响应</returns>
        public async Task<Response<TResult>?> GetAsync<TResult>(string? url, CancellationToken cancellationToken = default)
        {
            this.Log($"GET {url?.Split('?')[0]}");
            return url is null ? null : await RequestAsync<TResult>(client =>
            new RequestInfo("GET", url,
            () => client.GetAsync(url, cancellationToken)),
            cancellationToken)
                .ConfigureAwait(false);
        }

        /// <summary>
        /// POST 操作
        /// </summary>
        /// <typeparam name="TResult">返回的类类型</typeparam>
        /// <param name="url">地址</param>
        /// <param name="data">要发送的.NET（匿名）对象</param>
        /// <returns>响应</returns>
        public async Task<Response<TResult>?> PostAsync<TResult>(string? url, object data, CancellationToken cancellationToken = default)
        {
            string dataString = Json.Stringify(data);
            this.Log($"POST {url?.Split('?')[0]} with\n{dataString}");
            return url is null ? null : await RequestAsync<TResult>(client =>
            new RequestInfo("POST", url,
            () => client.PostAsync(url, new StringContent(dataString), cancellationToken)),
            cancellationToken)
                .ConfigureAwait(false);
        }

        /// <summary>
        /// POST 操作,Content-Type
        /// </summary>
        /// <typeparam name="TResult">返回的类类型</typeparam>
        /// <param name="url">地址</param>
        /// <param name="data">要发送的.NET（匿名）对象</param>
        /// <param name="contentType">内容类型</param>
        /// <returns>响应</returns>
        public async Task<Response<TResult>?> PostAsync<TResult>(string? url, object data, string contentType, CancellationToken cancellationToken = default)
        {
            string dataString = Json.Stringify(data);
            this.Log($"POST {url?.Split('?')[0]} with\n{dataString}");
            return url is null ? null : await RequestAsync<TResult>(client =>
            new RequestInfo("POST", url,
            () => client.PostAsync(url, new StringContent(dataString, Encoding.UTF8, contentType), cancellationToken)),
            cancellationToken)
                .ConfigureAwait(false);
        }
    }
}