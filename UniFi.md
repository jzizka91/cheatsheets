
### ADOPT multiple ranges of UniFi Wifi:

```
for host in $(echo {43..47} {53..56}) {63..66}; do echo "10.7.20.$host is adopting" && ssh <username>@10.7.20.$host 'mca-cli-op set-inform http://10.7.31.32:8080/inform'; done
```

### REBOOT multiple ranges of UniFi Wifi:

```
for host in $(echo {43..47} {53..56} {63..66}); do echo "10.7.20.$host is restarting" && ssh <username>@10.7.20.$host 'reboot; done
```
