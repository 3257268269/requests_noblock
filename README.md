# requests_noblock
经典python库requests的绝不线程卡死的解决方案

问题背景：
项目中有个业务场景如下：
   自己的服务器A需要定时去第三方服务器以http协议获取数据。A是用python搭建的，
因此使用了经典的python库requests。
           response = requests.get(url)
