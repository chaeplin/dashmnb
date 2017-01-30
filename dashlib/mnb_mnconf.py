import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'dashlib'))

import collections
import json

from config import *
from mnb_misc import *
from mnb_rpc import *
from mnb_explorer import *

def check_mtime_of_config(config_py_file_abs_path, masternode_conf_file_abs_path, cache_config_check_abs_path):

    # check file mtime to do config parse again
    mtime_of_masternode_conf = int(os.path.getmtime(masternode_conf_file_abs_path))
    mtime_of_config_py = int(os.path.getmtime(config_py_file_abs_path))

    if os.path.exists(cache_config_check_abs_path):
        mtime_of_cache_config_check = int(os.path.getmtime(cache_config_check_abs_path))
    else:
        return True

    cache_config_statinfo = os.stat(cache_config_check_abs_path)
    if cache_config_statinfo.st_size == 0:
        return True

    if (mtime_of_masternode_conf >= mtime_of_cache_config_check 
       or mtime_of_config_py >= mtime_of_cache_config_check):
        return True

    if time.time() > (mtime_of_cache_config_check + (config_cache_refresh_interval_hour * 60 * 60)): 
        return True

    return False


def checking_mn_config(access, signing, chain_pubkey):

    print('\n---> checking masternode config ....')

    # abs path of config.py, masternode.conf and cachetime of configcache.dat
    masternode_conf_file_abs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../mnconf/' + masternode_conf_file)
    config_py_file_abs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.py')
    cache_config_check_abs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../cache/' + ('MAINNET' if MAINNET else 'TESTNET') + '-configcache.dat')

    bParseConfigAgain = check_mtime_of_config(config_py_file_abs_path, masternode_conf_file_abs_path, cache_config_check_abs_path)


    if bParseConfigAgain:
        lines = []
        if os.path.exists(masternode_conf_file_abs_path):
            with open(masternode_conf_file_abs_path) as mobj:
                for line in mobj:
                    lines.append(line.strip())
    
            parse_masternode_conf(lines, access, chain_pubkey, cache_config_check_abs_path)


        else:
            err_msg = 'no %s file' % masternode_conf_file
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)


    with open(cache_config_check_abs_path) as data_file:    
        mn_config_all = json.load(data_file)

    print('\n[masternodes config]')
    print('\tconfigured : %s' % mn_config_all.get('configured'))
    print('\tpassed     : %s' % len(mn_config_all.get('mn_config')))
 
    if 'alias' in mn_config_all.get('errorsnprogress'):
        print('\n[duplicated alias]')
        for x in [item for item, count in collections.Counter(
                mn_config_all.get('mn_v_alias')).items() if count > 1]:
            print('\t %s' % x)
 
    if 'ip:port' in mn_config_all.get('errorsnprogress'):
        print('\n[duplicated ip:port]')
        for x in [item for item, count in collections.Counter(
                mn_config_all.get('mn_v_ipport')).items() if count > 1]:
            print('\t %s' % x)
 
    if 'mn_private_key' in mn_config_all.get('errorsnprogress'):
        print('\n[duplicated mn_private_key]')
        for x in [item for item, count in collections.Counter(
                mn_config_all.get('mn_v_mnprivkey_wif')).items() if count > 1]:
            print('\t %s' % x)
 
    if 'txid_index' in mn_config_all.get('errorsnprogress'):
        print('\n[duplicated txid_index]')
        for x in [item for item, count in collections.Counter(
                mn_config_all.get('mn_v_txidtxidn')).items() if count > 1]:
            print('\t %s' % x)
 
    if len(mn_config_all.get('errorinconf')) > 0:
        signing = False
        print('\n[errors in config]')
        for x in mn_config_all.get('errorinconf'):
            print('\t %s' % x)

    if MOVE_1K_COLLATERAL:
        signing = True

    check_wallet_lock(access)
    mns = check_masternodelist(access)
    mna = check_masternodeaddr(access)

    return mn_config_all.get('mn_config'), signing, mns, mna


