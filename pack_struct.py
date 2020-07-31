#coding=utf-8

'''
用于存放所有可能会用到的数据包结构体
基础类中包含了一个变异函数, 可以由用户重定义来进行包变异
尽量让整个数据包能够达到直接能发送的形式
不用做额外处理

好像不太好用抽象类来写啊=。=
那算了

对齐有问题
结构体强制对齐4位, 没法单字节似乎
只能结构体和封包两边拆分了

加上强制对齐的_pack_ = 1解决了
把所有的类名需要加入到一个大list中, 方便别的地方调用

字节对齐出了点问题, 因为为了1宽度对齐, 结果导致包的16进制对齐方式出错
'''

#from abc import ABCMeta, abstractmethod
from baseclass import pack
from ctypes import *
from extra_info import *

pack_list = [
'CTOS_PlayerInfo',
'CTOS_JoinGame',
#'CTOS_Kick',
'CTOS_Chat',
'CTOS_HS_Ready',
'CTOS_HS_ToDuelist',
'CTOS_HS_ToObserver',
'CTOS_LEAVE_Game',
'CTOS_UPDATE_Deck',
]

class CTOS_PlayerInfo(pack):
    _fields_ = [
        ('name',    c_ushort*20),
        ]

    def __init__(self, name):
        self.length = sizeof(self) - 2
        self.proto = CTOS_PLAYER_INFO
        name = name.encode('utf-8')
        for i in range(len(name)):
            self.name[i] = name[i]

class CTOS_JoinGame(pack):
    _fields_ = [
        ('version', c_ushort),
        ('gameid',  c_uint),
        ('pass_',   c_ushort*20)
        ]

    def __init__(self, version, gameid, pass_):
        self.length = sizeof(self) - 2
        self.proto = CTOS_JOIN_GAME
        self.version = version
        self.gameid = gameid
        for i in range(len(pass_)):
            self.pass_[i] = pass_[i]

class CTOS_Kick(pack):
    _fields_ = [
        ('pos', c_ubyte)
    ]

    def __init__(self, pos):
        self.length = sizeof(self) - 2
        self.proto = CTOS_HS_KICK
        self.pos = pos

class CTOS_Chat(pack):
    _fields_ = [
        ('player',  c_ushort),
        ('msg',     c_ushort*256)
    ]
    def __init__(self, player, msg):
        self.length = sizeof(self) - 2
        self.proto = CTOS_CHAT
        self.player = player
        msg = msg.encode('utf-8')
        for i in range(len(msg)):
            self.msg[i] = msg[i]

class CTOS_HS_Ready(pack):
    _fields_ = [
    ]
    def __init__(self,):
        self.length = 1
        self.proto = CTOS_HS_READY

class CTOS_HS_ToDuelist(pack):
    _fields_ = [
    ]
    def __init__(self,):
        self.length = 1
        self.proto = CTOS_HS_TODUELIST

class CTOS_HS_ToObserver(pack):
    _fields_ = [
    ]
    def __init__(self,):
        self.length = 1
        self.proto = CTOS_HS_TOOBSERVER

class CTOS_LEAVE_Game(pack):
    _fields_ = [
    ]
    def __init__(self,):
        self.length = 1
        self.proto = CTOS_LEAVE_GAME

class CTOS_UPDATE_Deck(pack):
    # 少数可以由用户自由输入内容的大块区域
    # 可能可以通过控制堆申请来做些东西
    # 卡组长度看情况扩大吧, 有多余空间
    _fields_ = [
        ('deck',    c_ubyte*300)
    ]
    def __init__(self, deck_buf):
        length = len(deck_buf)
        self.length = length + 1
        self.proto = CTOS_UPDATE_DECK
        for i in range(length):
            self.deck[i] = deck_buf[i]

class CTOS_HS_Start(pack):
    _fields_ = [
    ]
    def __init__(self,):
        self.length = 1
        self.proto = CTOS_HS_START

if __name__ == ('__main__'):
    #test = CTOS_Chat(2, '你好')
    #print(bytes(test))
    #print(test.length)
    test = CTOS_UPDATE_Deck()
    print(bytes(test))
    print(sizeof(test))
    print(test.length)
