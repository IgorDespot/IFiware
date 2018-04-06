from collections import defaultdict
import json
import base64 
import logging
import requests

client_id = "e06c4df9f9ce4fd6ae3f364c41b37a2f"
client_secret = "4a9e3026a8b24a67b20c3a523f64542b"

def tree():
    return defaultdict(tree)

def get_token(keystone_url):
  logging.debug('getting token...')
  root=tree()
  root['auth']['identity']['methods']=["password"]
  root['auth']['identity']['password']['user']['name']= "idm"
  root['auth']['identity']['password']['user']['domain']['id']= "default"
  root['auth']['identity']['password']['user']['password']= password
  json_payload =json.dumps(root, indent=4)
  headers = {'Content-Type': 'application/json'}
  response = requests.post(url=keystone_url + '/v3/auth/tokens',
                                 data=json_payload,headers=headers)
  if response.status_code in (201, 200):
    token = response.headers['X-Subject-Token']
    logging.info('TOKEN --- ' + token)
    return token
  else:
    logging.error('GET TOKEN ### ' + response.text)

def create_user(keystone_url, token,usuario,nombre,password,correo):
  root=tree()
  root['userName'] = usuario
  root['displayname'] = nombre
  root['password'] = password
  root['emails']=[{"value": correo }]
  json_payload =json.dumps(root, indent=4)
  headers = {'X-Auth-token': token, 'Content-Type': 'application/json'}
  response = requests.post(url=keystone_url + '/v3/OS-SCIM/v2/Users/',
                                 data=json_payload, headers=headers)
  if response.status_code in (201, 200):
    logging.info(response.text)
        else:
            logging.error(response.text)

def get_access_token(keyrock_url,user,password):
    logging.debug('getting auth token...')
    encoded = client_id+":"+client_secret
    encoded = 'BASIC ' + base64.b64encode(encoded.encode('ascii')).decode("utf-8")
    headers = {'Authorization': encoded, 'Content-Type': 'application/x-www-form-urlencoded'}
    payload = "grant_type=password&username="+ user +"&password=" + password + "&client_id=" + client_id +"&client_secret=" + client_secret
    response = requests.post(url=keyrock_url + '/oauth2/token',
                             data=payload,headers=headers)
    if response.status_code in (201, 200):
        token = json.loads(response.text)['access_token']
        logging.info('TOKEN --- ' + token)
        return token
    else:
        logging.error('GET TOKEN ### ' + response.text)

def get_all_entities(orion,token):
    logging.debug('getting all ...')
    headers = {'X-Auth-token': token}
    response = requests.get(url=orion + '/v2/entities/', headers=headers)
    if response.status_code in (201, 200):
        entities = response.text
        return entities
    else:
        return response.text
        logging.error('GET TOKEN ### ' + response.text)
