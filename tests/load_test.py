import string
import random
import time

import rethinkdb as r

def gen_str(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

conn = r.connect("docker.local.io", 28016)
# insert channel data
data = [
    {
        'namespace': 'chat',
        'channel': 'public',
        'message': 'Ahoy from RethinkDB {}'
    },
    {
	   'namespace': 'chat',
      'channel': 'user1',
      'message': 'Ahoy! from RethinkDB for user1 only {}'
    },
    {
	   'namespace': 'chat',
       'channel': 'user2',
       'message': 'Ahoy! from RethinkDB for user 2 only {}'
    },
    {
	   'namespace': 'chat',
       'channel': 'user3',
       'message': 'Ahoy! from RethinkDB for user 3 only {}'
    },
    {
	   'namespace': 'news',
       'channel': 'private',
       'message': 'News from RethinkDB {}'
    }
]
for i in range(100):
    time.sleep(0.1)
    print("running {}".format(i))
    for d in data:
        c = d.copy()
        rd = gen_str()
        c.update({'message': c['message'].format(rd)})
        r.db('notification').table('messages').insert(c).run(conn)

print("completed")
