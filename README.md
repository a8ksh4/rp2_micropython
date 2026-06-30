# rp2_micropython
Test code for rp2 boards with micropython incl pio

** INDEX **
* all_pins_print_pio.py
* capacitive_touch_pio.py
* encoder_wheel_pio.py
* paintbrush_pin_bitshift_pio.py

## all_pins_print_pio.py
Simple pio tool to print the state, in binary, of all pins in a loop.

## capacitive_touch_pio.py
This works with the steamdeck joystick capacitive touch sensor (at least my firt gen lcd).  There is a test pad near the ribbon connector you can solder to to use this.  Wiring with the rp board is like:  
  
gpio_pin -> test_pad -> 1k_ohm_resostor -> big_touch_solder_pad -> joystick_touch_pad

The general process is this:
* set gpio pin to output pin
* set pin high for 5ms to charge the sensor
* set pin to input pin
* recort current time
* loop on pin check and sleep 1ms until pin reports low
* If time to report low is below a threshold, a touch is detected. 

I'm seeing 50ms to go low when touched and I think timeout at 1s when not touched (takes a lot longer to go low).  This can be done in software, but it's annoying to have to spin on a pin for 1/20th of a second to check touch.  So this is a good application for pio to handle in the background and report discharge times via fifo.

## encoder_wheel_pio.py
This should work with any 3 pin (ground, A, B) encoder wheel, or be pretty easily adaptable to wheels with additional signal pins since it tracks state and records changes on the fifo.  There is no traffic if the wheel isn't touched, and the pio program doesn't need to know that it's an encoder wheel since it only reports changes to pin states.


## matrix_scan_pio.py
Will this work?  Sholud be able to matrix scan and report a matrix of keys as large as 1x32, 2x16, 3x10, 4x8, or 5x6 keys - up to 32 bits data.  Matrix shapes supported might depend on how the code works.

## paintbrush_pin_bitshift_pio.py
"Paintbrush" is a 2x4 (8 key) keyboard used for artsey.io layout.
It uses non-contiguous pins, but in our pio script, we can read
 in all the pins and bitshift their values with the scratch registers
to track and output state changes for only the pins corresponding 
with the buttons.


