import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

import time
import random
import binascii
import hashlib

from config import *
from dash_hashs import *
from dash_utils import *
from dash_b58 import *
from dash_jacobian import *


long = int
_bchr = lambda x: bytes([x])
_bord = lambda x: x


def random_string(x):
    return str(os.urandom(x))


def random_key():
    entropy = random_string(32) \
        + str(random.randrange(2**256)) \
        + str(int(time.time() * 1000000))
    return sha256(entropy)


def decode_hexto_int(string):
    return int.from_bytes(bytes.fromhex(string), byteorder='big')


def get_random_key():
    valid_private_key = False
    while not valid_private_key:
        private_key = random_key()
        decoded_private_key = decode_hexto_int(private_key)
        valid_private_key = 0 < decoded_private_key < N

    return {
        'privkey': private_key,
        'privkey_decoded': decoded_private_key
    }


def pubkey_to_address(string):
    #data = binascii.unhexlify(string)
    data = bytes.fromhex(string)
    data_hash = Hash160(data)
    vs = _bchr(addr_prefix) + data_hash
    check = double_sha256(vs)[0:4]
    return b58encode(vs + check)


def private_key_to_wif(string, compressed=False):
    if compressed:
        #prv = binascii.unhexlify(string + '01')
        prv = bytes.fromhex(string + '01')
    else:
        #prv = binascii.unhexlify(string)
        prv = bytes.fromhex(string)

    vs = _bchr(wif_prefix) + prv

    check = double_sha256(vs)[0:4]
    return b58encode(vs + check)


def wif_to_privkey(string):
    wif_compressed = 52 == len(string)
    pvkeyencoded = b58decode(string).hex()
    wifversion = pvkeyencoded[:2]
    checksum = pvkeyencoded[-8:]

    #vs = binascii.unhexlify(pvkeyencoded[:-8])
    vs = bytes.fromhex(pvkeyencoded[:-8])
    check = double_sha256(vs)[0:4]

    if wifversion == wif_prefix.to_bytes(
            1, byteorder='big').hex() and checksum == check.hex():

        if wif_compressed:
            compressed = True
            privkey = pvkeyencoded[2:-10]

        else:
            compressed = False
            privkey = pvkeyencoded[2:-8]

        return {
            'compressed': compressed,
            'privkey': privkey
        }

    else:
        return None


def get_public_key(string):  # from private_key
    decoded_private_key = decode_hexto_int(string)
    public_key = fast_multiply(G, decoded_private_key)
    hex_encoded_public_key = str('04') + public_key[0].to_bytes(
        32, byteorder='big').hex() + public_key[1].to_bytes(32, byteorder='big').hex()

    (public_key_x, public_key_y) = public_key
    if (public_key_y % 2) == 0:
        compressed_prefix = '02'
    else:
        compressed_prefix = '03'

    hex_compressed_public_key = compressed_prefix + \
        public_key_x.to_bytes(32, byteorder='big').hex()

    return {
        'pubkeyhex': hex_encoded_public_key,
        'pubkeyhex_compressed': hex_compressed_public_key
    }


#
