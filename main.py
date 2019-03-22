# Startup LED Badge
# 3/20/2019 - For Make717 Board (SAMD21)
# Functions examples
# https://learn.adafruit.com/circuitpython-essentials/circuitpython-dotstar

import time
import adafruit_dotstar
import board
import pulseio
import touchio
from random import randint
import game

# Globals based on our board
num_pixels = 4
pixels = adafruit_dotstar.DotStar(board.SDA, board.SCL, num_pixels, brightness=0.05, auto_write=False)
pattern = []

# Define the RGB colors we'll be using
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
ORANGE = (255, 40, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
MAGENTA = (255, 0, 20)

# HACKING IDEA: What other colors could you create?
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Use the game code to detect button presses
def check_button_press():
    # HACKING IDEA: What else could you call from the game code?
    if game.check_button_press():
        print("Go to Game")
        pixels.deinit()
        game.setup()
        game.main()

# Function for color transitions
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

# Color transition each LED in a cycle
def rainbow_cycle(wait):
    # HACKING IDEA: Could you show more than 32 colors?
    for j in range(32):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(rc_index & 255)
        pixels.show()
        check_button_press()
        time.sleep(wait)

# Make all the lights display a color
def color_fill(color, wait):
    pixels.fill(color)
    pixels.show()
    check_button_press()
    time.sleep(wait)

# Light up one LED at a time clockwise
def chase(color, wait):
    for i in range(num_pixels):
        pixels.fill((0,0,0))
        pixels[i] = color
        pixels.show()
        check_button_press()
        time.sleep(wait)

# Light up one LED at a time counter-clockwise
def chaseback(color,wait):
    for i in range(num_pixels):
        i = (num_pixels -1) - i
        pixels.fill((0,0,0))
        pixels[i] = color
        pixels.show()
        check_button_press()
        time.sleep(wait)

# Powersave with checking for button presses
def goblack(wait):
    pixels.fill((0,0,0))
    pixels.show()
    for i in range(wait):
        check_button_press()
        time.sleep(1)

# Main loop - Do these LED patterns
while True:
    # HACKING IDEA: make your own pattern for the lights
    chase(RED, 0.05)
    chase(YELLOW, 0.05)
    chase(GREEN, 0.05)
    chaseback(BLUE, 0.05)
    chaseback(PURPLE, 0.05)
    color_fill(MAGENTA, 0.5)
    rainbow_cycle(0)
    goblack(3)
