var config = {};

// Used only if https is disabled
config.pep_port = 80;

// Set this var to undefined if you don't want the server to listen on HTTPS
config.https = {
    enabled: false,
    cert_file: 'cert/cert.crt',
    key_file: 'cert/key.key',
    port: 443
};

config.account_host = 'http://192.168.1.51:8000';

config.keystone_host = 'http://192.168.1.51';
config.keystone_port = 5000;

config.app_host = 'http://192.168.1.51';  
config.app_port = '1026';
// Use true if the app server listens in https
config.app_ssl = false;

// Credentials obtained when registering PEP Proxy in Account Portal
config.username = 'pep_proxy_154de9ea954248d9904a2c66d52b5e0b';
config.password = '7252ed4b0cce469cb70fb6d436e69798';

// in seconds
config.cache_time = 300;

// if enabled PEP checks permissions with AuthZForce GE. 
// only compatible with oauth2 tokens engine
//
// you can use custom policy checks by including programatic scripts 
// in policies folder. An script template is included there
config.azf = {
    enabled: false,     //TESTES: reativar
    host: 'authzforce', //usar o nome do container (o --link cria a entrada no hosts)
    port: 8080,
    path: '/authzforce/domains/',
    custom_policy: undefined, // use undefined to default policy checks (HTTP verb + path).
    protocol: 'http'
};

// list of paths that will not check authentication/authorization
// example: ['/public/*', '/static/css/']
config.public_paths = [];

// options: oauth2/keystone
config.tokens_engine = 'oauth2';

config.magic_key = undefined;

module.exports = config;
