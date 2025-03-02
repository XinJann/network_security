# Part I : Lab Setup

## C. Let's config

- VM 1 :

Network interface config => interface `enp1s0` en mode static, avec l'IP 10.1.1.11
```
[vm-1@localhost ~]$ cat /etc/sysconfig/network-scripts/ifcfg-enp1s0

DEVICE=enp1s0

ONBOOT=yes
BOOTPROTO=static

IPADDR=10.1.1.11
NETMASK=255.255.255.0
```

```
[vm-1@localhost ~]$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: enp1s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 52:54:00:2d:8b:c8 brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.11/24 brd 10.1.1.255 scope global noprefixroute enp1s0
       valid_lft forever preferred_lft forever
    inet6 fe80::5054:ff:fe2d:8bc8/64 scope link 
       valid_lft forever preferred_lft forever
```

Fichier `/etc/hosts` :
```
[vm-1@node1 ~]$ cat /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6

10.1.1.253   dhcp.tp1.my
10.1.1.12   node2.tp1.my
```


Ping vers `node2.tp1.my` puis `dhcp.tp1.my`
```
[vm-1@node1 ~]$ ping -c 3 node2.tp1.my
PING node2.tp1.my (10.1.1.12) 56(84) bytes of data.
64 bytes from node2.tp1.my (10.1.1.12): icmp_seq=1 ttl=64 time=0.401 ms
64 bytes from node2.tp1.my (10.1.1.12): icmp_seq=2 ttl=64 time=0.666 ms
64 bytes from node2.tp1.my (10.1.1.12): icmp_seq=3 ttl=64 time=0.678 ms

--- node2.tp1.my ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2058ms
rtt min/avg/max/mdev = 0.401/0.581/0.678/0.127 ms

[vm-1@node1 ~]$ ping -c 3 dhcp.tp1.my
PING dhcp.tp1.my (10.1.1.253) 56(84) bytes of data.
64 bytes from dhcp.tp1.my (10.1.1.253): icmp_seq=1 ttl=64 time=0.716 ms
64 bytes from dhcp.tp1.my (10.1.1.253): icmp_seq=2 ttl=64 time=0.741 ms
64 bytes from dhcp.tp1.my (10.1.1.253): icmp_seq=3 ttl=64 time=0.934 ms

--- dhcp.tp1.my ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2023ms
rtt min/avg/max/mdev = 0.716/0.797/0.934/0.097 ms
```

Hostname de la machine => node1.tp1.my
```
[vm-1@node1 ~]$ sudo hostnamectl
[sudo] password for vm-1: 
 Static hostname: node1.tp1.my
       Icon name: computer-vm
         Chassis: vm 🖴
      Machine ID: c7c95cec88a14c94b4414213943a804e
         Boot ID: ca991f6d4aaf499d99570289de96ae08
  Virtualization: kvm
Operating System: Rocky Linux 9.5 (Blue Onyx)       
     CPE OS Name: cpe:/o:rocky:rocky:9::baseos
          Kernel: Linux 5.14.0-503.23.1.el9_5.x86_64
    Architecture: x86-64
 Hardware Vendor: QEMU
  Hardware Model: Standard PC _Q35 + ICH9, 2009_
Firmware Version: Arch Linux 1.16.3-1-1
```

Fermeture des ports inutiles ouvert par défault par rocky :
```
### Fermer les ports inutiles (=> les services par défault de Rocky)
[vm-1@node1 ~]$ sudo firewall-cmd --permanent --remove-service dhcpv6-client
success
[vm-1@node1 ~]$ sudo firewall-cmd --permanent --remove-service cockpit
success
[vm-1@node1 ~]$ sudo firewall-cmd --reload
success

### Il reste seulement le service ssh (c-a-d => le port 22)
[vm-1@node1 ~]$ sudo firewall-cmd --list-all
public (active)
  target: default
  icmp-block-inversion: no
  interfaces: enp1s0
  sources: 
  services: ssh
  ports: 
  protocols: 
  forward: yes
  masquerade: no
  forward-ports: 
  source-ports: 
  icmp-blocks: 
  rich rules: 
```

- VM 2 :
Network interface config => interface `enp1s0` en mode static, avec l'IP 10.1.1.12
```
[vm-2@localhost ~]$ cat /etc/sysconfig/network-scripts/ifcfg-enp1s0 
DEVICE=enp1s0

ONBOOT=yes
BOOTPROTO=static

IPADDR=10.1.1.12
NETMASK=255.255.255.0
```

```
[vm-2@localhost ~]$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: enp1s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 52:54:00:7b:ae:9d brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.12/24 brd 10.1.1.255 scope global noprefixroute enp1s0
       valid_lft forever preferred_lft forever
    inet6 fe80::5054:ff:fe7b:ae9d/64 scope link 
       valid_lft forever preferred_lft forever
```

