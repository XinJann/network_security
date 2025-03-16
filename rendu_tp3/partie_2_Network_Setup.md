# Partie II : Network Setup

## 5. DHCP

### DHCP dans les réseaux clients


PC 1 (Client numéro 1) :

```
VPCS> ip dhcp  
DDORA IP 10.3.10.10/24 GW 10.3.10.254  

VPCS> ping ynov.com  
ynov.com resolved to 104.26.10.233  

84 bytes from 104.26.10.233 icmp_seq=1 ttl=52 time=29.603 ms  
84 bytes from 104.26.10.233 icmp_seq=2 ttl=52 time=25.544 ms  
84 bytes from 104.26.10.233 icmp_seq=3 ttl=52 time=36.584 ms  
^C
```

PC 2 (Admin numéro 1) :
```
VPCS> ip dhcp  
DDORA IP 10.3.20.12/24 GW 10.3.20.254  
  
VPCS> ping ynov.com  
ynov.com resolved to 104.26.10.233  
  
84 bytes from 104.26.10.233 icmp_seq=1 ttl=52 time=29.436 ms  
84 bytes from 104.26.10.233 icmp_seq=2 ttl=52 time=36.981 ms  
84 bytes from 104.26.10.233 icmp_seq=3 ttl=52 time=29.252 ms  
^C
```

PC 3 (Client numéro 2) :

```
VPCS> ip dhcp  
DDORA IP 10.3.20.13/24 GW 10.3.20.254  

VPCS> ping ynov.com  
ynov.com resolved to 172.67.74.226  

84 bytes from 172.67.74.226 icmp_seq=1 ttl=52 time=40.177 ms  
84 bytes from 172.67.74.226 icmp_seq=2 ttl=52 time=25.819 ms  
84 bytes from 172.67.74.226 icmp_seq=3 ttl=52 time=28.024 ms  
^C
```

## 6. Preuve de conf et rendu

### `show running-config` des équipements

- Router 1 :
```
R1#sh running-config    
Building configuration...  
  
Current configuration : 1510 bytes  
!  
! Last configuration change at 12:46:57 UTC Thu Mar 6 2025  
!  
version 15.2  
service timestamps debug datetime msec  
service timestamps log datetime msec  
!  
hostname R1  
!  
boot-start-marker  
boot-end-marker  
!  
!  
!  
no aaa new-model  
!  
!  
!  
!  
!  
!  
ip cef       
no ipv6 cef  
!  
!  
multilink bundle-name authenticated  
!  
!  
!  
!  
!  
!  
!  
!  
!  
!  
!  
!  
!    
!  
!  
!  
!  
!  
!            
!  
!  
interface FastEthernet0/0  
no ip address  
duplex full  
!  
interface FastEthernet0/0.10  
encapsulation dot1Q 10  
ip address 10.3.10.252 255.255.255.0  
ip helper-address 10.3.30.251  
ip nat inside  
standby 100 ip 10.3.10.254  
standby 100 priority 120  
standby 100 preempt delay minimum 10  
!  
interface FastEthernet0/0.20  
encapsulation dot1Q 20  
ip address 10.3.20.252 255.255.255.0  
ip helper-address 10.3.30.251 
ip nat inside  
standby 101 ip 10.3.20.254  
standby 101 priority 120  
standby 101 preempt delay minimum 10  
!  
interface FastEthernet0/0.30  
encapsulation dot1Q 30  
ip address 10.3.30.252 255.255.255.0  
ip nat inside  
standby 102 ip 10.3.30.254  
standby 102 priority 110  
standby 102 preempt delay minimum 10  
!  
interface FastEthernet1/0  
no ip address  
shutdown  
duplex full  
!  
interface FastEthernet2/0  
ip address 10.99.99.2 255.255.255.0  
ip nat outside  
duplex full  
!  
ip nat inside source list 1 interface FastEthernet2/0 overload  
ip forward-protocol nd  
!  
!            
no ip http server  
no ip http secure-server  
ip route 0.0.0.0 0.0.0.0 10.99.99.1  
!  
access-list 1 permit any  
!  
!  
!  
control-plane  
!  
!  
line con 0  
stopbits 1  
line aux 0  
stopbits 1  
line vty 0 4  
login  
!  
!  
end
```

- Router 2 :
```
R2#sh running-config    
Building configuration...  
  
Current configuration : 1454 bytes  
!  
! Last configuration change at 12:47:31 UTC Thu Mar 6 2025  
!  
version 15.2  
service timestamps debug datetime msec  
service timestamps log datetime msec  
!  
hostname R2  
!  
boot-start-marker  
boot-end-marker  
!  
!  
!  
no aaa new-model  
!  
!  
!  
!  
!  
!  
ip cef       
no ipv6 cef  
!  
!  
multilink bundle-name authenticated  
!  
!  
!  
!  
!  
!  
!  
!  
!  
!  
!  
!  
!    
!  
!  
!  
!  
!  
!            
!  
!  
interface FastEthernet0/0  
no ip address  
duplex full  
!  
interface FastEthernet0/0.10  
encapsulation dot1Q 10  
ip address 10.3.10.253 255.255.255.0  
ip helper-address 10.3.30.251
ip nat inside  
standby 100 ip 10.3.10.254  
standby 100 priority 110  
standby 100 preempt delay minimum 10  
!  
interface FastEthernet0/0.20  
encapsulation dot1Q 20  
ip address 10.3.20.253 255.255.255.0  
ip helper-address 10.3.30.251
ip nat inside  
standby 101 ip 10.3.20.254  
standby 101 priority 110  
standby 101 preempt delay minimum 10  
!  
interface FastEthernet0/0.30  
encapsulation dot1Q 30  
ip address 10.3.30.253 255.255.255.0  
ip nat inside  
standby 102 ip 10.3.30.254  
standby 102 priority 120  
standby 102 preempt delay minimum 10  
!  
interface FastEthernet1/0  
no ip address  
shutdown  
duplex full  
!  
interface FastEthernet2/0  
ip address 10.100.100.2 255.255.255.0  
ip nat outside  
duplex full  
!  
ip nat inside source list 1 interface FastEthernet2/0 overload  
ip forward-protocol nd  
!  
!  
no ip http server  
no ip http secure-server  
ip route 0.0.0.0 0.0.0.0 10.100.100.1  
!  
access-list 1 permit any  
!  
!  
!  
control-plane  
!  
!  
line con 0  
stopbits 1  
line aux 0  
stopbits 1  
line vty 0 4  
login  
!  
!  
end
```

