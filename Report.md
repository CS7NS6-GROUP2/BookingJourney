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
endpoint_snitch: Ec2Snitch
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
* ![](https://github.com/CS7NS6-GROUP2/BookingJourney/blob/main/images/test1.png?raw=true)
### TestCase 2: Replicas of data
* Check the replicas by `nodetool getendpoints` which can provide the IP addresses or names of replicas that own the partition key. For example, "2030559" is a partition key in admin table
* As we can see from the results, three replicas were distributed in different machines, and these machines are in different racks.
![](https://github.com/CS7NS6-GROUP2/BookingJourney/blob/main/images/test2.png?raw=true)

### TestCase 3: Reliability of database
### TestCase 4: Consistency of data
### TestCase 5: Check the cache
* Since we did not use `RowCache`, here we only check the `KeyCache` by `nodetool info`, as the results, we can see the hit rates of KeyCache
![](https://github.com/CS7NS6-GROUP2/BookingJourney/blob/main/images/test5.png?raw=true)
## Allocation of work
## Summary