Fichier `/etc/hosts`
```
[vm-2@node2 ~]$ cat /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6

10.1.1.253   dhcp.tp1.my
10.1.1.11   node1.tp1.my
```

Ping vers `node1.tp1.my` puis `dhcp.tp1.my`
```
[vm-2@node2 ~]$ ping -c 3 node1.tp1.my
PING node1.tp1.my (10.1.1.11) 56(84) bytes of data.
64 bytes from node1.tp1.my (10.1.1.11): icmp_seq=1 ttl=64 time=0.356 ms
64 bytes from node1.tp1.my (10.1.1.11): icmp_seq=2 ttl=64 time=0.468 ms
64 bytes from node1.tp1.my (10.1.1.11): icmp_seq=3 ttl=64 time=0.690 ms

--- node1.tp1.my ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2049ms
rtt min/avg/max/mdev = 0.356/0.504/0.690/0.138 ms


[vm-2@node2 ~]$ ping -c 3 dhcp.tp1.my
PING dhcp.tp1.my (10.1.1.253) 56(84) bytes of data.
64 bytes from dhcp.tp1.my (10.1.1.253): icmp_seq=1 ttl=64 time=0.625 ms
64 bytes from dhcp.tp1.my (10.1.1.253): icmp_seq=2 ttl=64 time=0.866 ms
64 bytes from dhcp.tp1.my (10.1.1.253): icmp_seq=3 ttl=64 time=0.783 ms

--- dhcp.tp1.my ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2021ms
rtt min/avg/max/mdev = 0.625/0.758/0.866/0.099 ms
```

Hostname de la machine => node2.tp1.my
```
[vm-2@node2 ~]$ sudo hostnamectl
[sudo] password for vm-2: 
 Static hostname: node2.tp1.my
       Icon name: computer-vm
         Chassis: vm 🖴
      Machine ID: c7c95cec88a14c94b4414213943a804e
         Boot ID: e310e2098e9349d28b8157339d9fb208
  Virtualization: kvm
Operating System: Rocky Linux 9.5 (Blue Onyx)       
     CPE OS Name: cpe:/o:rocky:rocky:9::baseos
          Kernel: Linux 5.14.0-503.23.1.el9_5.x86_64
    Architecture: x86-64
 Hardware Vendor: QEMU
  Hardware Model: Standard PC _Q35 + ICH9, 2009_
Firmware Version: Arch Linux 1.16.3-1-1
```

Fermeture des ports inutiles ouvert par défault par rocky :
```
### Idem que pour le node1, on ferme les ports par defautl
[vm-2@node2 ~]$ sudo firewall-cmd --permanent --remove-service dhcpv6-client
[sudo] password for vm-2: 
success
[vm-2@node2 ~]$ sudo firewall-cmd --permanent --remove-service cockpit
success
[vm-2@node2 ~]$ sudo firewall-cmd --reload
success


[vm-2@node2 ~]$ sudo firewall-cmd --list-all
public (active)
  target: default
  icmp-block-inversion: no
  interfaces: enp1s0
  sources: 
  services: ssh
  ports: 
  protocols: 
  forward: yes
  masquerade: no
  forward-ports: 
  source-ports: 
  icmp-blocks: 
  rich rules: 
```  

- VM 3 :

Network interface config => interface `enp1s0` en mode static, avec l'IP 10.1.1.253
```
[vm-3@localhost ~]$ cat /etc/sysconfig/network-scripts/ifcfg-enp1s0 
DEVICE=enp1s0

ONBOOT=yes
BOOTPROTO=static

IPADDR=10.1.1.253
NETMASK=255.255.255.0
```

```
[vm-3@localhost ~]$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: enp1s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 52:54:00:ad:a7:59 brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.253/24 brd 10.1.1.255 scope global noprefixroute enp1s0
       valid_lft forever preferred_lft forever
    inet6 fe80::5054:ff:fead:a759/64 scope link 
       valid_lft forever preferred_lft forever
```
Fichier `/etc/hosts`
```
[vm-3@dhcp ~]$ cat /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6

10.1.1.11   node1.tp1.my
10.1.1.12   node2.tp1.my
```

