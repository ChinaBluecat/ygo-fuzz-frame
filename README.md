# ygo-fuzz-frame

An simple fuzz frame I use to fuzz test ygocore yo-gi-oh card game.

### 1. memory leak

Run ygocore.exe, you can get this game in the link below.

https://f95e1b.link.yunpan.360.cn/lk/surl_yqKswy5qjaZ#/-0

If you get a higher version program, you should change the VERSION patameter in extra_info.py.

Click the first button, witch means play with others.

![image](https://github.com/ChinaBluecat/ygo-fuzz-frame/tree/master/pic/0.png)

Then click the button top right to create a room.

![image](https://github.com/ChinaBluecat/ygo-fuzz-frame/tree/master/pic/1.png)

Click the button '确定'. It will create a server thread in your local network with port==7911.

![image](https://github.com/ChinaBluecat/ygo-fuzz-frame/tree/master/pic/2.png)

You should check your IP address, and change ygo_server_addr in leak_ygo.py.

Then just run leak_ygo.py

```sh
python3 leak_ygo.py
```
