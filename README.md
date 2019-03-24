# MemoryGame
Python code for Memory Game running on custom [Make717 PCB](https://github.com/make717gh/MemoryGame-PCB) soldering badge. When powered up, the badge will start with [main.py](https://github.com/make717gh/MemoryGame/blob/master/main.py) to display light patterns while waiting for input. Press either B1 or B4 to start the [soundboard.py](https://github.com/make717gh/MemoryGame/blob/master/soundboard.py). Pressing B2 or B3 will start the [game.py](https://github.com/make717gh/MemoryGame/blob/master/game.py).

This requires the [Adafruit DotStar](https://github.com/adafruit/Adafruit_CircuitPython_DotStar/releases) library for Circuit Python. Make sure the *adafruit_dotstar.mpy* file is in the device's *lib* folder.

# Changing the Game
To update or change the code on the badge, simply plug it into a computer over the USB port. A new drive called "CIRCUITPY" should show up. You can now view the code by opening the files in a text editor (we recommend [Mu](https://codewith.mu/)). 

We've added some comments with the label *HACKING IDEA* to get you going. This includes changing the LED colors, updating the songs that are played, and making the game run faster.

# Adding Hardware
The badge supports adding on more memory, an external clock, extending the DotStar lights, and other hardware hacks. Some hacks might require changes to the firmware. You can find schematics at [Make717 PCB](https://github.com/make717gh/MemoryGame-PCB) and builds of the firmware at our [CircuitPython fork](https://github.com/make717gh/circuitpython/releases). And if you need more help with your badge or soldering, visit us at [Make717](https://www.make717.org/).

# Troubleshooting
Drive not showing up?
* Some USB cables are "charging only" cables. While this will let the badge turn on, you won't be able to edit the code.
* Make sure the switch (SW1) is moved toward the side that says "USB"
* Try removing the batteries and powering only over USB

Button not working?
* Make sure nothing is touching the button triangles, then switch the power from Battery to USB (or back). The capacitive buttons need to be clear when the code starts or they won't measure the right capacitance.
