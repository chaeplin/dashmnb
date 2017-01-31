import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

import hashlib
import binascii

from dash_utils import *


def double_sha256(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def Hash160(msg):
    return hashlib.new('ripemd160', hashlib.sha256(msg).digest()).digest()


def bin_sha256(string):
    binary_data = string if isinstance(
        string, bytes) else bytes(
        string, 'utf-8')
    return hashlib.sha256(binary_data).digest()


def sha256(string):
    return bin_sha256(string).hex()

def get_code_string(base):
    if base in code_strings:
        return code_strings[base]
    else:
        raise ValueError("Invalid base!")

def format_hash(hash_):
    return hash_[::-1].hex()
    # return str(binascii.hexlify(hash_[::-1]).decode("utf-8"))

def changebase(string, frm, to, minlen=0):
    if frm == to:
        return lpad(string, get_code_string(frm)[0], minlen)
    return encode(decode(string, frm), to, minlen)


def json_changebase(obj, changer):
    if isinstance(obj, string_or_bytes_types):
        return changer(obj)
    elif isinstance(obj, int_types) or obj is None:
        return obj
    elif isinstance(obj, list):
        return [json_changebase(x, changer) for x in obj]
    return dict((x, json_changebase(obj[x], changer)) for x in obj)


def from_int_to_byte(a):
    return bytes([a])


def from_byte_to_int(a):
    return a


def safe_hexlify(a):
    return a.hex()
    # return str(binascii.hexlify(a), 'utf-8')

def decode(string, base):
    if base == 256 and isinstance(string, str):
        string = bytes(bytearray.fromhex(string))
    base = int(base)
    code_string = get_code_string(base)
    result = 0
    if base == 256:
        def extract(d, cs):
            return d
    else:
        def extract(d, cs):
            return cs.find(d if isinstance(d, str) else chr(d))

    if base == 16:
        string = string.lower()
    while len(string) > 0:
        result *= base
        result += extract(string[0], code_string)
        string = string[1:]
    return result

def encode(val, base, minlen=0):
    base, minlen = int(base), int(minlen)
    code_string = get_code_string(base)
    result_bytes = bytes()
    while val > 0:
        curcode = code_string[val % base]
        result_bytes = bytes([ord(curcode)]) + result_bytes
        val //= base

    pad_size = minlen - len(result_bytes)

    padding_element = b'\x00' if base == 256 else b'1' \
        if base == 58 else b'0'
    if (pad_size > 0):
        result_bytes = padding_element*pad_size + result_bytes

    result_string = ''.join([chr(y) for y in result_bytes])
    result = result_bytes if base == 256 else result_string

    return result


def hash_to_int(x):
    if len(x) in [40, 64]:
        return decode(x, 16)
    return decode(x, 256)


#
