import math
import time
from operator import itemgetter

import numpy
import pyaudio
from scipy import interpolate


class NotePlayer:

    def __init__(self):
        self.__noteDic = {"Null": 0,
                          "C0": 16.3516,
                          "D♭0": 17.32391,
                          "C♯0": 17.32391,
                          "D0": 18.35405,
                          "E♭0": 19.44544,
                          "D♯0": 19.44544,
                          "E0": 20.60172,
                          "F0": 21.82676,
                          "G♭0": 23.12465,
                          "F♯0": 23.12465,
                          "G0": 24.49971,
                          "A♭0": 25.95654,
                          "G♯0": 25.95654,
                          "A0": 27.5,
                          "B♭0": 29.13524,
                          "A♯0": 29.13524,
                          "B0": 30.86771,
                          "C1": 32.7032,
                          "D♭1": 34.64783,
                          "C♯1": 34.64783,
                          "D1": 36.7081,
                          "E♭1": 38.89087,
                          "D♯1": 38.89087,
                          "E1": 41.20344,
                          "F1": 43.65353,
                          "G♭1": 46.2493,
                          "F♯1": 46.2493,
                          "G1": 48.99943,
                          "A♭1": 51.91309,
                          "G♯1": 51.91309,
                          "A1": 55,
                          "B♭1": 58.2704,
                          "A♯1": 58.2704,
                          "B1": 61.73541,
                          "C2": 65.40639,
                          "D♭2": 69.29566,
                          "C♯2": 69.29566,
                          "D2": 73.41619,
                          "E♭2": 77.78175,
                          "D♯2": 77.78175,
                          "E2": 82.40689,
                          "F2": 87.30706,
                          "G♭2": 92.49861,
                          "F♯2": 92.49861,
                          "G2": 97.99886,
                          "A♭2": 103.8262,
                          "G♯2": 103.8262,
                          "A2": 110,
                          "B♭2": 116.540,
                          "A♯2": 116.540,
                          "B2": 123.4708,
                          "C3": 130.8128,
                          "D♭3": 138.5913,
                          "C♯3": 138.5913,
                          "D3": 146.8324,
                          "E♭3": 155.5635,
                          "D♯3": 155.5635,
                          "E3": 164.8138,
                          "F3": 174.6141,
                          "G♭3": 184.9972,
                          "F♯3": 184.9972,
                          "G3": 195.9977,
                          "A♭3": 207.6523,
                          "G♯3": 207.6523,
                          "A3": 220,
                          "B♭3": 233.081,
                          "A♯3": 233.081,
                          "B3": 246.9417,
                          "C4": 261.6256,
                          "D♭4": 277.1826,
                          "C♯4": 277.1826,
                          "D4": 293.6648,
                          "E♭4": 311.127,
                          "D♯4": 311.127,
                          "E4": 329.6276,
                          "F4": 349.2282,
                          "G♭4": 369.9944,
                          "F♯4": 369.9944,
                          "G4": 391.9954,
                          "A♭4": 415.3047,
                          "G♯4": 415.3047,
                          "A4": 440,
                          "B♭4": 466.1638,
                          "A♯4": 466.1638,
                          "B4": 493.8833,
                          "C5": 523.2511,
                          "D♭5": 554.3653,
                          "C♯5": 554.3653,
                          "D5": 587.3295,
                          "E♭5": 622.254,
                          "D♯5": 622.254,
                          "E5": 659.2551,
                          "F5": 698.4565,
                          "G♭5": 739.9888,
                          "F♯5": 739.9888,
                          "G5": 783.9909,
                          "A♭5": 830.6094,
                          "G♯5": 830.6094,
                          "A5": 880,
                          "B♭5": 932.327,
                          "A♯5": 932.327,
                          "B5": 987.7666,
                          "C6": 1046.502,
                          "D♭6": 1108.731,
                          "C♯6": 1108.731,
                          "D6": 1174.659,
                          "E♭6": 1244.508,
                          "D♯6": 1244.508,
                          "E6": 1318.51,
                          "F6": 1396.913,
                          "G♭6": 1479.978,
                          "F♯6": 1479.978,
                          "G6": 1567.982,
                          "A♭6": 1661.219,
                          "G♯6": 1661.219,
                          "A6": 1760,
                          "B♭6": 1864.65,
                          "A♯6": 1864.65,
                          "B6": 1975.533,
                          "C7": 2093.005,
                          "D♭7": 2217.461,
                          "C♯7": 2217.461,
                          "D7": 2349.318,
                          "E♭7": 2489.016,
                          "D♯7": 2489.016,
                          "E7": 2637.02,
                          "F7": 2793.826,
                          "G♭7": 2959.955,
                          "F♯7": 2959.955,
                          "G7": 3135.963,
                          "A♭7": 3322.438,
                          "G♯7": 3322.438,
                          "A7": 3520,
                          "B♭7": 3729.3,
                          "A♯7": 3729.3,
                          "B7": 3951.066,
                          "C8": 4186.009,
                          "D♭8": 4434.922,
                          "C♯8": 4434.922,
                          "D8": 4698.636,
                          "E♭8": 4978.032,
                          "D♯8": 4978.032,
                          "E8": 5274.041,
                          "F8": 5587.652,
                          "G♭8": 5919.911,
                          "F♯8": 5919.911,
                          "G8": 6271.927,
                          "A♭8": 6644.875,
                          "G♯8": 6644.875,
                          "A8": 7040,
                          "B♭8": 7458.6,
                          "A♯8": 7458.6,
                          "B8": 7902.133
                          }

    def sine(self, frequency, length, rate):
        length = int(length * rate)
        factor = float(frequency) * (math.pi * 2) / rate
        return numpy.sin(numpy.arange(length) * factor)

    def shape(self, data, points, kind='slinear'):
        items = points.items()
        sorted(items, key=itemgetter(0))
        keys = list(map(itemgetter(0), items))
        vals = list(map(itemgetter(1), items))
        interp = interpolate.interp1d(keys, vals, kind=kind)
        factor = 1.0 / len(data)
        shape = interp(numpy.arange(len(data)) * factor)
        return data * shape

    def harmonics1(self, freq, length):
        a = self.sine(freq * 1.00, length, 44100)
        b = self.sine(freq * 2.00, length, 44100) * 0.5
        c = self.sine(freq * 4.00, length, 44100) * 0.125
        return (a + b + c) * 0.2

    def harmonics2(self, freq, length):
        a = self.sine(freq * 1.00, length, 44100)
        b = self.sine(freq * 2.00, length, 44100) * 0.5
        return (a + b) * 0.2

    def pluckNumber(self, note, length=1.0):
        chunk = self.harmonics1(list(self.__noteDic.values())[note], length)
        return self.shape(chunk, {0.0: 0.0, 0.005: 1.0, 0.25: 0.5, 0.9: 0.1, 1.0: 0.0})

    def pluckNote(self, note, length=1.0):
        chunk = self.harmonics1(self.__noteDic[note], length)
        return self.shape(chunk, {0.0: 0.0, 0.005: 1.0, 0.25: 0.5, 0.9: 0.1, 1.0: 0.0})

    def chord(self, n, scale):
        root = scale.get(n)
        third = scale.transpose(root, 2)
        fifth = scale.transpose(root, 4)
        return self.pluckNumber(root) + self.pluckNumber(third) + self.pluckNumber(fifth)

    def round1(self):
        chunks = []
        chunks.append(self.pluckNote("C4", 0.75))
        chunks.append(self.pluckNote("C4", 0.75))
        chunks.append(self.pluckNote("C4", 1))
        self.play(chunks)

    def round2(self):
        chunks = []
        chunks.append(self.pluckNote("C4", 0.3))
        chunks.append(self.pluckNote("D4", 0.3))
        chunks.append(self.pluckNote("E4", 0.3))
        chunks.append(self.pluckNote("F4", 0.3))
        chunks.append(self.pluckNote("G4", 0.5))
        self.play(chunks)

    def round3(self):
        chunks = []
        chunks.append(self.pluckNote("A3", 0.5))
        chunks.append(self.pluckNote("C4", 0.5))
        chunks.append(self.pluckNote("E4", 0.5))
        chunks.append(self.pluckNote("Null", 0.1))
        chunks.append(self.pluckNote("A3") + self.pluckNote("C4") + self.pluckNote("E4"))
        self.play(chunks)

    # A#7 F#6
    def round4(self):
        chunks = []
        chunks.append(self.pluckNote("A♯5", 0.4) + self.pluckNote("F♯4", 0.4))
        chunks.append(self.pluckNote("A♯5", 0.2) + self.pluckNote("F♯4", 0.2))
        chunks.append(self.pluckNote("A♯5", 0.2) + self.pluckNote("F♯4", 0.2))
        chunks.append(self.pluckNote("A♯5", 0.2) + self.pluckNote("F♯4", 0.2))
        chunks.append(self.pluckNote("D♯4", 0.4) + self.pluckNote("G♯5", 0.4))
        chunks.append(self.pluckNote("D♯4", 0.4) + self.pluckNote("G♯5", 0.4))
        chunks.append(self.pluckNote("C♯4", 0.4) + self.pluckNote("F♯5", 0.4))
        chunks.append(self.pluckNote("C♯4", 0.4) + self.pluckNote("F♯5", 0.4))
        chunks.append(self.pluckNote("D♯4", 0.4) + self.pluckNote("G♯5", 0.4))
        self.play(chunks)

    def round5(self):
        chunks = []
        chunks.append(self.pluckNote("E4", 0.4))
        chunks.append(self.pluckNote("D4", 0.4))
        chunks.append(self.pluckNote("C4", 0.4))
        chunks.append(self.pluckNote("D4", 0.4))
        chunks.append(self.pluckNote("E4", 0.4))
        chunks.append(self.pluckNote("E4", 0.4))
        chunks.append(self.pluckNote("E4"))
        chunks.append(self.pluckNote("D4", 0.4))
        chunks.append(self.pluckNote("D4", 0.4))
        chunks.append(self.pluckNote("D4"))
        chunks.append(self.pluckNote("E4", 0.4))
        chunks.append(self.pluckNote("G4", 0.4))
        chunks.append(self.pluckNote("G4"))
        self.play(chunks)

    def play(self, chunks):
        chunks.append(self.pluckNote("Null", 0.1))
        chunk = numpy.concatenate(chunks) * 0.25

        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=1)
        stream.write(chunk.astype(numpy.float32).tostring())
        stream.close()
        p.terminate()
        time.sleep(1)
