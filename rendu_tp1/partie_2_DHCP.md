# Part II : DHCP Service


## Installation serveur DHCP

Fichier de configuration de `dhcpd`
```
[root@dhcp vm-3]# cat /etc/dhcp/dhcpd.conf
# IP du serveur DNS
option domain-name-servers     1.1.1.1;

# Temps par défault du bail
default-lease-time 86400;

# Temps maximum du bail
max-lease-time 172800;

# On déclare le serveur DHCP comme ayant autorité dans tous les blocs de sous-réseau qu'on va définir
authoritative;

# Déclaration du sous-réseau
subnet 10.1.1.0 netmask 255.255.255.0 {
    # On indique les adresses IP que le serveur DHCP va distribuer
    range dynamic-bootp 10.1.1.100 10.1.1.200;
    # Address de Broadcast
    option broadcast-address 10.1.1.255;
}
```


Démarrage du démon `dhcpd`
```
[vm-3@dhcp ~]$ sudo systemctl enable dhcpd
Created symlink /etc/systemd/system/multi-user.target.wants/dhcpd.service → /usr/lib/systemd/system/dhcpd.service.
[vm-3@dhcp ~]$ sudo systemctl start dhcpd
```

Ajout de règle pour `firewalld`
```
[vm-3@dhcp ~]$ sudo firewall-cmd --add-service=dhcp 
success

## Pour rendre permanent les règles actuels
[vm-3@dhcp ~]$ sudo firewall-cmd --runtime-to-permanent 
success
```

## Ask an address

- Test d'utilisation du DHCP avec `node1`
=> Modification de `/etc/sysconfig/network-scripts/ifcfg-enp1s0` pour utiliser le DHCP
```
[vm-1@node1 ~]$ sudo cat /etc/sysconfig/network-scripts/ifcfg-enp1>
DEVICE=enp1s0

ONBOOT=yes
BOOTPROTO=dhcp
```

=> Récupération de l'IP `10.1.1.100`
```
[vm-1@node1 ~]$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: enp1s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 52:54:00:2d:8b:c8 brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.100/24 brd 10.1.1.255 scope global dynamic noprefixroute enp1s0
       valid_lft 85954sec preferred_lft 85954sec
    inet6 fe80::5054:ff:fe2d:8bc8/64 scope link 
       valid_lft forever preferred_lft forever
```

=> On remarque bien l'ajout du serveur DNS `1.1.1.1`
```
[vm-1@node1 ~]$ cat /etc/resolv.conf 
# Generated by NetworkManager
search tp1.my
nameserver 1.1.1.1
```


- Bail DHCP du `node1`

```
[root@dhcp vm-3]# cat /var/lib/dhcpd/dhcpd.leases

lease 10.1.1.100 {
  starts 2 2025/02/11 14:40:04;
  ends 3 2025/02/12 14:40:04;
  cltt 2 2025/02/11 14:40:04;
  binding state active;
  next binding state free;
  rewind binding state free;
  hardware ethernet 52:54:00:2d:8b:c8;
  uid "\001RT\000-\213\310";
  client-hostname "node1";
}
```

La 🦈 [capture](./pcaps/dhcp_1.pcap) du DORA


[Partie 3 Nmap](./partie_3_Nmap.md)
