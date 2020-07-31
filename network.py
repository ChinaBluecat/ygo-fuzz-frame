#coding=utf-8

'''
实现数据包的发送方式, 以及一些特殊封包
还有回包的解析方式

可能要写多socket管理
多线程管理之类的
因为可能涉及多个通信请求
'''

import socket
from pack_struct import *
from baseclass import Net_Handle
import threading
import select
from extra_info import *
import struct

#class_ = getattr(pack_struct,'CTOS_JoinGame')
# 这样写能够根据字符串获得一个类的创建类型
# class_()可以创建
# 记得用sock.shutdown(2) sock.close()来关闭一个连接sock
handles = [
'ygo_handle',
]


class ygo_handle(Net_Handle):

    def __init__(self, addr, port, display=False, name=None, t_lock=None):
        assert(t_lock)  # 保证有线程锁, 为了在控制台输出的打印数据好看
        self.lock = t_lock
        self.name = name
        self.display = display
        #self.control = False
        self.connect(addr, port)
        self.buffer = b''   # 存储缓冲区
        self.callback_func = None   # 用来调用处理获得的数据
        pass

    def connect(self, addr, port):
        #print('connect')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect_ex((addr, port))
        #print('[*] connect successful')

    def recv_callback(self,):
        try:
            length = struct.unpack('H', self.buffer[:2])[0]
            if len(self.buffer) < length + 2:
                return
            proto = self.buffer[2]
            data = self.buffer[3:length+2]
        except Exception as e:
            #print(e)
            return
        if self.display:
            self.lock.acquire()
            print('')
            print('='*30)
            print('[-] Got data from threading <{}>'.format(self.name))
            print('[*] Got data length: {:d}'.format(length))
            print('[*] Got proto: {:x} {}'.format(proto, STOC_dict[proto]))
            print('[*] Got data: {}'.format(data))
            print('='*30)
            self.lock.release()
        if self.callback_func:
            self.callback_func(length, STOC_dict[proto], data)
        #if proto == STOC_ERROR_MSG:
            # 似乎大多数err都会直接断开通信端, 可能需要注意看一下
            #self.disconnect()
            #print('[*] handle <{}> disconnect'.format(self.name))

        self.buffer = self.buffer[length+2:]
        if self.buffer != '':
            self.recv_callback()
        #print('[-] terminal>> ')
        return data

    def disconnect(self,):
        self.socket.shutdown(2)
        self.socket.close()

    def start(self,):
        listener = threading.Thread(target=self.listen)
        listener.setDaemon(True)
        listener.start()
        return

    def listen(self,):
        socket_lock = threading.Lock()
        while True:
            if not self.socket:
                break
            rs, _, _ = select.select([self.socket], [], [], 10)
            for r in rs:
                socket_lock.acquire()
                if not self.socket:
                    socket_lock.release()
                    break
                recv = self.socket.recv(1024)
                if len(recv) < 2:
                    socket_lock.release()
                    break
                self.buffer += recv
                #print(self.buffer)
                self.recv_callback()
                socket_lock.release()

    def send_package(self, num=0, pack=None, DEBUG=False, control=True):
        # pack_list 里面存着可以发送的包
        # 啊干啊=。=, 还有包的创建参数怎么搞啊, 默认么
        # 还是人为带参?
        # 这边真的有点不好写啊=。=
        # 只能先选择包都是设计好了的, 不用人为输入方便些
        if pack:
            self.socket.send(pack,)
        else:
            if control:
                while True:
                    self.lock.acquire()
                    print('[-] Those pack can be send')
                    for i in range(len(pack_list)):
                        print('[*] {}. {}'.format(i, pack_list[i]))
                    print('[*] {}. quit'.format(i+1))
                    num = int(input('[-] your choice (num)>> '))
                    self.lock.release()
                    if int(num) == i+1:
                        break
                    func = getattr(self, 'send_{}'.format(pack_list[num]))
                    func(DEBUG=DEBUG)
                    print('[-] your choice (num)>> ')

            else:
                func = getattr(self, 'send_{}'.format(pack_list[num]))
                func(DEBUG=DEBUG)
            #print(func)

#===========================================================================
# 这些函数需要稍作修改
    def send_CTOS_PlayerInfo(self, DEBUG=False):
        player_name = 'a'*20
        player_info = CTOS_PlayerInfo(player_name)
        pack = player_info.aberrance() if DEBUG else bytes(player_info)
        self.send_package(pack=pack)
        return

    def send_CTOS_JoinGame(self, DEBUG=False):
        version = 0x134b#0x1351#0x134b
        gameid = 0x62
        pass_ = b'Marshtomp' if DEBUG else b'M#123'
        join_game = CTOS_JoinGame(version, gameid, pass_)
        pack = join_game.aberrance() if DEBUG else bytes(join_game)
        self.send_package(pack=pack)
        return

    def send_CTOS_HS_Ready(self, DEBUG=False):
        hs_ready = CTOS_HS_Ready()
        pack = hs_ready.aberrance() if DEBUG else bytes(hs_ready)
        self.send_package(pack=pack)

    def send_CTOS_HS_ToDuelist(self, DEBUG=False):
        hs_toduelist = CTOS_HS_ToDuelist()
        pack = hs_toduelist.aberrance() if DEBUG else bytes(hs_toduelist)
        self.send_package(pack=pack)

    def send_CTOS_HS_ToObserver(self, DEBUG=False):
        hs_toobserver = CTOS_HS_ToObserver()
        pack = hs_toobserver.aberrance() if DEBUG else bytes(hs_toobserver)
        self.send_package(pack=pack)

    def send_CTOS_LEAVE_Game(self, DEBUG=False):
        leave_game = CTOS_LEAVE_Game()
        pack = leave_game.aberrance() if DEBUG else bytes(leave_game)
        self.send_package(pack=pack)

    def send_CTOS_Chat(self, DEBUG=False):
        player = 2
        msg = 'hello world'
        chat = CTOS_Chat(player, msg)
        pack = chat.aberrance() if DEBUG else bytes(chat)
        self.send_package(pack=pack)

#    def send_CTOS_Kick(self, DEBUG=False):
#        pos =

# 暂时还没用到这个函数
#    def send_CTOS_CREAT_GAME(self, DEBUG=False):
#        info = HostInfo()
#        name = b'player'
#        pass_ = ''#b'Marshtomp'
#        creat_game = CTOS_CreateGame(info, name, pass_)
#        pack = creat_game.aberrance() if DEBUG else bytes(creat_game)
#        self.send_package(pack=pack)

    def send_CTOS_UPDATE_Deck(self, DEBUG=False, deck=deck_buf):
        update_deck = CTOS_UPDATE_Deck(deck)
        pack = update_deck.aberrance() if DEBUG else bytes(update_deck)
        self.send_package(pack=pack)

#===========================================================================

if __name__ == ('__main__'):
    ygo_server_addr = 's1.ygo233.com'
    ygo_server_port = 233
    t_lock = threading.Lock()
    test = ygo_handle(ygo_server_addr, ygo_server_port, display=True, t_lock=t_lock)
    test.listen()
