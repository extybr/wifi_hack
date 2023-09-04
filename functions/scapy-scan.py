import scapy.all as scapy
from sys import argv

net = argv[1].split()
print(*net, sep=' | ')
mac = []


def scan(ip):
    global mac
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    head = "\nIP\t\t\tMAC address\n".center(102, '-')
    if answered_list:
        print(head)
        for element in answered_list:
            result = element[1].psrc + "\t\t" + element[1].hwsrc + "\n"
            if element[1].hwsrc not in mac:
                print(result + "-" * 42)
            mac.append(element[1].hwsrc)


[scan(i) for i in net]
# scan("192.168.0.1/24")
# scan("192.168.1.1/24")
