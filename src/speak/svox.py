import re
import subprocess
from tempfile import NamedTemporaryFile
import os

def speak_sampa(sampaphonemes):
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
