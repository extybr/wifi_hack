#!/usr/bin/env python
from scapy.all import *
from sys import argv

ap_list = []


def ssid(pkt):
    if pkt.haslayer(Dot11):
        if pkt.type == 0 and pkt.subtype == 8:
            if pkt.addr2 not in ap_list:
                ap_list.append(pkt.addr2)
                print("AP: %s SSID: %s" % (pkt.addr2, pkt.info.decode()))


sniff(iface=argv[1], prn=ssid)
