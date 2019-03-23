# Soundboard 
# 3/21/2019 - For Make717 Board (SAMD21)
import time
import adafruit_dotstar
import board
import pulseio
import touchio
from random import randint

buzzer = None

# Colors for LED lights
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
    
PIXEL_LEFT = 0
PIXEL_RIGHT = 2
PIXEL_TOP = 1
PIXEL_BOTTOM = 3

SIM = [
    { 
        'button': touchio.TouchIn(board.B2),
        'light': PIXEL_LEFT,
        'color': GREEN,
        'tone': 995
    },
    {
        'button': touchio.TouchIn(board.B3),
        'light': PIXEL_RIGHT,
        'color': YELLOW,
        'tone': 939
    },
        { 
        'button': touchio.TouchIn(board.B4),
        'light': PIXEL_TOP,
        'color': BLUE,
        'tone': 837
    },
    {
        'button': touchio.TouchIn(board.B1),
        'light': PIXEL_BOTTOM,
        'color': RED,
        'tone': 790
    }
]

# Audio Code
def start_tone(frequency):
    buzzer.frequency = frequency 
    buzzer.duty_cycle = 2**15
        
def stop_tone():
    buzzer.duty_cycle = 0

def play_startup_song():
    start_tone(880)
    time.sleep(.2)
    stop_tone()
    start_tone(932)
    time.sleep(.2)
    stop_tone()
    start_tone(988)
    time.sleep(.2)
    stop_tone()
    start_tone(1047)
    time.sleep(.2)
    stop_tone()
    
def main():
    global buzzer
    
    num_pixels = 4
    pixels =  adafruit_dotstar.DotStar(board.SDA, board.SCL, num_pixels, brightness=0.2, auto_write=False)
    buzzer = pulseio.PWMOut(board.BUZZER, variable_frequency=True)
    play_startup_song()
        
    # Main loop for checking tones
    print("starting soundboard loop")
    last_frequency = 0
    while True:
        frequency = 0
        pixels.fill((0, 0, 0))

        for i in range(len(SIM)):
            if SIM[i]["button"].value:
                print("Pressed", i)
                frequency += SIM[i]["tone"]
                pixels[SIM[i]['light']] = SIM[i]['color']

        pixels.show()

        # If this is a new frequency, stop the old one
        if last_frequency != frequency:
            stop_tone()
            
        if frequency > 0:
            start_tone(frequency)
        
        # Remember what our frequency is
        last_frequency = frequency
        time.sleep(0.01)
        
