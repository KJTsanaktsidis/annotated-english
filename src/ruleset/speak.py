#!/usr/bin/python
import sys
from subprocess import Popen, PIPE
import subprocess
import re
import os
from tempfile import NamedTemporaryFile

#Contains the whole speaking chain!

#Read string from the command line
sentence = sys.argv[1]
words = sentence.split(" ")
wordblock = "\n".join(words)
phonemes = []
trace = True

#Open a pipe to each flookup stage sequentially
stages = ['phase3{}.fst'.format(s) for s in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']]

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
            print('{}:\t\t{}'.format(stage, ' :: '.join(phonemes)))

sampaphonemes = []

#We have our phonemes, let's SAMPA them
for ph in phonemes:
    with Popen(['nodejs', 'ipa-sampa.js', 'ipa2xsampa'], stdin=PIPE, stdout=PIPE) as ipa2xsampa:
        sampabytes = ipa2xsampa.communicate(input=ph.encode(encoding='UTF-8'))[0]
        sampaphonemes.append(sampabytes.decode(encoding='UTF-8'))

print('Sampa:\t\t\t {}'.format(' :: '.join(sampaphonemes)))

#XML escape our sampa by doing something clever
replace_dict = {
    "\\" : "\\\\",
    "\"" : "\\\""
}

regex = re.compile("(%s)" % "|".join(map(re.escape, replace_dict.keys())))
sampa_escape = lambda s: \
                    regex.sub(lambda mo: replace_dict[mo.string[mo.start():mo.end()]], s)

sampa_escaped_phonemes = [sampa_escape(s) for s in sampaphonemes]
#And bundle it all up in xml tags
sampa_xml_phonemes = ['<phoneme alphabet="xsampa" ph="{}" />'.format(s) for s in sampa_escaped_phonemes]

xml_string = ''.join(sampa_xml_phonemes)
#Make a wave file with our xml tags
tf = NamedTemporaryFile(suffix='.wav', delete=False)
tf.close()
#wave it up
subprocess.call(['pico2wave', '-w', tf.name, xml_string])
subprocess.call(['aplay', tf.name])

os.unlink(tf.name)
