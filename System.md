### Remove multiple lines of history with cycle:

```
for h in $(seq <from> <to>); do history -d <from>; done
```

### Locale fix for pip:

```
echo “export LC_ALL=C” >> .bashrc
source .bashrc
```

or
```
export LC_ALL=C
```

### GET Fingerprint from Servers:

```
for s in $(cat ~/server); do ssh-keyscan -t ecdsa $s >> known_hosts; done
```

### Encode string to base64 (Gitlab Token):

```
echo <username>:<‘token-string’> | base64
```

### Decode string to base64:

```
echo ‘<64base_token-string>’ | base64 --decode
```

### Create a virtual monitor:

```
xrandr --setmonitor "<monitor_name>" "width_px"/"width_mm"x"height_px"/"height_mm"+"x_offset_px"+"y_offset_px" "output_name"

Examples:
1080p** -> xrandr --setmonitor eDP-1-1~1 960/172x1080/193+0+0 eDP-1-1
2160p** -> xrandr --setmonitor "<monitor_name>" "1920"/"width_mm"x"2160"/"height_mm"+"x_offset_px"+"y_offset_px" "output_name"
```

 ### Create a binary file from a APIToken:

```
import io

#initialize string
strApiKey = "token"

#open file as a binary file
f = open('token.bin', 'wb')

#convert string to bytes
strBytes = strApiKey.encode()

#write byte string to binary file
f.write(strBytes)

f.close()
```

### Moniter setup - Laptop -> monitor:

```
xrandr --output HDMI-0 --auto --right-of eDP-1-1
```

### Clean Disk Fast:

```
sudo dd if=/dev/zero of=<DISK_PATH> bs=4096 status=progress
```

### Clean Disk Secure:

```
#! /bin/bash
for ((n=1;n<8;n++)); do
	sudo dd if=/dev/urandom of=<DISK_PATH> bs=4096 status=progress;
done
```

### Reverse SSH Tunneling:

```
ssh -A root@<server> # Client Machine
ssh -N -R 44444:localhost:22 root@<server> -p 2221 # NAS Node
ssh -N -L 44444:localhost:44444 root@<server> -p 2221 # Client Machine
ssh root@localhost -p 44444 # Client Machine
```

### Use NIC Mac address as the default ID for DHCP requests:

Built-in network config of Ubuntu 18.04 no longer uses the NIC Mac address as the default id for DHCP requests.

Uses the NIC MAC address as the default id for DHCP requests:

```
network:
    renderer: networkd
    version: 2
    ethernets:
        <nicdevicename>:
            dhcp4: true
            dhcp-identifier: mac
```

## Change directory names so they include the date from the name of the video inside a sub-directory.

```
#!/bin/bash

path='<path>'

for ks_name in $(ls $path); do
  for ks_date in $(ls $path/$ks_name | grep -E '[0-9]+_.*\.mp4$' | cut -d '_' -f 1 ); do
   mv ~/KS/$ks_name ~/KS/"$ks_date"_"$ks_name"
   echo "$ks_date"_"$ks_name"
  done
done
```
