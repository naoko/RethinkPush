import rethinkdb as r

conn = r.connect("docker.local.io", 28015)


class Table(object):
    notification = 'events'
    user = 'users'
    channels = 'channels'
    channels_users = 'channels_users'
    events = 'events'

# insert user data
r.table(Table.user).insert({'username': 'user1'}).run(conn)
r.table(Table.user).insert({'username': 'user2'}).run(conn)

# view data
for d in r.table(Table.user).run(conn):
    print(d)

# {u'username': u'user1', u'id': u'ba4d76eb-948f-4baf-8bbe-79d3eab48840'}
# {u'username': u'user2', u'id': u'52fd3547-10e7-4bca-aced-6c7159ee8640'}

# insert channel data
data = [
    {
        "name": "private-user1",
        "type": "direct",
    },
    {
        "name": "private-user2",
        "type": "direct",
    },
    {
        "name": "server-status",
        "type": "fanout",
    },
    {
        "name": "company-abc",
        "type": "topic",
    }
]
r.table(Table.channels).insert(data).run(conn)
for d in r.table(Table.channels).run(conn): print(d)

# creating index so that can query with secondary index
# when join with event
r.table("channels").index_create("name").run(conn)

# {u'type': u'direct', u'id': u'096eb439-dd18-426d-a4d6-518f0ef3dbd6', u'name': u'private-user1'}
# {u'type': u'topic', u'id': u'dfde46db-b3a2-44a6-bbda-ba207d90cf2b', u'name': u'company-abc'}
# {u'type': u'direct', u'id': u'4b43246d-9da5-46ab-aab9-001d2eac57e9', u'name': u'private-user2'}
# {u'type': u'fanout', u'id': u'8106eba3-513b-4325-824d-3af1fac815a2', u'name': u'server-status'}

# insert channels_users
data = [
    {
        "channel_id": "096eb439-dd18-426d-a4d6-518f0ef3dbd6",
        "user_id": "ba4d76eb-948f-4baf-8bbe-79d3eab48840"
    },
    {
        "channel_id": "4b43246d-9da5-46ab-aab9-001d2eac57e9",
        "user_id": "52fd3547-10e7-4bca-aced-6c7159ee8640"
    }
]
r.table(Table.channels_users).insert(data).run(conn)
for d in r.table(Table.channels_users).run(conn): print(d)

# select users based on channel
result = r.table(Table.channels_users).eq_join("channel_id", r.table(Table.channels)).zip().eq_join("user_id", r.table(Table.user)).zip().run(conn)
for d in result: print(d)
result = r.table(Table.channels_users).eq_join("channel_id", r.table(Table.channels)).zip().eq_join("user_id", r.table(Table.user)).zip().filter({'username': 'user2'}).run(conn)
for d in result: print(d)

# send event:
data = {
    "channel_name": "server-status",
    "data": {
        "key1": "value1",
        "key2": ["apple", "orange", "strawberry"]
    }
}
r.table(Table.events).insert([data]).run(conn)

data = {
    "channel_name": "server-status",
    "data": {
        "message": "Server is going down in a few"
    }
}
r.table(Table.events).insert([data]).run(conn)

# add private channel message
data = {
    "channel_name": "private-user1",
    "data": {
        "message": "Hello User 1. Secret message for you"
    }
}
r.table(Table.events).insert([data]).run(conn)

# add private channel message
data = {
    "channel_name": "private-user2",
    "data": {
        "message": "Hello User 2. this is private message ONLY for you"
    }
}
r.table(Table.events).insert([data]).run(conn)

# DataExplore syntax
# r.table('events').eqJoin('channel_name', r.table('channels'), {index: 'name'}).zip();

# delete data
# delete all notifications
r.table(Table.notification).delete().run(conn)
r.table(Table.user).delete().run(conn)

# r.table(table).get("fb87731f-ce38-4579-83ef-a41b6095c7cd").delete().run(conn)
# r.table(table).filter({'name': 'spiderman'}).delete().run(conn)
