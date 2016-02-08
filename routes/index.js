var express = require('express');
var path = require('path');
var router = express.Router();

var publicDir = path.resolve('public');

router.get('/', function(req, res){
  res.sendFile(publicDir + '/index.html');
})

router.get('/user2', function(req, res){
  res.sendFile(publicDir + '/index2.html');
});

module.exports = router;
