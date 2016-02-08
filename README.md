# RethinkPush with RethinkDB + socket.io

* Use of RethinkDB Changefeeds for Realtime messaging

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

## for testing
```bash
npm install -g mocha
npm install
npm test
```

## data schema
```bash

r.db('notification').table('messages').insert({
	'namespace': 'chat',
  'channel': 'public',
  'message': 'Ahoy from RethinkDB'
});

```


### Roadmap
* add more test
* production provisioning with [pm2](https://github.com/Unitech/pm2)
* add ts_to_send for scheduled notification
	* add filter on changes query
* primitive authentication
	* app wide secret key
* REST api
	* post notification
	* subscription level authentication

 ref:
 * [expressjs](http://expressjs.com/)
 * [rethinkdb](https://rethinkdb.com/blog/realtime-cluster-monitoring/)
 * [chai](http://chaijs.com/)
