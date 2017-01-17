import sys, os
sys.path.append( os.path.join( os.path.dirname(__file__), '..' ) )
sys.path.append( os.path.join( os.path.dirname(__file__), '..', 'dashlib' ) )

from tx import *
from mnb_misc import *

def get_rawtxid(alias, txid, txidn, access):
    #print(get_function_name(), alias)
    try:
        data = access.getrawtransaction(txid)
        rawtx = decoderawtx(data)
        mntxidtxidn = get_txidtxidn(txid, txidn)

        for voutaddr in rawtx.keys():
            if mntxidtxidn == rawtx.get(voutaddr).get('txid') and rawtx.get(voutaddr).get('value') == '1000.00000000':
                return voutaddr

        return None

    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(get_caller_name(), get_function_name(), err_msg, e.args)


def checksynced(access):
    try:
        status = access.mnsync('status')
        return status.get('IsSynced')

    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(get_caller_name(), get_function_name(), err_msg, e.args)


def check_dashd_syncing(access):
    from progress.spinner import Spinner
    spinner = Spinner('---> checking dashd syncing status ')
    while(not checksynced(access)):
        spinner.next()
        time.sleep(1)
            
def check_wallet_lock(access):
    try:
        getinfo = access.getinfo()
        if getinfo.get('unlocked_until', None) != None:
            print('\n---> please unlock wallet \n\t==> Menu | Setting | Unlock Wallet or \n\t==> (dash-cli) walletpassphrase "passphrase" timeout')

    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(get_caller_name(), get_function_name(), err_msg, e.args)

def check_masternodelist(access):
    try:
        mn_of_net = access.masternodelist()
        return mn_of_net

    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(get_caller_name(), get_function_name(), err_msg, e.args)

def check_masternodeaddr(access):
    try:
        mn_of_net = access.masternodelist('addr')
        return mn_of_net

    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(get_caller_name(), get_function_name(), err_msg, e.args)

def validateaddress(address, access, checkismine=True):
    r = access.validateaddress(address)
    if r['isvalid'] and r['address'] == address:
        if checkismine:
            return r['ismine']
        else:
            return r['iswatchonly']
    else:
        return None

def importaddress(address, access):
    try:
        r = access.importaddress(address, address, False)

    except Exception as e:
        err_msg = 'Please enter the wallet passphrase with walletpassphrase first'
        print_err_exit(get_caller_name(), get_function_name(), err_msg, e.args)

def importprivkey(privkey, alias, access):
    try:
        r = access.importprivkey(privkey, alias, False)

    except Exception as e:
        err_msg = 'Please enter the wallet passphrase with walletpassphrase first'
        print_err_exit(get_caller_name(), get_function_name(), err_msg, e.args)

def decoderawtransaction(signedrawtx, access):
    try:
        r = access.decoderawtransaction(signedrawtx)
        return r

    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(get_caller_name(), get_function_name(), err_msg, e.args)

def sendrawtransaction(signedrawtx, access):
    try:
        r = access.sendrawtransaction(signedrawtx)
        return r
        
    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(get_caller_name(), get_function_name(), err_msg, e.args)


# end