import pyautogui as ag
import time

i = 1
time.sleep(2)
ag.hotkey('Alt', 'Tab')

while i < 4:
    time.sleep(2)
    ag.click(x=608, y=529)
    time.sleep(2)
    ag.click(x=715, y=436)
    time.sleep(2)
    i = i + 1
time.sleep(2)
ag.hotkey('Alt', 'Tab')
print("Finalizado")