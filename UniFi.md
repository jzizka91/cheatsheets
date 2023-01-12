
### ADOPT all UniFi Wifi:

```
for host in $(echo {11..23}); do echo "10.7.31.$host is adopting" && ssh <ap_user>@10.7.31.$host 'mca-cli-op set-inform http://unificontroller.dtml:8080/inform'; done
```

### REBOOT all UniFi Wifi:

```
for host in $(echo {11..23}); do echo "10.7.31.$host is adopting" && ssh <ap_user>@10.7.31.$host 'reboot; done
```