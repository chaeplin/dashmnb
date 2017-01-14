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
        #sys.exit(alias + ' has wrong txid and nout, check masternode_conf')

    except Exception as e:
        print(e.args)
        sys.exit("\n\nDash-QT or dashd running ?\n")


def checksynced(access):
    try:
        status = access.mnsync('status')
        return status.get('IsSynced')

    except Exception as e:
        print("\n")
        print('%s - %s' % (get_function_name(), e.args))
        print('can\'t connect using rpc, is Dash-QT or dashd running ?')
        sys.exit()

def check_wallet_lock(access):
    try:
        getinfo = access.getinfo()
        if getinfo.get('unlocked_until', None) != None:
            print('\n---> please unlock wallet \n\t==> Menu | Setting | Unlock Wallet or \n\t==> (dash-cli) walletpassphrase "passphrase" timeout')

    except Exception as e:
        print("\n")
        print('%s - %s' % (get_function_name(), e.args))
        print('can\'t connect using rpc, is Dash-QT or dashd running ?')
        sys.exit()

def check_masternodelist(access):
    try:
        mn_of_net = access.masternodelist()
        return mn_of_net

    except Exception as e:
        print("\n")
        print('%s - %s' % (get_function_name(), e.args))
        print('can\'t connect using rpc, is Dash-QT or dashd running ?')
        sys.exit()

def check_masternodeaddr(access):
    try:
        mn_of_net = access.masternodelist('addr')
        return mn_of_net

    except Exception as e:
        print("\n")
        print('%s - %s' % (get_function_name(), e.args))
        print('can\'t connect using rpc, is Dash-QT or dashd running ?')
        sys.exit()

def validateaddress(address, access, checkismine=True):
    r = access.validateaddress(address)
    if r['isvalid'] and r['address'] == address:
        if checkismine:
            return r['ismine']
        else:
            return r['iswatchonly']
    else:
        return False
def importaddress(address, access):
    try:
        print('importing watch only address without rescaning the wallet\tRestart dashd with -rescan')
        r = access.importaddress(address, address, False)

    except Exception as e:
        print(e.args)
        sys.exit("\n\nPlease enter the wallet passphrase with walletpassphrase first\n")

def importprivkey(privkey, alias, access):
    try:
        r = access.importprivkey(privkey, alias, False)

    except Exception as e:
        print(e.args)
        sys.exit("\n\nPlease enter the wallet passphrase with walletpassphrase first\n")
        