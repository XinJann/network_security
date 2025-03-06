# Partie I : Setup Lab

## sh running-config de tous les équipements ....

- Router "R1"
```
R1#sh ru  
R1#sh running-config    
Building configuration...  
  
Current configuration : 1240 bytes  
!  
! Last configuration change at 14:55:44 UTC Mon Mar 3 2025  
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
ip nat inside  
!  
interface FastEthernet0/0.20  
encapsulation dot1Q 20  
ip address 10.2.20.254 255.255.255.0  
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

- Switch "Access1"

```
access1#sh running-config    
Building configuration...  
  
Current configuration : 1084 bytes  
!  
! Last configuration change at 13:28:31 UTC Mon Mar 3 2025  
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
!  
interface Ethernet0/1  
switchport access vlan 20  
switchport mode access  
!  
interface Ethernet0/2  
!  
interface Ethernet0/3  
!  
interface Ethernet1/0  
!  
interface Ethernet1/1  
!  
interface Ethernet1/2  
!  
interface Ethernet1/3  
switchport trunk allowed vlan 10,20  
switchport trunk encapsulation dot1q  
switchport mode trunk  
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

- Switch "Access2"

```
access2#sh running-config    
Building configuration...  
  
Current configuration : 1137 bytes  
!  
! Last configuration change at 13:29:41 UTC Mon Mar 3 2025  
!  
version 15.2  
service timestamps debug datetime msec  
service timestamps log datetime msec  
no service password-encryption  
service compress-config  
!  
hostname Switch  
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
!  
interface Ethernet0/1  
switchport access vlan 20  
switchport mode access  
!  
interface Ethernet0/2  
switchport access vlan 30  
switchport mode access  
!  
interface Ethernet0/3  
!  
interface Ethernet1/0  
!  
interface Ethernet1/1  
!  
interface Ethernet1/2  
!  
interface Ethernet1/3  
switchport trunk allowed vlan 10,20,30  
switchport trunk encapsulation dot1q  
switchport mode trunk  
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

- Switch "Core"

```
core#sh running-config    
Building configuration...  
  
Current configuration : 1181 bytes  
!  
! Last configuration change at 13:32:12 UTC Mon Mar 3 2025  
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
!  
interface Ethernet0/1  
!  
interface Ethernet0/2  
!  
interface Ethernet0/3  
!  
interface Ethernet1/0  
!  
interface Ethernet1/1  
switchport trunk allowed vlan 10,20,30  
switchport trunk encapsulation dot1q  
switchport mode trunk  
!  
interface Ethernet1/2  
switchport trunk allowed vlan 10,20  
switchport trunk encapsulation dot1q  
switchport mode trunk  
!  
interface Ethernet1/3  
switchport trunk allowed vlan 10,20,30  
switchport trunk encapsulation dot1q  
switchport mode trunk  
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

## [Pcap du ping entre `vpcs1` et `vpcs5`](./pcaps/ping1.pcap)

## [Pcap du ping entre `vpcs1` et `1.1.1.1`](./pcaps/ping2.pcap)


[Partie 2 : Sécurité](./partie_2_security.md)
