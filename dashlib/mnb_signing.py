import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))


from config import *
from dash_ecdsa import *
from mnb_misc import *
from mnb_hwwallet import *


def serialize_input_str(tx, prevout_n, sequence, scriptSig):
    """Used by MasternodePing in its serialization for signing."""
    s = ['CTxIn(']
    s.append('COutPoint(%s, %s)' % (tx, prevout_n))
    s.append(', ')
    if tx == '00' * 32 and prevout_n == 0xffffffff:
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


def signmessage(last_ping_serialize_for_sig, address, access):

    import base64
    try:
        r = access.signmessage(address, last_ping_serialize_for_sig)
        return(base64.b64decode(r).hex())

    except Exception as e:
        err_msg = 'Please enter the wallet passphrase with walletpassphrase first'
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg,
            e.args)


def signmessage_ecdsa(message, privkeywif):
    import base64
    try:
        r = ecdsa_sign(message, privkeywif)
        return(base64.b64decode(r).hex())

    except Exception as e:
        err_msg = 'dash_ecdsa has problem'
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg,
            e.args)


def signmessage_ecdsa_no_encoding(message, privkeywif):
    try:
        r = ecdsa_sign(message, privkeywif)
        return r

    except Exception as e:
        err_msg = 'dash_ecdsa has problem'
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg,
            e.args)


def hwwallet_signmessage(
        serialize_for_sig,
        spath,
        address,
        client,
        mpath):

    # print_hw_wallet_check()

    purpose, coin_type, account, change = chain_path(mpath)

    try:
        sig = client.sign_message(coin_name,
                                  [purpose | 0x80000000,
                                   coin_type | 0x80000000,
                                   account | 0x80000000,
                                   change,
                                   int(spath)],
                                  serialize_for_sig)

    except Exception as e:
        err_msg = str(e.args)
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg)

    except KeyboardInterrupt:
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            'KeyboardInterrupt')

    if sig.address != address:
        err_msg = '**** ----> check key path'
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg)

    return sig.signature.hex()

# end
