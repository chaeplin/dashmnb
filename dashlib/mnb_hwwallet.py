import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'dashlib'))

from config import *
from mnb_misc import *


def chain_path(mpath):
    import re
    pathmatch = re.search("^(.*)'/(.*)'/(.*)'/(.*)$", mpath)
    if (pathmatch):
        purpose = pathmatch.group(1)
        coin_type = pathmatch.group(2)
        account = pathmatch.group(3)
        change = pathmatch.group(4)

        return int(purpose), int(coin_type), int(account), int(change)

    else:
        err_msg = 'check bip32 mpath'
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg)


def get_chain_pubkey(client, bip32):
    try:
        mpath = get_mpath()

        chain_pubkey = {}

        for i in range(max_gab):
            child_path = '%s%s' % (mpath + '/', str(i))
            address = client.get_address(
                coin_name, client.expand_path(child_path))
            publicnode = client.get_public_node(
                client.expand_path(child_path)).node.public_key.hex()

            chain_pubkey[address] = {"spath": i, "addrpubkey": publicnode}

        return chain_pubkey

    except AssertionError as e:
        err_msg = str(e.args)
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg)

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
            "KeyboardInterrupt")


def get_mpath(default_account=False):
    # return without address_index

    #  Dash  : 44'/5'/account'/0/0
    #  tDash : 44'/165'/account'/0/0

    if default_account:
        return "44'/5'/0'/0" if MAINNET else "44'/165'/0'/0"

    else:
        return "44'/5'/" + \
            str(account_no) + "'/0" if MAINNET else "44'/165'/" + str(account_no) + "'/0"


def list_coins(client):
    return [coin.coin_name for coin in client.features.coins]


def check_hw_wallet():
    printdbg('checking hw wallet')
    #client = None

    client = None
    signing = False

    if TYPE_HW_WALLET.lower().startswith("keepkey"):
        from keepkeylib.client import KeepKeyClient
        from keepkeylib.transport_hid import HidTransport
        import keepkeylib.ckd_public as bip32

        try:
            devices = HidTransport.enumerate()

        except Exception as e:
            err_msg = str(e.args)
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

        if len(devices) == 0:
            print('===> No HW Wallet found')
            signing = False

        else:

            try:
                print('===> keepkey HW Wallet found')
                transport = HidTransport(devices[0])
                client = KeepKeyClient(transport)
                signing = True

            except Exception as e:
                err_msg = str(e.args)
                print_err_exit(
                    get_caller_name(),
                    get_function_name(),
                    err_msg)

    elif TYPE_HW_WALLET.lower().startswith("trezor"):
        from trezorlib.client import TrezorClient
        from trezorlib.transport_hid import HidTransport
        import trezorlib.ckd_public as bip32

        try:
            devices = HidTransport.enumerate()

        except Exception as e:
            err_msg = str(e.args)
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

        if len(devices) == 0:
            print('===> No HW Wallet found')
            signing = False

        else:
            try:
                print('===> trezor HW Wallet found')
                transport = HidTransport(devices[0])
                client = TrezorClient(transport)
                signing = True

            except Exception as e:
                err_msg = str(e.args)
                print_err_exit(
                    get_caller_name(),
                    get_function_name(),
                    err_msg)

    if client is not None:

        try:
            wallet_supported_coins = list_coins(client)

        except Exception as e:
            err_msg = str(e.args)
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

        if coin_name not in wallet_supported_coins:
            err_msg = 'only following coins supported by wallet\n\t' + \
                str(wallet_supported_coins)
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

    else:
        err_msg = "Can't run dashmnb without hw wallet"
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg)

    try:
        mpath = get_mpath()
        bip32_path = client.expand_path(mpath)
        xpub = bip32.serialize(
            client.get_public_node(bip32_path).node,
            (0x0488B21E if MAINNET else 0x043587CF))

    except AssertionError as e:
        err_msg = str(e.args)
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg)

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
            "KeyboardInterrupt")

    return client, signing, bip32, mpath, xpub
