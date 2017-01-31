import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

import time 
def clear_screen():
    os.system('clear')


def logo_show():
    from pyfiglet import Figlet
    from config import MAINNET
    from config import MOVE_1K_COLLATERAL

    f = Figlet(font='slant')
    #f = Figlet(font='small')
    print(f.renderText('Dash Masternode with HW Wallet'))
    #print('\n\t\t\tdonation : xxxxxxxxxx')
    print('\t\t\tby : chaeplin\n')
    print('Network : ' + ('MAINNET' if MAINNET else 'TESTNET'))
    if MOVE_1K_COLLATERAL:
        print()
        print('**** MOVE_1K_COLLATERAL is True *******')
        print()
        time.sleep(5)

    else:
        time.sleep(1)

    # clear_screen()


def get_txidtxidn(txid, txidn):
    if txid is None or txidn is None:
        return None
    else:
        return txid + '-' + str(txidn)


def print_mnlist(mnconfig, ipmatch, mnstatus):
    print(mnconfig.get('alias') + '\t' + mnconfig.get('ipport') + ':' +
          ipmatch + '\t' + mnconfig.get('collateral_address') + ' ' + mnstatus)


def print_mnstatus(mn_config, mns, mna):
    print()
    print('[masternodes status]')
    print('alias\tip (m: ip/port match)\tcollateral address\t\t   status')

    for m in mn_config:
        mna_ip = mna.get(m.get('collateral_txidtxidn', '-------'))
        mns_status = mns.get(m.get('collateral_txidtxidn', '-------'))
        if m.get('ipport') != mna_ip:
            ipmatch = '-'
        else:
            ipmatch = 'm'
        print_mnlist(m, ipmatch, mns_status)

    print()


def get_function_name():
    return sys._getframe(1).f_code.co_name


def get_caller_name():
    return sys._getframe(2).f_code.co_name


def print_err_exit(
        caller_name,
        function_name,
        err_msg,
        errargs=None):
#    import signal

    msg = '\n\n\tversion  : 0.2a\n'
    msg += '\tcaller   : ' + caller_name + '\n'
    msg += '\tfunction : ' + function_name + '\n'
    if errargs:
        msg += '\terr      : ' + str(errargs) + '\n'
    msg += '\t===> ' + err_msg + '\n'

#    if tunnel:
#        os.kill(tunnel, signal.SIGTERM)

    raise SystemExit(msg)


def now():
    return int(time.time())


def printdbg(str):
    ts = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(now()))
    logstr = "{} {}".format(ts, str)
    if os.environ.get('DASHMNB_DEBUG', None):
        print(logstr)


def print_hw_wallet_check():
    print('---> check hw wallet, check message on screen and press button')
    print('\tif PIN protected, wallet ask your PIN(once per session)')
    print('\tif Passphrase protected, wallet ask your Passphrase(once per session)')
    print('\tcheck message on screen and press button on hw wallet to proceed(all signing)\n')

# end
