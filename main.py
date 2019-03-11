# Memory Game "Simon Says"
# 3/10/2019 - For Make717 Board (SAMD21)

import time
import adafruit_dotstar
import board
import pulseio
import touchio
from random import randint


# Globals
num_pixels = 4
pixels = adafruit_dotstar.DotStar(board.SDA, board.SCL, num_pixels, brightness=0.2, auto_write=False)
pattern = []
sim_speed = 0.25
MAX_TIME = 5  # in seconds
MAX_ROUNDS = 100

# Setup Sound
buzzer = pulseio.PWMOut(board.D11, variable_frequency=True)
OFF = 0
ON = 2**15
    
# Colors
RED = (0x10, 0, 0)
YELLOW = (0x10, 0x10, 0)
GREEN = (0, 0x10, 0)
BLUE = (0, 0, 0x10)
BLACK = (0, 0, 0)

# Pixels/LEDs
PIXEL_LEFT = 0
PIXEL_RIGHT = 2
PIXEL_TOP = 1
PIXEL_BOTTOM = 3
SIM = [
    { 
        'button': touchio.TouchIn(board.A0),
        'light': PIXEL_LEFT,
        'color': GREEN,
        'tone': 995
    },
    {
        'button': touchio.TouchIn(board.A1),
        'light': PIXEL_RIGHT,
        'color': YELLOW,
        'tone': 939
    },
        { 
        'button': touchio.TouchIn(board.A4),
        'light': PIXEL_TOP,
        'color': BLUE,
        'tone': 837
    },
    {
        'button': touchio.TouchIn(board.A5),
        'light': PIXEL_BOTTOM,
        'color': RED,
        'tone': 790
    }
]

    
def setup():
    pixels.fill((0, 0, 0))
    pixels.show()
    buzzer.frequency = 1500
    buzzer.duty_cycle = ON
    time.sleep(0.5)
    buzzer.duty_cycle = OFF


def make_pattern(level):
    choice = randint(0, (len(SIM) - 1))
    pattern.append(choice)


def show_pattern():
    for p in pattern:
        start_tone(SIM[p]['tone'])
        pixels[SIM[p]['light']] = SIM[p]['color']
        pixels.show()
        time.sleep(sim_speed * 2)
        stop_tone()
        pixels[SIM[p]['light']] = BLACK
        pixels.show()
        time.sleep(sim_speed)


def user_input_loop():
    start_time = time.monotonic()
    last_press = None
    pattern_place = 0
    
    while time.monotonic() < (start_time + MAX_TIME):
        x = check_button_press()
        if x != last_press:
            
            # If the button was released, turn out lights
            if x is None:
                pixels.fill((0, 0, 0))
                pixels.show()
                last_press = None
                stop_tone()
                
                # Check for win state
                if pattern_place == len(pattern):
                    time.sleep(.6)
                    return True
                continue

            # This should be a new button press
            # light up the color next to button
            pixels.fill((0, 0, 0))
            pixels[SIM[x]['light']] = SIM[x]['color']
            pixels.show()
            start_tone(SIM[x]['tone'])
            
            # check if it was the right button
            if pattern[pattern_place] == x:
                # Good choice
                print("Good choice")
                pattern_place += 1
            else:
                time.sleep(.2)
                stop_tone()
                wrong_choice(pattern[pattern_place], x)
                return False
    
        last_press = x
    print("Time Out")
    wrong_choice(pattern[pattern_place], 0)
    return False

    
def check_button_press():
    for i in range(len(SIM)):
        if SIM[i]["button"].value:
            return i
    return None


def wrong_choice(correct, incorrect):
    print("Wrong choice")
    start_tone(300)
    # Blink the right choice a few times
    for i in range(5):
        pixels.fill((0, 0x10, 0x10))
        pixels[SIM[correct]['light']] = SIM[correct]['color']
        pixels.show()
        time.sleep(.25)
        pixels.fill((0, 0, 0))
        pixels.show()       
        time.sleep(.25)
    stop_tone()

        
def main():
    global sim_speed, pattern
    
    while True:
        for i in range(MAX_ROUNDS):
            make_pattern(i)
            show_pattern()
            good_round = user_input_loop()
            
            # Check for incorrect answer
            if not good_round:
                break
            
            # Speed up each time we add a new pattern
            sim_speed = sim_speed - 0.05
            time.sleep(1.0)

        print("Starting new round")    
        pattern = []
        sim_speed = 0.5
        time.sleep(3)


# Audio Code
def start_tone(frequency):
    buzzer.frequency = frequency 
    buzzer.duty_cycle = ON
        
def stop_tone():
    buzzer.duty_cycle = OFF


# Start main code
setup()
main()
