import tinytuya
import pyautogui
from PIL import Image, ImageOps
import pytesseract
import cv2
from time import sleep
from scipy.interpolate import interp1d

def hexcolor(value):
    value = int(value)
    if value <= 50:
        r = 255
        g = int(255*value/50)
        b = 0
    else:
        r = int(255*(100-value)/50)
        g = 255
        b = 0
    return (r, g, b)


# Load text PCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

# Connect to LED Strip
d = tinytuya.BulbDevice('bf69b2a86f215887bbp19a', '192.168.1.151', 'ae8e6e02b3dbcb6a')
d.set_version(3.3)

# Screenshiot cutting
left = 585
top = 945
right = 860
bottom = 960

last = 100

while True:
    sleep(0.2)

    # Take screnshot and crop it
    ss = pyautogui.screenshot()
    image = ss.crop((left, top, right, bottom))

    # Get the health value
    text = pytesseract.image_to_string(image,lang='eng', config="-c tessedit_char_whitelist=0123456789/")
    text = text.rstrip()
    
    # Try to get clean health numbers
    try:
        hp, max = text.split("/")
        hp = int(hp)
        max = int(max)
    except:
        continue

    # Convert helath into percentage
    x = hp * 100/ max 
    print(hp, max, x)

    # Reset on respawn
    # if x == 100:
    #     last = 100
    
    # Ignore bugged values
    # if hp > max:
    #     continue

    # Prevent max health from bugging (orbitrary value)
    # if max > 20000:
    #     continue

    # Prevent sudden hp change bug
    # if last - x > 25:
    #     continue
    
    # Send the values
    r, g, b = hexcolor(x)
    d.set_colour(r, g, b)
    last = x
    