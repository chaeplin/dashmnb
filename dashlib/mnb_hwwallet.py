import sys, os
sys.path.append( os.path.join( os.path.dirname(__file__), '..' ) )
sys.path.append( os.path.join( os.path.dirname(__file__), '..', 'dashlib' ) )

from config import *
from mnb_misc import *


def check_hw_wallet():
    printdbg('checking hw wallet')
    #client = None

    client   = None
    signing  = False

    if TYPE_HW_WALLET.lower().startswith("keepkey"):
        from keepkeylib.client import KeepKeyClient
        from keepkeylib.transport_hid import HidTransport
        import keepkeylib.ckd_public as bip32

        devices = HidTransport.enumerate()
    
        if len(devices) == 0:
            print('===> No HW Wallet found')
            signing  = False
            
        else:
            print('===> keepkey HW Wallet found')
            transport = HidTransport(devices[0])
            client = KeepKeyClient(transport)
            signing  = True

    elif TYPE_HW_WALLET.lower().startswith("trezor"):
        from trezorlib.client import TrezorClient
        from trezorlib.transport_hid import HidTransport
        import trezorlib.ckd_public as bip32

        devices = HidTransport.enumerate()

        if len(devices) == 0:
            print('===> No HW Wallet found')
            signing  = False
            
        else:
            print('===> trezor HW Wallet found')
            transport = HidTransport(devices[0])
            client = TrezorClient(transport)
            signing  = True

    return client, signing

