import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

import collections
import json

from config import *
from mnb_rpc import *


def check_mtime_of_config(
        config_py_file_abs_path,
        masternode_conf_file_abs_path,
        cache_config_check_abs_path,
        showall):

    # check file mtime to do config parse again
    mtime_of_masternode_conf = int(
        os.path.getmtime(masternode_conf_file_abs_path))
    mtime_of_config_py = int(os.path.getmtime(config_py_file_abs_path))

    if os.path.exists(cache_config_check_abs_path):
        mtime_of_cache_config_check = int(
            os.path.getmtime(cache_config_check_abs_path))
    else:
        return True

    cache_config_statinfo = os.stat(cache_config_check_abs_path)
    if cache_config_statinfo.st_size == 0:
        return True

    if (mtime_of_masternode_conf >= mtime_of_cache_config_check
            or mtime_of_config_py >= mtime_of_cache_config_check):
        return True

    if time.time() > (mtime_of_cache_config_check +
                      (config_cache_refresh_interval_hour * 60 * 60)):
        return True

    if showall:
        return True

    return False


def check_collateral_in_chain_pubkey(addrs, chain_pubkey, alias=None):
    # check collateral_address and chain_pubkey again

    printdbg(
        'check_collateral_in_chain_pubkey : caller : %s' %
        get_caller_name())
    printdbg(
        'check_collateral_in_chain_pubkey : type(addrs) : %s' %
        type(addrs))
    printdbg(
        'check_collateral_in_chain_pubkey : chain_pubkey.keys() : %s' %
        chain_pubkey.keys())

    if isinstance(addrs, list):
        for x in addrs:
            collateral_address = x.get('collateral_address')
            printdbg(
                'check_collateral_in_chain_pubkey : collateral_address : %s' %
                collateral_address)
            if collateral_address in chain_pubkey.keys():
                pass
            else:
                err_msg = 'collateral_address %s\n\tnot in bip32 path(ex: Passphrase err) : %s' % (
                    collateral_address, x.get('alias'))
                print_err_exit(
                    get_caller_name(),
                    get_function_name(),
                    err_msg)
    else:
        collateral_address = addrs
        printdbg(
            'check_collateral_in_chain_pubkey : collateral_address : %s' %
            collateral_address)
        if collateral_address in chain_pubkey.keys():
            return True
        else:
            err_msg = 'collateral_address %s\n\tnot in bip32 path(ex: Passphrase err) : %s' % (
                collateral_address, alias)
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)


def checking_mn_config(access, signing, chain_pubkey, showall):

    # abs path of config.py, masternode.conf and cachetime of configcache.dat
    masternode_conf_file_abs_path = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)),
        '../mnconf/' +
        masternode_conf_file)
    config_py_file_abs_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'config.py')
    cache_config_check_abs_path = os.path.join(os.path.dirname(os.path.abspath(
        __file__)), '../cache/' + ('MAINNET' if MAINNET else 'TESTNET') + '-configcache.dat')

    printdbg(
        'checking_mn_config : masternode.conf : %s' %
        masternode_conf_file_abs_path)
    printdbg('checking_mn_config : config.py : %s' % config_py_file_abs_path)
    printdbg(
        'checking_mn_config : config cache : %s' %
        cache_config_check_abs_path)

    if not os.path.exists(masternode_conf_file_abs_path):
        err_msg = 'no %s file' % masternode_conf_file
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg)

    bParseConfigAgain = check_mtime_of_config(
        config_py_file_abs_path,
        masternode_conf_file_abs_path,
        cache_config_check_abs_path,
        showall)

    printdbg(
        'checking_mn_config : bbParseConfigAgain : %s' %
        bParseConfigAgain)

    if bParseConfigAgain:
        print(
            '\n---> checking masternode config using %s ....' %
            masternode_conf_file)
        lines = []
        if os.path.exists(masternode_conf_file_abs_path):
            with open(masternode_conf_file_abs_path) as mobj:
                for line in mobj:
                    lines.append(line.strip())

            parse_masternode_conf(
                lines,
                access,
                chain_pubkey,
                cache_config_check_abs_path,
                showall)

        else:
            err_msg = 'no %s file' % masternode_conf_file
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

    else:
        print('\n---> checking masternode config using cache ....')

    with open(cache_config_check_abs_path) as data_file:
        mn_config_all = json.load(data_file)

    check_collateral_in_chain_pubkey(mn_config_all['mn_config'], chain_pubkey)

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

    # check_wallet_lock(access)
    print()
    print('---> get masternodelist : status')
    printdbg('checking_mn_config : check_masternodelist')
    mns = check_masternodelist(access)

    print('---> get masternodelist : addr')
    printdbg('checking_mn_config : check_masternodeaddr')
    mna = check_masternodeaddr(access)
    printdbg('checking_mn_config : done')

    return mn_config_all.get('mn_config'), signing, mns, mna


def parse_masternode_conf(
        lines,
        access,
        chain_pubkey,
        cache_config_check_abs_path,
        showall):

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
            if len(default_receiving_address) != 0:
                raddr = default_receiving_address
            else:
                raddr = None

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

        printdbg('\tchecking rawtxid..')
        mnaddr = get_rawtxid(alias, txid, txidn, access)
        printdbg('\tchecking rawtxid collateral_address : %s' % mnaddr)
        if mnaddr is None:
            errorinconf.append(
                'line: %d : %s : no matching txid with 1K collateral in blockchain' %
                (lno, alias))
            continue

        printdbg('\tchecking getaddressbalance..')
        collateral_cur_balance = float(getaddressbalance(mnaddr, access) / 1e8)
        printdbg('\tchecking getaddressbalance : %s' % collateral_cur_balance)
        if collateral_cur_balance < 1000:
            errorinconf.append(
                'line: %d : %s : collateral_address has less than 1K balance : %s' %
                (lno, alias, collateral_cur_balance))

            if not MOVE_1K_COLLATERAL and not showall:
                continue

        printdbg('\tprocess_chain ....')
        if check_collateral_in_chain_pubkey(mnaddr, chain_pubkey, alias):
            collateral_spath = chain_pubkey.get(mnaddr).get('spath', None)
            collateral_pubkey = chain_pubkey.get(
                mnaddr).get('addrpubkey', None)
        else:
            err_msg = 'collateral_address not in bip32 path(ex: Passphrase err) : ' + alias
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

        if collateral_spath is None or collateral_pubkey is None:
            errorinconf.append(
                'line: %d : %s : can\'t find spath and publickey' %
                (lno, alias))
            continue

        printdbg('\tget masternode_pubkey ....')
        try:
            masternode_pubkey = get_public_key(
                wif_to_privkey(mnprivkey_wif).get('privkey')).get('pubkeyhex')

        except:
            errorinconf.append(
                'line: %d : %s : has wrong masternode private key' %
                (lno, alias))
            continue

        masternode_address = pubkey_to_address(masternode_pubkey)

        printdbg('\tvalidateaddress ....')

        if not validateaddress(mnaddr, access):
            err_msg = 'collateral_address error : ' + alias
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

        # use rpc to validateaddress
        if not validateaddress(masternode_address, access):
            err_msg = 'masternode_address error : ' + alias
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

        if raddr is not None:
            if not validateaddress(raddr, access):
                err_msg = 'receiving_address error : ' + alias
                print_err_exit(
                    get_caller_name(),
                    get_function_name(),
                    err_msg)

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
            "receiving_address": raddr
        })

        printdbg('\tdone')

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

    # return mn_config_all

# end
