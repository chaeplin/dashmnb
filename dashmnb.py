#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# mnb.py

# codes form code from https://github.com/dashpay/electrum-dash
# ref : https://github.com/dashpay/dash/blob/v0.12.1.x/dash-docs/protocol-documentation.md

import sys, os
sys.path.append( os.path.join( os.path.dirname(__file__), '.' ) )
sys.path.append( os.path.join( os.path.dirname(__file__), '.', 'dashlib' ) )

import argparse
import time

from config import *
from mnb_misc import *
from mnb_mnconf import *
from mnb_rpc import *
from mnb_start import *
from mnb_xfer import *
from mnb_sshtunnel import *
from mnb_hwwallet import *

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException    

def main(args, tunnel=None):    
    #clear_screen()
    logo_show()

    # access
    serverURL = 'http://' + rpcuser + ':' + rpcpassword + '@' + rpcbindip + ':' + str(rpcport if tunnel == None else SSH_LOCAL_PORT)  
    access = AuthServiceProxy(serverURL) 

    client, signing = check_hw_wallet()

    if len(mpath) == 0:
        err_msg = 'please configure bip49 path'
        print_err_exit(get_caller_name(), get_function_name(), err_msg, None, tunnel)
    
    if len(xpub) == 0:
        err_msg = 'please configure bip32 xpub/tpub'
        print_err_exit(get_caller_name(), get_function_name(), err_msg, None, tunnel)

    check_dashd_syncing(access, tunnel)

    if args.check or args.status or args.anounce or args.balance or args.maketx or args.xfer:
        mn_config, signing, mns, mna = checking_mn_config(access, signing, tunnel)


    if args.status or args.anounce or args.balance or args.maketx or args.xfer:
        print_mnstatus(mn_config, mns, mna)

    if args.anounce:
        if not signing:
            err_msg = 'need HW wallet to anounce'
            print_err_exit(get_caller_name(), get_function_name(), err_msg, None, tunnel)

        
#        mn_alias_list = [
#                { 
#                    mn_config.get(m).get('alias'): mn_config.get(m)
#                } 
#                for m in sorted(list(mn_config.keys()))]

        mns_to_start = {}
        for x in sorted(list(mn_config.keys())):
            txidtxidn = mn_config.get(x).get('collateral_txidtxidn')
            if len(args.masternode_to_start) > 0:
                if mn_config.get(x).get('alias') in args.masternode_to_start:
                    mns_to_start[x] = mn_config[x]

            else:
                if ((mns.get(txidtxidn, None) != 'ENABLED' \
                    and mns.get(txidtxidn, None) != 'PRE_ENABLED')) :
                    mns_to_start[x] = mn_config[x]

#            if ((mns.get(txidtxidn, None) != 'ENABLED' \
#                and mns.get(txidtxidn, None) != 'PRE_ENABLED')) \
#                or mn_config.get(x).get('alias') in args.masternode_to_start :
#
#                mns_to_start[x] = mn_config[x]

        if len(mns_to_start) > 0 and signing:
            start_masternode(mns_to_start, access, client, args.anounce, tunnel)

    # wallet rescan
    if args.balance or args.maketx or args.xfer:
        for m in sorted(list(mn_config.keys())):
            mn_config[m]["unspent"], mn_config[m]["txs"], mn_config[m]["collateral_dashd_balance"] = get_unspent_txs(mn_config.get(m), access, tunnel)

        need_wallet_rescan = print_balance(mn_config)

        if need_wallet_rescan:
            err_msg = '\n\trestarting Dash-QT or dashd with -rescan needed'
            print_err_exit(get_caller_name(), get_function_name(), err_msg, None, tunnel)

    if not signing:
        err_msg = 'need HW wallet to spend'
        print_err_exit(get_caller_name(), get_function_name(), err_msg, None, tunnel)


    if args.maketx or args.xfer:

        if need_wallet_rescan:
            err_msg = '\n\t1) to spend mn payments in HW Wallet, restart Dash-QT or dashd with -rescan\n\t2) if did -rescan and still see this messge, check if 1K was spent'
            print_err_exit(get_caller_name(), get_function_name(), err_msg, None, tunnel)

        if signing:
            print('[making txs]')
            for x in sorted(list(mn_config.keys())):
                if len(args.masternode_to_start) > 0:
                    if mn_config.get(x).get('alias') in args.masternode_to_start:
                        print('---> signing txs for mn %s: ' % mn_config[x].get('alias'))
                        mn_config[x]["signedrawtx"] = make_txs_for_hwwallet(mn_config[x], client, tunnel)

                else:
                    print('---> signing txs for mn %s: ' % mn_config[x].get('alias'))
                    mn_config[x]["signedrawtx"] = make_txs_for_hwwallet(mn_config[x], client, tunnel)

    if args.xfer and signing:
        xfertxid = broadcast_signedrawtx(mn_config, access, tunnel)

        print()
        if xfertxid != None:
            for x in xfertxid:
                print('\t' + x)

    if tunnel:
        os.kill(tunnel, signal.SIGTERM)


def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument(dest ='masternode_to_start',
                        metavar = 'masternode_alias_to_start',
                        nargs = '*' )

    parser.add_argument('-c','--check',
                        dest = 'check',
                        action = 'store_true',
                        help='check masternode config') 

    parser.add_argument('-s','--status',
                        dest = 'status',
                        action = 'store_true',
                        help='show masternode status') 

    parser.add_argument('-a','--anounce',
                        dest = 'anounce',
                        action = 'store_true',
                        help='anounce missing masternodes')                        

    parser.add_argument('-b','--balance',
                        dest = 'balance',
                        action = 'store_true',
                        help='show masternodes balance')   

    parser.add_argument('-m','--maketx',
                        dest = 'maketx',
                        action = 'store_true',
                        help='make signed raw tx')

    parser.add_argument('-x','--xfer',
                        dest = 'xfer',
                        action = 'store_true',
                        help='broadcast signed raw tx')


    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()


if __name__ == "__main__":

    printdbg('main starting')
    if (sys.version_info < (3, 0)):
        sys.exit('need python3')

    try:

        tunnel_pid = None
        # ssh tunnel
        if USE_SSH_TUNNEL:
            tunnel = start_ssh_tunnel()
            tunnel_pid = tunnel._getpid()

        args = parse_args()
        main(args, tunnel_pid)

    except KeyboardInterrupt:
        if tunnel_pid:
            os.kill(tunnel_pid, signal.SIGTERM)
        sys.exit()

# end

