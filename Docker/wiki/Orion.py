from collections import defaultdict
import json
import base64
import logging
import requests
import pickle as pk

cygnus_ip = "192.168.1.51"


def tree():
    return defaultdict(tree)


def get_access_token(idm_host, user, password):
    logging.debug('getting auth token...')
    app = open('Fiware/dic/main_app.pckl', 'rb')
    main_app = pk.load(app)
    app.close()
    del app
    encoded = main_app['app_id'] + ":" + main_app['app_secret']
    encoded = 'BASIC ' + base64.b64encode(encoded.encode('ascii')).decode("utf-8")
    headers = {'Authorization': encoded, 'Content-Type': 'application/x-www-form-urlencoded'}
    payload = "grant_type=password&username=" + user + "&password=" + password + "&client_id=" + main_app['app_id'] +\
              "&client_secret=" + main_app['app_secret']
    try:
        response = requests.post(url=idm_host + '/oauth2/token', verify=False, data=payload, headers=headers)
        if response.status_code in (201, 200):
            token = json.loads(response.text)['access_token']
            logging.info('TOKEN --- ' + token)
            return token
        else:
            logging.error('GET TOKEN ### ' + response.text)
    except requests.exceptions.RequestException as e:
        return e


def get_all_entities(proxy, token):
    logging.debug('getting all ...')
    # headers = {'X-Auth-token': token, 'Fiware-ServicePath': '/Nodes'}
    headers = {'X-Auth-token': token, 'Fiware-ServicePath': '/Nodes'}
    response = requests.get(url=proxy + '/v2/entities/', headers=headers)
    if response.status_code in (201, 200):
        entities = response.text
        return entities
    else:
        return response.text
        logging.error('GET TOKEN ### ' + response.text)


def do_subs(orion, token):
    logging.debug('making subscriptions ...')
    headers = {'X-Auth-token': token, 'Fiware-ServicePath': '/Nodes', 'Content-Type': 'application/json'}
    root = tree()
    root['subject']['entities'] = [{"type": "nodo_aire", "idPattern": ".*"}]
    root['subject']['condition'] = {"attrs": []}
    root['notification']['http']['url'] = "http://" + cygnus_ip + ":5050/notify"
    root['notification']['attrs'] = []
    root['notification']['attrsFormat'] = "legacy"
    root['notification']['attrsFormat'] = "legacy"
    root['expires'] = "2099-12-31T23:00:00.00Z"
    root['throttling'] = 5
    json_payload = json.dumps(root, indent=4)
    response = requests.post(url=orion + '/v2/subscriptions', data=json_payload, headers=headers)
    if response.status_code in (201, 200):
        logging.info('subscription OK')
        print('subscription OK')
    else:
        logging.error('Error subscription ### ' + response.text)


class Node:

    def __init__(self, ident, contaminants, wheater, node,
                 location, dataobserved):
        self.ident = ident
        self.contaminants = contaminants
        self.wheater = wheater
        self.node = node
        self.location = location
        self.dataobserved = dataobserved

    def update(self, ident, contaminants, wheater, node,
               location, dataobserved, orion, token):
        self.ident = ident
        self.contaminants = contaminants
        self.wheater = wheater
        self.node = node
        self.location = location
        self.dataobserved = dataobserved
        logging.debug('updating entity...')
        headers = {'X-Auth-token': token, 'Fiware-ServicePath': '/Nodes',
                   'Content-Type': 'application/json', 'accept': 'application/json'}
        data = {"actionType": "UPDATE", "entities": [json.loads(str(self))]}
        payload = json.dumps(data, indent=4)
        response = requests.post(url=orion + '/v2/op/update',
                                 data=payload, headers=headers)
        if response.status_code in (204, 200):
            logging.info('node updated OK')
            print(' updated')
        else:
            print('error updating ### ' + response.text)

    def create_to_orion(self, orion, token):
        logging.debug('creating entity...')
        headers = {'X-Auth-token': token, 'Fiware-ServicePath': '/Nodes',
                   'Content-Type': 'application/json', 'accept': 'application/json'}
        response = requests.post(url=orion + '/v2/entities',
                                 data=self.__str__(), headers=headers)
        if response.status_code in (201, 200):
            logging.info('node created OK')
            print(' created')
        else:
            print('error created ### ' + response.text)

    def __str__(self):
        root = tree()
        root['id'] = self.ident
        root['type'] = "nodo_aire"
        root['contaminants']['value']['PM25'] = self.contaminants['PM25']
        root['contaminants']['value']['PM10'] = self.contaminants['PM10']
        root['contaminants']['value']['NO'] = self.contaminants['NO']
        root['contaminants']['value']['NO2'] = self.contaminants['NO2']
        root['contaminants']['value']['NOX'] = self.contaminants['NOX']
        root['contaminants']['value']['O3'] = self.contaminants['O3']
        root['contaminants']['value']['CO'] = self.contaminants['CO']
        root['contaminants']['value']['SO2'] = self.contaminants['SO2']
        root['contaminants']['type'] = "StructuredValue"
        root['wheater']['value']['winddirection'] = self.wheater['winddirection']
        root['wheater']['value']['relativehumidity'] = self.wheater['relativehumidity']
        root['wheater']['value']['pressure'] = self.wheater['pressure']
        root['wheater']['value']['precipitation'] = self.wheater['precipitation']
        root['wheater']['value']['temperature'] = self.wheater['temperature']
        root['wheater']['value']['windspeed'] = self.wheater['windspeed']
        root['wheater']['type'] = "StructuredValue"
        root['node']['value']['source'] = self.node['source']
        root['node']['value']['code'] = self.node['code']
        root['node']['value']['name'] = self.node['name']
        root['node']['value']['street'] = self.node['street']
        root['node']['type'] = "StructuredValue"
        root['location']['value'] = self.location
        root['location']['type'] = "geo:point"
        root['dataobserved']['value'] = self.dataobserved
        root['dataobserved']['type'] = "DateTime"
        payload = json.dumps(root, indent=4)
        return payload