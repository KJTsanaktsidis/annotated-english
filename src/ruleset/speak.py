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
ipablock = ""

print('Wordblock: {}\n'.format(wordblock))

#Open a pipe to flookup...
with Popen(['flookup', '-w', '', '-i', '-x', 'all.fst'], stdin=PIPE, stdout=PIPE) as flookup:
    ipablockbytes = flookup.communicate(input=wordblock.encode(encoding='UTF-8'))[0]
    ipablock = ipablockbytes.decode(encoding='UTF-8')

phonemes = ipablock.split("\n")

print('Phonemes: {}\n'.format(phonemes))

sampaphonemes = []

#We have our phonemes, let's SAMPA them
for ph in phonemes:
    with Popen(['nodejs', 'ipa-sampa.js', 'ipa2xsampa'], stdin=PIPE, stdout=PIPE) as ipa2xsampa:
        sampabytes = ipa2xsampa.communicate(input=ph.encode(encoding='UTF-8'))[0]
        sampaphonemes.append(sampabytes.decode(encoding='UTF-8'))

print('Sampa: {}\n'.format(sampaphonemes))

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

print('XML string: {}\n'.format(xml_string))

#Make a wave file with our xml tags
tf = NamedTemporaryFile(suffix='.wav', delete=False)
tf.close()
#wave it up
subprocess.call(['pico2wave', '-w', tf.name, xml_string])
subprocess.call(['aplay', tf.name])

os.unlink(tf.name)
