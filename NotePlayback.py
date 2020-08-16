import pyaudio
import wave
import sys

class NotePlayback():

    def __init__(self):
        self.__CHUNK = 1024

    def playBack(self):
        wf = wave.open("file.wav", 'rb')

        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(self.__CHUNK)

        while True:
            if data != '':
                stream.write(data)
                data = wf.readframes(self.__CHUNK)

            if data == b'':
                break

        stream.stop_stream()
        stream.close()

        p.terminate()