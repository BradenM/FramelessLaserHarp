from machine import Pin, DAC, mem32
from micropython import const
import time
import math

# GPIO Registrar Addresses
GPIO_REG = const(0x3ff44000)
GPIO_EN = const(0x8)
GPIO_CLR = const(0xC)

# Buck Voltage Control
vCtrlPin = Pin(25, Pin.OUT)
vCtrl = DAC(vCtrlPin, bits=8)
vCtrl.write(0)

# Speaker Driver & Laser Pin
spLeftPin = Pin(16, Pin.OUT, value=0)
spRightPin = Pin(17, Pin.OUT, value=0)
laserPin = Pin(21, Pin.OUT, value=1)
spLeft = const(1 << 16)
spRight = const(1 << 17)
laserP = const(1 << 21)

# Beam Step Points
steps = [255, 0]

# Initial Setup
vCtrl.write(255)
direction = 1
spLeftPin.value(not direction)
spRightPin.value(direction)


print("Ready...")
time.sleep(5)
while 1:
    for i in steps:
        mem32[GPIO_REG + GPIO_CLR] ^= laserP
        time.sleep_ms(10)
        vCtrl.write(i)
        time.sleep_ms(25)
        mem32[GPIO_REG + GPIO_EN] ^= laserP
        time.sleep_ms(100)
    if direction:
        mem32[GPIO_REG + GPIO_EN] ^= spRight
        mem32[GPIO_REG + GPIO_CLR] ^= spLeft
    else:
        mem32[GPIO_REG + GPIO_EN] ^= spLeft
        mem32[GPIO_REG + GPIO_CLR] ^= spRight
    direction = not direction
