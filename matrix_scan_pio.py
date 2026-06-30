

###############################################
# Keyboard Matrix Scanner and State Reporting #
###############################################
# set pins_in_base for the read pins, and pins_side_base
# for the driven pins (either rows/cols depending on diodie
# orientation)
# Can we assume max 16 pins on either and step through those?
# Hmmmm.....
# We'll assume 4 driven rows and 6 read cols
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def  matrix_monitor():
    '''PIO program to matrix scan a keyboard with up to 32 keys (could use two
    instances for each half of a larger keyboard) and push any state changes to
    the ouotput fifo.
    We step through the output pins one at a time and shift
    the state of the input pins to the OSR.
    Then we push the osr to the fifo and start over.'''
    mov(y, invert(null))

    label("loop")
    move(osr, null)
    move(isr, null)

    set(pins, 0x0001)
    in_(pins, 6)
    set(pins, 0x0010)
    in_(pins, 6)
    set(pins, 0x0100)
    in_(pins, 6)
    set(pins, 0x1000)
    in_(pins, 6)

    mov(x, isr)
    jmp(x_not_y, "state_changed")
    jmp("loop")

    label("state_changed")
    mov(y, x)
    push(noblock)
    jmp("loop")


def repeat_print_binary(sm):
    '''Wait for anything in the fifo and return it.'''
    while True:
        if not sm.rx_fifo():
            time.sleep(0.01)
            continue
        state = sm.get()
        print("pins: {:032b}".format(state))


in_pins = [1, 2, 3, 4, 5, 6]
in_pins = [Pin(p) for p in in_pins]
out_pins = [7, 8, 9, 10]
out_pins = [Pin(p) for p in out_pins]
sm = rp2.StateMachine(0, matrix_monitor, in_base=in_pins[0], out_base=out_pins[0])
repeat_print_bainry(sm)

