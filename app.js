var express = require('express');
var http = require('http')
var socketio = require('socket.io')
var r = require("rethinkdb");

var db = require("./database.js")
var config = require('./config');

var app = express();
var server = http.createServer(app);
var io = socketio(server);

server.listen(config.port);

app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});
app.get('/user2', function(req, res){
  res.sendFile(__dirname + '/index2.html');
});

var chat = io.of('/chat')
var news = io.of('/news')
db.startServer(server, config.rethinkDB, {'chat': chat, 'news': news})
