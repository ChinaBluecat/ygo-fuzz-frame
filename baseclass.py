#coding=utf-8

'''
用于存放所有会用到的一些基础类
'''


from ctypes import *
import struct
from abc import ABC, abstractmethod

class pack(Structure):
    #_pack_ = 1              # offset = 1
    _fields_ = []
    def __init__(self):
        pass
    #@abstractmethod
    def aberrance(self,):
        return bytes(self)
    def __bytes__(self,):
        # 获得自身的二进制内容, 返回是b格式
        # length+2这样写可以让卡组那里多开辟一些空间, 但是读的时候不读多余的
        return struct.pack('HB', self.length, self.proto) + string_at(addressof(self), self.length-1)

class Net_Handle(ABC):
# 除了网络handle, 以后也可以写本地handle
    def __init__(self,):
        self.sock = None
    @abstractmethod
    def send_package(self,):
        pass
    @abstractmethod
    def recv_callback(self,):
        pass
    @abstractmethod
    def listen(self,):
        pass
    @abstractmethod
    def start(self,):
        pass
    @abstractmethod
    def connect(self,):
        pass
    @abstractmethod
    def disconnect(self,):
        pass




if __name__ == ('__main__'):
    print('haha')
