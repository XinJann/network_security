# Partie II. Security

## 1. ACL

La règle access-list à mettre sur les sous-interfaces des VLANs 10 et 20 :
```
access-list 100 deny ip any 10.2.30.0 0.0.0.255
access-list 100 permit ip any any
```

**Bonus** : On bloque l'envoie de réponse ICMP de type "administrative" => `(ICMP type:3, code:13, Communication administratively prohibited)`  
Via la commande executée dans les sous-interfaces:
```
no ip unreachables
```

## 2. DAI

- Switch `Access1` :
```
arp access-list ARP-VLAN10
permit ip host 10.2.10.1 mac host 00:50:79:66:68:04
exit
ip arp inspection filter ARP-VLAN10 vlan 10 static
arp access-list ARP-VLAN20
permit ip host 10.2.20.1 mac host 00:50:79:66:68:05
exit
ip arp inspection filter ARP-VLAN20 vlan 20 static
ip arp inspection vlan 10,20

# Puis on trust le port vers le switch Core avec la commande suviante :
(conf-if)ip arp inspection trust
```

- Switch `Access2` :
```
arp access-list ARP-VLAN10
permit ip host 10.2.10.2 mac host 00:50:79:66:68:03
exit
ip arp inspection filter ARP-VLAN10 vlan 10 static
arp access-list ARP-VLAN20
permit ip host 10.2.20.2 mac host 00:50:79:66:68:06
exit
ip arp inspection filter ARP-VLAN20 vlan 20 static
arp access-list ARP-VLAN30
permit ip host 10.2.30.1 mac host 00:50:79:66:68:07
exit
ip arp inspection filter ARP-VLAN30 vlan 30 static
ip arp inspection vlan 10,20,30

# Puis on trust les ports vers le switch Core avec la commande suivante :
(conf-if)ip arp inspection trust
```

Besoin de faire sur le Switch `Core` ?
- Switch `Core`
```
ip arp inspection vlan 10,20,30

# Puis on trust les ports vers les autres Switch et router (=> les interfaces "trunk")
(conf-if)ip arp inspection trust
```

## 3. BPDUGuard

Sur TOUS les ports sauf ceux menant vers un autre Switch on execute la commande :
```
spanning-tree bpduguard enable
```

## 4. Rendus de Configuration (`show running-config`)

- Router `R1`

```
R1#sh running-config    
Building configuration...  
  
Current configuration : 1412 bytes  
!  
! Last configuration change at 08:55:06 UTC Tue Mar 4 2025  
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
ip address 10.2.10.254 255.255.255.0  
ip access-group 100 in  
no ip unreachables  
ip nat inside  
!  
interface FastEthernet0/0.20  
encapsulation dot1Q 20  
ip address 10.2.20.254 255.255.255.0  
ip access-group 100 in  
no ip unreachables  
ip nat inside  
!  
interface FastEthernet0/0.30  
encapsulation dot1Q 30  
ip address 10.2.30.254 255.255.255.0  
ip nat inside  
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
interface FastEthernet3/0  
no ip address  
shutdown  
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
access-list 100 deny   ip any 10.2.30.0 0.0.0.255  
access-list 100 permit ip any any  
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

- Switch `Core`

```
core#sh running-config    
Building configuration...  
  
Current configuration : 1480 bytes  
!  
! Last configuration change at 10:06:28 UTC Tue Mar 4 2025  
!  
version 15.2  
service timestamps debug datetime msec  
service timestamps log datetime msec  
no service password-encryption  
service compress-config  
!  
hostname core  
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
ip arp inspection vlan 10,20,30  
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
spanning-tree bpduguard enable  
!  
interface Ethernet1/0  
spanning-tree bpduguard enable  
!  
interface Ethernet1/1  
switchport trunk allowed vlan 10,20,30  
switchport trunk encapsulation dot1q  
switchport mode trunk  
ip arp inspection trust  
!  
interface Ethernet1/2  
switchport trunk allowed vlan 10,20  
switchport trunk encapsulation dot1q  
switchport mode trunk  
ip arp inspection trust  
!  
interface Ethernet1/3  
switchport trunk allowed vlan 10,20,30  
switchport trunk encapsulation dot1q  
switchport mode trunk  
ip arp inspection trust  
spanning-tree bpduguard enable  
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

- Switch `Access1`

```

access1#sh running-config    
Building configuration...  
  
Current configuration : 1624 bytes  
!  
! Last configuration change at 09:58:03 UTC Tue Mar 4 2025  
!  
version 15.2  
service timestamps debug datetime msec  
service timestamps log datetime msec  
no service password-encryption  
service compress-config  
!  
hostname access1  
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
ip arp inspection vlan 10,20  
ip arp inspection filter ARP-VLAN10 vlan  10 static  
ip arp inspection filter ARP-VLAN20 vlan  20 static  
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
spanning-tree bpduguard enable  
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
arp access-list ARP-VLAN10  
permit ip host 10.2.10.1 mac host 0050.7966.6804    
arp access-list ARP-VLAN20  
permit ip host 10.2.20.1 mac host 0050.7966.6805    
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

- Switch `Access2`

```
access2#sh running-config    
Building configuration...  
  
Current configuration : 1811 bytes  
!  
! Last configuration change at 09:58:55 UTC Tue Mar 4 2025  
!  
version 15.2  
service timestamps debug datetime msec  
service timestamps log datetime msec  
no service password-encryption  
service compress-config  
!  
hostname access2  
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
ip arp inspection vlan 10,20,30  
ip arp inspection filter ARP-VLAN10 vlan  10 static  
ip arp inspection filter ARP-VLAN20 vlan  20 static  
ip arp inspection filter ARP-VLAN30 vlan  30 static  
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
switchport access vlan 30  
switchport mode access  
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
spanning-tree bpduguard enable  
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
arp access-list ARP-VLAN10  
permit ip host 10.2.10.2 mac host 0050.7966.6803    
arp access-list ARP-VLAN20  
permit ip host 10.2.20.2 mac host 0050.7966.6806    
arp access-list ARP-VLAN30  
permit ip host 10.2.30.1 mac host 0050.7966.6807    
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
