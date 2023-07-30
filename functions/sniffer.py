#!/usr/bin/env python
from scapy.all import *
from scapy.layers.dot11 import *
from pprint import pprint
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

PROBE_REQUEST_TYPE = 0
PROBE_REQUEST_SUBTYPE = 4


class iSniffer(object):
    def __init__(self, iface='en1', whitelist=None, verbose=False):
        if not whitelist:
            whitelist = ['00:00:00:00:00:00', ]
        self.iface = iface
        self.whitelist = whitelist
        self.verbose = verbose
        self.aps = {}
        self.clients = {}

    def handle_probe(self, pkt):
        if pkt.haslayer(Dot11ProbeReq) and '\x00' not in pkt[Dot11ProbeReq].info:
            essid = pkt[Dot11ProbeReq].info
        else:
            essid = 'Hidden SSID'
        client = pkt[Dot11].addr2

        if client in self.whitelist or essid in self.whitelist:
            return

        if client not in self.clients:
            self.clients[client] = []
            print('[!] New client:  %s ' % client)

        if essid not in self.clients[client]:
            self.clients[client].append(essid)
            print('[+] New ProbeRequest: from %s to %s' % (client, essid))

    def handle_beacon(self, pkt):
        if not pkt.haslayer(Dot11Elt):
            return
        essid = pkt[Dot11Elt].info if '\x00' not in pkt[Dot11Elt].info and pkt[Dot11Elt].info != '' else 'Hidden SSID'
        bssid = pkt[Dot11].addr3
        client = pkt[Dot11].addr2
        if client in self.whitelist or essid in self.whitelist or bssid in self.whitelist:
            return
        try:
            channel = int(ord(pkt[Dot11Elt:3].info))
        except:
            channel = 0
        try:
            extra = pkt.notdecoded
            rssi = -(256-ord(extra[-4:-3]))
        except:
            rssi = -100

        p = pkt[Dot11Elt]
        capability = pkt.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}"
                          "{Dot11ProbeResp:%Dot11ProbeResp.cap%}").split('+')
        crypto = set()
        while isinstance(p, Dot11Elt):
            if p.ID == 48:
                crypto.add("WPA2")
            elif p.ID == 221 and p.info.startswith('\x00P\xf2\x01\x01\x00'):
                crypto.add("WPA")
            p = p.payload
        if not crypto:
            if 'privacy' in capability:
                crypto.add("WEP")
            else:
                crypto.add("OPN")
        enc = '/'.join(crypto)
        if bssid not in self.aps:
            self.aps[bssid] = (channel, essid, bssid, enc, rssi)
            print("[+] New AP {0:5}\t{1:20}\t{2:20}\t{3:5}\t{4:4}".format(channel, essid, bssid, enc, rssi))

    def pkt_handler(self, pkt):
        if pkt.type == PROBE_REQUEST_TYPE and pkt.subtype == PROBE_REQUEST_SUBTYPE:
            self.handle_probe(pkt)
        if pkt.haslayer(Dot11Beacon) or pkt.haslayer(Dot11ProbeResp):
            self.handle_beacon(pkt)

    def sniff(self, count=0):
        print('Press Ctrl-C to stop sniffing.')
        sniff(iface=self.iface,
              prn=self.pkt_handler,
              # lfilter=lambda p: p.haslayer(Dot11))
              lfilter=lambda p: p.haslayer(Dot11Beacon) or p.haslayer(Dot11ProbeResp) or p.haslayer(Dot11ProbeReq))

    def stat(self):
        print('\nAP list:')
        pprint(self.aps)
        print('Clients:')
        pprint(self.clients)


if __name__ == '__main__':
    parser = ArgumentParser('iSniff', description='Tiny iSniff for RFMON under OS X',
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--interface', default='en1', required=False, help='Interface to used')
    args = parser.parse_args()
    isniff = iSniffer(args.interface)
    isniff.sniff()
    isniff.stat()
