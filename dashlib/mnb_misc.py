import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

import time

def clear_screen():
    os.system('clear')

def check_version():
    from mnb_explorer import get_version_txt

    cur_version = get_dashmnbversion()
    git_version = get_version_txt()

    if ((cur_version.get('major') != git_version.get('major')) or \
         (cur_version.get('minor') != git_version.get('minor')) or \
         (cur_version.get('fix') != git_version.get('fix'))):

        print('\t*** New version is available, ple update ! do git pull\n')
        if git_version.get('msgs', None):
            print('\t*** %s\n\n' % git_version.get('msgs', None))

def logo_show():
    
    from pyfiglet import Figlet
    from config import MAINNET
    from config import MOVE_1K_COLLATERAL

    f = Figlet(font='slant')
    #f = Figlet(font='small')
    print(f.renderText('Dash Masternode with HW Wallet'))
    #print('\n\t\t\tdonation : xxxxxxxxxx')
    print('\t\t\tby : chaeplin\n')
    check_version()
    print('Network : ' + ('MAINNET' if MAINNET else 'TESTNET'))
    if MOVE_1K_COLLATERAL:
        print()
        print('**** MOVE_1K_COLLATERAL is True *******')
        print()
        time.sleep(5)

    else:
        time.sleep(1)

    # clear_screen()


def get_xferblockcount_cache(getblock=False):
    from config import MAINNET
    import simplejson as json
    
    xferblockcount_cache_abs_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '../cache/' + ('MAINNET' if MAINNET else 'TESTNET') + '-xferblockcount.dat')

    if getblock:
        xferblockcount = 0
        if os.path.exists(xferblockcount_cache_abs_path):
            with open(xferblockcount_cache_abs_path) as data_file:
                xferblockcount = json.load(data_file)

        return  xferblockcount
    else:
    
        return xferblockcount_cache_abs_path

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
        mna_ip = mna.get(m.get('collateral_txidtxidn', '-------'), '-')
        mns_status = mns.get(m.get('collateral_txidtxidn', '-------'), '-')
        if m.get('ipport') != mna_ip:
            ipmatch = '-'
        else:
            ipmatch = 'm'
        print_mnlist(m, ipmatch, mns_status)

    print('\n* be sure to check masternode status again using online tools like dashninja')


def get_function_name():
    return sys._getframe(1).f_code.co_name


def get_caller_name():
    return sys._getframe(2).f_code.co_name


def get_dashmnbversion():
    import simplejson as json
    version_file = os.path.join( os.path.dirname( os.path.abspath(__file__)), 'version.txt')
    with open(version_file) as data_file:
        data = json.load(data_file)
    return data

def print_err_exit(
        caller_name,
        function_name,
        err_msg,
        errargs=None):

    VERSION = get_dashmnbversion()

    msg = '\n\n\tversion  : %s.%s.%s\n' % (VERSION.get('major'), VERSION.get('minor'), VERSION.get('fix'))
    msg += '\tcaller   : %s\n' % caller_name
    msg += '\tfunction : %s\n' % function_name 
    if errargs:
        msg += '\terr      : %s' % str(errargs)
    msg += '\t===> %s\n' % err_msg

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
