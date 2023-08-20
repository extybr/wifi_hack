#!/usr/bin/python3
from scapy.all import *
from sys import argv
from random import random

iface = argv[1]
essid = argv[2]
INTERVAL = 0.05


def set_new_mac():
    src = list(map(lambda x: "%02x".upper() % int(random() * 0xFF), range(5)))
    new_mac = "00:" + ':'.join(src)
    return new_mac


source = set_new_mac()
target = 'ff:ff:ff:ff:ff:ff'
WPA = 'ESS+privacy'
OPN = 'ESS'
RATE_1B = b"\x82"
RATE_2B = b"\x84"
RATE_5_5B = b"\x8b"
RATE_11B = b"\x96"

radio = RadioTap(len=18, present=0x482e, Rate=2, Channel=2412,
                 ChannelFlags=0x00a0, dBm_AntSignal=chr(1), Antenna=1)
dot11 = Dot11(type=0, subtype=8, addr1=target, addr2=source, addr3=source)
beacon = (Dot11Beacon(cap=OPN)/Dot11Elt(ID='SSID', info=essid, len=len(essid))
          /Dot11Elt(ID='Rates', info=RATE_1B+RATE_2B+RATE_5_5B+RATE_11B)
          /Dot11Elt(ID='ERPinfo', info=b"\x04")
          /Dot11Elt(ID='DSset', info=b"\x01"))
#Dot11Elt(ID='ESRates', info=b"\x30\x48\x60\x6c")/
# Dot11Elt(ID='ExtendendCapatibilities',
# info=b"\x00\x00\x00\x02\x00\x00\x00\x02")/"\x05\x04\x01\x02\x00\x00"
sendp(radio/dot11/beacon, iface=iface, inter=INTERVAL, loop=1)