- Switch `Core1` :
```
Core1#sh running-config    
Building configuration...  
  
Current configuration : 1811 bytes  
!  
! Last configuration change at 10:20:28 UTC Thu Mar 6 2025  
!  
version 15.2  
service timestamps debug datetime msec  
service timestamps log datetime msec  
no service password-encryption  
service compress-config  
!  
hostname Core1  
!  
boot-start-marker  
boot-end-marker  
!  
!  
!  
no aaa new-model  
!  
!  
!  
!  
!            
!  
!  
!  
ip cef  
no ipv6 cef  
!  
!  
!  
spanning-tree mode pvst  
spanning-tree extend system-id  
!  
!  
!    
!  
!  
!  
!  
!  
!  
!  
!  
!  
!            
!  
!  
interface Port-channel1  
switchport trunk allowed vlan 10,20,30  
switchport trunk encapsulation dot1q  
switchport mode trunk  
ip arp inspection trust  
!  
interface Ethernet0/0  
spanning-tree bpduguard enable  
!  
interface Ethernet0/1  
spanning-tree bpduguard enable  
!  
interface Ethernet0/2  
spanning-tree bpduguard enable  
!  
interface Ethernet0/3  
switchport trunk allowed vlan 10,20,30  
switchport trunk encapsulation dot1q  
switchport mode trunk  
ip arp inspection trust  
!            
interface Ethernet1/0  
switchport trunk allowed vlan 10,20,30  
switchport trunk encapsulation dot1q  
switchport mode trunk  
ip arp inspection trust  
!  
interface Ethernet1/1  
switchport trunk allowed vlan 10,20,30  
switchport trunk encapsulation dot1q  
switchport mode trunk  
ip arp inspection trust  
channel-group 1 mode active  
!  
interface Ethernet1/2  
switchport trunk allowed vlan 10,20,30  
switchport trunk encapsulation dot1q  
switchport mode trunk  
ip arp inspection trust  
channel-group 1 mode active  
!  
interface Ethernet1/3  
switchport trunk allowed vlan 10,20,30  
switchport trunk encapsulation dot1q  
switchport mode trunk  
ip arp inspection trust  
!  
ip forward-protocol nd  
!  
ip http server  
!  
ip ssh server algorithm encryption aes128-ctr aes192-ctr aes256-ctr  
ip ssh client algorithm encryption aes128-ctr aes192-ctr aes256-ctr  
!  
!  
!  
!  
!  
control-plane  
!  
!  
line con 0  
logging synchronous  
line aux 0  
line vty 0 4  
!  
!            
!  
end
```

- Switch `Core2` :
```
Core2#sh running-config    
Building configuration...  
  
Current configuration : 1811 bytes  
!  
! Last configuration change at 10:29:21 UTC Thu Mar 6 2025  
!  
version 15.2  
service timestamps debug datetime msec  
service timestamps log datetime msec  
no service password-encryption  
service compress-config  
!  
hostname Core2  
!  
boot-start-marker  
boot-end-marker  
!  
!  
!  
no aaa new-model  
!  
!  
!  
!  
!            
!  
!  
!  
ip cef  
no ipv6 cef  
!  
!  
!  
spanning-tree mode pvst  
spanning-tree extend system-id  
!  
!  
!    
!  
!  
!  
!  
!  
!  
!  
!  
!  
!            
!  
!  
interface Port-channel1  
switchport trunk allowed vlan 10,20,30  
switchport trunk encapsulation dot1q  
switchport mode trunk  
ip arp inspection trust  
!  
interface Ethernet0/0  
spanning-tree bpduguard enable  
!  
interface Ethernet0/1  
spanning-tree bpduguard enable  
!  
interface Ethernet0/2  
spanning-tree bpduguard enable  
!  
interface Ethernet0/3  
switchport trunk allowed vlan 10,20,30  
switchport trunk encapsulation dot1q  
switchport mode trunk  
ip arp inspection trust  
!            
interface Ethernet1/0  
switchport trunk allowed vlan 10,20,30  
switchport trunk encapsulation dot1q  
switchport mode trunk  
ip arp inspection trust  
!  
interface Ethernet1/1  
switchport trunk allowed vlan 10,20,30  
switchport trunk encapsulation dot1q  
switchport mode trunk  
ip arp inspection trust  
channel-group 1 mode active  
!  
interface Ethernet1/2  
switchport trunk allowed vlan 10,20,30  
switchport trunk encapsulation dot1q  
switchport mode trunk  
ip arp inspection trust  
channel-group 1 mode active  
!  
interface Ethernet1/3  
switchport trunk allowed vlan 10,20,30  
switchport trunk encapsulation dot1q  
switchport mode trunk  
ip arp inspection trust  
!  
ip forward-protocol nd  
!  
ip http server  
!  
ip ssh server algorithm encryption aes128-ctr aes192-ctr aes256-ctr  
ip ssh client algorithm encryption aes128-ctr aes192-ctr aes256-ctr  
!  
!  
!  
!  
!  
control-plane  
!  
!  
line con 0  
logging synchronous  
line aux 0  
line vty 0 4  
!  
!            
!  
end
```

