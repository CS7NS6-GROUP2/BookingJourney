from cassandra.cluster import Cluster

cluster = Cluster(['35.172.217.174'])
connection =  cluster.connect('group2')