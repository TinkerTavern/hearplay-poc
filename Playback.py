import pyaudio
import wave
import sys

CHUNK = 1024

wf = wave.open("file.wav", 'rb')

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

data = wf.readframes(CHUNK)

while True:
    if data != '':
        stream.write(data)
        data = wf.readframes(CHUNK)

    if data == b'':
        break

stream.stop_stream()
stream.close()

p.terminate()