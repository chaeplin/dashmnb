import sys, os
sys.path.append( os.path.join( os.path.dirname(__file__), '..' ) )
sys.path.append( os.path.join( os.path.dirname(__file__), '..', 'dashlib' ) )

from config import *
from mnb_misc import *
from bip32utils import BIP32Key

def process_chain(collateral_address, txid, txidn, alias):
    acc_node = BIP32Key.fromExtendedKey(xpub)
    i = 0
    while True:
        mpathi = '%s/%d' % (mpath, i)
        addr_node = acc_node.ChildKey(i)
        address   = addr_node.Address()
        addrpkey  = addr_node.PublicKey().hex()
        if address == collateral_address:
            return {"spath": i, "addrpubkey": addrpkey}

        if i > max_gab:
            return None

        i += 1

def chain_path(tunnel=None):
    import re
    pathmatch = re.search("^(.*)'/(.*)'/(.*)'/(.*)$", mpath)
    if (pathmatch):
        purpose   = pathmatch.group(1)
        coin_type = pathmatch.group(2)
        account   = pathmatch.group(3)
        change    = pathmatch.group(4)

        return int(purpose), int(coin_type), int(account), int(change)

    else:
        err_msg = 'check bip32 mpath'
        print_err_exit(get_caller_name(), get_function_name(), err_msg, None, tunnel)


# end