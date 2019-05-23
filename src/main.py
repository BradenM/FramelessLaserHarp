from machine import Pin, DAC, mem32
from micropython import const
import time

# GPIO Registrar Addresses
GPIO_REG = const(0x3ff44000)
GPIO_EN = const(0x8)
GPIO_CLR = const(0xC)

# Buck Voltage Control
vCtrlPin = Pin(25, Pin.OUT)
vCtrl = DAC(vCtrlPin, bits=8)

# Laser Pin
laserPin = Pin(21, Pin.OUT, value=1)
laserP = const(1 << 21)
mem32[GPIO_REG + GPIO_CLR] ^= laserP

# Speaker Pins
spQ1 = const(1 << 16)
spQ2 = const(1 << 17)
spQ3 = const(1 << 26)
spQ4 = const(1 << 27)
mem32[GPIO_REG + GPIO_CLR] ^= sum([spQ1, spQ2, spQ3, spQ4])


# Beam Step Points
steps = [255, 0]

# Initial Setup
vCtrl.write(255)
direction = 1


print("Ready...")
time.sleep(5)
while 1:
    for i in steps:
        mem32[GPIO_REG + GPIO_CLR] ^= laserP
        time.sleep_ms(10)
        vCtrl.write(i)
        time.sleep_ms(250)
        mem32[GPIO_REG + GPIO_EN] ^= laserP
        time.sleep_ms(1000)
    if direction:
        mem32[GPIO_REG + GPIO_EN] ^= spQ1 + spQ4
        mem32[GPIO_REG + GPIO_CLR] ^= spQ2 + spQ3
    else:
        mem32[GPIO_REG + GPIO_CLR] ^= spQ1 + spQ4
        mem32[GPIO_REG + GPIO_EN] ^= spQ2 + spQ3
    direction = not direction
