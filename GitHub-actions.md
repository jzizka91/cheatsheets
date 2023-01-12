### Changed-Files

Changed-Files action allows conditional execution of workflow steps and jobs, based on the modified files.

You can run slow tasks like integration tests or deployments only for changed components. It saves time and resources, especially in monorepo setups.

GitHub workflows built-in path filters don't work on a level of individual jobs or steps.

#### Example:

The example below demonstrates how changed-files action can be used on the workflow jobs level.

The workflow below will run on successful completion of dnsmasq-deploy workflow. The workflow will first run changes-detection job which will detect changes to files inside the {{ env.SERVICES_OFFICE_PRAGUE_DIR }} and {{ env.CONFIGS_DIR }} directories.  If any files have changed since the last commit (changes-detection.outputs.healthchecks returned true), the next job deploy-healthchecks will be executed.

```
name: deploy-office-prague

on:
  workflow_run:
    workflows:
      - dnsmasq-deploy
    branches:
      - main
    types:
      - completed
env:
  SERVICES_OFFICE_PRAGUE_DIR: "clusters/office-prague"
  CONFIGS_DIR: "config"

jobs:
  changes-detection:
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    runs-on: ubuntu-20.04
    outputs:
      healthchecks: ${{ steps.healthchecks.outputs.any_changed }}
    steps:
      - uses: actions/checkout@v3
      - name: get-changed-files-healthchecks
        uses: tj-actions/changed-files@v33
        id: healthchecks
        with:
          files: |
             {{ env.SERVICES_OFFICE_PRAGUE_DIR }}/**
             {{ env.CONFIGS_DIR }}: "config"/**

  deploy-healthchecks:
    needs: changes-detection
    if: ${{ needs.changes-detection.outputs.healthchecks == 'true' }}
    runs-on: ubuntu-20.04
    steps:
      - run: echo "run something..."
```

#### Alternative: paths-filter

Be aware of paths-filter workflow_run limitation: If action runs in workflow which runs upon completion of workflow_run, the action always returns true, even though no files were changed!





