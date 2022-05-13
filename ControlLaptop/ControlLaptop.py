#!/usr/bin/python3
import time
from os import system

system('clear')
t = "00:45:00".split(':')
st = ":".join(t)
time_in_seconds = int(t[0]) * 3600 + int(t[1]) * 60 + int(t[2])
system("zenity --warning --text '45 minutes remaining'")
while True:
    print("\x1b[%d;%dH" % (1, 1), end="")
    print(time_in_seconds)
    time_in_seconds = time_in_seconds - 1
    time.sleep(1)
    if time_in_seconds == 60:
        system("zenity --warning --text 'Less than minute left to stop everything'")
    if time_in_seconds < 1:
        break
system('xset dpms force off')
