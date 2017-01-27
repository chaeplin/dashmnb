import sys, os
sys.path.append( os.path.join( os.path.dirname(__file__), '..' ) )
sys.path.append( os.path.join( os.path.dirname(__file__), '..', 'dashlib' ) )

# use block explorer to check balance, block height to check fork

import requests
from config import *
from mnb_misc import *


def make_request(url, tunnel=None):
    USERAGET = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14'
    headers = {'user-agent': USERAGET}

    try:
        response = requests.get(url, headers=headers, timeout=(3,5))
        if response.status_code == requests.codes.ok and float(response.text) >= 0:
            return response.text

        else:
            return None

    except requests.exceptions.RequestException:
        err_msg = requests.exceptions.RequestException
        print_err_exit(get_caller_name(), get_function_name(), err_msg, None, tunnel)        

    except Exception as e:
        err_msg = str(e.args)
        print_err_exit(get_caller_name(), get_function_name(), err_msg, None, tunnel)


def get_explorer_balance(address, tunnel=None):
    if MAINNET:
        url  = 'https://explorer.dash.org/chain/Dash/q/addressbalance/' + address
    else:
        url  = 'https://test.explorer.dash.org/chain/tDash/q/addressbalance/' + address

    response = make_request(url, tunnel)

    return response

# end