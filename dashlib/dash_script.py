import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

try:
    from config import *
except:
    print('please config dashlib/config.py')
    sys.exit()
    
from dash_b58 import *
from dash_hashs import *
from dash_jacobian import *
from dash_keys import *
from dash_utils import *

long = int
_bchr = lambda x: bytes([x])
_bord = lambda x: x


def script_to_addr(script_hex):
    # list : outpu of deserialize_script
    if isinstance(script_hex, list):
        if len(script_hex) == 2:
            #script_bin = binascii.unhexlify(script_hex[1])
            script_bin = bytes.fromhex(script_hex[1])
        elif len(script_hex) == 1:
            return 'pay_to_pubkey'

    else:
        #script_bin = binascii.unhexlify(script_hex)
        script_bin = bytes.fromhex(script_hex)

    # format # 5
    if (len(script_bin) == 25
            and _bord(script_bin[0]) == OP_DUP
            and _bord(script_bin[1]) == OP_HASH160
            and _bord(script_bin[2]) == 0x14               # 20 byte
            and _bord(script_bin[23]) == OP_EQUALVERIFY
            and _bord(script_bin[24]) == OP_CHECKSIG):
        data = script_bin[3:23]                             # take 20 byte
        vs = _bchr(addr_prefix) + data
        check = double_sha256(vs)[0:4]
        return b58encode(vs + check)

    # format # 1
    elif (len(script_bin) == 67
            and _bord(script_bin[0]) == 0x41
            and _bord(script_bin[66]) == OP_CHECKSIG):
        data = script_bin[1:66]                             # 65 byte
        data_hash = Hash160(data)
        vs = _bchr(addr_prefix) + data_hash
        check = double_sha256(vs)[0:4]
        return b58encode(vs + check)

    # format # 2, technically invalid.
    elif (len(script_bin) == 66
            and _bord(script_bin[65]) == OP_CHECKSIG):
        data = script_bin[0:65]                             # 65 byte
        data_hash = Hash160(data)
        vs = _bchr(addr_prefix) + data_hash
        check = double_sha256(vs)[0:4]
        return b58encode(vs + check)

    # format # 3
    elif (len(script_bin) >= 25
            and _bord(script_bin[0]) == OP_DUP
            and _bord(script_bin[1]) == OP_HASH160
            and _bord(script_bin[2]) == 0x14):             # 20 byte
        data = script_bin[3:23]                            # take 20 byte
        vs = _bchr(addr_prefix) + data
        check = double_sha256(vs)[0:4]
        return b58encode(vs + check)

    # format # 4
    elif (len(script_bin) == 5
            and _bord(script_bin[0]) == OP_DUP
            and _bord(script_bin[1]) == OP_HASH160
            and _bord(script_bin[2]) == 0x00               # 0 byte
            and _bord(script_bin[3]) == OP_EQUALVERIFY
            and _bord(script_bin[4]) == OP_CHECKSIG):
        return 'unspendable'

    # 33 byte (spend coinbase tx ?)
    elif (len(script_bin) == 33):
        data_hash = Hash160(script_bin)
        vs = _bchr(addr_prefix) + data_hash
        check = double_sha256(vs)[0:4]
        return b58encode(vs + check)

    elif (len(script_bin) == 35  # compressed
            and _bord(script_bin[0]) == 0x21
            and _bord(script_bin[34]) == OP_CHECKSIG):
        data = script_bin[1:34]
        data_hash = Hash160(data)
        vs = _bchr(addr_prefix) + data_hash
        check = double_sha256(vs)[0:4]
        return b58encode(vs + check)

    elif (_bord(script_bin[0]) == OP_RETURN):
        return 'nulldata'

    else:
        return 'invalid'


#
