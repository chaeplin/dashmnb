#!/usr/bin/env python3

import sys, os
sys.path.append( os.path.join( os.path.dirname(__file__), '.' ) )
sys.path.append( os.path.join( os.path.dirname(__file__), '.', 'dashlib' ) )

from config import *
from mnb_hwwallet import *

def main():
    client, signing, bip32 = check_hw_wallet(None, True)

    if client == None:
        sys.exit()

    # Print out hw wallet's features and settings
    # print(client.features)

    keypath = mpath
    bip32_path = client.expand_path(keypath)

    try:
        print('xpub/tpub --> ' + bip32.serialize(client.get_public_node(bip32_path).node, ( 0x0488B21E if MAINNET else 0x043587CF )))

        for i in range(max_gab):
            child_path = '%s%s' % (keypath + '/', str(i))
            address = client.get_address(coin_name, client.expand_path(child_path))
            print (coin_name +' address:', child_path, address)

        client.close()

    except Exception as e:
        print(e)

    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    main()

