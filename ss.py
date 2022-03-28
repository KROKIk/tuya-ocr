import pyautogui
from PIL import Image, ImageOps

left = 585
top = 945
right = 860
bottom = 960

ss = pyautogui.screenshot()
image = ss.crop((left, top, right, bottom))

image.show()