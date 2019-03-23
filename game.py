# Memory Game "Simon Says"
# 3/20/2019 - For Make717 Board (SAMD21)

import time
import adafruit_dotstar
import board
import pulseio
import touchio
from random import randint


# Globals
num_pixels = 4
pixels = None
pattern = []
sim_speed = 0.25
sim_speed_min = 0.015
MAX_TIME = 5  # in seconds
MAX_ROUNDS = 100

# Setup Sound output and variables
buzzer = None
OFF = 0
ON = 2**15
    
# Colors for LED lights
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Define the order of LEDs
PIXEL_LEFT = 0
PIXEL_RIGHT = 2
PIXEL_TOP = 1
PIXEL_BOTTOM = 3

# Map the buttons, LEDs, Colors and Tone
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

# Setup the LEDS and let the user know we're about to start a game
def setup():
    global pixels, buzzer
    pixels = adafruit_dotstar.DotStar(board.SDA, board.SCL, num_pixels, brightness=0.2, auto_write=False)
    buzzer = pulseio.PWMOut(board.BUZZER, variable_frequency=True)
    pixels.fill((80, 80, 80))
    pixels.show()
    buzzer.frequency = 1500
    buzzer.duty_cycle = ON
    time.sleep(0.3)
    buzzer.duty_cycle = OFF
    pixels.fill((0, 0, 0))
    pixels.show()

# Choose the next LED in the pattern
def make_pattern(level):
    choice = randint(0, (len(SIM) - 1))
    pattern.append(choice)

# Play back the current memory pattern
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

# Timed loop to see if the player enters the right pattern in time
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

# Return which button is currently pressed. Will only return the first one held.
def check_button_press():
    for i in range(len(SIM)):
        if SIM[i]["button"].value:
            return i
    return None

# What to do if the wrong pattern is entered.
def wrong_choice(correct, incorrect):
    print("Wrong choice")
    pixels.fill((0x10, 0x0, 0x0))
    pixels.show()
    play_sad_song()
    # Blink the right choice a few times
    for i in range(5):
        pixels.fill((0x10, 0x0, 0x0))
        pixels[SIM[correct]['light']] = SIM[correct]['color']
        pixels.show()
        time.sleep(.25)
        pixels.fill((0, 0, 0))
        pixels.show()       
        time.sleep(.25)
    stop_tone()

# Try making your own song. You can find notes/tones at
# https://www.arduino.cc/en/Tutorial/toneMelody
def play_sad_song():
    start_tone(1047)
    time.sleep(.5)
    stop_tone()
    start_tone(988)
    time.sleep(.5)
    stop_tone()
    start_tone(932)
    time.sleep(.5)
    stop_tone()
    start_tone(880)
    # make sure stop_tone() happens in your calling code

# The main game code lives here        
def main():
    global sim_speed, pattern
    
    #Save this value for when the game resets
    start_speed = sim_speed

    while True:
        for i in range(MAX_ROUNDS):
            make_pattern(i)
            show_pattern()
            good_round = user_input_loop()
            
            # Check for incorrect answer
            if not good_round:
                break
            
            # Speed up each time we add a new pattern
            sim_speed = sim_speed - 0.005
            # Check that we don't go negative time
            if sim_speed < sim_speed_min:
                sim_speed = sim_speed_min
            time.sleep(.5)

        print("Starting new round")
        # Reset the variables for a new round
        pattern = []
        sim_speed = start_speed
        time.sleep(2)


# Audio Code
def start_tone(frequency):
    buzzer.frequency = frequency 
    buzzer.duty_cycle = ON
        
def stop_tone():
    buzzer.duty_cycle = OFF


# Start main code
# setup()
# main()