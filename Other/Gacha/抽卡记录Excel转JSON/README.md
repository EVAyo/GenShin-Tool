# CORS报错

> from origin 'null' has been blocked by CORS policy: Cross origin requests are only supported for protocol schemes: http, data, chrome, chrome-extension, chrome-untrusted, https, isolated-app.

解决办法：

本地搭建一个server服务器 安装http-server，用npm、cnpm等等都行； 1、打开cmd，全局安装。记得用管理员身份，不然会报错：

```
>npm install http-server -g
```

2、打开跨域文件所在文件夹，即需要共享的资源目录。比如A项目下的X.html跨域，则进入A文件夹目录，输入：

```
>http-server
```

会显示可用服务，就可以顺利运行了； 3、终止服务，cmd里点击ctrl+c就停止了。