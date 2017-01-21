import sys, os
sys.path.append( os.path.join( os.path.dirname(__file__), '..' ) )
sys.path.append( os.path.join( os.path.dirname(__file__), '..', 'dashlib' ) )

from tx import *
from mnb_misc import *

def get_rawtxid(alias, txid, txidn, access, tunnel=None):
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
        print_err_exit(get_caller_name(), get_function_name(), err_msg, e.args, tunnel)


def checksynced(access, tunnel=None):
    try:
        status = access.mnsync('status')
        return status.get('IsSynced')

    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(get_caller_name(), get_function_name(), err_msg, e.args, tunnel)


def check_dashd_syncing(access, tunnel=None):
    from progress.spinner import Spinner
    spinner = Spinner('---> checking dashd syncing status ')
    while(not checksynced(access, tunnel)):
        try:
            spinner.next()
            time.sleep(1)

        except KeyboardInterrupt:
            print_err_exit(get_caller_name(), get_function_name(), 'KeyboardInterrupt', None, tunnel)
            
def check_wallet_lock(access, tunnel=None):
    try:
        getinfo = access.getinfo()
        if getinfo.get('unlocked_until', None) != None:
            print('\n---> please unlock wallet \n\t==> Menu | Setting | Unlock Wallet or \n\t==> (dash-cli) walletpassphrase "passphrase" timeout')

    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(get_caller_name(), get_function_name(), err_msg, e.args, tunnel)

def check_masternodelist(access, tunnel=None):
    try:
        mn_of_net = access.masternodelist()
        return mn_of_net

    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(get_caller_name(), get_function_name(), err_msg, e.args, tunnel)

def check_masternodeaddr(access, tunnel=None):
    try:
        mn_of_net = access.masternodelist('addr')
        return mn_of_net

    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(get_caller_name(), get_function_name(), err_msg, e.args, tunnel)

def validateaddress(address, access, checkismine, tunnel=None):
    r = access.validateaddress(address)
    if r['isvalid'] and r['address'] == address:
        if checkismine:
            return r['ismine']
        else:
            return r['iswatchonly']
    else:
        return None

def importaddress(address, access, tunnel=None):
    try:
        r = access.importaddress(address, address, False)

    except Exception as e:
        err_msg = 'Please enter the wallet passphrase with walletpassphrase first'
        print_err_exit(get_caller_name(), get_function_name(), err_msg, e.args, tunnel)

def importprivkey(privkey, alias, access, tunnel=None):
    try:
        r = access.importprivkey(privkey, alias, False)

    except Exception as e:
        err_msg = 'Please enter the wallet passphrase with walletpassphrase first'
        print_err_exit(get_caller_name(), get_function_name(), err_msg, e.args, tunnel)

def decoderawtransaction(signedrawtx, access, tunnel=None):
    try:
        r = access.decoderawtransaction(signedrawtx)
        return r

    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(get_caller_name(), get_function_name(), err_msg, e.args, tunnel)

def sendrawtransaction(signedrawtx, access, tunnel=None):
    try:
        r = access.sendrawtransaction(signedrawtx)
        return r
        
    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(get_caller_name(), get_function_name(), err_msg, e.args, tunnel)

def get_listunspent(min, max, addsress, access, tunnel=None):
    try:
        r = access.listunspent(min, max, [addsress])
        return r
        
    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(get_caller_name(), get_function_name(), err_msg, e.args, tunnel)

def get_getblockcount(access, tunnel=None):
    try:
        r = access.getblockcount()
        return r
        
    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(get_caller_name(), get_function_name(), err_msg, e.args, tunnel)    

def get_block_hash_for_mnb(access, tunnel=None):
    try:
        r = access.getblockhash(get_getblockcount(access) - 12)
        return r
        
    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(get_caller_name(), get_function_name(), err_msg, e.args, tunnel)    

def rpc_masternode(what, hexto, access, tunnel=None):
    try:
        r = access.masternodebroadcast(what, hexto)
        return r
        
    except Exception as e:
        err_msg = 'Dash-QT or dashd running ?'
        print_err_exit(get_caller_name(), get_function_name(), err_msg, e.args, tunnel)
        

# end