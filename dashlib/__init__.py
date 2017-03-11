import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

import traceback

try:
    from config import *
except:
    print('please config dashlib/config.py')
    sys.exit()

from dash_b58 import *
#from dash_block import *
from dash_ecdsa import *
from dash_hashs import *
from dash_jacobian import *
from dash_keys import *
from dash_script import *
from dash_tx import *
from dash_utils import *
from mnb_explorer import *
from mnb_hwwallet import *
from mnb_makemnb import *
from mnb_maketx import *
from mnb_makevote import *
from mnb_misc import *
from mnb_mnconf import *
from mnb_rpc import *
from mnb_signing import *
from mnb_sshtunnel import *
from mnb_start import *
from mnb_vote import *
from mnb_xfer import *

try:
    assert isinstance(MAINNET, bool)
    assert isinstance(account_no, int)
    assert (account_no >= 0)

    hw_list = ['KEEPKEY', 'TREZOR', 'LEDGERNANOS']
    if TYPE_HW_WALLET.upper() not in hw_list:
        err_msg = 'check TYPE_HW_WALLET in dashlib/config.py'
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg)

except AssertionError:
    _, _, tb = sys.exc_info()
    traceback.print_tb(tb)  # Fixed format
    tb_info = traceback.extract_tb(tb)
    filename, line, func, text = tb_info[-1]

    err_msg = 'An error occurred on line {} in statement {}'.format(line, text)
    print_err_exit(
        get_caller_name(),
        get_function_name(),
        err_msg)
