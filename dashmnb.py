#!/usr/bin/env python3

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

def check_unspent_ismine(account_list, unspent):
    unspent_address   = unspent['address']
    unspent_txidtxidn = get_txidtxidn(unspent['txid'], unspent['vout'])
    unspent_amount    = unspent['amount']

    if unspent_address in account_list:
        if (account_list.get(unspent_address) != unspent_txidtxidn) and (unspent_amount < 100):
            return True
    else:
        return False

def check_listunspent(mn_config, access):
    account_list = {}
    for uniqalias in mn_config:
        account_list[mn_config[uniqalias]['collateral_address']] = get_txidtxidn(mn_config[uniqalias]['collateral_txid'], mn_config[uniqalias]['collateral_txidn'])
        if not validateaddress(mn_config[uniqalias]['collateral_address'], access, False):
            importaddress(mn_config[uniqalias]['collateral_address'], access)
    
    try:
        unspent_mine = []
        listunspent = access.listunspent(min_conf)
        for unspent in listunspent:
            if check_unspent_ismine(account_list, unspent):
                unspent_mine.append(unspent)

        return unspent_mine

    except Exception as e:
        print(e.args)
        sys.exit("\n\nDash-QT or dashd running ?\n")


def main():

    clear_screen()
    logo_show()

    serverURL = 'http://' + rpcuser + ':' + rpcpassword + '@' + rpcbindip + ':' + str(rpcport)
    access = AuthServiceProxy(serverURL) 

    if TYPE_HW_WALLET == 'Keepkey':
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
    
    spinner = Spinner('---> checking dashd syncing status ')
    while(not checksynced(access)):
        try:
            spinner.next()
            time.sleep(1)
    
        except:
            sys.exit()    

    print('\n---> checking masternode config')
    lines =[]
    if os.path.exists(masternode_conf_file):
        with open(masternode_conf_file) as mobj:
            for line in mobj:            
                lines.append(line.strip())
   
        mn_config, signing = parse_masternode_conf(lines, access, signing)
        # to test invalid masternode config, need hw wallet
        # signing  = True
    
    else:
        sys.exit('no %s file' % masternode_conf_file)

    check_wallet_lock(access)
    mns = check_masternodelist(access)
    mna = check_masternodeaddr(access)

    print_mnstatus(mn_config, mns, mna)

    #if args.l:
    #    sys.exit()

    mns_to_start = {}
    for x in sorted(list(mn_config.keys())):
        txidtxidn = get_txidtxidn(mn_config[x].get('collateral_txid'), str(mn_config[x].get('collateral_txidn')))
        if (mns.get(txidtxidn, None) != 'ENABLED' and mns.get(txidtxidn, None) != 'PRE_ENABLED'):
            mns_to_start[x] = mn_config[x]

    if len(mns_to_start) > 0 and signing:
        start_masternode(mns_to_start, access, client)

#    unspent_mine = check_listunspent(mn_config, access)
#    print(json.dumps(unspent_mine, sort_keys=True, indent=4, separators=(',', ': ')))

def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('-a','--anounce', 
                        help='anounce missing masternodes')                        

    parser.add_argument("-l",
                        help='print masternode status')   

    return parser.parse_args()



if __name__ == "__main__":
    
#    args = parse_args()
#    main(args)

    main()




# end




# end of mnb.py
