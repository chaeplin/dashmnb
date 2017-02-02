import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from dash_tx import *
from config import *
from mnb_misc import *


def get_rawtxid(alias, txid, txidn, access):
    #print(get_function_name(), alias)
    try:
        data = access.getrawtransaction(txid)
        rawtx = decoderawtx(data)
        mntxidtxidn = get_txidtxidn(txid, txidn)

        for voutaddr in rawtx.keys():
            if mntxidtxidn == rawtx.get(voutaddr).get('txid'):
                if MOVE_1K_COLLATERAL == False and rawtx.get(
                        voutaddr).get('value') == '1000.00000000':
                    return voutaddr

                if MOVE_1K_COLLATERAL:
                    return voutaddr

        return None

    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg,
            e.args)


def rpcgetinfo(access):
    try:
        getinfo = access.getinfo()
        istestnet = getinfo.get('testnet')

        if MAINNET and istestnet:
            err_msg = 'dashd is on testnet, check config plz'
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

        if MAINNET == False and istestnet == False:
            err_msg = 'dashd is on mainnet, check config plz'
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

        return getinfo.get('protocolversion')

    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg,
            e.args)


def checksynced(access, pversion=False):
    protocolversion = rpcgetinfo(access)

    try:
        status = access.mnsync('status')

        if protocolversion > 70201:
            if pversion:
                return protocolversion
            else:
                return status.get('IsSynced')

        else:
            err_msg = 'Dash 12.0 not supported'
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg,
            e.args)


def check_dashd_syncing(access):
    from progress.spinner import Spinner
    spinner = Spinner('\n---> checking dashd syncing status ')
    protocolversion = checksynced(access, True)

    while(not checksynced(access, False)):
        try:
            spinner.next()
            time.sleep(1)

        except KeyboardInterrupt:
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                'KeyboardInterrupt')

    print('\n')
    return protocolversion


def check_wallet_lock(access):
    try:
        getinfo = access.getinfo()
        if getinfo.get('unlocked_until', None) is not None:
            print('\n---> please unlock wallet \n\t==> Menu | Setting | Unlock Wallet or \n\t==> (dash-cli) walletpassphrase "passphrase" timeout')

    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg,
            e.args)


def check_masternodelist(access):
    try:
        mn_of_net = access.masternodelist()
        return mn_of_net

    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg,
            e.args)


def check_masternodeaddr(access):
    try:
        mn_of_net = access.masternodelist('addr')
        return mn_of_net

    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg,
            e.args)


def validateaddress(address, access, checkismine):
    # print(address)
    r = access.validateaddress(address)
    if r.get('isvalid') and r.get('address') == address:
        if checkismine:
            return r.get('ismine')
        else:
            return r.get('iswatchonly', False)
    else:
        return None


def importaddress(address, access):
    try:
        r = access.importaddress(address, address, False)

    except Exception as e:
        err_msg = 'Please enter the wallet passphrase with walletpassphrase first'
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg,
            e.args)


def importprivkey(privkey, alias, access):
    try:
        r = access.importprivkey(privkey, alias, False)

    except Exception as e:
        err_msg = 'Please enter the wallet passphrase with walletpassphrase first'
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg,
            e.args)


def decoderawtransaction(signedrawtx, access):
    try:
        r = access.decoderawtransaction(signedrawtx)
        return r

    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg,
            e.args)


def sendrawtransaction(signedrawtx, access):
    try:
        r = access.sendrawtransaction(signedrawtx)
        return r

    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg,
            e.args)


def get_listunspent(min, max, addsress, access):
    try:
        r = access.listunspent(min, max, [addsress])
        return r

    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg,
            e.args)


def get_getblockcount(access):
    try:
        r = access.getblockcount()
        return r

    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg,
            e.args)


def get_block_hash_for_mnb(access):
    try:
        r = access.getblockhash(get_getblockcount(access) - 12)
        return r

    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg,
            e.args)


def rpc_masternode(what, hexto, access):
    try:
        r = access.masternodebroadcast(what, hexto)
        return r

    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg,
            e.args)


# end
