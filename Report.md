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
```
sudo wget -qO - https://raw.githubusercontent.com/xurui1995/script/main/ds.sh | bash
```
* Edit config and join the cluster
* `sudo vim /etc/cassandra/cassandra.yaml `
```
seed_provider:
    - class_name: org.apache.cassandra.locator.SimpleSeedProvider
        - seeds: "172.31.66.97,172.31.87.4"
listen_address: "your EC2 private IP"
rpc_address: 0.0.0.0
broadcast_rpc_address: "your EC2 private IP"
endpoint_snitch: GossipingPropertyFileSnitch
```
* Start service
```
sudo wget -qO - https://raw.githubusercontent.com/xurui1995/script/main/start.sh | bash
```
* Check the new node status
```
nodetool status
```
* Result


## Allocation of work
## Summary

