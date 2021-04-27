# cs7ns6-groupwork

TCD CS7NS6 Distributed Systems Exercise 2

## Introduciton

This project aim to implement a 

## Requirements

We need to implement a global-oriented journey management system that allows drivers to book/cancel journeys. According to the requirement, all road-vehicle drivers are required to prebook every journey that they wish to make, no driver is allowed to start a journey without having received a notification that the requested journey is acceptable.

These require us to provide a high-performance service, it has to meet at least the following requirements (The focus of our system implementation exercise is not the business logic of journey management) :

* This service needs to be scalable. (All journeys required a prebook, the number of users might be very large.)

* The service needs to be highly available. (No driver is allowed to start a journey without having received a notification)

* The service needs to be reliable. (Before starting the journey, the drivers receive a notification that the requested journey is acceptable)

  

  #### Functional requirements-API

  -- prebook_journey(driverId)

  -- confirm_journey(driverId)

  -- cancel_journey(driverId, orderId)

  -- get_journey(driverId)

  

  #### Non-functional requirements

  | Scale               | **1M/s** |
  | :------------------ | -------- |
  | **I/O performance** | **ms**   |
  | **scalability**     | **..**   |
  | **availability**    | **..**   |
  | **reliability**     | **..**   |
  |                     |          |

  

## Specifications

