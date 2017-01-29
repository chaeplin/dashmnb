#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'dashlib'))

from config import *
from mnb_hwwallet import *
from bip32utils import BIP32Key
from mnb_misc import *


def main():
    logo_show()

    client, signing, bip32, _, _ = check_hw_wallet()

    if client is None:
        sys.exit()

    mpath = {}
    mpath['masternode'] = get_mpath()
    mpath['default'] = get_mpath(True)

    HEADER_PRINTED = False
    for key in sorted(list(mpath.keys()), reverse=True):

        keypath = mpath[key]

        try:
            bip32_path = client.expand_path(keypath)
            xpub = bip32.serialize(
                client.get_public_node(bip32_path).node,
                (0x0488B21E if MAINNET else 0x043587CF))

            acc_node = BIP32Key.fromExtendedKey(xpub)

            for i in range(max_gab):
                child_path = '%s%s' % (keypath + '/', str(i))
                address = client.get_address(
                    coin_name, client.expand_path(child_path))
                publicnode = client.get_public_node(
                    client.expand_path(child_path)).node.public_key.hex()

                if not HEADER_PRINTED:
                    if key == 'masternode':
                        print(
                            '**** ====> use following address for 1K collateral of masternode')

                    else:
                        print(
                            '**** ====> use following address for trezor/keepkey wallet(default path)')

                    HEADER_PRINTED = True

                # make sure xpub/tub
                bip32_addr_node = acc_node.ChildKey(i)
                bip32_address = bip32_addr_node.Address()
                bip32_addrpkey = bip32_addr_node.PublicKey().hex()

                #print(address, bip32_addrpkey, publicnode)
                # print(publicnode)

                print(coin_name +' address: ' + '{:20}'.format(child_path) + ' ' + address)
                assert bip32_address == address, "address mismatch, bip32 : %s <--> hw : %s" % (
                    bip32_address, address)
                assert publicnode == bip32_addrpkey, "pubkey mismatch, bip32 : %s <--> hw : %s" % (
                    bip32_addrpkey, publicnode)

            HEADER_PRINTED = False
            print()

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

    client.close()

if __name__ == '__main__':
    main()
