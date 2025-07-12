import network
import time

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print('Verbinde mit WLAN...')
        wlan.connect(ssid, password)
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1

    if wlan.isconnected():
        print('Verbunden mit:', ssid)
        print('IP-Adresse:', wlan.ifconfig()[0])
    else:
        print('WLAN-Verbindung fehlgeschlagen')

connect_wifi('Galaxy Note10+ Henri', '12345678')