## Architecture

  ![](https://github.com/CS7NS6-GROUP2/BookingJourney/blob/main/images/image-architecture.png?raw=true)


## Implementation

### Sharding and partitioning:
In Cassandra, when writing or reading data, the nodes in a datacenter are treated as a ring, and each node contains a range of virtual nodes which is token, tehn system use  a consistent hash function to determining how to distribute the data across the nodes in the cluster given the partition key of a partition key. 
In our system, we build the cluster by using Amazon EC2, we created six instances on the datacenter us-east.
![](https://github.com/CS7NS6-GROUP2/BookingJourney/blob/main/images/ring.png?raw=true)
![](https://github.com/CS7NS6-GROUP2/BookingJourney/blob/main/images/status.png?raw=true)
### Data Scalability and Maintainability
As we mentioned in the previous part, we can scale vertically by enlarge the token number of a node, and also we can scale horizontally by adding more nodes and datacenters. 
Two shell scripts are written for building the cassandra environment, which make the cluster easier to manage. The only things we need to do is edit the config file of new machine to add it into cluster.

### Data replication and availability
In Cassandra, when data come to cassdran, after finding the node position in token ring, it will continue moving around the ring and adding the data to the node according to replica strategy until meet the replica factor requirements.
The replication factor was set by the following CQL when creating key space.
```
CREATE KEYSPACE group2 
WITH REPLICATION = {'class' : 'NetworkTopologyStrategy', 'us-east' : 3 } 
AND DURABLE_WRITES = true;
```
Here, we set the replication strategy as NetworkTopologyStrategy, and specifies the replia factor is 3 in us-east datacenter(the total machines are 6).
The NetworkTopologyStrategy will attempt to place replicas on distinct racks by walking the ring clockwise, because the  nodes in the same rack often fail at the same time, so we want the replicas in different racks in our project which can have more probability to avoid failures.

### Partition and fault tolerance
As menthioned before, we have different racks in our datacenter with a NetworkTopologyStrategy replica strategy, which means when one of rack fails, the database can still provide service, because other racks will not be affected and have the replicas. In addition, we can add more datacenter, but here we hava a limit of aws education account.
The nodes in cassandra are not follow a master-salve rule, all nodes communicate with each other through a peer-to-peer communication protocol called Gossip Protocol, which can make sure the cluster doesn't hava a single point failure. Besides, the Gossip Protocol also works on failure detection by a periodically ping mechanism.  

### Data consistency
According to CAP theorem, a distributed system can not simultaneously guarantee consistency, availability and partition tolerance. here, we decided to prioritize consistency over availability, but the consistency, we used the tunable consistency provided by Cassandra, and by setting the consistency level to QUORUM to tradeoff the 
consistency and availability.

QUORUM is calculated by the following formula.
```
quorum = (sum_of_replication_factors / 2) + 1
```
In our system, the replication_factors is 3, that means quorum is 2, when writing data, it can guarantee the data at least be written successfully on 2 nodes, when reading the data, it will at least compare results of two replicas, and return the recent version data, for those inconsistent data, a read repair process will help correct the data to improve consistency.
It was mentioned that, strong consistency can be guaranteed when the following condition is true:
```
R + W > N
```
R is the consistency level of read operations
W is the consistency level of write operations
N is the number of replicas
Here in our system, we set consistency level to QUORUM so that it meet that requirement.

### Durability
The write request in Cassandra is appended to the commit log in the disk. This ensures data durability, and the write request is also sent to memtable (a structure stored in the memory), When the memtable is full, the data is flushed to a SSTable on disk and the data in the commit log is purged. If a crash occurs before the memtables are flushed to disk,  the commit log is replayed on restart to recover any lost writes.

### Failure detection and recovery
As we mentioned before, the nodes in Cassandra communicate by gossip, Once per second, each node contacts 1-3 other nodes asking about the node state and location.
the Hinted Handoff can help recovery a node when a node comes back online. when a node is unable to receive a write, the write's coordinator node saves the data to be written as a set of hints for the unavailable node. When the unavailable node comes back online, the coordinator node will sent hints to help catch up with write.
### Caching
There are two layers of cache in Cassandra, key cache helps C* know where a particular partition begins in the SStables and row cache pulls entire partitions into memory. Firstly the system will try to retrieve data from row rache, then if can not find, it will retrieve data according to key cache.
Here in our system, we used both of the caches to avoid latency problem by setting the config.
### Atomicity
In Cassandra, a write is atomic at the row-level, in our system, we provide a function for booking muti-leg jouney, it will need more than one database writes, we need to guarantee the atomicity, here we achieved that by using the Bacth statement in Cassandra which can ensure atomicity. 





## Test

### TestCase 1: Database Scalability and Maintainability

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

### TestCase 2: Replicas of data and Partition

* Check the replicas by `nodetool getendpoints` which can provide the IP addresses or names of replicas that own the partition key. For example, "20335559" is a partition key in admin table
* As we can see from the results, three replicas were distributed in different machines, and these machines are in different racks.
  ![](https://github.com/CS7NS6-GROUP2/BookingJourney/blob/main/images/test2.png?raw=true)

### TestCase 3: Reliability of database

* Shut down one of the machines that contains the test data
* Test if we can retrieve the test data from the left machines
  ![](https://github.com/CS7NS6-GROUP2/BookingJourney/blob/main/images/test3.png?raw=true)


### TestCase 4: Consistency of data

* Check the consistency level
  ![](https://github.com/CS7NS6-GROUP2/BookingJourney/blob/main/images/test4-1.png?raw=true)
* Check the eventual consistency, two machines update a same row in short interval, the first one changed the 
  name to "admin1", the second one changed it to "admin2", the eventual result should be the last one on both machines. 

```
update group2.admin_table set name = 'admin1' where id = 1;
update group2.admin_table set name = 'admin2' where id = 1;
```

* ![](https://github.com/CS7NS6-GROUP2/BookingJourney/blob/main/images/test4-2.png?raw=true)

### TestCase 5: Check the cache

* Check the rough cache situation by `nodetool info`
* We open the tracing, we query the data of id = 20305559 again, we can see the results shows the we hit the cache.
  ![](https://github.com/CS7NS6-GROUP2/BookingJourney/blob/main/images/test5.png?raw=true)
  
### TestCase 6: Test the atomicity
* Use Batch statement for two update cql with condition,

## Allocation of work
* Discussing the requirements (All members)
* Searching for suitable middlewares (All members)
* Discussing the technique stack and architecture (All members)
* Working on the distributed session and authentication (Wei Hu)
* Working on the business logic and API (Youxin Zhou)
* Working on the Cassandra database (Rui Xu)
* Working on the keepalived and nigix (Niejun Yin)
## Summary
