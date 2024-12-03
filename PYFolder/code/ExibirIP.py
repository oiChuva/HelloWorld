import pyautogui as ag
import time

#digitar win R
time.sleep(1)
ag.hotkey('win', 'r')
#abrir o cmd
time.sleep(2)
ag.write("cmd.exe")
time.sleep(2)
ag.press('enter')
#digitar ipconfig
time.sleep(2)
ag.write('ipconfig/all')
time.sleep(1)
ag.press('enter')