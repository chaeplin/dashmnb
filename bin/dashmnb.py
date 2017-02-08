#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# mnb.py

# code from https://github.com/dashpay/electrum-dash
# most bitcoin code from https://github.com/vbuterin/pybitcointools
# ref :
# https://github.com/dashpay/dash/blob/v0.12.1.x/dash-docs/protocol-documentation.md

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'dashlib'))

import argparse
import time
import signal
import atexit

from dashlib import *

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException


def main(args):
    logo_show()

    # access
    # access
    if rpcusessl:
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

    protocolversion = check_dashd_syncing(access)
    blockcount = get_getblockcount(access)
    blockhash = get_block_hash(blockcount, access)

    print('-> protocolv : %s' % str(protocolversion))
    print('-> blockcnt  : %s' % blockcount)
    print('-> blockhash : %s\n' % blockhash)


    client, signing, bip32, mpath, xpub = check_hw_wallet()
    chain_pubkey = get_chain_pubkey(client, bip32)

    mn_config, signing, mns, mna = checking_mn_config(
        access, signing, chain_pubkey, args.showall)

    print_mnstatus(mn_config, mns, mna)

    if args.anounce and MOVE_1K_COLLATERAL == False:
        if not signing:
            err_msg = 'check masternode config'
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

        mns_to_start = []

        list_of_mn_status_ok = ["ENABLED", "PRE_ENABLED", "WATCHDOG_EXPIRED"]
        list_of_mn_status_to_ignore = ["OUTPOINT_SPENT"]

        for m in mn_config:
            txidtxidn = m.get('collateral_txidtxidn')
            if len(args.masternode_to_start) > 0:
                if m.get('alias') in args.masternode_to_start:
                    mns_to_start.append(m)
            else:
                if ((mns.get(txidtxidn, None) not in list_of_mn_status_ok) and
                    (mns.get(txidtxidn, None) not in list_of_mn_status_to_ignore)):
                #if ((mns.get(txidtxidn, None) != 'ENABLED'
                #     and mns.get(txidtxidn, None) != 'PRE_ENABLED')):
                    mns_to_start.append(m)

        if len(mns_to_start) > 0 and signing:
            start_masternode(
                mns_to_start,
                protocolversion,
                blockcount,
                access,
                client,
                args.anounce,
                mpath)

    # wallet rescan
    if args.balance : #or args.maketx or args.xfer:
        for m in mn_config:
            #m["unspent"], m["txs"], m["collateral_dashd_balance"] = get_unspent_txs(m, access)
            m["txs"], m["collateral_dashd_balance"] = get_unspent_txs(
                m, blockcount, access)

        need_wallet_rescan = print_balance(mn_config)

        if need_wallet_rescan:
            err_msg = '\n\trestarting Dash-QT or dashd with -rescan needed'
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

#    if not signing:
#        err_msg = 'need HW wallet to spend'
#        print_err_exit(
#            get_caller_name(),
#            get_function_name(),
#            err_msg)
#
#    if args.maketx or args.xfer:
#
#        if need_wallet_rescan:
#            err_msg = '\n\t1) to spend mn payout in HW Wallet, restart Dash-QT or dashd with -rescan\n\t2) if did -rescan and still see this messge, check if 1K was spent'
#            print_err_exit(
#                get_caller_name(),
#                get_function_name(),
#                err_msg)
#
#        if signing:
#            print('[making txs]')
#            for m in mn_config:
#                if len(
#                    m.get('collateral_dashd_balance')) > 0 and len(
#                    m.get(
#                        'txs',
#                        None)) > 0:
#                    if len(args.masternode_to_start) > 0:
#                        if m.get('alias') in args.masternode_to_start:
#                            print(
#                                '---> signing txs for mn %s: ' %
#                                m.get('alias'))
#                            m["signedrawtx"] = make_txs_for_hwwallet(
#                                m, client, mpath)
#
#                    else:
#                        print('---> signing txs for mn %s: ' % m.get('alias'))
#                        m["signedrawtx"] = make_txs_for_hwwallet(
#                            m, client, mpath)
#
#    if args.xfer and signing:
#        xfertxid = broadcast_signedrawtx(mn_config, access)
#
#        print()
#        if xfertxid is not None:
#            for x in xfertxid:
#                print('\t' + x)
#
    print_err_exit(
        get_caller_name(),
        get_function_name(),
        'end of pg')


def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument(dest='masternode_to_start',
                        metavar='masternode_alias_to_start/spend',
                        nargs='*')

    parser.add_argument('-c', '--check',
                        dest='check',
                        action='store_true',
                        help='check masternode config')

    parser.add_argument('-s', '--status',
                        dest='status',
                        action='store_true',
                        help='show masternode status')

    parser.add_argument('-a', '--anounce',
                        dest='anounce',
                        action='store_true',
                        help='anounce missing masternodes')

    parser.add_argument('-b', '--balance',
                        dest='balance',
                        action='store_true',
                        help='show masternodes balance')

    parser.add_argument('-l', '--showall',
                        dest='showall',
                        action='store_true',
                        help='show all configured masternodes')

#    parser.add_argument('-m', '--maketx',
#                        dest='maketx',
#                        action='store_true',
#                        help='make signed raw tx')
#
#    parser.add_argument('-x', '--xfer',
#                        dest='xfer',
#                        action='store_true',
#                        help='broadcast signed raw tx')

    if len(sys.argv) < 2:
        parser.print_help()
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            'print help')

    return parser.parse_args()


if __name__ == "__main__":
    def killsubprocess():
        if tunnel_pid:
            os.kill(tunnel_pid, signal.SIGTERM)

    printdbg('main starting')
    if (sys.version_info < (3, 5, 1)):
        sys.exit('need python 3.5.1')

    try:

        tunnel_pid = None
        # ssh tunnel
        if USE_SSH_TUNNEL:
            tunnel = start_ssh_tunnel()
            tunnel_pid = tunnel._getpid()

        atexit.register(killsubprocess)
        args = parse_args()
        main(args)

    except KeyboardInterrupt:
        if tunnel_pid:
            os.kill(tunnel_pid, signal.SIGTERM)
        sys.exit()

# end
