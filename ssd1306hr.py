from microbit import i2c
from microbit import Image

ADDR = 0x3C
zoom = 1

NUM_PAGE = 8
NUM_WCOL = 16
NUM_IPGE = 8
buf = bytearray(NUM_IPGE)


def set_pos(col=0, page=0):
    i2c.write(ADDR, b'\x00' + bytearray((0xb0 | page,)))
    c1, c2 = col & 0x0F, col >> 4
    i2c.write(ADDR, bytearray((0x00, 0x00 | c1)))
    i2c.write(ADDR, bytearray((0x00, 0x10 | c2)))

def initialize():
    i2c.write(ADDR,b'\x00\xae\x00\xa4\x00\xd5\xf0\x00\xa8?\x00\xd3\x00\x00\x00\x00\x8d\x14\x00 \x00\x00!\x00\x7f\x00"\x00?\x00\xa1\x00\xc8\x00\xda\x12\x00\x81\xcf\x00\xd9\xf1\x00\xdb@\x00\xa6\x00\xd6\x01\x00\xaf')


def clear_oled():
    i2c.write(ADDR, b'\x00\xb0\x00\x00\x00\x10')
    tmp = '\x40' + '\x00' * 8
    for i in range(NUM_PAGE * NUM_WCOL):
        i2c.write(ADDR, tmp)

def put_text(row, text, init_pos=0):
    for i, cha in enumerate(text):
        if i + init_pos >= NUM_WCOL:
            break
        img = Image(cha)
        for icol in range(1, 7):
            buf[icol] = 0
            for irow in range(2, 7): # 0th and 7th are always empty
                ii, ij = irow - 2, icol - 1
                if icol >= 4: ij -= 1

                buf[icol] |= (img.get_pixel(ij, ii) // 4) << (irow)
            set_pos((i + init_pos) * NUM_IPGE, row)
            i2c.write(ADDR, b'\x40' + buf)

def add_text(x, y, text, draw=1):
    if draw:
        put_text(y, text, x)

