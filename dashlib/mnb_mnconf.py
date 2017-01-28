import sys, os
sys.path.append( os.path.join( os.path.dirname(__file__), '..' ) )
sys.path.append( os.path.join( os.path.dirname(__file__), '..', 'dashlib' ) )

import collections

from config import *
from mnb_misc import *
from mnb_rpc import *
from mnb_explorer import *

def checking_mn_config(access, signing, chain_pubkey, tunnel=None):
    
    print('\n---> checking masternode config ....')
    lines =[]
    if os.path.exists(masternode_conf_file):
        with open(masternode_conf_file) as mobj:
            for line in mobj:            
                lines.append(line.strip())
   
        mn_config, signing = parse_masternode_conf(lines, access, signing, chain_pubkey, tunnel)
    
    else:
        err_msg = 'no %s file' % masternode_conf_file
        print_err_exit(get_caller_name(), get_function_name(), err_msg, None, tunnel)

    check_wallet_lock(access)
    mns = check_masternodelist(access)
    mna = check_masternodeaddr(access)

    return mn_config, signing, mns, mna

def parse_masternode_conf(lines, access, signing, chain_pubkey, tunnel=None):

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

        print('\tmasternode : ' + alias )
        printdbg('parse_masternode_conf :' + alias )
        
        txidtxidn = get_txidtxidn(txid, txidn)
        mn_v_txidtxidn.append(txidtxidn)

        printdbg('\trawtxid for')
        mnaddr = get_rawtxid(alias, txid, txidn, access, tunnel)
        if mnaddr == None:
            errorinconf.append('line: %d / %s : no matching txid with 1K collateral in blockchain' % (lno, alias))
            continue

        printdbg('\tget_explorer_balance for')
        collateral_exp_balance = float(get_explorer_balance(mnaddr))
        if collateral_exp_balance < 1000:
            errorinconf.append('line: %d / %s : collateral_address has less than 1K balance : %s' % (lno, alias, collateral_exp_balance))
            if MOVE_1K_COLLATERAL == False:
                continue

        printdbg('\tprocess_chain for')
        #check_mpath = process_chain(mnaddr, txid, txidn, alias, mpath, xpub)
        #if check_mpath == None:
        #    errorinconf.append('line: %d / %s : can\'t find spath and publickey' % (lno, alias))
        #    continue

        if mnaddr in chain_pubkey:
            collateral_spath = chain_pubkey.get(mnaddr).get('spath', None)
            collateral_pubkey = chain_pubkey.get(mnaddr).get('addrpubkey', None)
        else:
            err_msg = 'collateral_address not ip bip32 path(ex: Passphrase err) : ' +  alias
            print_err_exit(get_caller_name(), get_function_name(), err_msg, None, tunnel)

        if collateral_spath == None or collateral_pubkey == None:
            errorinconf.append('line: %d / %s : can\'t find spath and publickey' % (lno, alias))
            continue


        printdbg('\tget masternode_pubkey for')
        try:
            masternode_pubkey  = get_public_key(wif_to_privkey(mnprivkey_wif).get('privkey')).get('pubkeyhex')
        
        except:
            errorinconf.append('line: %d / %s : has wrong masternode private key' % (lno, alias))
            continue

        masternode_address = pubkey_to_address(masternode_pubkey)

        printdbg('\tvalidateaddress for')

        if (validateaddress(mnaddr, access, False, tunnel) == None):
            err_msg = 'collateral_address error : ' +  alias
            print_err_exit(get_caller_name(), get_function_name(), err_msg, None, tunnel)

        if (validateaddress(masternode_address, access, False, tunnel) == None): 
            err_msg = 'masternode_address error : ' +  alias
            print_err_exit(get_caller_name(), get_function_name(), err_msg, None, tunnel)

        if (validateaddress(raddr, access, False, tunnel) == None): 
            err_msg = 'receiving_address error : ' +  alias
            print_err_exit(get_caller_name(), get_function_name(), err_msg, None, tunnel)

        printdbg('\tvalidateaddress for')

        # import mnprivkey_wif
        validate_masternode_address = validateaddress(masternode_address, access, True, tunnel)
        if validate_masternode_address != True: # None or validate_masternode_address == False:
            printdbg('\timportprivkey for')
            importprivkey(mnprivkey_wif, masternode_address, access)

        # import watch only address
        validate_collateral_address = validateaddress(mnaddr, access, False, tunnel)
        if validate_collateral_address != True:  # or validate_collateral_address == False:
            printdbg('\timportaddress for')
            importaddress(mnaddr, access, tunnel)

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
            "collateral_exp_balance": collateral_exp_balance,
            "receiving_address": raddr
        }

        printdbg('\tdone for')
            
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
    #if len(errorsnprogress) > 0:
    #    signing  = False
    #    print('\tdups       : %s' % errorsnprogress)

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
    if MOVE_1K_COLLATERAL == True:
        return mn_config, True

    else:
        return mn_config, signing

# end