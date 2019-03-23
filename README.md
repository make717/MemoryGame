# MemoryGame
Python code for Memory Game running on custom PCB soldering badge

This requires the [Adafruit DotStar](https://github.com/adafruit/Adafruit_CircuitPython_DotStar/releases) library for Circuit Python. Make sure the *adafruit_dotstar.mpy* file is in the device's *lib* folder.

# Changing the Game
To update or change the code on the badge, simply plug it into a computer over the USB port. A new drive called "CIRCUITPY" should show up. You can now view the code by opening the files in a text editor (we recommend [Mu](https://codewith.mu/)). 

We've added some comments with the label *HACKING IDEA* to get you going. This includes changing the LED colors, updating the songs that are played, and making the game run faster.

# Drive not showing up?
Here's some things to try.
* Some USB cables are "charging only" cables. While this will let the badge turn on, you won't be able to edit the code.
* Make sure the switch (SW1) is moved toward the side that says "USB"
* Try removing the batteries and powering only over USB
