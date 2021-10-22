using DGP.Genshin.MiHoYoAPI.Response;
using System;
using System.Collections.Generic;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace DGP.Genshin.MiHoYoAPI.Request
{
    /// <summary>
    /// MiHoYo API 专用请求器
    /// </summary>
    public class Requester
    {
        public RequestOptions Headers { get; set; } = new RequestOptions();

        public Requester() { }
        public Requester(RequestOptions headers)
        {
            Headers = headers;
        }

        private Response<T>? Request<T>(Func<WebClient, string> requestMethod)
        {
            try
            {
                using (WebClient client = new())
                {
                    client.Encoding = Encoding.UTF8;
                    foreach (KeyValuePair<string, string> entry in Headers)
                    {
                        client.Headers[entry.Key] = entry.Value;
                    }
                    string response = requestMethod(client);
                    Response<T>? resp = Json.ToObject<Response<T>>(response);
                    return resp;
                }
            }
            catch (Exception ex)
            {
                return new Response<T>
                {
                    ReturnCode = (int)KnownReturnCode.Failed,
                    Message = ex.Message
                };
            }
        }
        internal Response<T>? Get<T>(string? url)
        {
            return url is null ? null : Request<T>(client => client.DownloadString(url));
        }

        internal Response<T>? Post<T>(string url, dynamic data)
        {
            return Request<T>(client => client.UploadString(url, Json.Stringify(data)));
        }

        internal Response<T>? Post<T>(string url, string str)
        {
            return Request<T>(client => client.UploadString(url, str));
        }


        /// <summary>
        /// 对<see cref="Get{T}(string)"/>方法的异步包装
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="url"></param>
        /// <returns></returns>
        public async Task<Response<T>?> GetAsync<T>(string url)
        {
            return await Task.Run(() => Get<T>(url));
        }

        /// <summary>
        /// 对<see cref="Post{T}(string, object)"/>方法的异步包装
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="url"></param>
        /// <param name="data"></param>
        /// <returns></returns>
        public async Task<Response<T>?> PostAsync<T>(string url, dynamic data)
        {
            return await Task.Run(() => Post<T>(url, data));
        }

        /// <summary>
        /// 对<see cref="Post{T}(string, object)"/>方法的异步包装
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="url"></param>
        /// <param name="data"></param>
        /// <returns></returns>
        public async Task<Response<T>?> PostAsync<T>(string url, string data)
        {
            return await Task.Run(() => Post<T>(url, data));
        }
    }
}