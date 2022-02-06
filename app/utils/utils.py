from binascii import unhexlify
from gmpy2 import digits


def int_to_bytes(val, endianness='big'):
    if val == 0:
        return bytes(0)

    width = val.bit_length()
    width += 8 - ((width % 8) or 8)
    fmt = '%%0%dx' % (width // 4)
    s = unhexlify(fmt % val)
    if endianness == 'little':
        s = s[::-1]
    return s


def bytes_to_int(bytes_number, endianness='big'):
    return int.from_bytes(bytes_number, endianness)


def get_current_link(current_number, number_char):
    return digits(current_number, number_char)
