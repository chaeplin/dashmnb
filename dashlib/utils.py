# utils.py

# Elliptic curve parameters (secp256k1)

P = 2**256 - 2**32 - 977
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337
A = 0
B = 7
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
G = (Gx, Gy)

#
OP_DUP = 0x76
OP_HASH160 = 0xa9
OP_EQUALVERIFY = 0x88
OP_CHECKSIG = 0xac
OP_RETURN = 0x6a

#
string_types = (str)
string_or_bytes_types = (str, bytes)
int_types = (int, float)

code_strings = {
    2: '01',
    10: '0123456789',
    16: '0123456789abcdef',
    32: 'abcdefghijklmnopqrstuvwxyz234567',
    58: '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz',
    256: ''.join([chr(x) for x in range(256)])
}


def num_to_varint(a):
    x = int(a)
    if x < 253:
        return x.to_bytes(1, byteorder='big')
    elif x < 65536:
        return int(253).to_bytes(1, byteorder='big') + \
            x.to_bytes(2, byteorder='little')
    elif x < 4294967296:
        return int(254).to_bytes(1, byteorder='big') + \
            x.to_bytes(4, byteorder='little')
    else:
        return int(255).to_bytes(1, byteorder='big') + \
            x.to_bytes(8, byteorder='little')


def varint_to_num(a):
    format_ = int.from_bytes(bytes.fromhex(a[:2]), byteorder='big')
    assert(format_ <= 255)
    if format_ < 253:
        return format_
    elif format_ < 65536:
        return int.from_bytes(bytes.fromhex(a[2:18]), byteorder='little')
    elif format_ < 4294967296:
        return int.from_bytes(bytes.fromhex(a[2:34]), byteorder='little')
    else:
        return int.from_bytes(bytes.fromhex(a[2:66]), byteorder='little')

#