Ping vers `node1.tp1.my` puis `node2.tp1.my`
```
[vm-3@dhcp ~]$ ping -c 3 node1.tp1.my
PING node1.tp1.my (10.1.1.11) 56(84) bytes of data.
64 bytes from node1.tp1.my (10.1.1.11): icmp_seq=1 ttl=64 time=0.465 ms
64 bytes from node1.tp1.my (10.1.1.11): icmp_seq=2 ttl=64 time=0.668 ms
64 bytes from node1.tp1.my (10.1.1.11): icmp_seq=3 ttl=64 time=0.520 ms

--- node1.tp1.my ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2030ms
rtt min/avg/max/mdev = 0.465/0.551/0.668/0.085 ms


[vm-3@dhcp ~]$ ping -c 3 node2.tp1.my
PING node2.tp1.my (10.1.1.12) 56(84) bytes of data.
64 bytes from node2.tp1.my (10.1.1.12): icmp_seq=1 ttl=64 time=0.582 ms
64 bytes from node2.tp1.my (10.1.1.12): icmp_seq=2 ttl=64 time=0.810 ms
64 bytes from node2.tp1.my (10.1.1.12): icmp_seq=3 ttl=64 time=0.737 ms

--- node2.tp1.my ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2037ms
rtt min/avg/max/mdev = 0.582/0.709/0.810/0.095 ms
```

Et le 🦈 [pcap](./pcaps/ping_1.pcap) du ping

Hostname de la machine => dhcp.tp1.my
```
[vm-3@dhcp ~]$ sudo hostnamectl
[sudo] password for vm-3: 
 Static hostname: dhcp.tp1.my
       Icon name: computer-vm
         Chassis: vm 🖴
      Machine ID: c7c95cec88a14c94b4414213943a804e
         Boot ID: ef8d7373ade54e99861dcde370d1b130
  Virtualization: kvm
Operating System: Rocky Linux 9.5 (Blue Onyx)       
     CPE OS Name: cpe:/o:rocky:rocky:9::baseos
          Kernel: Linux 5.14.0-503.23.1.el9_5.x86_64
    Architecture: x86-64
 Hardware Vendor: QEMU
  Hardware Model: Standard PC _Q35 + ICH9, 2009_
Firmware Version: Arch Linux 1.16.3-1-1
```

Fermeture des ports inutiles ouvert par défault par rocky :
```
### idem que pour node1 et node2
[vm-3@dhcp ~]$ sudo firewall-cmd --permanent --remove-service dhcpv6-client
[sudo] password for vm-3: 
success
[vm-3@dhcp ~]$ sudo firewall-cmd --permanent --remove-service cockpit
success
[vm-3@dhcp ~]$ sudo firewall-cmd --reload
success


[vm-3@dhcp ~]$ sudo firewall-cmd --list-all
public (active)
  target: default
  icmp-block-inversion: no
  interfaces: enp1s0
  sources: 
  services: ssh
  ports: 
  protocols: 
  forward: yes
  masquerade: no
  forward-ports: 
  source-ports: 
  icmp-blocks: 
  rich rules: 
```


## ARP

- Table ARP de `node1.tp1.my`
```
[vm-1@node1 ~]$ ip neigh show
10.1.1.12 dev enp1s0 lladdr 52:54:00:7b:ae:9d STALE 
10.1.1.253 dev enp1s0 lladdr 52:54:00:ad:a7:59 STALE 
10.1.1.1 dev enp1s0 lladdr 52:54:00:da:33:63 REACHABLE 
```

- Vérification des addresses MAC
MAC node2 => `52:54:00:7b:ae:9d`
```
[vm-2@node2 ~]$ ip a
....
2: enp1s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 52:54:00:7b:ae:9d brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.12/24 brd 10.1.1.255 scope global noprefixroute enp1s0
       valid_lft forever preferred_lft forever
    inet6 fe80::5054:ff:fe7b:ae9d/64 scope link 
       valid_lft forever preferred_lft forever
```

MAC dhcp => `52:54:00:ad:a7:59`
```
[vm-3@dhcp ~]$ ip a
....
2: enp1s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 52:54:00:ad:a7:59 brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.253/24 brd 10.1.1.255 scope global noprefixroute enp1s0
       valid_lft forever preferred_lft forever
    inet6 fe80::5054:ff:fead:a759/64 scope link 
       valid_lft forever preferred_lft forever
```

- Manipulation de la table ARP
Vider la table ARP
```
[vm-1@node1 ~]$ sudo ip neigh flush all
[vm-1@node1 ~]$ ip neigh show
10.1.1.1 dev enp1s0 lladdr 52:54:00:da:33:63 REACHABLE 
```

Pinger puis vérifier que la table ARP à une nouvelle entré (celle de node2)
```
[vm-1@node1 ~]$ ping node2.tp1.my
......
[vm-1@node1 ~]$ ip neigh show
10.1.1.12 dev enp1s0 lladdr 52:54:00:7b:ae:9d REACHABLE 
10.1.1.1 dev enp1s0 lladdr 52:54:00:da:33:63 REACHABLE 
```

- 🦈 La [capture](./pcaps/arp_1.pcap) ARP