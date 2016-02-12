# RethinkPush

Works almost like firebase - Internal hosted solution powered by RethinkDB, Node.js, Express.js and Socket.IO

Data pushed to RethinkDB synchronized in realtime to every connected client via WebSocket

* Use of [RethinkDB](https://www.rethinkdb.com/) Changefeeds for Realtime messaging
* [Socket.IO](http://socket.io/) enables real-time bidirectional event-based communication. It works on every platform, browser or device, focusing equally on reliability and speed.

## How does it work
view sequence diagram in [stackedit.io](https://stackedit.io/editor)

**direct**

![alt text](http://www.plantuml.com/plantuml/img/NP0zRyCW48PtViLDtHZIqOei9Kwt3laQks3x52EZEm97ylUBdRGXtX3lytv0uooIw7hZVGMEBvPKFkhwY39O6lSf3XK4l2QC0i8ZplfQwmKWAT1Brxfkvk0AOcfZ5wmNomGfEFXuOisp-Is8FHBSiOtSZQWSimTbdEJxoR-2tWRiH06K8tVR2dosGs_4mCqQEEBXEqF_kbxKp7Gt6BgWGkgBYi-7_-jqNfGKngdcXoOkBnsOnpcZu8hdltO9__r5YpsaY66o_G80 "direct sequence diagram")

 * **client app**: web browser (use WebSocket)
 * **app**: RESTful API Server
 * **RethinkPush**: push notification service
 * **RethinkDB**: JSON doc storage (in lieu of Firebase)

## install dependencies
```bash
# test dependency
npm install -g mocha  
npm install
```

## how to run test
```bash
npm test
```

## JSON schema
```bash
{
	"title": "Message Schema",
	"type": "object",
	"properties": {
		"namespace": {
			"description": "resource identifier. e.g.: chat, case_count, notification",
			"type": "string"
		},
		"channel": {
			"description": "channel name e.g: uuid_for_private, public_for_broadcasting",
			"type": "string"
		},
		"message": {
			"description": "message to be consumed",
			"type": "object"
		}
	},
	"required": ["namespace", "channel", "message"]
}
```

## data example
```bash

r.db('notification').table('messages').insert({
	'namespace': 'chat',
  'channel': 'public',
  'message': {'greeting': 'Ahoy from RethinkDB'}
});

```

### Roadmap
* **docker or vagrant for quick up and running**
* **primitive authentication**
	* app wide secret key
* **add more tests and run on jenkins**
* **production provisioning with [pm2](https://github.com/Unitech/pm2)**
* add ts_to_send for scheduled notification
	* add filter on changes query
* REST api
	* post notification
	* subscription level authentication
* make record deletion optional after notification is sent

 ref:
 * [expressjs](http://expressjs.com/)
 * [rethinkdb](https://rethinkdb.com/blog/realtime-cluster-monitoring/)
 * [chai](http://chaijs.com/)