- Switch `Distrib1` :
```
Distrib1#sh running-config    
Building configuration...  
  
Current configuration : 1589 bytes  
!  
! Last configuration change at 09:51:45 UTC Thu Mar 6 2025  
!  
version 15.2  
service timestamps debug datetime msec  
service timestamps log datetime msec  
no service password-encryption  
service compress-config  
!  
hostname Distrib1  
!  
boot-start-marker  
boot-end-marker  
!  
!  
!  
no aaa new-model  
!  
!  
!  
!  
!            
!  
!  
!  
ip cef  
no ipv6 cef  
!  
!  
!  
spanning-tree mode pvst  
spanning-tree extend system-id  
!  
!  
!    
!  
!  
!  
!  
!  
!  
!  
!  
!  
!            
!  
!  
interface Ethernet0/0  
spanning-tree bpduguard enable  
!  
interface Ethernet0/1  
spanning-tree bpduguard enable  
!  
interface Ethernet0/2  
spanning-tree bpduguard enable  
!  
interface Ethernet0/3  
switchport trunk allowed vlan 30  
switchport trunk encapsulation dot1q  
switchport mode trunk  
ip arp inspection trust  
!  
interface Ethernet1/0  
switchport trunk allowed vlan 20  
switchport trunk encapsulation dot1q  
switchport mode trunk  
ip arp inspection trust  
!            
interface Ethernet1/1  
switchport trunk allowed vlan 10,20  
switchport trunk encapsulation dot1q  
switchport mode trunk  
ip arp inspection trust  
!  
interface Ethernet1/2  
switchport trunk allowed vlan 10,20,30  
switchport trunk encapsulation dot1q  
switchport mode trunk  
ip arp inspection trust  
!  
interface Ethernet1/3  
switchport trunk allowed vlan 10,20,30  
switchport trunk encapsulation dot1q  
switchport mode trunk  
ip arp inspection trust  
!  
ip forward-protocol nd  
!  
ip http server  
!  
ip ssh server algorithm encryption aes128-ctr aes192-ctr aes256-ctr  
ip ssh client algorithm encryption aes128-ctr aes192-ctr aes256-ctr  
!  
!  
!  
!  
!  
control-plane  
!  
!  
line con 0  
logging synchronous  
line aux 0  
line vty 0 4  
!  
!  
!  
end
```

- Switch `Distrib2` :
```
Distrib2#sh running-config    
Building configuration...  
  
Current configuration : 1589 bytes  
!  
! Last configuration change at 09:52:53 UTC Thu Mar 6 2025  
!  
version 15.2  
service timestamps debug datetime msec  
service timestamps log datetime msec  
no service password-encryption  
service compress-config  
!  
hostname Distrib2  
!  
boot-start-marker  
boot-end-marker  
!  
!  
!  
no aaa new-model  
!  
!  
!  
!  
!            
!  
!  
!  
ip cef  
no ipv6 cef  
!  
!  
!  
spanning-tree mode pvst  
spanning-tree extend system-id  
!  
!  
!    
!  
!  
!  
!  
!  
!  
!  
!  
!  
!            
!  
!  
interface Ethernet0/0  
spanning-tree bpduguard enable  
!  
interface Ethernet0/1  
spanning-tree bpduguard enable  
!  
interface Ethernet0/2  
spanning-tree bpduguard enable  
!  
interface Ethernet0/3  
switchport trunk allowed vlan 10,20  
switchport trunk encapsulation dot1q  
switchport mode trunk  
ip arp inspection trust  
!  
interface Ethernet1/0  
switchport trunk allowed vlan 20  
switchport trunk encapsulation dot1q  
switchport mode trunk  
ip arp inspection trust  
!            
interface Ethernet1/1  
switchport trunk allowed vlan 30  
switchport trunk encapsulation dot1q  
switchport mode trunk  
ip arp inspection trust  
!  
interface Ethernet1/2  
switchport trunk allowed vlan 10,20,30  
switchport trunk encapsulation dot1q  
switchport mode trunk  
ip arp inspection trust  
!  
interface Ethernet1/3  
switchport trunk allowed vlan 10,20,30  
switchport trunk encapsulation dot1q  
switchport mode trunk  
ip arp inspection trust  
!  
ip forward-protocol nd  
!  
ip http server  
!  
ip ssh server algorithm encryption aes128-ctr aes192-ctr aes256-ctr  
ip ssh client algorithm encryption aes128-ctr aes192-ctr aes256-ctr  
!  
!  
!  
!  
!  
control-plane  
!  
!  
line con 0  
logging synchronous  
line aux 0  
line vty 0 4  
!  
!  
!  
end
```

