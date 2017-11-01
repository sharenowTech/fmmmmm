import requests
from config import fmm_int_config, fmm_hack_config, fmm_auth_token_config
from pymongo import MongoClient

client_int = MongoClient(
    host=fmm_int_config['host'],
    port=fmm_int_config['port'],
    document_class=dict,
    username=fmm_int_config['username'],
    password=fmm_int_config['password'],
    readPreference=fmm_int_config['readPreference']
)

common_int = client_int.get_database('common')
fmm_int = client_int.get_database('fmm')


client_hack = MongoClient(
    host=fmm_hack_config['host'],
    port=fmm_hack_config['port'],
    document_class=dict,
    username=fmm_hack_config['username'],
    password=fmm_hack_config['password'],
    readPreference=fmm_hack_config['readPreference']
)

common_hack = client_hack.get_database('common')
fmm_hack = client_hack.get_database('fmm')

api_credentials = requests.post(
    fmm_auth_token_config['url'],
    json=fmm_auth_token_config['json']
).json()['serviceResponse']['payLoadData']['authorization']

userId = api_credentials['userId']
accessToken = api_credentials['accessToken']