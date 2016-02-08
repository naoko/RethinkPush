var express = require('express');
var router = express.Router();

router.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
})

router.get('/user2', function(req, res){
  res.sendFile(__dirname + '/index2.html');
});
