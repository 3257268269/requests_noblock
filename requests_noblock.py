# -*- coding: UTF-8 -*-

import requests, threading, time

import inspect
import ctypes


class requests_noblock(object):

    def __init__(self, timeout = 3.5, check_interval = 0.1):
        self.response = {"code":0,"data":""}
        self.check_interval = check_interval  #每隔一定时间检测是否有返回结果
        self.timeout = timeout                #超时时间

    def real_get(self, **kwargs):
        repo = requests.get(url = kwargs["url"], params = kwargs["params"])
        self.response["code"] = 1
        self.response["data"] = repo

    def get(self, url, params = ''):
        t_req = threading.Thread(target = self.real_get, kwargs = {"url":url,"params":params}) 
        t_req.start()

        wait_count = int(self.timeout / self.check_interval)
        for i in range(wait_count):
            print(i)
            time.sleep(self.check_interval)
            if self.response["code"] == 1 :
                break  #请求结束

        if t_req.isAlive(): #杀死卡住的请求线程
            self.stop_thread(t_req)

        return self.response

          
    def _async_raise(self, tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def stop_thread(self, thread):
        self._async_raise(thread.ident, SystemExit)
      