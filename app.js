var express = require('express');
var http = require('http')
var socketio = require('socket.io')
var r = require("rethinkdb");

var routes = require('./routes/index.js');
var db = require("./database.js")
var config = require('./config');

var app = express();

app.use('/', routes);
var server = http.createServer(app);
var io = socketio(server);

server.listen(config.port[app.settings.env]);

var chat = io.of('/chat')
var news = io.of('/news')
db.startServer(server, config.rethinkDB, {'chat': chat, 'news': news})

module.exports = app;