def parse_masternode_conf(lines, access, chain_pubkey, cache_config_check_abs_path):

    i = 0
    lno = 0

    mn_config = []
    errorinconf = []

    mn_v_alias = []
    mn_v_ipport = []
    mn_v_mnprivkey_wif = []
    mn_v_txidtxidn = []

    for line in lines:
        lno += 1
        if line.startswith('#'):
            continue

        s = line.split(' ')
        if len(s) < 5:
            continue

        alias = s[0]
        ipport = s[1]
        mnprivkey_wif = s[2]
        txid = s[3]
        txidn = s[4]

        if len(s) == 6:
            raddr = s[5]
        elif len(s) == 5:
            raddr = default_receiving_address

        lineno = lno

        i += 1

        ###############################
        mn_v_alias.append(alias)
        mn_v_ipport.append(ipport)
        mn_v_mnprivkey_wif.append(mnprivkey_wif)

        print('\tmasternode : ' + alias)
        printdbg('parse_masternode_conf :' + alias)

        txidtxidn = get_txidtxidn(txid, txidn)
        mn_v_txidtxidn.append(txidtxidn)

        printdbg('\trawtxid for')
        mnaddr = get_rawtxid(alias, txid, txidn, access)
        if mnaddr is None:
            errorinconf.append(
                'line: %d : %s : no matching txid with 1K collateral in blockchain' %
                (lno, alias))
            continue

        printdbg('\tget_explorer_balance for')
        collateral_exp_balance = float(get_explorer_balance(mnaddr))
        if collateral_exp_balance < 1000:
            errorinconf.append(
                'line: %d : %s : collateral_address has less than 1K balance : %s' %
                (lno, alias, collateral_exp_balance))
            if not MOVE_1K_COLLATERAL:
                continue

        printdbg('\tprocess_chain for')

        if mnaddr in chain_pubkey:
            collateral_spath = chain_pubkey.get(mnaddr).get('spath', None)
            collateral_pubkey = chain_pubkey.get(mnaddr).get('addrpubkey', None)
        else:
            err_msg = 'collateral_address not ip bip32 path(ex: Passphrase err) : ' + alias
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

        if collateral_spath is None or collateral_pubkey is None:
            errorinconf.append(
                'line: %d : %s : can\'t find spath and publickey' %
                (lno, alias))
            continue

        printdbg('\tget masternode_pubkey for')
        try:
            masternode_pubkey = get_public_key(
                wif_to_privkey(mnprivkey_wif).get('privkey')).get('pubkeyhex')

        except:
            errorinconf.append(
                'line: %d : %s : has wrong masternode private key' %
                (lno, alias))
            continue

        masternode_address = pubkey_to_address(masternode_pubkey)

        printdbg('\tvalidateaddress for')

        if (validateaddress(mnaddr, access, False) is None):
            err_msg = 'collateral_address error : ' + alias
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

        if (validateaddress(masternode_address, access, False) is None):
            err_msg = 'masternode_address error : ' + alias
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

        if (validateaddress(raddr, access, False) is None):
            err_msg = 'receiving_address error : ' + alias
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

        printdbg('\tvalidateaddress for')

        # import mnprivkey_wif
        validate_masternode_address = validateaddress(
            masternode_address, access, True)
        # None or validate_masternode_address == False:
        if not validate_masternode_address:
            printdbg('\timportprivkey for')
            importprivkey(mnprivkey_wif, masternode_address, access)

        # import watch only address
        validate_collateral_address = validateaddress(
            mnaddr, access, False)
        # or validate_collateral_address == False:
        if not validate_collateral_address:
            printdbg('\timportaddress for')
            importaddress(mnaddr, access)

        mn_config.append({
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
        })

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

    mn_config_all = {
                "mn_config": mn_config,
                "configured": i,
                "mn_v_alias": mn_v_alias,
                "mn_v_ipport": mn_v_ipport,
                "mn_v_mnprivkey_wif": mn_v_mnprivkey_wif,
                "mn_v_txidtxidn": mn_v_txidtxidn,
                "errorinconf": errorinconf,
                "errorsnprogress": errorsnprogress
    }

    with open(cache_config_check_abs_path, 'w') as outfile:
        json.dump(mn_config_all, outfile)

    #return mn_config_all

# end
