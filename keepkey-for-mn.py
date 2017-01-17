#!/usr/bin/env python3

import sys, os
sys.path.append( os.path.join( os.path.dirname(__file__), '.' ) )
sys.path.append( os.path.join( os.path.dirname(__file__), '.', 'dashlib' ) )

from config import *

from keepkeylib.client import KeepKeyClient
from keepkeylib.transport_hid import HidTransport
import keepkeylib.ckd_public as bip32


def main():
    # List all connected KeepKeys on USB
    devices = HidTransport.enumerate()

    # Check whether we found any
    if len(devices) == 0:
        print('No KeepKey found')
        return

    # Use first connected device
    transport = HidTransport(devices[0])

    # Creates object for manipulating KeepKey
    client = KeepKeyClient(transport)

    # Print out KeepKey's features and settings
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


# end