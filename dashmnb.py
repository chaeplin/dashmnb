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

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException    

def checking_mn_config(access, signing):
    
    print('\n---> checking masternode config')
    lines =[]
    if os.path.exists(masternode_conf_file):
        with open(masternode_conf_file) as mobj:
            for line in mobj:            
                lines.append(line.strip())
   
        mn_config, signing = parse_masternode_conf(lines, access, signing)
    
    else:
        sys.exit('no %s file' % masternode_conf_file)

    check_wallet_lock(access)
    mns = check_masternodelist(access)
    mna = check_masternodeaddr(access)

    return mn_config, signing, mns, mna

def main(args):

    #clear_screen()
    logo_show()

    serverURL = 'http://' + rpcuser + ':' + rpcpassword + '@' + rpcbindip + ':' + str(rpcport)
    access = AuthServiceProxy(serverURL) 

    if TYPE_HW_WALLET == 'keepkey':
        from keepkeylib.client import KeepKeyClient
        from keepkeylib.transport_hid import HidTransport
        
        devices = HidTransport.enumerate()
    
        if len(devices) == 0:
            print('===> No HW Wallet found')
            announce = False
            signing  = False
            
        else:
            transport = HidTransport(devices[0])
            client = KeepKeyClient(transport)
            signing  = True
    
    if len(mpath) == 0:
        sys.exit('please configure bip49 path')
    
    if len(xpub) == 0:
        sys.exit('please configure bip32 xpub')
    
    check_dashd_syncing(access)  


    if args.check or args.status or args.anounce:
        mn_config, signing, mns, mna = checking_mn_config(access, signing)

    if args.status or args.anounce:
        print_mnstatus(mn_config, mns, mna)

    if args.anounce:
        mns_to_start = {}
        for x in sorted(list(mn_config.keys())):
            txidtxidn = get_txidtxidn(mn_config[x].get('collateral_txid'), str(mn_config[x].get('collateral_txidn')))
            if (mns.get(txidtxidn, None) != 'ENABLED' and mns.get(txidtxidn, None) != 'PRE_ENABLED'):
                mns_to_start[x] = mn_config[x]
    
        if len(mns_to_start) > 0 and signing:
            start_masternode(mns_to_start, access, client, args.anounce)

#    # MOVE 
#    ####################
#    unspent_mine = check_listunspent(mn_config, access)
#
#    # make txs list
#    for x in sorted(list(mn_config.keys())):
#        mn_config[x]["txs"] = make_txlist_for_mn(unspent_mine, mn_config.get(x))
#
#    # make tx for keepkey
#    if signing:
#        for x in sorted(list(mn_config.keys())):
#            make_txs_for_keepkey(mn_config[x], client)


def parse_args():

    parser = argparse.ArgumentParser()

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


    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()


if __name__ == "__main__":

    if (sys.version_info < (3, 0)):
        sys.exit('need python3')

    args = parse_args()
    main(args)


# end

