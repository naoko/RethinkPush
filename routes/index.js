var express = require('express');
var path = require('path');
var router = express.Router();

var publicDir = path.resolve('public');

router.get('/', function(req, res){
  res.sendFile(publicDir + '/index.html');
})

router.get('/user:id', function(req, res){
  res.sendFile(publicDir + '/index' + req.params.id + '.html');
});

module.exports = router;
