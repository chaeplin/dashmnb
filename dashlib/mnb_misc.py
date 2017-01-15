import sys, os, time
sys.path.append( os.path.join( os.path.dirname(__file__), '..' ) )
sys.path.append( os.path.join( os.path.dirname(__file__), '..', 'dashlib' ) )


def clear_screen():
    os.system('clear')

def logo_show():
    from pyfiglet import Figlet
    from config import MAINNET
    
    f = Figlet(font='slant')
    #f = Figlet(font='small')
    print(f.renderText('Dash Masternode with HW Wallet'))
    #print('\n\t\t\tdonation : xxxxxxxxxx')
    print('\t\t\tby : chaeplin\n')
    print('Network : ' +  ('MAINNET' if MAINNET else 'TESTNET'))
    time.sleep(3)
    #clear_screen()

def get_txidtxidn(txid, txidn):
    return txid + '-' + str(txidn)

def print_mnlist(lineno, mnconfig, ipmatch, mnstatus):
    print(mnconfig.get('alias') + '\t' + mnconfig.get('ipport') + ':' + ipmatch + '\t' + mnconfig.get('collateral_address') + ' ' + mnstatus)
#    print(alias + '\t' + mnconfig.get('ipport') + '\t' + mnconfig.get('collateral_address') + ' ' + mnstatus)

def print_mnstatus(mn_config, mns, mna):
    print()
    print('[masternodes status]')
    print('alias\tip (m: ip/port match)\tcollateral address\t\t   status')
    for m in sorted(list(mn_config.keys())):
        mna_ip     = mna.get(get_txidtxidn(mn_config[m].get('collateral_txid'), str(mn_config[m].get('collateral_txidn'))), '-------')
        mns_status = mns.get(get_txidtxidn(mn_config[m].get('collateral_txid'), str(mn_config[m].get('collateral_txidn'))), '-------')
        if mn_config[m].get('ipport') != mna_ip:
            ipmatch = '-'
        else:
            ipmatch = 'm'
        print_mnlist(m, mn_config[m], ipmatch, mns_status)
    print()

def get_function_name():
    return sys._getframe(1).f_code.co_name

def get_caller_name():
    return sys._getframe(2).f_code.co_name


# end