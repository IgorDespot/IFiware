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
	host: 'localhost',
	port: 443,
	ssl: true
}

config.app = {
	host: 'localhost',
	port: '1026',
	ssl: false // Use true if the app server listens in https
}


// Credentials obtained when registering PEP Proxy in app_id in Account Portal run first IDM.deploy and set this
config.pep = {
        app_id:    '30f38b53-842b-4d7a-8dd3-0c54774b842e',
        username:  'pep_proxy_9d0019c5-617f-4878-8fdc-aab6b3e67dc0',
        password:  'pep_proxy_9640d95a-4dc9-4878-b4d2-f6b01786f767',
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
    host: 'localhost',
    port: 8080,
    custom_policy: undefined // use undefined to default policy checks (HTTP verb + path).
};

// list of paths that will not check authentication/authorization
// example: ['/public/*', '/static/css/']
config.public_paths = [];

config.magic_key = undefined;

module.exports = config;
