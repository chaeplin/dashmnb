#!/usr/bin/env python3

import sys, os
sys.path.append( os.path.join( os.path.dirname(__file__), '.' ) )
sys.path.append( os.path.join( os.path.dirname(__file__), '.', 'dashlib' ) )

from config import *

def main():
    if TYPE_HW_WALLET.lower().startswith("keepkey"):
        from keepkeylib.client import KeepKeyClient
        from keepkeylib.transport_hid import HidTransport
        import keepkeylib.ckd_public as bip32

    elif TYPE_HW_WALLET.lower().startswith("trezor"):
        from trezorlib.client import TrezorClient
        from trezorlib.transport_hid import HidTransport
        import trezorlib.ckd_public as bip32

    devices = HidTransport.enumerate()

    if len(devices) == 0:
        print('No HW Wallet found')
        return

    transport = HidTransport(devices[0])

    if TYPE_HW_WALLET.lower().startswith("keepkey"):    
        client = KeepKeyClient(transport)

    elif TYPE_HW_WALLET.lower().startswith("trezor"):
        client = TrezorClient(transport)


    # Print out hw wallet's features and settings
    # print(client.features)

    keypath = mpath
    bip32_path = client.expand_path(keypath)

    # xpub to use 
    #print('xpub/tpub --> ' + bip32.serialize(client.get_public_node(bip32_path).node, 0x043587CF))
    print('xpub/tpub --> ' + bip32.serialize(client.get_public_node(bip32_path).node, ( 0x0488B21E if MAINNET else 0x043587CF )))

    for i in range(max_gab):
        child_path = '%s%s' % (keypath + '/', str(i))
        address = client.get_address(coin_name, client.expand_path(child_path))
        print (coin_name +' address:', child_path, address)

    client.close()

if __name__ == '__main__':
    main()

