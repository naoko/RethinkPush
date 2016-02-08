process.env.NODE_ENV = 'test';

var assert = require('assert');
var chai = require('chai');
var chaiHttp = require('chai-http');
var server = require('../app');

chai.use(chaiHttp);

var should = chai.should();

describe('router', function() {
  it('should return 404 for bogus route', function (done) {
    chai.request(server)
      .get('/bogus')
      .end(function(err, res) {
        res.should.have.status(404);
        done();
      })
  });

  it('should serve index page ok', function (done) {
    chai.request(server)
      .get('/')
      .end(function(err, res) {
        should.equal(err, null);
        res.should.have.status(200);
        res.should.be.html;
        done();
      })
  });

  [2, 3].forEach(function (itemNumber) {
    it('should serve /user' + itemNumber + ' page ok', function (done) {
      chai.request(server)
        .get('/user' + itemNumber)
        .end(function(err, res) {
          should.equal(err, null);
          res.should.have.status(200);
          res.should.be.html;
          done();
        })
    })
  });

});
