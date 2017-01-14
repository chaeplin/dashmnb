# hashs.py
import sys, os
sys.path.append( os.path.join( os.path.dirname(__file__), '..' ) )
sys.path.append( os.path.join( os.path.dirname(__file__), '..', 'dashlib' ) )

import hashlib
import binascii

from utils import *


def double_sha256(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

def Hash160(msg):
    return hashlib.new('ripemd160', hashlib.sha256(msg).digest()).digest()

def bin_sha256(string):
    binary_data = string if isinstance(string, bytes) else bytes(string, 'utf-8')
    return hashlib.sha256(binary_data).digest()

def sha256(string):
    return bin_sha256(string).hex()

#
def format_hash(hash_):
    return hash_[::-1].hex()
    #return str(binascii.hexlify(hash_[::-1]).decode("utf-8"))

def json_changebase(obj, changer):
    if isinstance(obj, string_or_bytes_types):
        return changer(obj)
    elif isinstance(obj, int_types) or obj is None:
        return obj
    elif isinstance(obj, list):
        return [json_changebase(x, changer) for x in obj]
    return dict((x, json_changebase(obj[x], changer)) for x in obj)

def get_code_string(base):
    if base in code_strings:
        return code_strings[base]
    else:
        raise ValueError("Invalid base!")

def from_int_to_byte(a):
    return bytes([a])

def from_byte_to_int(a):
    return a

def safe_hexlify(a):  
    return a.hex()
    #return str(binascii.hexlify(a), 'utf-8')

#