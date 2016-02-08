var config = {};

config.port = {
  'test': 9001,
  'development': 9000
}
config.rethinkDB = {
  host: 'docker.local.io',
  port: '28016'
};

module.exports = config;
