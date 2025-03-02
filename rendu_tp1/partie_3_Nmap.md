# Part III : Nmap

## 1. Network scan

=> On récupère bien les IPs des 2 machines `node2` et `dhcp` (et l'IP de mon PC dans le réseau `10.1.1.1` + `node1` d'ailleurs)
```
[vm-1@node1 ~]$ sudo nmap -sn -PR 10.1.1.0/24
[sudo] password for vm-1: 
Starting Nmap 7.92 ( https://nmap.org ) at 2025-02-11 16:40 CET
Nmap scan report for 10.1.1.1
Host is up (0.00019s latency).
MAC Address: 52:54:00:DA:33:63 (QEMU virtual NIC)
Nmap scan report for 10.1.1.101
Host is up (0.00038s latency).
MAC Address: 52:54:00:7B:AE:9D (QEMU virtual NIC)
Nmap scan report for dhcp.tp1.my (10.1.1.253)
Host is up (0.00029s latency).
MAC Address: 52:54:00:AD:A7:59 (QEMU virtual NIC)
Nmap scan report for 10.1.1.100
Host is up.
Nmap done: 256 IP addresses (4 hosts up) scanned in 27.77 seconds
```

🦈 Dans le [pcap](./pcaps/nmap_1.pcap) on voit bien le spam ARP sur toutes les IPs possible, et les réponses des différentes VMs


## 2. Machine Scan

- Scan de services et de système d'exploitation sur `dhcp.tp1.my`

=> `-p1-70` pour scaner les ports de 1 à 70 (pour gagner du temps :) )
=> `-O` pour scaner les système d'exploitation
=> `-sV` pour scaner les version des services
=> `-sS` scan TCP
=> `-sU` scan UDP
```
[vm-1@node1 ~]$ sudo nmap -p1-70 -O -sV -sS -sU dhcp.tp1.my
Starting Nmap 7.92 ( https://nmap.org ) at 2025-02-11 17:03 CET
Nmap scan report for dhcp.tp1.my (10.1.1.253)
Host is up (0.00066s latency).
Not shown: 69 filtered udp ports (admin-prohibited), 62 filtered tcp ports (no-response), 7 filtered tcp ports (admin-prohibited)
PORT   STATE         SERVICE VERSION
22/tcp open          ssh     OpenSSH 8.7 (protocol 2.0)
67/udp open|filtered dhcps
MAC Address: 52:54:00:AD:A7:59 (QEMU virtual NIC)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 2.6.32 (94%), Linux 3.10 - 4.11 (94%), Linux 3.2 - 4.9 (94%), Linux 3.4 - 3.10 (94%), Linux 4.15 - 5.6 (94%), Linux 5.1 (94%), Linux 2.6.32 - 3.10 (93%), Linux 2.6.32 - 3.13 (93%), Linux 3.10 (93%), Linux 5.0 - 5.4 (93%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 1 hop

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 177.52 seconds
```

La 🦈 [capture](./pcaps/nmap_2.pcap) du scan juste au dessus

[Partie 4 ARP Poisoning](./partie_4_apr_poisoning.md)