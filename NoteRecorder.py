import pyaudio
import wave


class NoteRecorder():

    def __init__(self):
        self.__FORMAT = pyaudio.paInt16
        self.__CHANNELS = 2
        self.__RATE = 48000
        self.__CHUNK = 1024
        self.__RECORD_SECONDS = 5
        self.__WAVE_OUTPUT_FILENAME = "file.wav"


    def record(self):
        audio = pyaudio.PyAudio()

        # start Recording
        try:
            stream = audio.open(format=self.__FORMAT, channels=self.__CHANNELS,
                                rate=self.__RATE, input=True,
                                frames_per_buffer=self.__CHUNK)
        except OSError:
            stream = audio.open(format=self.__FORMAT, channels=1,
                                rate=self.__RATE, input=True,
                                frames_per_buffer=self.__CHUNK)
        print("recording...")
        frames = []

        for i in range(0, int(self.__RATE / self.__CHUNK * self.__RECORD_SECONDS)):
            data = stream.read(self.__CHUNK)
            frames.append(data)
        print("finished recording")

        # stop Recording
        stream.stop_stream()
        stream.close()
        audio.terminate()

        waveFile = wave.open(self.__WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(self.__CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(self.__FORMAT))
        waveFile.setframerate(self.__RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
