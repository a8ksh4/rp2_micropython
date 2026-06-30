'''simple moudle to print the state of all gpio pins repeatedly using pio.
It conveniently uses binary print representation.
'''

from machine import Pin
import rp2
import time


#######################################
# Report all pins every iter          #
#######################################
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def report_pins():
    in_(pins, 30)
    # mov(osr, isr)
    push()
    nop()   [29]
    nop()   [29]
    nop()   [29]
    nop()   [29]
    nop()   [29]
    nop()   [29]
    nop()   [29]

def repeat_print_binary(sm):
    '''Wait for anything in the fifo and return it.'''
    while True:
        if not sm.rx_fifo():
            time.sleep(0.01)
            continue
        state = sm.get()
        print("pins: {:032b}".format(state))

print(1)
pins = range(30)
pins = [Pin(p, Pin.IN, Pin.PULL_UP) for p in pins]
sm = rp2.StateMachine(0, report_pins, freq=2000, set_base=Pin(pins[0]))
sm.active(1)
print(2)
repeat_print_binary(sm)

print(3)

