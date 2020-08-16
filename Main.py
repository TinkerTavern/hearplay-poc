import sys
import time

from NotePlayer import NotePlayer
from NotePlayback import NotePlayback
from NoteRecorder import NoteRecorder

def playRound(roundNo):
    print("Playing round", roundNo)
    input("Press enter when ready")

    note.round(roundNo)
    input("Press enter to start recording")
    if roundNo == 5:
        record.record(10)
    else:
        record.record()
    print("Your attempt...")
    player.playBack()
    print("The original...")
    note.round(roundNo)
    time.sleep(2)
    print("\n")


note = NotePlayer()
record = NoteRecorder()
player = NotePlayback()

print("Welcome to the PlayByEar app!")
print("You will be asked to enter a number between 1 and 5 in a bit")
print("Once you have selected your level, you will be prompted to press enter to start")
print("When you do that, it will play a series of notes. Pay attention, as you will need to play these back")
print("You will then be prompted to press enter again, where it will record you playing it")
print("After that, you will hear your playback followed by the original to see if you match!")
print("Enjoy\n")

while True:
    ans = input("Please enter a number betwen 1 and 5 to play, or press q to quit: ")
    if ans in ["1", "2", "3", "4", "5"]:
        playRound(int(ans))
    elif ans == "q":
        sys.exit(0)
    else:
        print("Invalid input, please try again: ")
        time.sleep(1)
