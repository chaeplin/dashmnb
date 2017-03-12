#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'dashlib'))

import time
import signal
import atexit

from bip32utils import BIP32Key
from dashlib import *
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException


def main():
    logo_show()

    # access
    if 'rpcusessl' in globals() and rpcusessl:
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context

        serverURL = 'https://' + rpcuser + ':' + rpcpassword + '@' + rpcbindip + \
            ':' + str(rpcport if USE_SSH_TUNNEL is False else SSH_LOCAL_PORT)

    else:
        serverURL = 'http://' + rpcuser + ':' + rpcpassword + '@' + rpcbindip + \
            ':' + str(rpcport if USE_SSH_TUNNEL is False else SSH_LOCAL_PORT)

    access = AuthServiceProxy(serverURL)

    if len(str(account_no)) == 0:
        err_msg = 'please configure bip32 path : account_no'
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg)

    if TYPE_HW_WALLET.lower().startswith("ledgernanos"):
        client, signing, mpath = check_hw_wallet()

    else:
        client, signing, bip32, mpath, xpub = check_hw_wallet()

    if client is None:
        sys.exit()

    if TYPE_HW_WALLET.lower().startswith("ledgernanos"):
        
        try:

            print('**** ====> use following address for 1K collateral of masternode')
    
            for i in range(max_gab):
                addr_path = mpath + '/' + str(i)
                nodedata = client.getWalletPublicKey(addr_path)
                address   = (nodedata.get('address')).decode("utf-8")
    
                addr_balance = round(
                    Decimal(
                        getaddressbalancewithoutexcept(
                            address,
                            access) / 1e8),
                    8)
        
                print(
                    coin_name +
                    ' address: ' +
                    '{:20}'.format(addr_path) +
                    ' ' +
                    address +
                    ' ' +
                        '{:13.8f}'.format(addr_balance))            

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

    else:
        keypath = mpath
    
        try:
            #bip32_path = client.expand_path(keypath)
            # xpub = bip32.serialize(
            #    client.get_public_node(bip32_path).node,
            #    (0x0488B21E if MAINNET else 0x043587CF))
    
            acc_node = BIP32Key.fromExtendedKey(xpub)
    
            print('**** ====> use following address for 1K collateral of masternode')
    
            for i in range(max_gab):
                child_path = '%s%s' % (keypath + '/', str(i))
                address = client.get_address(
                    coin_name, client.expand_path(child_path))
                publicnode = client.get_public_node(
                    client.expand_path(child_path)).node.public_key.hex()
    
                # make sure xpub/tub
                bip32_addr_node = acc_node.ChildKey(i)
                bip32_address = bip32_addr_node.Address()
                bip32_addrpkey = bip32_addr_node.PublicKey().hex()
    
                addr_balance = round(
                    Decimal(
                        getaddressbalancewithoutexcept(
                            address,
                            access) / 1e8),
                    8)
    
                print(
                    coin_name +
                    ' address: ' +
                    '{:20}'.format(child_path) +
                    ' ' +
                    address +
                    ' ' +
                    '{:13.8f}'.format(addr_balance))
    
                assert bip32_address == address, "address mismatch, bip32 : %s <--> hw : %s" % (
                    bip32_address, address)
                assert publicnode == bip32_addrpkey, "pubkey mismatch, bip32 : %s <--> hw : %s" % (
                    bip32_addrpkey, publicnode)
    
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

if __name__ == '__main__':
    def killsubprocess():
        if tunnel_pid:
            os.kill(tunnel_pid, signal.SIGTERM)

    if (sys.version_info < (3, 5, 1)):
        sys.exit('need python 3.5.1')

    try:

        tunnel_pid = None
        # ssh tunnel
        if USE_SSH_TUNNEL:
            tunnel = start_ssh_tunnel()
            tunnel_pid = tunnel._getpid()

        atexit.register(killsubprocess)
        main()

    except KeyboardInterrupt:
        if tunnel_pid:
            os.kill(tunnel_pid, signal.SIGTERM)
        sys.exit()
