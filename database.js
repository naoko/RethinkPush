var r = require("rethinkdb");
const assert = require('assert');

var dbName = 'notification'
var dbTable = 'messages'

this.startServer = function(server, rConn, namespaces) {
  r.connect(rConn)
  .then(function(conn){
    initDB(conn, namespaces);
  })
  .error(function(e){
    console.log("db connection error! closing server")
    console.log(e)
    server.close();
  })
}

var initDB = function(conn, namespaces) {
  r.dbCreate(dbName).run(conn, function(err){
    if (!err) {
      console.log('db created')
    } else {
      if (err.name === 'ReqlOpFailedError') {
        console.log('db already exists')
      } else {
        throw err
      }
    }
    // create table
    r.db(dbName).tableCreate(dbTable).run(conn, function(err){
      if (!err) {
        console.log("table created")
      } else {
        console.log(err)
      }
    });

    // subscribe changes to table
    r.db(dbName).table(dbTable).changes().run(conn)
    .then(function(cursor) {
      cursor.each(function(err, item) {
        if (!err) {
          data = item.new_val;
          if (data) {
            assert(data.channel)
            namespace = data.namespace
            socket = namespaces[namespace]
            socket.emit(data.channel, {message: data.message});
            r.db(dbName).table(dbTable).filter({'id': data.id}).delete({returnChanges: false}).run(conn)
          } else {
            // must be delete event
          }
        } else {
          // handle error
        }
      });
    });

  });
}
