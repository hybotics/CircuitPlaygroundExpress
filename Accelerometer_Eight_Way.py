# The MIT License (MIT)
#
# Copyright (c) 2017 Scott Shawcroft for Adafruit Industries LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# Accelerometer example.
# Reads the accelerometer x, y, z values and prints them every tenth of a second.
# Open the serial port after running to see the output printed.
# Author: Tony DiCola
#
# Version:  0.2.1
# Date:     26-Mar-2018
# Purpose;  Added SENSITIVITY parameter to allow tuning tilt sensitivity
# Author:   Dale Weber <hybotics@hybotics.org>
#
# Version:  0.2.0
# Date:     21-Mar-2018
# Purpose;  Corrected backwards orientation of board; added color
# Author:   Dale Weber <hybotics@hybotics.org>
#
# Version:  0.1.0
# Date:     15-Mar-2018
# Purpose:  Added the tiltDirection function to get tilt direction
# Author:   Dale Weber <hybotics@hybotics.org>
#
import time
import board
import busio
import neopixel
import adafruit_lis3dh

# Change this to alter the sensitivity of the tilt detection.
# Greater makes the detection less sensitive, and less makes it more
#   sensitive.
# Positive values ONLY, since this is handled in detection
SENSITIVITY = 300

RED = 0x100000 # (0x10, 0, 0) also works
YELLOW=(0x10, 0x10, 0)
GREEN = (0, 0x10, 0)
AQUA = (0, 0x10, 0x10)
BLUE = (0, 0, 0x10)
PURPLE = (0x10, 0, 0x10)
BLACK = (0, 0, 0)

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=.1)
pixels.show()

# Hardware I2C setup on CircuitPlayground Express:
i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19)

# Set range of accelerometer (can be RANGE_2_G, RANGE_4_G, RANGE_8_G or RANGE_16_G).
lis3dh.range = adafruit_lis3dh.RANGE_2_G

def tiltDirection(x, y, z):
  xm, ym, zm = int(x * 1000), int(y * 1000), int(z * 1000)
  print('xm = {0}, ym = {1}, zm = {2}'.format(xm, ym, zm))

  if (xm > -SENSITIVITY) and (xm < SENSITIVITY) and (ym < SENSITIVITY) and (ym > -SENSITIVITY):
    # Level
    return 1
  elif (ym > SENSITIVITY) and (xm > SENSITIVITY):
    # Bacward and right
    return 2
  elif (ym > SENSITIVITY) and (xm < -SENSITIVITY):
    # Backward and left
    return 3
  elif (ym < -SENSITIVITY) and (xm > SENSITIVITY):
    # Forward and right
    return 4
  elif (ym < -SENSITIVITY) and (xm < -SENSITIVITY):
    # Forward and left
    return 5
  elif (xm > SENSITIVITY):
    # Left
    return 6
  elif (xm < -SENSITIVITY):
    # Right
    return 7
  elif (ym > SENSITIVITY):
    # Backward
    return 8
  elif (ym < -SENSITIVITY):
    # Forward
    return 9
  else:
    # Invalid
    return 0

def showTiltDirection(tilt):
  if (tilt == 1):
    print("Leveled Out")
    pixels[0] = BLUE
    pixels[4] = BLUE
    pixels[5] = BLUE
    pixels[9] = BLUE
    pixels[1] = BLUE
    pixels[3] = BLUE
    pixels[6] = BLUE
    pixels[8] = BLUE
    pixels.show()
  elif (tilt == 2):
    print("Tilting Backward and Left")
    pixels[3] = PURPLE
    pixels[4] = PURPLE
    pixels.show()
  elif (tilt == 3):
    print("Tilting Backward and Right")
    pixels[5] = PURPLE
    pixels[6] = PURPLE
    pixels.show()
  elif (tilt == 4):
    print("Tilting Forward and Left")
    pixels[0] = PURPLE
    pixels[1] = PURPLE
    pixels.show()
  elif (tilt == 5):
    print("Tilting Forward and Right")
    pixels[8] = PURPLE
    pixels[9] = PURPLE
    pixels.show()
  elif (tilt == 6):
    print("Tilting Left")
    pixels[1] = GREEN
    pixels[3] = GREEN
    pixels.show()
  elif (tilt == 7):
    print("Tilting Right")
    pixels[6] = GREEN
    pixels[8] = GREEN
    pixels.show()
  elif (tilt == 8):
    print("Tilting Backward")
    pixels[4] = GREEN
    pixels[5] = GREEN
    pixels.show()
  elif (tilt == 9):
    print("Tilting Forward")
    pixels[0] = GREEN
    pixels[9] = GREEN
    pixels.show()

  print("Result = {0}".format(tilt))

# Loop forever printing accelerometer values
while True:
  # Read accelerometer values (in m / s ^ 2).  Returns a 3-tuple of x, y,
  # z axis values.  Divide them by 9.806 to convert to Gs.
  x, y, z = lis3dh.acceleration
  print("x = {0:.4f}, y = {1:.4f}, z = {2:.4f}".format(x, y, z))

  xG, yG, zG = x / 9.806, y / 9.806, z / 9.806
  print("xG = {0:.4f}G, yG = {1:.4f}G, zG = {2:.4f}G".format(xG, yG, zG))

  tilt = tiltDirection(x, y, z)
  showTiltDirection(tilt)

  print()

  time.sleep(2)
  pixels.fill(BLACK)
  pixels.show()
