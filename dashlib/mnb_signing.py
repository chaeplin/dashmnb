import sys, os
sys.path.append( os.path.join( os.path.dirname(__file__), '..' ) )
sys.path.append( os.path.join( os.path.dirname(__file__), '..', 'dashlib' ) )

from config import *
from mnb_bip32 import *
from mnb_misc import *

def serialize_input_str(tx, prevout_n, sequence, scriptSig):

    """Used by MasternodePing in its serialization for signing."""
    s = ['CTxIn(']
    s.append('COutPoint(%s, %s)' % (tx, prevout_n))
    s.append(', ')
    if tx == '00'*32 and prevout_n == 0xffffffff:
        s.append('coinbase %s' % scriptSig)
    else:
        scriptSig2 = scriptSig
        if len(scriptSig2) > 24:
            scriptSig2 = scriptSig2[0:24]
        s.append('scriptSig=%s' % scriptSig2)

    if sequence != 0xffffffff:
        s.append(', nSequence=%d' % sequence)
    s.append(')')
    return ''.join(s)

def signmessage(last_ping_serialize_for_sig, address, access, tunnel=None):
    
    import base64
    try:
        r = access.signmessage(address, last_ping_serialize_for_sig)
        return(base64.b64decode(r).hex())

    except Exception as e:
        err_msg = 'Please enter the wallet passphrase with walletpassphrase first'
        print_err_exit(get_caller_name(), get_function_name(), err_msg, e.args, tunnel)

def hwwallet_signmessage(serialize_for_sig, spath, address, client, tunnel=None):

    print('---> check keepkey and press button')
    purpose, coin_type, account, change = chain_path()

    sig = client.sign_message(coin_name, [purpose | 0x80000000, coin_type | 0x80000000, account | 0x80000000, change, int(spath)], serialize_for_sig)
    if sig.address != address:
        err_msg = '**** ----> check key path'
        print_err_exit(get_caller_name(), get_function_name(), err_msg, None, tunnel)

    return sig.signature.hex()

# end
