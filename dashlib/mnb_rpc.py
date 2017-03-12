import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from config import *
from dash_tx import *
from mnb_misc import *


def get_rawtxid(alias, txid, txidn, access):
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
        err_msg = '\n\t===> 1) check account_no\n\t===> 2) Dash-QT or dashd running ?'
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


def checksynced(protocolversion, access):
    if 'rpcusessl' in globals() and rpcusessl and rpcbindip == "test.stats.dash.org":
        return True

    try:
        status = access.mnsync('status')
#        if MOVE_1K_COLLATERAL:
#            return True

        if protocolversion > 70201:
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
    spinner = Spinner('\n--> checking syncing status ')
    protocolversion = rpcgetinfo(access)

    while(not checksynced(protocolversion, access)):
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


def validateaddress(address, access):
    try:
        r = access.validateaddress(address)
        return r.get('isvalid')

    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
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


def getaddressbalance(address, access):
    try:
        params = {
            "addresses": [address]
        }
        r = access.getaddressbalance(params)
        return r.get('balance')

    except Exception as e:
        err_msg = '\n\tif dashd/QT is running, check\n\thttps://github.com/chaeplin/dashmnb#to-run-own-dashd--dash-qt'
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg,
            e.args)


def getaddressbalancewithoutexcept(address, access):
    try:
        params = {
            "addresses": [address]
        }
        r = access.getaddressbalance(params)
        return r.get('balance')

    except:
        return 0


def getaddressutxos(address, access):
    try:
        params = {
            "addresses": [address]
        }
        r = access.getaddressutxos(params)
        return r

    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg,
            e.args)

def getaddressmempool(address, access):
    try:
        params = {
            "addresses": [address]
        }
        r = access.getaddressmempool(params)
        return r

    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg,
            e.args)    

#def get_listunspent(min, max, address, access):
#    try:
#        r = access.listunspent(min, max, [address])
#        return r
#
#    except Exception as e:
#        err_msg = 'Dash-QT or dashd running ?'
#        print_err_exit(
#            get_caller_name(),
#            get_function_name(),
#            err_msg,
#            e.args)
#

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


def get_block_hash(no, access):
    try:
        r = access.getblockhash(no)
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


def rpc_getproposals(access):
    try:
        r = access.gobject('list', 'valid', 'proposals')
        return r

    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg,
            e.args)


def rpc_getcurrentvotes(proposal_hash, access):
    try:
        r = access.gobject('getcurrentvotes', proposal_hash)
        return r

    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg,
            e.args)


def rpc_voteraw(voteconf, access):
    try:
        masternodetxhash = voteconf['collateral_txid']
        masternodetxindex = voteconf['collateral_txidn']
        governancehash = voteconf['proposal_hash']
        vote = voteconf['vote']
        sigtime = int(voteconf['sig_time'])
        votesig = voteconf['sig']

        r = access.voteraw(
            masternodetxhash,
            masternodetxindex,
            governancehash,
            'funding',
            vote,
            sigtime,
            votesig)
        return r

    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg,
            e.args)

# end
