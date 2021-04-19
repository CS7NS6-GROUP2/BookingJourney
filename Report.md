# CS7NS6

## Introduciton
## Requirements
## Specifications
## Architecture
## Implementation
## Test
### TestCase 1: Scalability of database
* Create a new ubuntu machine on your AWS EC2
* Install the cassandra environment
`sudo wget -qO - https://raw.githubusercontent.com/xurui1995/script/main/ds.sh | bash`
* Edit config and join the cluster
  * `sudo vim /etc/ca`
```
  sudo /lib/systemd/systemd-sysv-install enable cassandra
  sudo systemctl start cassandra
  sudo systemctl -l status cassandra
```
* Check the new node status

## Allocation of work
## Summary

