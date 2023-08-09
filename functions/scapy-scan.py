import scapy.all as scapy

def scan(ip):
	arp_request = scapy.ARP(pdst=ip)
	broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	arp_request_broadcast = broadcast/arp_request
	answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
	
	head = "-------------------------------------------\nIP\t\t\tMAC address\n-------------------------------------------"
	
	if answered_list:
	    print(head)
	    for element in answered_list:
	        result = element[1].psrc + "\t\t" + element[1].hwsrc
	        tail = "-------------------------------------------"
	        print(result + '\n' + tail)	
	
scan("192.168.1.1/24")
scan("192.168.0.1/24")
