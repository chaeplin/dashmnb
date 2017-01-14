import sys, os
sys.path.append( os.path.join( os.path.dirname(__file__), '..' ) )
sys.path.append( os.path.join( os.path.dirname(__file__), '..', 'dashlib' ) )

import collections
from config import *
from mnb_rpc import *
from mnb_misc import *
from mnb_bip32 import *

def parse_masternode_conf(lines, access, signing):

    i = 0
    lno = 0

    mn_conf = {}
    errorinconf = []

    mn_v_alias         = []
    mn_v_ipport        = []
    mn_v_mnprivkey_wif = []
    mn_v_txidtxidn     = []

    for line in lines:
        lno += 1
        if line.startswith('#'):
            continue

        s = line.split(' ')
        if len(s) < 5:
            continue

        alias         = s[0]
        ipport        = s[1]
        mnprivkey_wif = s[2]
        txid          = s[3]
        txidn         = s[4]

        lineno        = lno

        i += 1

        ###############################
        mn_v_alias.append(alias)
        mn_v_ipport.append(ipport)
        mn_v_mnprivkey_wif.append(mnprivkey_wif)

        txidtxidn = get_txidtxidn(txid, txidn)
        mn_v_txidtxidn.append(txidtxidn)

        mnaddr = get_rawtxid(alias, txid, txidn, access)
        if mnaddr == None:
            errorinconf.append('line: %d / %s : no matching txid in blockchain' % (lno, alias))
            continue

        check_mpath = process_chain(mnaddr, txid, txidn, alias)
        if check_mpath == None:
            errorinconf.append('line: %d / %s : can\'t find spath and publickey' % (lno, alias))
            continue

        collateral_spath = check_mpath.get('spath', None)
        collateral_pubkey = check_mpath.get('addrpubkey', None)

        try:
            masternode_pubkey  = get_public_key(wif_to_privkey(mnprivkey_wif).get('privkey')).get('pubkeyhex')
        
        except:
            errorinconf.append('line: %d / %s : has wrong masternode private key' % (lno, alias))
            continue
            #sys.exit('===> ' + alias + ' has wrong masternode private key')

        masternode_address = pubkey_to_address(masternode_pubkey)

        mn_conf[lineno] = {
            "alias": alias,
            "lineno": str(lineno),
            "ipport": ipport,
            "masternode_privkey": mnprivkey_wif,
            "masternode_pubkey": masternode_pubkey,
            "masternode_address": masternode_address,
            "collateral_txid": txid,
            "collateral_txidn": int(txidn),
            "collateral_spath": collateral_spath,
            "collateral_pubkey": collateral_pubkey,
            "collateral_address": mnaddr
        }
            
    ###########################################
    if len(mn_conf) != i:
        errorsnprogress.append('alias')

    if len(mn_conf) != len(mn_v_ipport):
        errorsnprogress.append('ip:port')        

    if len(mn_conf) != len(mn_v_mnprivkey_wif):
        errorsnprogress.append('mn_private_key')

    if len(mn_conf) != len(mn_v_txidtxidn):
        errorsnprogress.append('txid_index')    

    ############################################

    print('\n[masternodes]')
    print('\tconfigured : %s' % i)
    print('\tpassed     : %s' % len(mn_conf))
    if len(errorsnprogress) > 0:
        announce = False
        signing  = False
        print('\tdups       : %s' % errorsnprogress)

    if 'alias' in errorsnprogress:
        print('\n[duplicated alias]')
        for x in [item for item, count in collections.Counter(mn_v_alias).items() if count > 1]:
            print('\t %s' % x)

    if 'ip:port' in errorsnprogress:
        print('\n[duplicated ip:port]')
        for x in [item for item, count in collections.Counter(mn_v_ipport).items() if count > 1]:
            print('\t %s' % x)
    
    if 'mn_private_key' in errorsnprogress:
        print('\n[duplicated mn_private_key]')
        for x in [item for item, count in collections.Counter(mn_v_mnprivkey_wif).items() if count > 1]:
            print('\t %s' % x)

    if 'txid_index' in errorsnprogress:
        print('\n[duplicated txid_index]')
        for x in [item for item, count in collections.Counter(mn_v_txidtxidn).items() if count > 1]:
            print('\t %s' % x)

    if len(errorinconf) > 0:
        announce = False
        signing  = False
        print('\n[errors in config]')
        for x in errorinconf:
            print('\t %s' % x)

    return mn_conf, signing