- Switch `Access1` :
```
Access1#sh running-config    
Building configuration...  
  
Current configuration : 1424 bytes  
!  
! Last configuration change at 09:48:30 UTC Thu Mar 6 2025  
!  
version 15.2  
service timestamps debug datetime msec  
service timestamps log datetime msec  
no service password-encryption  
service compress-config  
!  
hostname Access1  
!  
boot-start-marker  
boot-end-marker  
!  
!  
!  
no aaa new-model  
!  
!  
!  
!  
!            
!  
!  
!  
ip cef  
no ipv6 cef  
!  
!  
!  
spanning-tree mode pvst  
spanning-tree extend system-id  
!  
!  
!    
!  
!  
!  
!  
!  
!  
!  
!  
!  
!            
!  
!  
interface Ethernet0/0  
switchport access vlan 10  
switchport mode access  
spanning-tree bpduguard enable  
!  
interface Ethernet0/1  
switchport access vlan 20  
switchport mode access  
spanning-tree bpduguard enable  
!  
interface Ethernet0/2  
spanning-tree bpduguard enable  
!  
interface Ethernet0/3  
spanning-tree bpduguard enable  
!  
interface Ethernet1/0  
spanning-tree bpduguard enable  
!  
interface Ethernet1/1  
spanning-tree bpduguard enable  
!  
interface Ethernet1/2  
switchport trunk allowed vlan 10,20  
switchport trunk encapsulation dot1q  
switchport mode trunk  
ip arp inspection trust  
!  
interface Ethernet1/3  
switchport trunk allowed vlan 10,20  
switchport trunk encapsulation dot1q  
switchport mode trunk  
ip arp inspection trust  
!  
ip forward-protocol nd  
!  
ip http server  
!  
ip ssh server algorithm encryption aes128-ctr aes192-ctr aes256-ctr  
ip ssh client algorithm encryption aes128-ctr aes192-ctr aes256-ctr  
!  
!  
!  
!            
!  
control-plane  
!  
!  
line con 0  
logging synchronous  
line aux 0  
line vty 0 4  
login  
!  
!  
!  
end
```

- Switch `Access2` :
```
Access2#sh running-config    
Building configuration...  
  
Current configuration : 1367 bytes  
!  
! Last configuration change at 09:50:07 UTC Thu Mar 6 2025  
!  
version 15.2  
service timestamps debug datetime msec  
service timestamps log datetime msec  
no service password-encryption  
service compress-config  
!  
hostname Access2  
!  
boot-start-marker  
boot-end-marker  
!  
!  
!  
no aaa new-model  
!  
!  
!  
!  
!            
!  
!  
!  
ip cef  
no ipv6 cef  
!  
!  
!  
spanning-tree mode pvst  
spanning-tree extend system-id  
!  
!  
!    
!  
!  
!  
!  
!  
!  
!  
!  
!  
!            
!  
!  
interface Ethernet0/0  
switchport access vlan 20  
switchport mode access  
spanning-tree bpduguard enable  
!  
interface Ethernet0/1  
spanning-tree bpduguard enable  
!  
interface Ethernet0/2  
spanning-tree bpduguard enable  
!  
interface Ethernet0/3  
spanning-tree bpduguard enable  
!  
interface Ethernet1/0  
spanning-tree bpduguard enable  
!  
interface Ethernet1/1  
spanning-tree bpduguard enable  
!  
interface Ethernet1/2  
switchport trunk allowed vlan 20  
switchport trunk encapsulation dot1q  
switchport mode trunk  
ip arp inspection trust  
!  
interface Ethernet1/3  
switchport trunk allowed vlan 20  
switchport trunk encapsulation dot1q  
switchport mode trunk  
ip arp inspection trust  
!  
ip forward-protocol nd  
!  
ip http server  
!  
ip ssh server algorithm encryption aes128-ctr aes192-ctr aes256-ctr  
ip ssh client algorithm encryption aes128-ctr aes192-ctr aes256-ctr  
!  
!  
!  
!  
!  
control-plane  
!  
!  
line con 0  
logging synchronous  
line aux 0  
line vty 0 4  
login  
!  
!  
!  
end
```

- Switch `Access3` :
```
Access3#sh running-config    
Building configuration...  
  
Current configuration : 1367 bytes  
!  
! Last configuration change at 10:38:55 UTC Thu Mar 6 2025  
!  
version 15.2  
service timestamps debug datetime msec  
service timestamps log datetime msec  
no service password-encryption  
service compress-config  
!  
hostname Access3  
!  
boot-start-marker  
boot-end-marker  
!  
!  
!  
no aaa new-model  
!  
!  
!  
!  
!            
!  
!  
!  
ip cef  
no ipv6 cef  
!  
!  
!  
spanning-tree mode pvst  
spanning-tree extend system-id  
!  
!  
!    
!  
!  
!  
!  
!  
!  
!  
!  
!  
!            
!  
!  
interface Ethernet0/0  
switchport access vlan 30  
switchport mode access  
spanning-tree bpduguard enable  
!  
interface Ethernet0/1  
spanning-tree bpduguard enable  
!  
interface Ethernet0/2  
spanning-tree bpduguard enable  
!  
interface Ethernet0/3  
spanning-tree bpduguard enable  
!  
interface Ethernet1/0  
spanning-tree bpduguard enable  
!  
interface Ethernet1/1  
spanning-tree bpduguard enable  
!  
interface Ethernet1/2  
switchport trunk allowed vlan 30  
switchport trunk encapsulation dot1q  
switchport mode trunk  
ip arp inspection trust  
!  
interface Ethernet1/3  
switchport trunk allowed vlan 30  
switchport trunk encapsulation dot1q  
switchport mode trunk  
ip arp inspection trust  
!  
ip forward-protocol nd  
!  
ip http server  
!  
ip ssh server algorithm encryption aes128-ctr aes192-ctr aes256-ctr  
ip ssh client algorithm encryption aes128-ctr aes192-ctr aes256-ctr  
!  
!  
!  
!  
!  
control-plane  
!  
!  
line con 0  
logging synchronous  
line aux 0  
line vty 0 4  
login  
!  
!  
!  
end
```

