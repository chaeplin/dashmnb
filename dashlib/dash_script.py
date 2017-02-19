import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from config import *
from dash_b58 import *
from dash_hashs import *
from dash_jacobian import *
from dash_keys import *
from dash_utils import *


long = int
_bchr = lambda x: bytes([x])
_bord = lambda x: x

#OP_DUP = 0x76
#OP_HASH160 = 0xa9
#OP_EQUALVERIFY = 0x88
#OP_CHECKSIG = 0xac
#OP_RETURN = 0x6a

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

    # format # x, technically invalid ?.
    elif (len(script_bin) == 65):
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

if __name__ == "__main__":
    if MAINNET:

        def script_forma_5():                                      
            script_hex = '76a914fd85adfcf0c5c6a3f671428a7bfa3944cb84030588ac'
            assert script_to_addr(script_hex) == 'XyoLw1ahdjEgyK6FfRq6BNCrvbzdrmf8mm'
            #print('XyoLw1ahdjEgyK6FfRq6BNCrvbzdrmf8mm', script_to_addr(script_hex), len(bytes.fromhex(script_hex)))
        
        def script_forma_1(): 
            script_hex = '41047559d13c3f81b1fadbd8dd03e4b5a1c73b05e2b980e00d467aa9440b29c7de23664dde6428d75cafed22ae4f0d302e26c5c5a5dd4d3e1b796d7281bdc9430f35ac'
            assert script_to_addr(script_hex) == 'XqPQ26xGigKkq4yCNmTfgkRPdt8FyB547J'
            #print('XqPQ26xGigKkq4yCNmTfgkRPdt8FyB547J', script_to_addr(script_hex), len(bytes.fromhex(script_hex)))
        
        def script_forma_2(): 
            script_hex = '047559d13c3f81b1fadbd8dd03e4b5a1c73b05e2b980e00d467aa9440b29c7de23664dde6428d75cafed22ae4f0d302e26c5c5a5dd4d3e1b796d7281bdc9430f35ac'
            assert script_to_addr(script_hex) == 'XqPQ26xGigKkq4yCNmTfgkRPdt8FyB547J'
            #print('XqPQ26xGigKkq4yCNmTfgkRPdt8FyB547J', script_to_addr(script_hex), len(bytes.fromhex(script_hex)))
        
        def script_forma_3():
            script_hex = '76a914fd85adfcf0c5c6a3f671428a7bfa3944cb84030588acacaa'
            assert script_to_addr(script_hex) == 'XyoLw1ahdjEgyK6FfRq6BNCrvbzdrmf8mm'
            #print('XyoLw1ahdjEgyK6FfRq6BNCrvbzdrmf8mm', script_to_addr(script_hex), len(bytes.fromhex(script_hex)))
        
        def script_forma_4():                                       
            script_hex = '76a90088ac'
            assert script_to_addr(script_hex) == 'unspendable'
            #print('unspendable', script_to_addr(script_hex), len(bytes.fromhex(script_hex)))
        
        def script_p2p():
            script_hex = '6a281adb1bf4cef81ede4a63ad5ca5943e5288fffc210d90a861a60a96658d7f90580000000000000000'
            assert script_to_addr(script_hex) == 'nulldata'
            #print('nulldata', script_to_addr(script_hex))
        
        def script_compressed():
            script_hex = '2103717f7082f58395f02afb45b1ae871cae31293b33c64c8d9568d9cac09fa70c51ac'
            assert script_to_addr(script_hex) == 'XwcW25euh9VxJLxP6KtAygDuKLo7vjLJ5H'
            #print('XwcW25euh9VxJLxP6KtAygDuKLo7vjLJ5H', script_to_addr(script_hex), len(bytes.fromhex(script_hex)))    
        
        def script_forma_x(): 
            script_hex = '04353d9bf3677c65dc5fd35fd48d05d932b1bfa4cf1616d116a5d428b09a3b92529ed2bc3cdd31e2ef8b652676526df4facb070e06b7ecb8e5c43c1ad539f1d622'
            assert script_to_addr(script_hex) == 'XuDBtYYmkLKXEYt5aiPRmbGabn669dcFaR'
            #print('XuDBtYYmkLKXEYt5aiPRmbGabn669dcFaR', script_to_addr(script_hex), len(bytes.fromhex(script_hex)))
        
        
        script_forma_5()
        script_forma_1()
        script_forma_2()
        script_forma_3()
        script_forma_4()
        script_p2p()
        script_compressed()
        script_forma_x()
            