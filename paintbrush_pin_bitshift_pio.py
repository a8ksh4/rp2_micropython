

import rp2
from machine import Pin
import time
import gc

PB_PINS = (10, 18, 19, 20, 26, 27, 28, 29)

@rp2.asm_pio(autopush=False, autopull=False,
            #in_shiftdir=rp2.PIO.SHIFT_RIGHT,
            #out_shiftdir=rp2.PIO.SHIFT_RIGHT
             )
def bitshift_track_changes():
    mov(y, invert(null))

    label("loop")
    mov(osr, null)
    mov(isr, null)
    in_(null, 2)
    in_(pins, 30)

    # Move pin data to OSR and zero ISR
    mov(osr, isr)
    mov(isr, null)

    # Use X to bitshift pins from OSR to ISR
    # 00111100000111000000010000000000
    out(null, 2)
    out(x, 4)
    in_(x, 4)
    out(null, 5)
    out(x, 3)
    in_(x, 3)
    out(null, 7)
    out(x, 1)
    in_(x, 1)

    # Copy back to scratch X for comparison with Y
    mov(x, isr)

    # Check for state change
    jmp(x_not_y, "changed")
    jmp("loop")

    label("changed")
    # Save state to Y scratch register
    mov(y, x)

    # Copy state to OSR to push to tx fifo
    mov(osr, x)
    push(noblock)       # push #1:  raw values
    jmp("loop")


sm = rp2.StateMachine(1, bitshift_track_changes, freq=2000)
sm.active(1)

while True:
    if not sm.rx_fifo():
        continue
    state = sm.get()
    print("raw  {:032b}".format(state))
    # state = state | 0b00011111111110001111111111111111
    # state = state |  0b11100000000001110000000000000000 
    # print("flip {:032b}".format(state))
    # state = (state |  0b11100000000001110000000000000000) ^ 0b11101111111111110000111110001111
    # print("flip {:032b}".format(state))
    # state = sm.get()
    # print("osr  {:032b}".format(state))
    # state = sm.get()
    # print("isr  {:032b}".format(state))
    # print()