/interface bridge
add fast-forward=no name=bridge1 protocol-mode=none
/interface ethernet
set [ find default-name=ether1 ] comment=WAN-SpojeNet speed=100Mbps
set [ find default-name=ether2 ] comment=switch speed=100Mbps
set [ find default-name=ether3 ] comment=NC speed=100Mbps
set [ find default-name=ether4 ] speed=100Mbps
set [ find default-name=ether5 ] comment="Calculon main" speed=100Mbps
set [ find default-name=ether6 ] comment="Bucanero secondary" speed=100Mbps
set [ find default-name=ether7 ] comment="Bucanero main + management" speed=100Mbps
set [ find default-name=ether8 ] comment="Calculon management" speed=100Mbps
set [ find default-name=ether9 ] comment=Barcelo speed=100Mbps
set [ find default-name=ether10 ] comment=NC speed=100Mbps
set [ find default-name=ether11 ] comment=WAN-Vodafone disabled=yes speed=100Mbps
set [ find default-name=ether12 ] comment=NC disabled=yes speed=100Mbps
/interface wireguard
add listen-port=13231 mtu=1420 name=vpn-dtml-core
/interface vlan
add comment="KD PROPOSE VLAN" disabled=yes interface=bridge1 name=vlan1031-core-untagged vlan-id=1
add comment="KD PROPOSE VLAN" interface=bridge1 name=vlan1032-guests vlan-id=1032
add comment="KD PROPOSE VLAN" interface=bridge1 name=vlan1033-iot vlan-id=1033
add comment="KD PROPOSE VLAN" interface=bridge1 name=vlan1100-staff vlan-id=1100
/interface list
add name=WAN
add exclude=dynamic name=discover
add name=mactel
add name=LAN
/interface lte apn
set [ find default=yes ] ip-type=ipv4 use-network-apn=no
/interface wireless security-profiles
set [ find default=yes ] supplicant-identity="Datamole CCR1016"
/ip ipsec proposal
set [ find default=yes ] disabled=yes
add auth-algorithms=sha256,sha1 disabled=yes enc-algorithms=aes-256-cbc,aes-128-cbc lifetime=1h name=ipsec-vpn-00433ad193a3ae0ed-0
/ip pool
add name=dhcp ranges=10.7.31.85-10.7.31.254
add comment="KD PROPOSE VLAN" name=pool-vlan1100-staff ranges=10.7.100.5-10.7.103.250
add comment="KD PROPOSE VLAN" name=pool-vlan1033-iot ranges=10.7.33.5-10.7.33.250
add comment="KD PROPOSE VLAN" name=pool-vlan1032-guests ranges=10.7.32.5-10.7.32.250
add comment="KD PROPOSE VLAN" name=pool-vlan1031-core-untagged ranges=10.7.31.100-10.7.31.199
/ip dhcp-server
add address-pool=dhcp bootp-support=none interface=bridge1 name=dhcp1
add address-pool=pool-vlan1031-core-untagged comment="KD PROPOSE" disabled=yes interface=vlan1031-core-untagged name=dhcp-vlan1031-core-untagged
add address-pool=pool-vlan1032-guests comment="KD PROPOSE" interface=vlan1032-guests name=dhcp-vlan1032-guests
add address-pool=pool-vlan1033-iot comment="KD PROPOSE" interface=vlan1033-iot name=dhcp-vlan1033-iot
add address-pool=pool-vlan1100-staff comment="KD PROPOSE" interface=vlan1100-staff name=dhcp-vlan1100-staff
/port
set 0 name=serial0
set 1 name=serial1
/ppp profile
set *0 local-address=10.7.32.1 remote-address=pool-vlan1100-staff
/queue type
add kind=pcq name=pcq-down pcq-classifier=dst-address pcq-rate=350M
add kind=pcq name=pcq-up pcq-classifier=src-address pcq-rate=350M
/queue simple
add name=queue1 queue=pcq-up/pcq-down target=10.7.31.0/24
/routing bgp template
set default disabled=no output.network=bgp-networks
/routing table
add fib name=""
add fib name=karel
/snmp community
set [ find default=yes ] addresses=0.0.0.0/0
/system logging action
set 0 memory-lines=10000
set 1 disk-file-count=3 disk-lines-per-file=65000
add memory-lines=10000 name=wireless target=memory
add memory-lines=10000 name=firewall target=memory
add memory-lines=10000 name=dhcp target=memory
/caps-man manager
set ca-certificate=auto certificate=auto enabled=yes
/interface bridge port
add bridge=bridge1 hw=no ingress-filtering=no interface=ether2
add bridge=bridge1 hw=no ingress-filtering=no interface=ether3
add bridge=bridge1 hw=no ingress-filtering=no interface=ether4
add bridge=bridge1 hw=no ingress-filtering=no interface=ether5
add bridge=bridge1 hw=no ingress-filtering=no interface=ether6
add bridge=bridge1 hw=no ingress-filtering=no interface=ether7
add bridge=bridge1 hw=no ingress-filtering=no interface=ether8
add bridge=bridge1 hw=no ingress-filtering=no interface=ether9
add bridge=bridge1 hw=no ingress-filtering=no interface=ether10
/ip neighbor discovery-settings
set discover-interface-list=discover
/ip settings
set max-neighbor-entries=8192 tcp-syncookies=yes
/ipv6 settings
set disable-ipv6=yes max-neighbor-entries=8192
/interface l2tp-server server
set authentication=mschap2 default-profile=default enabled=yes use-ipsec=yes
/interface list member
add interface=ether1 list=WAN
add interface=ether12 list=WAN
add interface=ether2 list=discover
add interface=ether3 list=discover
add interface=ether4 list=discover
add interface=ether5 list=discover
add interface=ether6 list=discover
add interface=ether7 list=discover
add interface=ether8 list=discover
add interface=ether9 list=discover
add interface=ether10 list=discover
add interface=bridge1 list=discover
add interface=bridge1 list=mactel
add interface=ether11 list=discover
/interface ovpn-server server
set auth=sha1,md5
/interface wireguard peers
add allowed-address=10.255.69.9/32,10.9.0.0/16 comment="Router in Brno Offices" endpoint-address=77.240.187.142 endpoint-port=13231 interface=vpn-dtml-core persistent-keepalive=25s public-key="nHwLRSCBtgZ/iAADsE9gcHpRqhPRZAdIimm8ehGzXSM="
add allowed-address=10.255.69.8/32,10.8.0.0/16 comment="Router in Krumlov Office" interface=vpn-dtml-core persistent-keepalive=25s public-key="i42JUpz25TsaFkGZmVmDLM30lgbqdndgMydpSFv4BGQ="
add allowed-address=10.255.69.88/32,192.168.88.0/24,192.168.23.0/24,192.168.30.0/24 comment=KD-TEST interface=vpn-dtml-core persistent-keepalive=25s public-key="q//d/IKYWIPq/kZco8GAruqazXTi9G2eU4d0Jqe0Xjs="
/ip address
add address=10.7.31.1/24 interface=ether2 network=10.7.31.0
add address=192.168.100.5/24 comment="UPC modem management network (modem IP is 192.168.100.1)." disabled=yes interface=ether12 network=192.168.100.0
add address=77.87.240.41 interface=ether1 network=77.87.240.40
add address=10.255.69.7/24 interface=vpn-dtml-core network=10.255.69.0
add address=10.7.32.1/24 comment="KD PROPOSE VLAN vlan1032-guests" interface=vlan1032-guests network=10.7.32.0
add address=10.7.31.1/24 comment="KD PROPOSE VLAN vlan1031-core-utagged" disabled=yes interface=vlan1031-core-untagged network=10.7.31.0
add address=10.7.100.1/22 comment="KD PROPOSE vlan1100-staff" interface=vlan1100-staff network=10.7.100.0
add address=10.7.33.1/24 comment="KD PROPOSE vlan1033-iot" interface=vlan1033-iot network=10.7.33.0
/ip cloud
set ddns-enabled=yes
/ip dhcp-client
add add-default-route=no disabled=yes interface=ether1 use-peer-dns=no
add default-route-distance=2 interface=ether12 use-peer-dns=no
add default-route-distance=2 interface=ether11 use-peer-dns=no
/ip dhcp-server alert
add disabled=no interface=bridge1
add disabled=no interface=*20
/ip dhcp-server lease
add address=10.7.31.2 client-id=1:6c:3b:6b:6b:e:95 comment="Main Switch" mac-address=6C:3B:6B:6B:0E:95 server=dhcp1
add address=10.7.31.80 always-broadcast=yes client-id=1:c8:d3:ff:13:d0:4e comment="HP printer" mac-address=C8:D3:FF:13:D0:4E server=dhcp1
add address=10.7.31.31 always-broadcast=yes client-id=1:14:2:ec:62:35:bd comment="Office server management" mac-address=14:02:EC:62:35:BD server=dhcp1
add address=10.7.31.30 comment="Office server" mac-address=14:02:EC:62:35:BF server=dhcp1
add address=10.7.31.81 comment="Xerox printer" mac-address=9C:93:4E:6C:5C:FE server=dhcp1
add address=10.7.31.33 client-id=1:c:c4:7a:71:a7:7c comment="Calculon server management" mac-address=0C:C4:7A:71:A7:7C server=dhcp1
add address=10.7.31.60 client-id=1:f0:9f:c2:7f:db:35 comment="Camera NVR 5th floor" mac-address=F0:9F:C2:7F:DB:35 server=dhcp1
add address=10.7.31.3 client-id=1:cc:2d:e0:8d:aa:4c mac-address=CC:2D:E0:8D:AA:4C server=dhcp1
add address=10.7.31.13 client-id=1:68:D7:9A:65:C2:C5 comment="AP13 UniFi" mac-address=68:D7:9A:65:C2:C5 server=dhcp1
add address=10.7.31.14 client-id=1:24:5A:4C:95:3C:B4 comment="AP14 UniFi" mac-address=24:5A:4C:95:3C:B4 server=dhcp1
add address=10.7.31.15 client-id=1:fc:ec:da:4c:d8:69 comment="AP15 UniFi" mac-address=FC:EC:DA:4C:D8:69 server=dhcp1
add address=10.7.31.16 client-id=1:fc:ec:da:4b:fa:3f comment="AP16 UniFi" mac-address=FC:EC:DA:4B:FA:3F server=dhcp1
add address=10.7.31.71 comment="HoneyWell 5th floor" mac-address=B8:2C:A0:2B:CE:F1 server=dhcp1
add address=10.7.31.17 client-id=1:b4:fb:e4:2d:1d:9e comment="AP17 UniFi" mac-address=B4:FB:E4:2D:1D:9E server=dhcp1
add address=10.7.31.18 client-id=1:b4:fb:e4:2d:1e:4a comment="AP18 UniFi" mac-address=B4:FB:E4:2D:1E:4A server=dhcp1
add address=10.7.31.72 comment="HoneyWell 6th (R) floor" mac-address=B8:2C:A0:2B:CF:58 server=dhcp1
add address=10.7.31.73 comment="HoneyWell 6th (L) floor" mac-address=B8:2C:A0:2B:D1:2D server=dhcp1
add address=10.7.31.175 comment="Deep-Learning workstation" mac-address=04:92:26:C2:AA:B4 server=dhcp1
add address=10.7.31.61 client-id=1:fc:ec:da:30:f2:d3 comment="Camera NVR 6L" mac-address=FC:EC:DA:30:F2:D3 server=dhcp1
add address=10.7.31.62 client-id=1:fc:ec:da:30:5d:99 comment="Camera NVR 6R" mac-address=FC:EC:DA:30:5D:99 server=dhcp1
add address=10.7.31.11 client-id=1:18:e8:29:b7:15:57 comment="AP11 UniFi" mac-address=18:E8:29:B7:15:57 server=dhcp1
add address=10.7.31.12 client-id=1:18:e8:29:bf:30:da comment="AP12 UniFi" mac-address=18:E8:29:BF:30:DA server=dhcp1
add address=10.7.31.4 mac-address=74:4D:28:29:66:19 server=dhcp1
add address=10.7.31.247 mac-address=00:1E:06:30:72:1E server=dhcp1
add address=10.7.31.193 client-id=ff:f8:3:89:63:0:2:0:0:ab:11:a0:95:8d:4f:aa:1e:25:64 mac-address=D4:3B:04:78:21:11 server=dhcp1
add address=10.7.31.32 client-id=ff:af:ca:18:21:0:2:0:0:ab:11:f0:28:90:9d:f7:ca:8:4e comment="Calculon server" mac-address=16:21:C3:4E:F3:BF server=dhcp1
add address=10.7.31.51 client-id=ff:b5:5e:67:ff:0:2:0:0:ab:11:67:b:cf:48:14:3a:4e:8d comment="Microk8s1 on calculon" mac-address=52:54:00:3E:A3:21 server=dhcp1
add address=10.7.31.52 client-id=1:52:54:95:9f:f6:5f comment="mssql vm on calculon" mac-address=52:54:95:9F:F6:5F server=dhcp1
add address=10.7.31.63 client-id=1:fc:ec:da:d9:46:93 comment="Camera NVR 5th floor R " mac-address=FC:EC:DA:D9:46:93 server=dhcp1
add address=10.7.31.252 client-id=ff:56:50:4d:98:0:2:0:0:ab:11:5b:b:f2:40:d0:5f:d6:ed comment="Fandas board with cams" mac-address=00:18:7D:CA:8F:D3 server=dhcp1
add address=10.7.31.5 client-id=1:c4:ad:34:9c:be:57 mac-address=C4:AD:34:9C:BE:57 server=dhcp1
add address=10.7.31.19 client-id=1:e0:63:da:52:aa:bd comment="AP19 UniFi" mac-address=E0:63:DA:52:AA:BD server=dhcp1
add address=10.7.31.20 client-id=1:e0:63:da:52:ac:d9 comment="AP20 UniFi" mac-address=E0:63:DA:52:AC:D9 server=dhcp1
add address=10.7.31.21 client-id=1:74:83:c2:74:5:e9 comment="AP21 UniFi" mac-address=74:83:C2:74:05:E9 server=dhcp1
add address=10.7.31.22 client-id=1:74:83:c2:74:2:c5 comment="AP22 UniFi" mac-address=74:83:C2:74:02:C5 server=dhcp1
add address=10.7.31.23 client-id=1:74:83:c2:74:6:1d comment="AP23 UniFi" mac-address=74:83:C2:74:06:1D server=dhcp1
add address=10.7.31.76 comment="HoneyWell 5th floor" mac-address=B8:2C:A0:2B:DE:98 server=dhcp1
add address=10.7.31.64 client-id=1:74:83:c2:cf:8e:d6 comment="Camera NVR 4L" mac-address=74:83:C2:CF:8E:D6 server=dhcp1
add address=10.7.31.65 client-id=1:74:83:c2:cf:d6:da comment="Camera NVR 4R" mac-address=74:83:C2:CF:D6:DA server=dhcp1
add address=10.7.31.74 comment="HoneyWell 4th (L) floor" mac-address=B8:2C:A0:AF:6D:CB server=dhcp1
add address=10.7.31.75 comment="HoneyWell 4th (R) floor" mac-address=B8:2C:A0:A3:44:EC server=dhcp1
add address=10.7.31.248 client-id=ff:b8:98:8b:79:0:2:0:0:ab:11:d5:d6:49:8f:16:80:44:4a comment="Lely View Cam  " mac-address=00:14:2D:67:B7:53 server=dhcp1
add address=10.7.31.246 client-id=1:94:c6:91:a2:90:52 comment=Conferencing-Tool-Kitchen6L mac-address=94:C6:91:A2:90:52 server=dhcp1
add address=10.7.31.243 client-id=1:1c:69:7a:67:c0:a6 comment=Conferencing-Tool-Alpha mac-address=1C:69:7A:67:C0:A6 server=dhcp1
add address=10.7.31.104 client-id=1:1c:69:7a:66:b7:83 comment=Conferencing-Tool-Gamma mac-address=1C:69:7A:66:B7:83 server=dhcp1
add address=10.7.31.233 client-id=1:1c:69:7a:69:d3:2c comment=Conferencing-Tool-Psi mac-address=1C:69:7A:69:D3:2C server=dhcp1
add address=10.7.31.170 client-id=1:1c:69:7a:65:e8:5b comment=Conferencing-Tool-Beta mac-address=1C:69:7A:65:E8:5B server=dhcp1
add address=10.7.31.222 comment="Devio-SysAdmin-Conferencing Room" mac-address=78:45:01:0A:EC:3E server=dhcp1
add address=10.7.31.235 client-id=1:38:f3:ab:b0:4:f5 comment=Conferencing-Tool-Giga mac-address=38:F3:AB:B0:04:F5 server=dhcp1
add address=10.7.31.202 client-id=ff:b6:22:f:eb:0:2:0:0:ab:11:40:ca:0:ae:35:5f:4e:26 mac-address=00:18:7D:D7:39:01 server=dhcp1
add address=10.7.31.108 client-id=1:ac:74:b1:16:c4:16 mac-address=AC:74:B1:16:C4:16 server=dhcp1
add address=10.7.31.35 client-id=1:5c:ba:2c:58:f9:0 comment="Pohoda Server" mac-address=5C:BA:2C:58:F9:00 server=dhcp1
add address=10.7.31.36 client-id=0:5c:ba:2c:58:f9:3:0:0:0 comment="Pohoda Server Management" mac-address=5C:BA:2C:58:F9:03 server=dhcp1
/ip dhcp-server network
add address=10.7.31.0/24 comment="Main office network - vlan1031-core-untagged" dns-server=10.7.31.1 gateway=10.7.31.1 netmask=24
add address=10.7.32.0/24 comment="KD PROPOSE vlan1032-guests" dns-server=10.7.32.1 gateway=10.7.32.1 netmask=24
add address=10.7.33.0/24 comment="KD PROPOSE vlan1033-iot" dns-server=10.7.33.1 gateway=10.7.33.1 netmask=24
add address=10.7.100.0/22 comment="KD PROPOSE vlan1100-staff" dns-server=10.7.100.1 gateway=10.7.100.1 netmask=22
/ip dns
set allow-remote-requests=yes cache-max-ttl=30s cache-size=512KiB max-concurrent-queries=1000 max-concurrent-tcp-sessions=200 servers=10.7.31.30,10.7.31.32
/ip firewall address-list
add address=172.27.11.0/24 comment="Lely servers" list=tinc-network
add address=172.27.2.0/24 comment="Lely other" list=tinc-network
add address=172.18.18.0/24 comment="Jura private network" list=tinc-network
add address=10.161.132.0/24 list=tinc-network
/ip firewall filter
add action=accept chain=input comment="accept established,related" connection-state=established,related
add action=drop chain=input comment="drop invalid" connection-state=invalid
add action=accept chain=input comment=ICMP log-prefix=icmp protocol=icmp
add action=add-src-to-address-list address-list="port scanners" address-list-timeout=2w chain=input comment="Port scanners to list " in-interface-list=WAN log=yes log-prefix=PortScan protocol=tcp psd=21,3s,3,1
add action=accept chain=input comment="WireGuard Inbound rule" dst-port=13231 protocol=udp src-address=0.0.0.0/0
add action=drop chain=input comment="drop all from WAN" in-interface-list=WAN
add action=accept chain=forward comment="accept established,related" connection-state=established,related
add action=add-src-to-address-list address-list="port scanners" address-list-timeout=2w chain=forward comment="Port scanners to list " in-interface-list=WAN protocol=tcp psd=21,3s,3,1
add action=drop chain=forward comment="KD PROPOSE VLAN Drop traffic from vlan1032-guests into LAN" in-interface=vlan1032-guests out-interface-list=!WAN
add action=drop chain=forward comment="drop invalid" connection-state=invalid log-prefix=INV
add action=drop chain=forward comment="drop all from WAN not DSTNATed" connection-nat-state=!dstnat connection-state=new in-interface-list=WAN
add action=add-src-to-address-list address-list=tinc-vpn-clients address-list-timeout=none-dynamic chain=forward comment="Tinc VPN clients listing" dst-address-list=tinc-network log-prefix=TINC
add action=add-dst-to-address-list address-list=tinc-vpn-targets address-list-timeout=none-dynamic chain=forward comment="Tinc VPN targets listing" dst-address-list=tinc-network
/ip firewall mangle
add action=mark-packet chain=prerouting in-interface=bridge1 new-packet-mark=client_upload passthrough=yes
add action=mark-packet chain=prerouting in-interface=ether1 new-packet-mark=client_download passthrough=yes
/ip firewall nat
add action=masquerade chain=srcnat out-interface=ether1
add action=masquerade chain=srcnat out-interface=ether12
add action=dst-nat chain=dstnat comment="dst nat for Datamole VPN infra2.office.dtml on Calculon" disabled=yes dst-port=9411 in-interface=ether1 protocol=udp to-addresses=10.7.31.32 to-ports=9411
add action=dst-nat chain=dstnat comment="Tinc infra.office.dtml TCP infra2.office.dtml on Calculon" dst-port=655 in-interface=ether1 protocol=tcp to-addresses=10.7.31.32 to-ports=655
add action=dst-nat chain=dstnat comment="Tinc infra.office.dtml UDP infra2.office.dtml on Calculon" dst-port=655 in-interface=ether1 protocol=udp to-addresses=10.7.31.32 to-ports=655
add action=masquerade chain=srcnat comment="Gorgon NUC NAT" dst-address=10.8.31.0/24 src-address=10.7.31.0/24
add action=masquerade chain=srcnat comment="Masquerade for Tinc VPN (inbound)" dst-address-list=tinc-network log-prefix=TINC-MASS src-address=10.7.31.0/24
/ip ipsec policy
set 0 disabled=yes
/ip route
add disabled=yes dst-address=147.32.232.213/32 gateway=ether1 pref-src=94.113.223.167
add comment="Calculon VPN" disabled=no dst-address=192.168.94.0/24 gateway=10.7.31.32
add comment="Calculon LXD" disabled=no dst-address=10.68.63.0/24 gateway=10.7.31.32
add comment="Calculon MSSQL subnet" disabled=no dst-address=192.168.123.0/24 gateway=10.7.31.32
add check-gateway=ping comment="Default uplink route - Spoje.net" disabled=no distance=1 dst-address=0.0.0.0/0 gateway=77.87.240.40 pref-src=0.0.0.0 routing-table=main scope=30 suppress-hw-offload=no target-scope=10
add check-gateway=ping comment="Office (Datamole) VPN on Calculon" disabled=no distance=2 dst-address=192.168.92.0/24 gateway=10.7.31.32
add check-gateway=ping comment="Jura network though Tinc VPN infra2.office.dtml on Calculon" disabled=no distance=2 dst-address=172.18.18.0/24 gateway=10.7.31.32
add check-gateway=ping comment="Lely network though Tinc VPN infra2.office.dtml on Calculon" disabled=no distance=2 dst-address=172.27.2.0/24 gateway=10.7.31.32
add check-gateway=ping comment="Lely network though Tinc VPN infra2.office.dtml on Calculon" disabled=no distance=2 dst-address=172.27.11.0/24 gateway=10.7.31.32
add check-gateway=ping disabled=no dst-address=10.161.132.0/24 gateway=10.7.31.32
add comment="Route to Krumlov office - Tinc" disabled=yes distance=1 dst-address=10.8.31.0/24 gateway=10.7.31.32 pref-src="" routing-table=main scope=30 suppress-hw-offload=no target-scope=10
add comment="WireGuard route to Brno Office" disabled=no distance=1 dst-address=10.9.0.0/16 gateway=vpn-dtml-core pref-src=0.0.0.0 routing-table=main scope=30 suppress-hw-offload=no target-scope=10
add comment="WireGuard Route to Krumlov Office" disabled=no distance=1 dst-address=10.8.0.0/16 gateway=vpn-dtml-core pref-src=0.0.0.0 routing-table=main scope=30 suppress-hw-offload=no target-scope=10
add check-gateway=ping comment="KD-TEST - Nusle" disabled=no distance=1 dst-address=192.168.23.0/24 gateway=192.168.88.1 pref-src=0.0.0.0 routing-table=main scope=30 suppress-hw-offload=no target-scope=30
add check-gateway=ping comment="KD-TEST - Valid, table hAP" disabled=no distance=1 dst-address=192.168.88.0/24 gateway=10.255.69.88 pref-src=0.0.0.0 routing-table=main scope=30 suppress-hw-offload=no target-scope=10
add comment="KD-TEST VLANS" disabled=no distance=1 dst-address=192.168.30.0/24 gateway=vpn-dtml-core pref-src="" routing-table=main scope=30 suppress-hw-offload=no target-scope=10
add comment="KD-TEST VLANS" disabled=no distance=1 dst-address=192.168.50.0/24 gateway=vpn-dtml-core pref-src=0.0.0.0 routing-table=main scope=30 suppress-hw-offload=no target-scope=10
/ip service
set telnet disabled=yes
set ftp disabled=yes
set ssh address=10.7.31.0/24
/ip ssh
set allow-none-crypto=yes forwarding-enabled=remote
/ipv6 firewall address-list
add address=::/128 comment="defconf: unspecified address" list=bad_ipv6
add address=::1/128 comment="defconf: lo" list=bad_ipv6
add address=fec0::/10 comment="defconf: site-local" list=bad_ipv6
add address=::ffff:0.0.0.0/96 comment="defconf: ipv4-mapped" list=bad_ipv6
add address=::/96 comment="defconf: ipv4 compat" list=bad_ipv6
add address=100::/64 comment="defconf: discard only " list=bad_ipv6
add address=2001:db8::/32 comment="defconf: documentation" list=bad_ipv6
add address=2001:10::/28 comment="defconf: ORCHID" list=bad_ipv6
add address=3ffe::/16 comment="defconf: 6bone" list=bad_ipv6
add address=::224.0.0.0/100 comment="defconf: other" list=bad_ipv6
add address=::127.0.0.0/104 comment="defconf: other" list=bad_ipv6
add address=::/104 comment="defconf: other" list=bad_ipv6
add address=::255.0.0.0/104 comment="defconf: other" list=bad_ipv6
/ipv6 firewall filter
add action=accept chain=input comment="accept established, related, untracked" connection-state=established,related,untracked
add action=drop chain=input comment="drop invalid" connection-state=invalid log=yes log-prefix="IPv6 FW DROP INV"
add action=accept chain=input comment="accept ICMPv6" limit=50/5s,5:packet protocol=icmpv6
add action=accept chain=input comment="defconf: accept UDP traceroute" disabled=yes port=33434-33534 protocol=udp
add action=accept chain=input comment="defconf: accept DHCPv6-Client prefix delegation." disabled=yes dst-port=546 protocol=udp src-address=fe80::/16
add action=accept chain=input comment="defconf: accept IKE" disabled=yes dst-port=500,4500 protocol=udp
add action=accept chain=input comment="defconf: accept ipsec AH" disabled=yes protocol=ipsec-ah
add action=accept chain=input comment="defconf: accept ipsec ESP" disabled=yes protocol=ipsec-esp
add action=accept chain=input comment="defconf: accept all that matches ipsec policy" disabled=yes ipsec-policy=in,ipsec
add action=drop chain=input comment="drop everything else from WAN" in-interface-list=WAN log=yes log-prefix="IPv6 FW DROP"
add action=accept chain=forward comment="accept established, related, untracked" connection-state=established,related,untracked
add action=drop chain=forward comment="drop invalid fwd" connection-state=invalid log=yes log-prefix="IPv6 FW DROP INV"
add action=drop chain=forward comment="defconf: drop packets with bad src ipv6" src-address-list=bad_ipv6
add action=drop chain=forward comment="defconf: drop packets with bad dst ipv6" dst-address-list=bad_ipv6
add action=drop chain=forward comment="defconf: rfc4890 drop hop-limit=1" hop-limit=equal:1 protocol=icmpv6
add action=accept chain=forward comment="accept ICMPv6" limit=50/5s,5:packet protocol=icmpv6
add action=accept chain=forward comment="defconf: accept HIP" disabled=yes protocol=139
add action=accept chain=forward comment="defconf: accept IKE" disabled=yes dst-port=500,4500 protocol=udp
add action=accept chain=forward comment="defconf: accept ipsec AH" disabled=yes protocol=ipsec-ah
add action=accept chain=forward comment="defconf: accept ipsec ESP" disabled=yes protocol=ipsec-esp
add action=accept chain=forward comment="defconf: accept all that matches ipsec policy" disabled=yes ipsec-policy=in,ipsec
add action=drop chain=forward comment="drop rest" connection-state="" in-interface-list=WAN log=yes log-prefix="IPv6 FW DROP"
/ipv6 nd
set [ find default=yes ] advertise-dns=no
/lcd
set backlight-timeout=never default-screen=informative-slideshow time-interval=weekly
/lcd pin
set pin-number=3865
/radius
add address=10.7.31.40 service=wireless src-address=10.7.31.1 timeout=10s
/system clock
set time-zone-name=Europe/Prague
/system identity
set name=Datamole-CCR1016
/system logging
set 0 topics=info,!firewall,!caps,!dhcp
add disabled=yes topics=dhcp,wireless,caps
add action=wireless topics=caps
add action=firewall topics=firewall
add action=dhcp topics=dhcp,info
add action=wireless topics=wireless
add action=disk topics=system
add action=disk topics=critical
add action=disk topics=critical,dhcp,health,interface,route,ssh,stp,system,watchdog
/system scheduler
add disabled=yes interval=30s name=dns-failover-check on-event=dns-failover-check policy=ftp,reboot,read,write,policy,test,password,sniff,sensitive,romon start-time=startup
add interval=15s name=check-connection on-event=connection-logs policy=ftp,reboot,read,write,policy,test,password,sniff,sensitive,romon start-date=aug/29/2019 start-time=12:40:53
/system script
add dont-require-permissions=no name=dns-set-to-public owner=datamole_admin policy=read,write,romon source=\