### Fichier de configuration du serveur DHCP (dhcpd)

- `/etc/dhcp/dhcpd.conf`
```
[root@localhost user]# cat /etc/dhcp/dhcpd.conf 
#
# DHCP Server Configuration file.
#   see /usr/share/doc/dhcp-server/dhcpd.conf.example
#   see dhcpd.conf(5) man page
#


subnet 10.3.10.0 netmask 255.255.255.0 {
        range                           10.3.10.10 10.3.10.200; # Plage IP
        option domain-name-servers      1.1.1.1; # DNS
        option routers                  10.3.10.254; # Passerelle
        # Bail de 24H
        default-lease-time 86400;
        # Bail maxi de 48H
        max-lease-time 172800;
}

subnet 10.3.20.0 netmask 255.255.255.0 {
        range                           10.3.20.10 10.3.20.200; # Plage IP
        option domain-name-servers	    1.1.1.1; # DNS
        option routers                  10.3.20.254; # Passerelle
        # Bail de 24H
        default-lease-time 86400;
        # Bail maxi de 48H
        max-lease-time 172800;
}

subnet 10.3.30.0 netmask 255.255.255.0 {
        range                           10.3.30.10 10.3.30.200; # Plage IP
        option domain-name-servers	    1.1.1.1; # DNS
        option routers                  10.3.30.254; # Passerelle
        # Bail de 24H
        default-lease-time 86400;
        # Bail maxi de 48H
        max-lease-time 172800;
}
```

Remarque : Pas de conf supplémentaire en utilisant l'image CentOS-8 "offciel" de eve-ng, mise à part l'ajout d'une IP

### Les pings depuis les PC 1 (VLAN 10 clients) et 2 (VLAN 20 admins)

- PC 1 :
```
VPCS> ip dhcp  
DDORA IP 10.3.10.11/24 GW 10.3.10.254  

VPCS> ping 10.3.30.251  
  
84 bytes from 10.3.30.251 icmp_seq=1 ttl=63 time=14.836 ms  
84 bytes from 10.3.30.251 icmp_seq=2 ttl=63 time=16.346 ms  
84 bytes from 10.3.30.251 icmp_seq=3 ttl=63 time=16.943 ms  
^C  
VPCS> ping ynov.com  
ynov.com resolved to 104.26.11.233  
  
84 bytes from 104.26.11.233 icmp_seq=1 ttl=52 time=29.135 ms  
84 bytes from 104.26.11.233 icmp_seq=2 ttl=52 time=25.913 ms  
84 bytes from 104.26.11.233 icmp_seq=3 ttl=52 time=26.709 ms  
^C
```

- PC 2 :
```
VPCS> ip dhcp  
DDORA IP 10.3.20.14/24 GW 10.3.20.254  

VPCS> ping 10.3.30.251  

84 bytes from 10.3.30.251 icmp_seq=1 ttl=63 time=19.192 ms  
84 bytes from 10.3.30.251 icmp_seq=2 ttl=63 time=16.598 ms  
84 bytes from 10.3.30.251 icmp_seq=3 ttl=63 time=16.242 ms  
^C  
VPCS> ping ynov.com      
ynov.com resolved to 172.67.74.226  
  
84 bytes from 172.67.74.226 icmp_seq=1 ttl=52 time=29.378 ms  
84 bytes from 172.67.74.226 icmp_seq=2 ttl=52 time=26.432 ms  
84 bytes from 172.67.74.226 icmp_seq=3 ttl=52 time=27.505 ms  
^C
```

## 7. Test et résilience

### A. Get the state

#### Etat de l'agrégation LACP

Avec la commande `show etherchannel port-channel` sur le switch `Core2` on voit bien le LAG utilisant le protocole LACP :
```
Core2#show etherchannel port-channel    
               Channel-group listing:    
               ----------------------  
  
Group: 1    
----------  
               Port-channels in the group:    
               ---------------------------  
  
Port-channel: Po1    (Primary Aggregator)  
  
------------  
  
Age of the Port-channel   = 0d:05h:13m:42s  
Logical slot/port   = 16/0          Number of ports = 2  
HotStandBy port = null    
Port state          = Port-channel Ag-Inuse    
Protocol            =   LACP  
Port security       = Disabled  
Load share deferral = Disabled      
  
Ports in the Port-channel:    
  
Index   Load   Port     EC state        No of bits  
------+------+------+------------------+-----------  
 0     00     Et1/1    Active             0  
 0     00     Et1/2    Active             0  
  
Time since last port bundled:    0d:05h:13m:36s    Et1/2
```

#### Etat de la liaison HSRP

