import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from mnb_rpc import *
from mnb_misc import *
 
import simplejson as json


def broadcast_signedrawtx(mn_config, access, whalemode):
    xfertxid = []
    for x in mn_config:
        alias = x.get('alias')
        signedrawtx = x.get('signedrawtx', None)
        vout_addr   = x.get('receiving_address', None)

        if signedrawtx:

            print('\n--->erify tx for %s' % alias)
            print('--->pay_to : %s' % vout_addr)
            for tx in signedrawtx:
                r = decoderawtransaction(tx, access)

                print(
                    json.dumps(
                        r.get('vout'),
                        sort_keys=True,
                        indent=4,
                        separators=(
                            ',',
                            ': ')))

                for i in r.get('vout'):
                    scriptPubKey_addresses = i.get('scriptPubKey').get('addresses')[0]
                    if vout_addr != scriptPubKey_addresses:
                        err_msg = 'pay_to address is not match with signedrawtx'
                        print_err_exit(
                            get_caller_name(),
                            get_function_name(),
                            err_msg)


                if not whalemode:
                    user_input = input(
                        '\nBroadcast signed raw tx ? Yes / (any key to no) : ')
                    if user_input.lower() == 'yes':
                        print('\nYes, will broadcast')
                    else:
                        print('\nNo.')
                        continue

                s = sendrawtransaction(tx, access)
                xfertxid.append(s)
                print('\n====> txid : %s\n' % s)

    if len(xfertxid) > 0:
        return xfertxid

    else:
        return None
