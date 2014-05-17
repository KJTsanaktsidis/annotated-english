#!/usr/bin/python3
#Get a token from ATT for speaking

import http.client
import json
import urllib.parse

app_key = 'ksm0trvhpkcupjvjaqxpeglczp39lkpr'
app_secret = '3frjalpnr5n7cn5kndk9wmfbve33dcmk'

headers = {
    'Accept' : 'application/json'
}
reqdata = {
    'grant_type' : 'client_credentials',
    'client_id' : app_key,
    'client_secret' : app_secret,
    'scope' : 'TTS'
}

conn = http.client.HTTPSConnection('api.att.com')
reqstring = urllib.parse.urlencode(reqdata)
conn.request('POST', '/oauth/token', reqstring, headers)
restext = conn.getresponse().read().decode()
resobj = json.loads(restext)

token = resobj['access_token']

#write the token off

with open('att_token', 'w') as f:
    f.write(token)
