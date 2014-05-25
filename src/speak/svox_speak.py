#!/usr/bin/python3
import re
import subprocess
from tempfile import NamedTemporaryFile
import os
import sys
from subprocess import Popen, PIPE

def to_sampa(phonemes):
    sampaphonemes = []
    #doesn't look like svox works well with this sound
    phonemes = [s.replace('ɔ', 'ɒ').replace('i', 'ɪ').replace('a', 'ɒ') for s in phonemes] 
    for ph in phonemes:
        with Popen(['nodejs', 'src/speak/ipa-sampa.js', 'ipa2xsampa'], stdin=PIPE, stdout=PIPE) as ipa2xsampa:
            sampabytes = ipa2xsampa.communicate(input=ph.encode(encoding='UTF-8'))[0]
            sampaphonemes.append(sampabytes.decode(encoding='UTF-8'))
    return sampaphonemes

def speak_svox(sampaphonemes):
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
    
    xml_string = '<speed level="85">' + ''.join(sampa_xml_phonemes) + '</speed>'
    #Make a wave file with our xml tags
    tf = NamedTemporaryFile(suffix='.wav', delete=False)
    tf.close()
    #wave it up
    subprocess.call(['pico2wave', '-w', tf.name, xml_string], stdout=subprocess.DEVNULL)
    subprocess.call(['aplay', tf.name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    os.unlink(tf.name)

if __name__ == '__main__':
   speak_svox(to_sampa([sys.argv[1]])) 
