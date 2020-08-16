import time

from NotePlayer import NotePlayer
from NotePlayback import NotePlayback
from NoteRecorder import NoteRecorder

note = NotePlayer()
record = NoteRecorder()
player = NotePlayback()

note.round1()
record.record()
player.playBack()
note.round1()
time.sleep(2)

note.round2()
record.record()
player.playBack()
note.round2()
time.sleep(2)

note.round3()
record.record()
player.playBack()
note.round3()
time.sleep(2)

note.round4()
record.record()
player.playBack()
note.round4()
time.sleep(2)

note.round5()
record.record()
player.playBack()
note.round5()
time.sleep(2)
