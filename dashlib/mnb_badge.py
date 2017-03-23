import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from mnb_misc import *
from mnb_signing import *
import base64

def make_badge(mnconfig, mpath, client):

    forum_msg = "Masternode ownership proof for https://www.dash.org/forum/"

    print('\n[making a signed message for Masternode Owner/Operator badge]')
    print_hw_wallet_check()

    print("msg to sign : %s\n" % forum_msg)

    try:
        sig1 = hwwallet_signmessage(
            forum_msg,
            mnconfig['collateral_spath'],
            mnconfig['collateral_address'],
            client,
            mpath)

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

    print("New Forum Feature: Masternode Owner Badges : https://goo.gl/iIfgVZ")
    print("masternoe alias : %s" % mnconfig['alias'])
    print("masternoe address : %s" % mnconfig['collateral_address'])
    print("masternoe signed message : %s" % base64.b64encode(bytearray.fromhex(sig1)).decode("utf-8"))