Avec la commande `sh standby brief` sur le `Router1`, on voit bien que le HSRP est activé et que le `Router1` est utilisé pour les VLANs 10 et 20, et le `Router2` est utilisé pour le VLAN 30.
```

R1#sh standby brief    
                    P indicates configured to preempt.  
                    |  
Interface   Grp  Pri P State   Active          Standby         Virtual IP  
Fa0/0.10    100  120 P Active  local           10.3.10.253     10.3.10.254  
Fa0/0.20    101  120 P Active  local           10.3.20.253     10.3.20.254  
Fa0/0.30    102  110 P Standby 10.3.30.253     local           10.3.30.254
```

#### Etat de STP par VLANs

- Switch `Core1` :

```
Core1#sh spanning-tree vlan 10,20,30  
  
VLAN0010  
 Spanning tree enabled protocol ieee  
 Root ID    Priority    32778  
            Address     aabb.cc00.4000  
            Cost        200  
            Port        5 (Ethernet1/0)  
            Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec  
  
 Bridge ID  Priority    32778  (priority 32768 sys-id-ext 10)  
            Address     aabb.cc00.8000  
            Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec  
            Aging Time  300 sec  
  
Interface           Role Sts Cost      Prio.Nbr Type  
------------------- ---- --- --------- -------- --------------------------------  
Et0/3               Altn BLK 100       128.4    P2p    
Et1/0               Root FWD 100       128.5    P2p    
Et1/3               Desg FWD 100       128.8    P2p    
Po1                 Desg FWD 56        128.65   P2p    
  
  
VLAN0020  
 Spanning tree enabled protocol ieee  
 Root ID    Priority    32788  
            Address     aabb.cc00.3000  
            Cost        200  
            Port        5 (Ethernet1/0)  
            Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec  
  
 Bridge ID  Priority    32788  (priority 32768 sys-id-ext 20)  
            Address     aabb.cc00.8000  
            Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec  
            Aging Time  300 sec  
  
Interface           Role Sts Cost      Prio.Nbr Type  
------------------- ---- --- --------- -------- --------------------------------  
Et0/3               Altn BLK 100       128.4    P2p    
Et1/0               Root FWD 100       128.5    P2p    
Et1/3               Desg FWD 100       128.8    P2p    
Po1                 Desg FWD 56        128.65   P2p    
  
  
VLAN0030  
 Spanning tree enabled protocol ieee  
 Root ID    Priority    32798  
            Address     aabb.cc00.5000  
            Cost        200  
            Port        5 (Ethernet1/0)  
            Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec  
  
 Bridge ID  Priority    32798  (priority 32768 sys-id-ext 30)  
            Address     aabb.cc00.8000  
            Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec  
            Aging Time  300 sec  
  
Interface           Role Sts Cost      Prio.Nbr Type  
------------------- ---- --- --------- -------- --------------------------------  
Et0/3               Altn BLK 100       128.4    P2p    
Et1/0               Root FWD 100       128.5    P2p    
Et1/3               Desg FWD 100       128.8    P2p    
Po1                 Desg FWD 56        128.65   P2p
```

- Switch `Distrib1` :

```
Distrib1#sh spanning-tree vlan 10,20,30  
  
VLAN0010  
 Spanning tree enabled protocol ieee  
 Root ID    Priority    32778  
            Address     aabb.cc00.4000  
            Cost        100  
            Port        6 (Ethernet1/1)  
            Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec  
  
 Bridge ID  Priority    32778  (priority 32768 sys-id-ext 10)  
            Address     aabb.cc00.6000  
            Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec  
            Aging Time  300 sec  
  
Interface           Role Sts Cost      Prio.Nbr Type  
------------------- ---- --- --------- -------- --------------------------------  
Et1/1               Root FWD 100       128.6    P2p    
Et1/2               Desg FWD 100       128.7    P2p    
Et1/3               Desg FWD 100       128.8    P2p    
  
  
VLAN0020  
 Spanning tree enabled protocol ieee  
 Root ID    Priority    32788  
            Address     aabb.cc00.3000  
            Cost        100  
            Port        5 (Ethernet1/0)  
            Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec  
  
 Bridge ID  Priority    32788  (priority 32768 sys-id-ext 20)  
            Address     aabb.cc00.6000  
            Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec  
            Aging Time  300 sec  
  
Interface           Role Sts Cost      Prio.Nbr Type  
------------------- ---- --- --------- -------- --------------------------------  
Et1/0               Root FWD 100       128.5    P2p    
Et1/1               Desg FWD 100       128.6    P2p    
Et1/2               Desg FWD 100       128.7    P2p    
Et1/3               Desg FWD 100       128.8    P2p    
  
  
VLAN0030  
 Spanning tree enabled protocol ieee  
 Root ID    Priority    32798  
            Address     aabb.cc00.5000  
            Cost        100  
            Port        4 (Ethernet0/3)  
            Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec  
  
 Bridge ID  Priority    32798  (priority 32768 sys-id-ext 30)  
            Address     aabb.cc00.6000  
            Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec  
            Aging Time  300 sec  
  
Interface           Role Sts Cost      Prio.Nbr Type  
------------------- ---- --- --------- -------- --------------------------------  
Et0/3               Root FWD 100       128.4    P2p    
Et1/2               Desg FWD 100       128.7    P2p    
Et1/3               Desg FWD 100       128.8    P2p
```

- Switch `Access1` (il n'y a que 2 VLANs car il n'y a que le VLAN 10 et 20 qui passe à travers `Access1`)

