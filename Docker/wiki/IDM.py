from collections import defaultdict
import json
import logging
import requests
import pickle as pk




def tree():
    return defaultdict(tree)


# get token
def get_token(idm_host, user, password):
    logging.debug('getting token...')
    root = tree()
    root['name'] = user
    root['password'] = password
    json_payload = json.dumps(root, indent=4)
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url=idm_host + '/v3/auth/tokens', data=json_payload, headers=headers)
        if response.status_code in (201, 200):
            token = response.headers['X-Subject-Token']
            logging.info('TOKEN --- ' + token)
            return token
        else:
            return "error"
    except requests.exceptions.RequestException as e:
        return e


# create the main app
def create_app(idm_host, token, name, description, uri, url):
    logging.debug('creating app...')
    root = tree()
    root['application']['name'] = name
    root['application']['description'] = description
    root['application']['redirect_uri'] = uri
    root['application']['url'] = url
    root['application']['grant_type'] = ["authorization_code", "implicit", "password"]
    json_payload = json.dumps(root, indent=4)
    headers = {'X-Auth-token': token, 'Content-Type': 'application/json'}
    try:
        response = requests.post(url=idm_host + '/v1/applications', data=json_payload, headers=headers)
        if response.status_code in (201, 200):
            answer = json.loads(response.text)
            return answer['application']['id'], answer['application']['secret']
        else:
            return "error"
    except requests.exceptions.RequestException as e:
        return e


# Create PEPproxy arguments
def PEPproxy(idm_host, token, app_id):
    logging.debug('generating Pep elements...')
    headers = {'X-Auth-token': token, 'Content-Type': 'application/json'}
    try:
        response = requests.post(url=idm_host + '/v1/applications/' + app_id + '/pep_proxies', headers=headers)
        if response.status_code in (201, 200):
            answer = json.loads(response.text)
            return answer['pep_proxy']['id'], answer['pep_proxy']['password']
        else:
            return "error"
    except requests.exceptions.RequestException as e:
        return e


# Create user
def create_user(idm_host, token, name, email, password):
    logging.debug('creating user...')
    root = tree()
    root['user']['username'] = name
    root['user']['email'] = email
    root['user']['password'] = password
    json_payload = json.dumps(root, indent=4)
    headers = {'X-Auth-token': token, 'Content-Type': 'application/json'}
    try:
        response = requests.post(url=idm_host + '/v1/users', data=json_payload, headers=headers)
        if response.status_code in (201, 200):
            answer = json.loads(response.text)
            return answer['user']['id']
        else:
            return "error"
    except requests.exceptions.RequestException as e:
        return e


# create a permission
def create_permission(idm_host, token, app_id, name, action, resource):
    logging.debug('creating permission...')
    root = tree()
    root['permission']['name'] = name
    root['permission']['action'] = action
    root['permission']['resource'] = resource
    json_payload = json.dumps(root, indent=4)
    headers = {'X-Auth-token': token, 'Content-Type': 'application/json'}
    try:
        response = requests.post(url=idm_host + '/v1/applications/' + app_id + '/permissions',
                                 data=json_payload, headers=headers)
        if response.status_code in (201, 200):
            answer = json.loads(response.text)
            return answer['permission']['id']
        else:
            return "error"
    except requests.exceptions.RequestException as e:
        return e


# create roles
def create_role(idm_host, token, app_id, name):
    logging.debug('creating permission...')
    root = tree()
    root['role']['name'] = name
    json_payload = json.dumps(root, indent=4)
    headers = {'X-Auth-token': token, 'Content-Type': 'application/json'}
    try:
        response = requests.post(url=idm_host + '/v1/applications/' + app_id + '/roles',
                                 data=json_payload, headers=headers)
        if response.status_code in (201, 200):
            answer = json.loads(response.text)
            return answer['role']['id']
        else:
            return "error"
    except requests.exceptions.RequestException as e:
        return e


# Assign permission to role
def assign_permission(idm_host, token, app_id, role_id, permission_id):
    logging.debug('Assigning permission...')
    headers = {'X-Auth-token': token, 'Content-Type': 'application/json'}
    try:
        response = requests.post(url=idm_host + '/v1/applications/' + app_id + '/roles/' + role_id + '/permissions/' +
                                     permission_id, headers=headers)
        if response.status_code in (201, 200):
            logging.debug('ready...')
        else:
            logging.debug('error...')
    except requests.exceptions.RequestException as e:
        return e


