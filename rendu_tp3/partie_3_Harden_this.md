# Partie III : Harden this

## A. STP Protections

- BPDUGuard
```
(if-config)spanning-tree bpduguard enable
```

- BPDU filter => pour ne plus que le switch spam des requête STP alors qu'il n'est pas sensé avoir de switch derière un access port
```
(if-config)spanning-tree bpdufilter enable
```

- Portfast
```
(if-config)spanning-tree portfast
```

## B. DHCP Protection

- Activer le dhcp Snooping dans le switch
```
(conf t) ip dhcp snooping
(conf t) ip dhcp snooping vlan 10,20,30
```

- Maintenant il faut "truster" l'interface sur laquel le serveur DHCP est branché
```
(config-if) ip dhcp snooping trust 
```

## C. ARP Protections

- Mise en place du DAI
```
(conf t) ip arp inspection vlan 10,20,30
```

# 2. Protection L3

## A. ACL

- Permettre de communiquer avec le serveur DHCP depuis n'importe ou
```
access-list 100 permit ip any host 10.3.30.251
```

- Empêcher la communication avec n'importe qui du réseau 10.3.30.0/24
```  
access-list 100 deny   ip any 10.3.30.0 0.0.0.255
```

- Application des règles
```
interface fa0/0.30
  ip access-group 100 out
```
=> Seul l'IP `10.3.30.251` peut être joignable depuis les autres VLANs (et aussi les IP des sous-interfaces du router, ce qui nous emmène au bonus)

**Bonus**
- Les règles :
(Cas pour la sous-interface VLAN 10, 10.3.10.0/24)
```
access-list 101 permit ip 10.3.30.0 0.0.0.255 any  
access-list 101 deny   ip any host 10.3.10.252
```

- Application :
```
interface fa0/0.10
  ip access-group 101 in
```