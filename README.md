# RethinkPush with RethinkDB + socket.io

* Use of RethinkDB Changefeeds for Realtime
* RethinkPush is service to aid Websocket


## How does it work
view in [stackedit.io](https://stackedit.io/editor)


**direct**

```sequence
Client->App: realtime feed request
App->RethinkPush: register user
RethinkPush->RethinkDB: save user data
Note left of RethinkDB: w/ auth token
RethinkDB-->RethinkPush: OK
RethinkPush-->App: user access key
App-->Client: subscription url
Client->RethinkPush: open websocke
App->RethinkDB: push data via ReQL
RethinkDB-->RethinkPush: push change
Note left of RethinkPush: to subscribed user
RethinkPush-->Client: push data
App->RethinkPush: push data\nvia webhook
RethinkPush->RethinkDB: push data
```

**WebHook (call pop and chat pop)**
```sequence
App->RethinkPush: push data via REST
Note right of RethinkPush: to subscribed user
RethinkPush-->Client: push data
```

> **client**: web browser (use WebSocket)
> **app**: your application
> **RethinkPush**: push notification service
> **RethinkDB**: JSON doc storage (in lieu of Firebase)

## models
```bash
CHANNEL_TYPES = {
	"fanout": "everyone who is subscribing"
	"topic": "only memebers who subscribe the channel"
	"direct": "direct message to user"
}

table: users
{
	"id": "7644aaf2-9928-4231-aa68-4e65e31bf219",
	"username": "user_id_provided_by_app",
}

table: tokens
{
	"id": "abc4aaf2-9928-4231-aa68-4e65e31bfgge"
	"expire_dt": 23213131231
	"user_id": "7644aaf2-9928-4231-aa68-4e65e31bf219"
	"token": "superlogtokenthatwillbehandedofftoapp"
}

table: channels
{
	"name": "private-123",
	"type": "direct",
	"id": "543ad9c8-1744-4001-bb5e-450b2565d02c"
}

table: channels_users
{
	"channel_id": "543ad9c8-1744-4001-bb5e-450b2565d02c",
	"user_id": "7644aaf2-9928-4231-aa68-4e65e31bf219"
}
```
## APIs
```bash
authentication header
X-Rethinkpush-Key: <token>

POST: channels
	{
		"name": "public",
		"type": "fanout"
	}
	Response: 201 Created
GET: channels/:id

POST: users
	{
		"register_user": "unique_user_id"
	}
	Response: 200 OK
	{
		"token": "superlogtokenthatwillbehandedofftoapp",
		"channels": [
			"private-unique_user_id"
		]
	}
GET: users
GET: users/:id

POST: events
	{
		"channel": "private-unique_user_id",
		"data": {
			"key1": "value1",
			"key2": ["apple", "orange", "strawberry"]
		}
	}
	Response: 200 OK
```


### Start RethinkDB
check if docker-machine is runnign:
```bash
docker-machine status default
```

run RethinkDB docker
```bash
cd <project-root>
docker run --name rethink-io -v "$PWD:/data" -d -p 5002:8080 -p 28016:28015 rethinkdb
```

poiont browser to: http://docker.local.io:5002/ (supposedly you map your docker ip to the host on /etc/hosts)

to login rethinkdb container:
```bash
docker exec -it test-rethink bash
```

### Start web server to serve client app
```bash
cd <project-root>/http
python -m SimpleHTTPServer 8001
```

point your browser to ```<localhost>:8001```

### Start websocket server (Tornado)

```bash
cd <project-root>
source venv/bin/activate
cd server
python app.py
```

### Play with ReQL
```python
import rethinkdb as r
conn = r.connect( "docker.local.io", 28015)

# insert data
r.table("users").insert([
    { "name": "superman" , "email" : "super@email.com"},
    { "name": "spiderman" , "email" : "spider@email.com"}
]).run(conn)

# get data
cursor = r.table("users").run(conn)
for d in cursor: print(d)
```

### Roadmap
* save user data to db
* api
	* channel subscription system
	* authentication

 ref: https://www.rethinkdb.com/docs/introduction-to-reql/
