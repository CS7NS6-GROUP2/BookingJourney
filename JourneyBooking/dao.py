import json
import uuid

from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement, BatchStatement

cluster = Cluster(['18.207.249.168', '3.87.63.27','3.238.206.50', '54.242.60.190','52.91.41.155', '3.85.110.231'])
connection = cluster.connect('group2')

def jsonarray(results):
    if len(results.current_rows) == 0:
        return None
    ans = "["
    for r in results:
        ans += r.json + ","
    ans = ans[:-1]
    ans += ']'
    return ans

def insert_user(name, car, password, id):
    query = SimpleStatement(
        "INSERT INTO users (id, name, car, password) VALUES (%s, %s, %s, %s)",
        consistency_level=ConsistencyLevel.QUORUM)
    results = connection.execute(query, (id, name, car, password))
    return results

def get_all_journeys():
    user_lookup_stmt = connection.prepare("SELECT JSON * FROM journey_info")
    user_lookup_stmt.consistency_level = ConsistencyLevel.QUORUM
    results = connection.execute(user_lookup_stmt)
    return jsonarray(results)

def get_all_users():
    user_lookup_stmt = connection.prepare("SELECT JSON * FROM users")
    user_lookup_stmt.consistency_level = ConsistencyLevel.QUORUM
    results = connection.execute(user_lookup_stmt)
    return jsonarray(results)

def get_orders_by_user(uid):
    user_lookup_stmt = connection.prepare(
        "SELECT JSON * FROM orders where userid = {} and status >= 0 ALLOW FILTERING ;".format(uid))
    user_lookup_stmt.consistency_level = ConsistencyLevel.QUORUM
    results = connection.execute(user_lookup_stmt)
    return jsonarray(results)


def get_all_orders():
    user_lookup_stmt = connection.prepare("SELECT JSON * FROM orders")
    user_lookup_stmt.consistency_level = ConsistencyLevel.QUORUM
    results = connection.execute(user_lookup_stmt)
    return jsonarray(results)

def book_tickets(uid, journeys):
    batchId = uuid.uuid1()
    batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
    for journey in journeys:
        orderid = uuid.uuid1()
        batch.add(SimpleStatement(
            "insert into orders (orderid, userid, journeyId, batchId, status) VALUES ({}, {}, {}, {}, {}) ".format(
                orderid, uid, journey, batchId, 0
            )))
    result = connection.execute(batch)
    return result


def cancel_orders(uid, order_ids):
    batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
    for orderid in order_ids:
        batch.add(SimpleStatement("update orders set status = -1 "
                                  "where orderid = {} and userid = {} ;".format(orderid, uid)))
    result = connection.execute(batch)
    return result


def approve_orders(uid, order_ids):
    batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
    for orderid in order_ids:
        batch.add(SimpleStatement("update orders set status = 1 "
                                      " where orderid = {} and userid = {};".format(orderid, uid)))
    result = connection.execute(batch)
    return result

def create_journey(name):
    id = uuid.uuid1()
    batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
    batch.add(SimpleStatement("INSERT INTO journey_info (id, name ) VALUES (%s, %s)"), (id, name))
    result = connection.execute(batch)
