#!/usr/bin/python3
#File for communicating with ATT TTS API

import http.client
from tempfile import NamedTemporaryFile
import subprocess
import os
import sys

def speak_att(ipa_phonemes):
    markup_items = ['<phoneme alphabet="ipa" ph="{}" />'.format(s) for s in ipa_phonemes]
    markup_body = ''.join(markup_items)

    markup = """<?xml version="1.0" encoding="utf-8"?>
    <speak version="1.0" 
        xmlns="http://www.w3.org/2001/10/synthesis">{}</speak>""".format(markup_body).encode(encoding='UTF-8')
    token = ''

    #print('Writing ' + markup.decode())

    with open('att_token', 'r') as f:
        token = f.read()

    conn = http.client.HTTPSConnection('api.att.com')
    headers = {
        'Accept' : 'audio/amr-wb',
        'Content-Type' : 'application/ssml+xml; charset=utf-8',
        'Authorization': 'Bearer ' + token,
        'VoiceName' : 'mike',
        'Content-Language' : 'en-US'
    }
    conn.request('POST', '/speech/v3/textToSpeech', markup, headers) 
    tf = NamedTemporaryFile(suffix='.amr', delete=False)
    tf.write(conn.getresponse().read())
    tf.close()

    subprocess.call(['gst-play-1.0', tf.name])
    os.unlink(tf.name)

if __name__ == '__main__':
    speak_att([sys.argv[1]])
