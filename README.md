# RP2-SENT_TX
SENT Protocol Transmitter using Raspberry Pi Pico with PIO on MicroPython.
Written by Dmitriy Levchenkov (arithmechanics.com), 2021

*I am not a MicroPython guru. Any suggestions to restructure or improve the code are welcome. Always check signal timing with an oscilloscope or logic analyzer*

# Installation
Install MicroPython on your RP2
Upload script to RP2:
ampy --port /dev/ttyACM0  put SENT_Tx.py

Connect oscilloscope to GPIO16. This should get an inverted signal.
Optionally, create a MOSFET driver as shown in the PNG file.

Run your favorite terminal program (e.g., Putty). Execute:

```
from machine import Pin
from SENT_Tx import SENT_Tx
sent_tx = SENT_Tx(Pin(16))
sent_tx.s_da(9, [0,0,1,0xe,0xf,0xf])
sent_tx.s_12_12R(6, 1000, 1500)
sent_tx.raw(0x91234567, calc_crc=True)
```
