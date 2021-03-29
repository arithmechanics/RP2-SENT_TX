#SENT Protocol Transmission Library for Raspberry Pi Pico
#Written by Dmitriy Levchenkov (arithmechanics.com), 2021
#See usage examples at the bottom
#Confirm timing of output by an oscilloscope or logic analyzer

import rp2

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def sent_tx_pio():
     pull()
     set(pins,1) [5]
     set(pins,0) [31]
     nop() [16]
     set(y,7)
     label("out_nibbles")
     set(pins,1) [3]
     set(x,0)
     out(x,4)
     set(pins,0) [3]
     label("bitloop")
     jmp(x_dec, "bitloop")
     jmp(y_dec, "out_nibbles")
     set(pins,1) [5]
     set(pins,0) [31]
     nop() [31]

SENTcrcLookup = [0,13,7,10,14,3,9,4,1,12,6,11,15,2,8,5]

class SENT_Tx:
    def __init__(self, out_pin, sm_id=0):
        self.out_pin = out_pin
        self.sm = rp2.StateMachine(sm_id, sent_tx_pio, freq=333333, set_base=out_pin)
        self.sm.active(1)

    def activate(self):
        self.sm.active(1)

    def deactivate(self):
        self.sm.active(0)

    def raw(self, all_nibbles_32, calc_crc=False):
        if calc_crc:
            crc = SENTcrcLookup[5]
            tmp = all_nibbles_32 << 4
            for i in range(6):
                data_nibble = (tmp & 0xf0000000) >> 28
                crc ^= data_nibble
                crc = SENTcrcLookup[crc]
                tmp <<= 4
            all_nibbles_32 = (all_nibbles_32 & 0xfffffff0) | crc
        self.sm.put(all_nibbles_32)

    def s_da(self, status, data_array):
        all_nibbles_32 = status & 0xf
        crc = SENTcrcLookup[5]
        for i in range(6):
            all_nibbles_32 <<= 4
            data_nibble = data_array[i] & 0xf
            all_nibbles_32 |= data_nibble
            crc ^= data_nibble
            crc = SENTcrcLookup[crc]
        all_nibbles_32 <<= 4
        all_nibbles_32 |= crc
        self.sm.put(all_nibbles_32)

    def s_12_12R(self, status, d1, d2):
        data_array = [ (d1 & 0xf00)>>8, (d1 & 0xf0)>>4, d1 & 0xf, d2 & 0xf, (d2 & 0xf0)>>4, (d2 & 0xf00)>>8]
        self.s_da(status, data_array)

#from machine import Pin
#from SENT_Tx import SENT_Tx
#sent_tx = SENT_Tx(Pin(16))
#sent_tx.s_da(9, [0,0,1,0xe,0xf,0xf])
#sent_tx.s_da(5, [0,0,1,0xf,0x0,0xf])
#sent_tx.s_da(5, [0,0,1,0xf,0x1,0xf])
#sent_tx.s_da(0xd, [0,0,1,0xf,4,0xf])
#sent_tx.s_12_12R(6, 1000, 1500)
