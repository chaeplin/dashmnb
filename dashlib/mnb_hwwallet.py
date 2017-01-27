import sys, os
sys.path.append( os.path.join( os.path.dirname(__file__), '..' ) )
sys.path.append( os.path.join( os.path.dirname(__file__), '..', 'dashlib' ) )

from config import *
from mnb_misc import *

def list_coins(client):
    return [coin.coin_name for coin in client.features.coins]

def check_hw_wallet(tunnel=None, includebip32=False):
    printdbg('checking hw wallet')
    #client = None

    client   = None
    signing  = False

    if TYPE_HW_WALLET.lower().startswith("keepkey"):
        from keepkeylib.client import KeepKeyClient
        from keepkeylib.transport_hid import HidTransport
        if includebip32:
            import keepkeylib.ckd_public as bip32

        try:
            devices = HidTransport.enumerate()

        except Exception as e:
            err_msg = str(e.args)
            print_err_exit(get_caller_name(), get_function_name(), err_msg, None, tunnel)

        if len(devices) == 0:
            print('===> No HW Wallet found')
            signing  = False
            
        else:

            try:    
                print('===> keepkey HW Wallet found')
                transport = HidTransport(devices[0])
                client = KeepKeyClient(transport)
                signing  = True

            except Exception as e:
                err_msg = str(e.args)
                print_err_exit(get_caller_name(), get_function_name(), err_msg, None, tunnel)


    elif TYPE_HW_WALLET.lower().startswith("trezor"):
        from trezorlib.client import TrezorClient
        from trezorlib.transport_hid import HidTransport
        if includebip32:
            import trezorlib.ckd_public as bip32

        try:
            devices = HidTransport.enumerate()
        
        except Exception as e:
            err_msg = str(e.args)
            print_err_exit(get_caller_name(), get_function_name(), err_msg, None, tunnel)

        if len(devices) == 0:
            print('===> No HW Wallet found')
            signing  = False
            
        else:
            try:
                print('===> trezor HW Wallet found')
                transport = HidTransport(devices[0])
                client = TrezorClient(transport)
                signing  = True

            except Exception as e:
                err_msg = str(e.args)
                print_err_exit(get_caller_name(), get_function_name(), err_msg, None, tunnel)

    if client != None:

        try:
            wallet_supported_coins = list_coins(client)

        except Exception as e:
            err_msg = str(e.args)
            print_err_exit(get_caller_name(), get_function_name(), err_msg, None, tunnel)        

        if coin_name not in wallet_supported_coins:
            err_msg = 'only following coins supported by wallet\n\t' + str(wallet_supported_coins)
            print_err_exit(get_caller_name(), get_function_name(), err_msg, None, tunnel)

    if includebip32:
        return client, signing, bip32

    else:
        return client, signing