```
Access1#show spanning-tree vlan 10,20,30  
  
VLAN0010  
 Spanning tree enabled protocol ieee  
 Root ID    Priority    32778  
            Address     aabb.cc00.4000  
            This bridge is the root  
            Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec  
  
 Bridge ID  Priority    32778  (priority 32768 sys-id-ext 10)  
            Address     aabb.cc00.4000  
            Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec  
            Aging Time  300 sec  
  
Interface           Role Sts Cost      Prio.Nbr Type  
------------------- ---- --- --------- -------- --------------------------------  
Et0/0               Desg FWD 100       128.1    P2p    
Et1/2               Desg FWD 100       128.7    P2p    
Et1/3               Desg FWD 100       128.8    P2p    
  
  
VLAN0020  
 Spanning tree enabled protocol ieee  
 Root ID    Priority    32788  
            Address     aabb.cc00.3000  
            Cost        200  
            Port        8 (Ethernet1/3)  
            Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec  
  
 Bridge ID  Priority    32788  (priority 32768 sys-id-ext 20)  
            Address     aabb.cc00.4000  
            Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec  
            Aging Time  300 sec  
  
Interface           Role Sts Cost      Prio.Nbr Type  
------------------- ---- --- --------- -------- --------------------------------  
Et0/1               Desg FWD 100       128.2    P2p    
Et1/2               Altn BLK 100       128.7    P2p    
Et1/3               Root FWD 100       128.8    P2p
```

Remarque : On observe avec le dernier rendu que le switch `Access1` est le switch root pour le VLAN 10 (car dans les chemins possible, aucun de mène à `root`, c'est donc que c'est lui même le switch `root`)

### B. HSRP tests

#### Couper le router prioritaire (je l'éteint D: )

- Dans le CLI du VPC :
```
VPCS> ping 1.1.1.1 -c 200  
  
84 bytes from 1.1.1.1 icmp_seq=1 ttl=52 time=31.691 ms  
84 bytes from 1.1.1.1 icmp_seq=2 ttl=52 time=37.365 ms  
84 bytes from 1.1.1.1 icmp_seq=3 ttl=52 time=25.848 ms  
84 bytes from 1.1.1.1 icmp_seq=4 ttl=52 time=26.413 ms  
84 bytes from 1.1.1.1 icmp_seq=5 ttl=52 time=26.340 ms  
1.1.1.1 icmp_seq=6 timeout  
1.1.1.1 icmp_seq=7 timeout  
1.1.1.1 icmp_seq=8 timeout  
1.1.1.1 icmp_seq=9 timeout  
1.1.1.1 icmp_seq=10 timeout  
84 bytes from 1.1.1.1 icmp_seq=11 ttl=52 time=28.679 ms  
84 bytes from 1.1.1.1 icmp_seq=12 ttl=52 time=25.768 ms  
84 bytes from 1.1.1.1 icmp_seq=13 ttl=52 time=27.747 ms  
84 bytes from 1.1.1.1 icmp_seq=14 ttl=52 time=27.763 ms  
84 bytes from 1.1.1.1 icmp_seq=15 ttl=52 time=29.299 ms  
84 bytes from 1.1.1.1 icmp_seq=16 ttl=52 time=27.280 ms  
84 bytes from 1.1.1.1 icmp_seq=17 ttl=52 time=79.055 ms
^C
```

- Le [pcap](./pcaps/ping_hsrp.pcap), on voit très bien l'évolution du traffic HSRP et de l'envoie des requêtes `ARP Gratuitous` du `Router2` qui passe de Standby à Active


#### STP tests

- On choisi de couper le switch `Distrib1`, car il ne possède que des ports en mode `root` ou `Desg` et que le switch `Access1` est le switch root du VLAN10. On va donc faire écouter wireshark sur le 2ème trunk de `Access1` pour voir toutes les requêtes que le switch fera.
On pingera depuis `PC 2`, car vu qu'il appartient au VLAN 20, on devrait pouvoir observer la coupure

```
Access1#sh spanning-tree vlan 10,20,30  
  
VLAN0010  
 Spanning tree enabled protocol ieee  
 Root ID    Priority    32778  
            Address     aabb.cc00.4000  
            This bridge is the root  
            Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec  
  
 Bridge ID  Priority    32778  (priority 32768 sys-id-ext 10)  
            Address     aabb.cc00.4000  
            Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec  
            Aging Time  300 sec  
  
Interface           Role Sts Cost      Prio.Nbr Type  
------------------- ---- --- --------- -------- --------------------------------  
Et0/0               Desg FWD 100       128.1    P2p    
Et1/2               Desg FWD 100       128.7    P2p    
Et1/3               Desg FWD 100       128.8    P2p    
  
  
VLAN0020  
 Spanning tree enabled protocol ieee  
 Root ID    Priority    32788  
            Address     aabb.cc00.3000  
            Cost        200  
            Port        8 (Ethernet1/3)  
            Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec  
  
 Bridge ID  Priority    32788  (priority 32768 sys-id-ext 20)  
            Address     aabb.cc00.4000  
            Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec  
            Aging Time  300 sec  
  
Interface           Role Sts Cost      Prio.Nbr Type  
------------------- ---- --- --------- -------- --------------------------------  
Et0/1               Desg FWD 100       128.2    P2p    
Et1/2               Altn BLK 100       128.7    P2p    
Et1/3               Root FWD 100       128.8    P2p
```

