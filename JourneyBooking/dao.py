from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster

cluster = Cluster(['35.172.217.174'])
connection = cluster.connect('group2')


def get_all_journeys():
    user_lookup_stmt = connection.prepare("SELECT JSON * FROM journey_info")
    user_lookup_stmt.consistency_level = ConsistencyLevel.QUORUM
    results = connection.execute(user_lookup_stmt)
    ans = "["
    for r in results:
        print(r.json)
        ans += r.json + ","
    ans = ans[:-1]
    ans += ']'
    print(ans)
    return ans