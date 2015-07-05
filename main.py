import sys
from os import environ, path
import pyaudio
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

config = Decoder.default_config()
config.set_string('-hmm', path.join('model', 'en-us/en-us'))
config.set_string('-lm', path.join('model', 'en-us/en-us.lm.dmp'))
config.set_string('-dict', path.join('model', 'en-us/cmudict-en-us.dict'))
decoder = Decoder(config)

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
stream.start_stream()
in_speech_bf  = True
decoder.start_utt('')
while True:
    buf = stream.read(1024)
    if buf:
        decoder.process_raw(buf, False, False)
        try:
            if decoder.hyp().hypstr != '':
                print('Partial decoding result: {}'.format(decoder.hyp().hypstr))

        except AttributeError:
            pass

        if decoder.get_in_speech():
            sys.stdout.write('.')
            sys.stdout.flush()

        if decoder.get_in_speech() != in_speech_bf:
            in_speech_bf = decoder.get_in_speech()
            if not in_speech_bf:
                decoder.end_utt()
                try:
                    if decoder.hyp().hypst != '':
                        print('Stream decoding result: {}'.format(decoder.hyp().hypstr))
                except AttributError:
                    pass
                decoder.start_utt('')
    else:
        break
decoder.end_utt()
print('an error occured')
