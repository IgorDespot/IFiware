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

config.idm = {
	host: 'fiware-idm',
	port: 443,
	ssl: true
}

config.app = {
	host: 'orion',
	port: '1026',
	ssl: false // Use true if the app server listens in https
}


// Credentials obtained when registering PEP Proxy in app_id in Account Portal run first IDM.deploy and set this
config.pep = {
        app_id:    '05b69f39-b8da-4191-a2e0-7d2dc11987c0',
        username:  'pep_proxy_a3bfdb58-8650-492e-ab19-ebae69ae94a4',
        password:  'pep_proxy_9c23ae3c-720a-4fe8-991c-211e7c158708',
        trusted_apps : []
}
// in seconds
config.cache_time = 300;

// if enabled PEP checks permissions with AuthZForce GE. 
// only compatible with oauth2 tokens engine
//
// you can use custom policy checks by including programatic scripts 
// in policies folder. An script template is included there
config.azf = {
	enabled: true,
	protocol: 'http',
    host: 'authzforce',
    port: 8080,
    custom_policy: undefined // use undefined to default policy checks (HTTP verb + path).
};

// list of paths that will not check authentication/authorization
// example: ['/public/*', '/static/css/']
config.public_paths = [];

config.magic_key = undefined;

module.exports = config;