- Les pings depuis `PC 2`
```
VPCS> ping 1.1.1.1 -c 200  
  
84 bytes from 1.1.1.1 icmp_seq=1 ttl=52 time=29.565 ms  
84 bytes from 1.1.1.1 icmp_seq=2 ttl=52 time=26.430 ms  
84 bytes from 1.1.1.1 icmp_seq=3 ttl=52 time=28.042 ms  
84 bytes from 1.1.1.1 icmp_seq=4 ttl=52 time=26.819 ms  
84 bytes from 1.1.1.1 icmp_seq=5 ttl=52 time=28.182 ms  
84 bytes from 1.1.1.1 icmp_seq=6 ttl=52 time=29.416 ms  
84 bytes from 1.1.1.1 icmp_seq=7 ttl=52 time=26.311 ms  
84 bytes from 1.1.1.1 icmp_seq=8 ttl=52 time=26.418 ms  
84 bytes from 1.1.1.1 icmp_seq=9 ttl=52 time=30.915 ms  
84 bytes from 1.1.1.1 icmp_seq=10 ttl=52 time=23.579 ms  
84 bytes from 1.1.1.1 icmp_seq=11 ttl=52 time=26.052 ms  
84 bytes from 1.1.1.1 icmp_seq=12 ttl=52 time=25.809 ms  
84 bytes from 1.1.1.1 icmp_seq=13 ttl=52 time=25.627 ms  
84 bytes from 1.1.1.1 icmp_seq=14 ttl=52 time=25.534 ms  
84 bytes from 1.1.1.1 icmp_seq=15 ttl=52 time=26.832 ms  
84 bytes from 1.1.1.1 icmp_seq=16 ttl=52 time=27.126 ms  
84 bytes from 1.1.1.1 icmp_seq=17 ttl=52 time=26.085 ms  
84 bytes from 1.1.1.1 icmp_seq=18 ttl=52 time=26.101 ms  
84 bytes from 1.1.1.1 icmp_seq=19 ttl=52 time=26.057 ms  
84 bytes from 1.1.1.1 icmp_seq=20 ttl=52 time=26.253 ms  
84 bytes from 1.1.1.1 icmp_seq=21 ttl=52 time=26.594 ms  
84 bytes from 1.1.1.1 icmp_seq=22 ttl=52 time=26.987 ms  
84 bytes from 1.1.1.1 icmp_seq=23 ttl=52 time=25.631 ms  
84 bytes from 1.1.1.1 icmp_seq=24 ttl=52 time=26.403 ms  
84 bytes from 1.1.1.1 icmp_seq=25 ttl=52 time=29.932 ms  
84 bytes from 1.1.1.1 icmp_seq=26 ttl=52 time=30.737 ms  
1.1.1.1 icmp_seq=27 timeout  
1.1.1.1 icmp_seq=28 timeout  
1.1.1.1 icmp_seq=29 timeout  
1.1.1.1 icmp_seq=30 timeout  
1.1.1.1 icmp_seq=31 timeout  
1.1.1.1 icmp_seq=32 timeout  
1.1.1.1 icmp_seq=33 timeout  
1.1.1.1 icmp_seq=34 timeout  
1.1.1.1 icmp_seq=35 timeout  
1.1.1.1 icmp_seq=36 timeout  
1.1.1.1 icmp_seq=37 timeout  
1.1.1.1 icmp_seq=38 timeout  
1.1.1.1 icmp_seq=39 timeout  
1.1.1.1 icmp_seq=40 timeout  
1.1.1.1 icmp_seq=41 timeout  
1.1.1.1 icmp_seq=42 timeout  
1.1.1.1 icmp_seq=43 timeout  
1.1.1.1 icmp_seq=44 timeout  
1.1.1.1 icmp_seq=45 timeout  
1.1.1.1 icmp_seq=46 timeout  
1.1.1.1 icmp_seq=47 timeout  
1.1.1.1 icmp_seq=48 timeout  
1.1.1.1 icmp_seq=49 timeout  
1.1.1.1 icmp_seq=50 timeout  
84 bytes from 1.1.1.1 icmp_seq=51 ttl=52 time=31.211 ms  
84 bytes from 1.1.1.1 icmp_seq=52 ttl=52 time=28.422 ms  
84 bytes from 1.1.1.1 icmp_seq=53 ttl=52 time=47.988 ms  
84 bytes from 1.1.1.1 icmp_seq=54 ttl=52 time=27.683 ms  
84 bytes from 1.1.1.1 icmp_seq=55 ttl=52 time=27.502 ms  
84 bytes from 1.1.1.1 icmp_seq=56 ttl=52 time=28.974 ms  
84 bytes from 1.1.1.1 icmp_seq=57 ttl=52 time=27.393 ms  
84 bytes from 1.1.1.1 icmp_seq=58 ttl=52 time=27.443 ms  
84 bytes from 1.1.1.1 icmp_seq=59 ttl=52 time=27.741 ms  
84 bytes from 1.1.1.1 icmp_seq=60 ttl=52 time=27.394 ms  
84 bytes from 1.1.1.1 icmp_seq=61 ttl=52 time=29.762 ms  
84 bytes from 1.1.1.1 icmp_seq=62 ttl=52 time=28.626 ms
```

- le [pcap](./pcaps/stp.pcap), des pings qui apparaissent après la première trame indiquant que la Topologie à changer (trust me, ils n'apparaissaient pas avant)