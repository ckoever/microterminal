# microterminal
A linux-like remote terminal for Micropython 

![status](https://img.shields.io/badge/STATUS-%E2%9A%AA%20IN%20DEVELOPMENT-blue?style=for-the-badge)

![image](https://user-images.githubusercontent.com/77546092/139330248-201f2c31-45de-4afe-98c7-3a6ceb1b3133.png)

### Commands that are implemented yet
```
- ls
- cd
- exit
```

### Required modules
```
os, usocket, _thread, time
```

### Preparations
1. Upload the microtreminal directory onto your micropython board

![image](https://user-images.githubusercontent.com/77546092/139331707-20e5ac1e-a3d6-4215-aac0-c8cca469e942.png)

2. Edit your boot.py and add the following lines:
```python
import network
import machine

#Connect to Wifi
GLOB_WLAN=network.WLAN(network.STA_IF)
GLOB_WLAN.active(True)
GLOB_WLAN.connect("ssid", "passwd")

while not GLOB_WLAN.isconnected():
  machine.idle()

import microterminal
microterminal.start()
```

### Connect

Establish a RAW-TCP connection to the MCU('s IP address). With PuTTy for example.

![image](https://user-images.githubusercontent.com/77546092/139333035-8b6df3dd-1589-4d5d-b68b-bc8a828dfe12.png)
