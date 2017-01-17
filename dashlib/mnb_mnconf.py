import sys, os
sys.path.append( os.path.join( os.path.dirname(__file__), '..' ) )
sys.path.append( os.path.join( os.path.dirname(__file__), '..', 'dashlib' ) )

import collections

from config import *
from mnb_misc import *
from mnb_rpc import *
from mnb_bip32 import *

def checking_wallet_rescan(mn_config, access):
    
    need_wallet_rescan = False
    listunspent = []

    # todo : use listunspent 0 9999999999 address, get unspent for each address, not all unspent
    try:
        get_listunspent = access.listunspent(0)
    
    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(get_caller_name(), get_function_name(), err_msg, e.args)

    for x in get_listunspent:
        unspent_address = x.get('address')
        unspent_txid    = x.get('txid')
        unspent_txidn   = str(x.get('vout'))
        unspent_amount  = str(x.get('amount'))
        unspent_ = unspent_address + ':' + unspent_txid + ':' + unspent_txidn + ':' + unspent_amount
        listunspent.append(unspent_)

    for m in mn_config:
        collateral_address = mn_config.get(m).get('collateral_address')
        collateral_txid    = mn_config.get(m).get('collateral_txid')
        collateral_txidn   = mn_config.get(m).get('collateral_txidn')
        collateral_ = collateral_address + ':' + collateral_txid  + ':' + str(collateral_txidn) + ':' + '1000.00000000'

        if collateral_ not in listunspent:
            need_wallet_rescan = True

    return need_wallet_rescan

def checking_mn_config(access, signing):
    
    print('\n---> checking masternode config')
    lines =[]
    if os.path.exists(masternode_conf_file):
        with open(masternode_conf_file) as mobj:
            for line in mobj:            
                lines.append(line.strip())
   
        mn_config, signing = parse_masternode_conf(lines, access, signing)
    
    else:
        err_msg = 'no %s file' % masternode_conf_file
        print_err_exit(get_caller_name(), get_function_name(), err_msg)

    check_wallet_lock(access)
    mns = check_masternodelist(access)
    mna = check_masternodeaddr(access)

    return mn_config, signing, mns, mna

def parse_masternode_conf(lines, access, signing):

    i = 0
    lno = 0

    mn_config = {}
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

        if len(s) == 6:
            raddr     = s[5]
        elif len(s) == 5:
            raddr     = default_receiving_address

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

        masternode_address = pubkey_to_address(masternode_pubkey)

        if (validateaddress(mnaddr, access, False) == None): sys.exit('collateral_address error on ' + get_function_name())
        if (validateaddress(masternode_address, access, False) == None): sys.exit('masternode_address error on ' + get_function_name())
        if (validateaddress(raddr, access, False) == None): sys.exit('masternode_address error on ' + get_function_name())

        # import mnprivkey_wif
        validate_masternode_address = validateaddress(masternode_address, access)
        if validate_masternode_address == None or validate_masternode_address == False:
            importprivkey(mnprivkey_wif, masternode_address, access)

        # import watch only address
        validate_collateral_address = validateaddress(mnaddr, access, False)
        if validate_collateral_address == None or validate_collateral_address == False:
            importaddress(mnaddr, access)

        mn_config[lineno] = {
            "alias": alias,
            "lineno": str(lineno),
            "ipport": ipport,
            "masternode_privkey": mnprivkey_wif,
            "masternode_pubkey": masternode_pubkey,
            "masternode_address": masternode_address,
            "collateral_txid": txid,
            "collateral_txidn": int(txidn),
            "collateral_txidtxidn": txidtxidn,
            "collateral_spath": collateral_spath,
            "collateral_pubkey": collateral_pubkey,
            "collateral_address": mnaddr,
            "receiving_address": raddr
        }
            
    ###########################################
    if len(mn_config) != i:
        errorsnprogress.append('alias')

    if len(mn_config) != len(mn_v_ipport):
        errorsnprogress.append('ip:port')        

    if len(mn_config) != len(mn_v_mnprivkey_wif):
        errorsnprogress.append('mn_private_key')

    if len(mn_config) != len(mn_v_txidtxidn):
        errorsnprogress.append('txid_index')    

    ############################################

    print('\n[masternodes config]')
    print('\tconfigured : %s' % i)
    print('\tpassed     : %s' % len(mn_config))
    if len(errorsnprogress) > 0:
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
        signing  = False
        print('\n[errors in config]')
        for x in errorinconf:
            print('\t %s' % x)

    print()
    return mn_config, signing

# end