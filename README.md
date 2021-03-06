# requests_noblock
经典python库requests的绝不线程卡死的解决方案

问题背景：
项目中有个业务场景如下：
   自己的服务器A需要定时去第三方服务器以http协议获取数据。A是用python搭建的，
因此使用了经典的python库requests的最新版本(https://github.com/psf/requests)。
实战中发现程序有一定的几率卡死在下面这句代码（下文称之为目标代码）：
           response = requests.get(url)
本来以为是没有设置timeout导致requests连接请求一直重试，但是添加了该参数之后仍然
会出现这一问题。上网查找该问题解决方案
https://www.cnblogs.com/niansi/p/7143736.html
https://blog.csdn.net/pilipala6868/article/details/80712195
最新的版本似乎把timeout分为了连接超时和下载超时，因此理论上目标代码一定会在确定的
时间内结束。但是现实情况是的确会出现很小几率的卡死现象。我的业务场景对卡死的容错率
为0，因此必须保证目标代码能在一定时间内结束而不是一直阻塞。因此我对原始的requests
做了进一步封装，具体思路如下：
     主线程绝对不能无休止阻塞  +  目标代码有几率导致线程无休止阻塞
     =>  目标代码不能放到主线程执行
     因此可以将目标代码放到新建线程（请求线程）去执行，在主线程设置一个全局变量用来就接收目标代码
     返回结果。主线程定时循环查看全局变量是否有结果，如果有结果则返回该全局变量；如果没有结果且达到
     超时时间，说明目标代码卡死（或者超时），此时检查请求线程是否alive，如果alive则杀死该线程。
     最后返回未修改的全局变量。
     
python线程库未提供杀死线程的api，因此需要自己实现。我这里用的是
https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread
提供的方案。

本库只是实现了简单的get请求，重点在于库的设计思路。你可以继续完善该库的功能。
实战中最好还是使用原生的requests库。
当你总是遇到跟我类似的情况，线程卡死且不能容忍，尝试各种方案无解，可以试一下我这个方案。