# Assign role to user
def assign_role(idm_host, token, app_id, user_id, role_id):
    logging.debug('Assigning role...')
    headers = {'X-Auth-token': token, 'Content-Type': 'application/json'}
    try:
        response = requests.post(url=idm_host + '/v1/applications/' + app_id + '/users/' + user_id + '/roles/' +
                                 role_id, headers=headers)
        if response.status_code in (201, 200):
            logging.debug('ready...')
        else:
            logging.debug('error...')
    except requests.exceptions.RequestException as e:
        return e


#  Deploy App
def deploy_app(idm_host, user, password):
    name = 'Air2'
    description = 'Thesis application'
    uri = 'http://localhost/callback'
    url = 'http://localhost/'

    # Idm important values
    main_app = {'app_id': None, 'app_secret': None}
    token = get_token(idm_host, user, password)
    main_app['app_id'], main_app['app_secret'] = create_app(idm_host, token, name, description, uri, url)
    pep_id, pep_password = PEPproxy(idm_host, token, main_app['app_id'])
    app = open('main_app.pckl', 'wb')
    pk.dump(main_app, app)
    app.close()
    user_id = {}
    app = open('user_id.pckl', 'wb')
    user_id['freedom'] = create_user(idm_host, token, "freedom", "freedom@test.com", "freedom")
    user_id['App'] = create_user(idm_host, token, "App", "App@test.com", "App")
    user_id['Rios'] = create_user(idm_host, token, "Ríos", "rios@test.com", "blink182")
    pk.dump(user_id, app)
    app.close()
    permission_id = {}
    app = open('permission_id.pckl', 'wb')
    permission_id['get entities'] = create_permission(idm_host, token, main_app['app_id'], "get entities",
                                                      "GET", "v2/entities/")
    permission_id['publish entities'] = create_permission(idm_host, token, main_app['app_id'], "publish entities",
                                                          "POST", "v2/entities")
    permission_id['make a subscription'] = create_permission(idm_host, token, main_app['app_id'], "make a subscription",
                                                          "POST", "v2/subscriptions")
    permission_id['make an update'] = create_permission(idm_host, token, main_app['app_id'], "make an update",
                                                            "POST", "v2/op/update")
    pk.dump(permission_id, app)
    app.close()
    role_id = {}
    app = open('role_id.pckl', 'wb')
    role_id['freedom'] = create_role(idm_host, token, main_app['app_id'], "freedom")
    role_id['App'] = create_role(idm_host, token, main_app['app_id'], "App")
    role_id['Rios'] = create_role(idm_host, token, main_app['app_id'], "Rios")
    pk.dump(role_id, app)
    app.close()
    del app
    assign_permission(idm_host, token, main_app['app_id'], role_id['freedom'], permission_id['make an update'])
    assign_permission(idm_host, token, main_app['app_id'], role_id['App'], permission_id['get entities'])
    assign_permission(idm_host, token, main_app['app_id'], role_id['Rios'], permission_id['get entities'])
    assign_permission(idm_host, token, main_app['app_id'], role_id['Rios'], permission_id['publish entities'])
    assign_permission(idm_host, token, main_app['app_id'], role_id['Rios'], permission_id['make a subscription'])
    assign_permission(idm_host, token, main_app['app_id'], role_id['Rios'], permission_id['make an update'])
    assign_role(idm_host, token, main_app['app_id'], user_id['freedom'], role_id['freedom'])
    assign_role(idm_host, token, main_app['app_id'], user_id['App'], role_id['App'])
    assign_role(idm_host, token, main_app['app_id'], user_id['Rios'], role_id['Rios'])
    print(
        """Please open your PEPproxy config.js and set:
    config.pep = {{
        app_id:    '{app}',
        username:  '{user}',
        password:  '{password}',
        trusted_apps : []
    }}
    And run PEPproxy to continue
        """.format(app=main_app['app_id'], user=pep_id, password=pep_password))
