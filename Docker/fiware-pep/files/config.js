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
	host: '172.24.1.11',
	port: 443,
	ssl: true
}

config.app = {
	host: '172.24.1.7',
	port: '1026',
	ssl: false // Use true if the app server listens in https
}


// Credentials obtained when registering PEP Proxy in app_id in Account Portal run first IDM.deploy and set this
config.pep = {
        app_id:    '4fb44ebe-7f78-4a21-8247-a9b56cea7d60',
        username:  'pep_proxy_1b4a9ebb-b4e8-42bc-b2d5-0dedcf63ae56',
        password:  'pep_proxy_be24322b-2ec2-4cdb-a0de-25bd501dcf24',
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
    host: '172.24.1.10',
    port: 8080,
    custom_policy: undefined // use undefined to default policy checks (HTTP verb + path).
};

// list of paths that will not check authentication/authorization
// example: ['/public/*', '/static/css/']
config.public_paths = [];

config.magic_key = undefined;

module.exports = config;
