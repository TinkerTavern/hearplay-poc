import math
import numpy
import pyaudio
import itertools
from scipy import interpolate
from operator import itemgetter


class Note:

  NOTES = ['c','c#','d','d#','e','f','f#','g','g#','a','a#','b']

  def __init__(self, note, octave=4):
    self.octave = octave
    if isinstance(note, int):
      self.index = note
      self.note = Note.NOTES[note]
    elif isinstance(note, str):
      self.note = note.strip().lower()
      self.index = Note.NOTES.index(self.note)

  def transpose(self, halfsteps):
    octave_delta, note = divmod(self.index + halfsteps, 12)
    return Note(note, self.octave + octave_delta)

  def frequency(self):
    base_frequency = 16.35159783128741 * 2.0 ** (float(self.index) / 12.0)
    return base_frequency * (2.0 ** self.octave)

  def __float__(self):
    return self.frequency()


class Scale:

  def __init__(self, root, intervals):
    self.root = Note(root.index, 0)
    self.intervals = intervals

  def get(self, index):
    intervals = self.intervals
    if index < 0:
      index = abs(index)
      intervals = reversed(self.intervals)
    intervals = itertools.cycle(self.intervals)
    note = self.root
    for i in range(index):
      note = note.transpose(next(intervals))
    return note

  def index(self, note):
    intervals = itertools.cycle(self.intervals)
    index = 0
    x = self.root
    while x.octave != note.octave or x.note != note.note:
      x = x.transpose(next(intervals))
      index += 1
    return index

  def transpose(self, note, interval):
    return self.get(self.index(note) + interval)

class NotePlayer():

  def sine(self, frequency, length, rate):
    length = int(length * rate)
    factor = float(frequency) * (math.pi * 2) / rate
    return numpy.sin(numpy.arange(length) * factor)

  def shape(self, data, points, kind='slinear'):
      items = points.items()
      sorted(items,key=itemgetter(0))
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

  def pluck1(self, note, length=1):
    chunk = self.harmonics1(note.frequency(), length)
    return self.shape(chunk, {0.0: 0.0, 0.005: 1.0, 0.25: 0.5, 0.9: 0.1, 1.0:0.0})

  def pluck2(self, note, length=1):
    chunk = self.harmonics2(note.frequency(), length)
    return self.shape(chunk, {0.0: 0.0, 0.5:0.75, 0.8:0.4, 1.0:0.1})

  def chord(self, n, scale):
    root = scale.get(n)
    third = scale.transpose(root, 2)
    fifth = scale.transpose(root, 4)
    return self.pluck1(root) + self.pluck1(third) + self.pluck1(fifth)


  def __init__(self):
    root = Note('A', 3)
    scale = Scale(root, [2, 1, 2, 2, 1, 3, 1])

    chunks = []
    chunks.append(self.pluck1(scale.get(21),0.5))
    chunks.append(self.pluck1(scale.get(23),0.5))
    chunks.append(self.pluck1(scale.get(25),0.5))
    chunks.append(self.chord(21, scale))

    chunk = numpy.concatenate(chunks) * 0.25

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=1)
    stream.write(chunk.astype(numpy.float32).tostring())
    stream.close()
    p.terminate()