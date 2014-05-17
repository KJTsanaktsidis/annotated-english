#!/usr/bin/python3
import sys
from subprocess import Popen, PIPE
import subprocess
import re
import os
from tempfile import NamedTemporaryFile
from svox_speak import speak_svox, to_sampa
from att_speak import speak_att
#Contains the whole speaking chain!

#Read string from the command line
engine = sys.argv[1]
sentence = sys.argv[2]
words = sentence.split(" ")
wordblock = "\n".join(words)
phonemes = []
trace = True

#Open a pipe to each flookup stage sequentially
stages = ['fst/phase3{}.fst'.format(s) for s in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']]

if trace:
    print('Iniial:\t\t\t{} '.format(' :: '.join(words)))

phonemes = words

for stage in stages:
    with Popen(['flookup', '-w', '', '-i', '-x', stage], stdin=PIPE, stdout=PIPE) as flookup:
        
        inblock = wordblock
        
        ipablockbytes = flookup.communicate(input=inblock.encode(encoding='UTF-8'))[0]
        ipablock = ipablockbytes.decode(encoding='UTF-8')
        phonemes = ipablock.split("\n")
        phonemes.remove('')

        if trace:
            print('{}:\t{}'.format(stage, ' :: '.join(phonemes)))

sampaphonemes = to_sampa(phonemes)

print('Sampa:\t\t\t {}'.format(' :: '.join(sampaphonemes)))

if engine == '--att':
    speak_att(phonemes)
elif engine == '--svox':
    speak_svox(sampaphonemes)
