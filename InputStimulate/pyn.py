from pynput.mouse import Button, Controller
from time import sleep 
sleep(3)
mouse = Controller()
mouse.scroll(0, -3)
