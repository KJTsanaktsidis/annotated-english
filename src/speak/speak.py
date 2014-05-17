#!/usr/bin/python3
import sys
from subprocess import Popen, PIPE
import subprocess
import re
import os
from tempfile import NamedTemporaryFile
from svox import speak_sampa
#Contains the whole speaking chain!

#Read string from the command line
sentence = sys.argv[1]
words = sentence.split(" ")
wordblock = "\n".join(words)
phonemes = []
trace = True

#We might just want to speak
if sys.argv[1] == '--sampa':
    speak_sampa([sys.argv[2]])
    sys.exit()

#Open a pipe to each flookup stage sequentially
stages = ['fst/phase3{}.fst'.format(s) for s in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']]

if trace:
    print('Iniial:\t\t\t{} '.format(' :: '.join(words)))

phonemes = words

for stage in stages:
    print(stage)
    with Popen(['flookup', '-w', '', '-i', '-x', stage], stdin=PIPE, stdout=PIPE) as flookup:
        
        inblock = wordblock
        
        ipablockbytes = flookup.communicate(input=inblock.encode(encoding='UTF-8'))[0]
        ipablock = ipablockbytes.decode(encoding='UTF-8')
        phonemes = ipablock.split("\n")
        phonemes.remove('')

        if trace:
            print('{}:\t\t{}'.format(stage, ' :: '.join(phonemes)))

sampaphonemes = []

#We have our phonemes, let's SAMPA them
for ph in phonemes:
    with Popen(['nodejs', 'src/speak/ipa-sampa.js', 'ipa2xsampa'], stdin=PIPE, stdout=PIPE) as ipa2xsampa:
        sampabytes = ipa2xsampa.communicate(input=ph.encode(encoding='UTF-8'))[0]
        sampaphonemes.append(sampabytes.decode(encoding='UTF-8'))

print('Sampa:\t\t\t {}'.format(' :: '.join(sampaphonemes)))

speak_sampa(sampaphonemes)
