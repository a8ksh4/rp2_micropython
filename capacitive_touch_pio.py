'''Analog stick module
Supports two analog pins, read and translate to x,y position.'''


from machine import ADC, Pin
import rp2
import time


CAP_SENSE_PIN = 22
CAP_TRESHOLD = 50000
COUNT_MAX = 0xFFFFFFFF
SM_FREQ = 1_000_000

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def cap_measure():
    wrap_target()
    set(pindirs, 1)               # output
    set(pins, 1)                  # charge high
    nop()                  [31]
    nop()                  [31]
    set(pindirs, 0)               # release -> input, starts falling
    mov(x, invert(null))          # x = 0xFFFFFFFF
    label("loop")
    jmp(pin, "still_high")        # pin high -> keep counting
    jmp("done")                   # pin low  -> done
    label("still_high")
    jmp(x_dec, "loop")
    label("done")
    mov(isr, x)
    push(noblock)
    wrap()
 
 
cap_pin = Pin(CAP_SENSE_PIN, Pin.OUT, value=0)
cap_sm = rp2.StateMachine(0, cap_measure, freq=SM_FREQ,
                       set_base=cap_pin, jmp_pin=cap_pin)
cap_sm.active(1)
 
 
def read_cap(samples=4):
    """Averaged count. Lower = touched, higher = open."""
    while cap_sm.rx_fifo():          # drain stale samples
        cap_sm.get()
    total = 0
    for _ in range(samples):
        total += COUNT_MAX - cap_sm.get()
    return total // samples


def cap_touched():
    return read_cap() < CAP_THRESHOLD


def print_cap_state():
    cap_time = read_cap()
    print("Cap state:", 'touched' if cap_time < CAP_TRESHOLD else 'open', cap_time)

