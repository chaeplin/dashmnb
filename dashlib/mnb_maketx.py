import sys, os
sys.path.append( os.path.join( os.path.dirname(__file__), '..' ) )
sys.path.append( os.path.join( os.path.dirname(__file__), '..', 'dashlib' ) )

from config import *
from mnb_misc import *
from mnb_rpc import *
from mnb_mnconf import *
#from mnb_bip32 import *
from mnb_hwwallet import *

def print_balance(mn_config):

    need_wallet_rescan = False

    print('[masternodes balance]')
    print('alias\tcnt\tbalance(dashd)\tbalance(explorer)')
    
    for m in sorted(list(mn_config.keys())):
        alias         = mn_config[m].get('alias')
        exp_balance   = mn_config[m].get('collateral_exp_balance')
        if exp_balance == None:
            exp_balance = '---'
        unspent       = mn_config[m].get('collateral_dashd_balance')
        sumofunspent  = sum(unspent)
        cnt           = len(unspent)

        if cnt == 0:
            need_wallet_rescan = True

        print(alias  + '\t' + '{:2d}\t{:13.8f}\t{:13.8f}'.format(cnt, sumofunspent, exp_balance))

    print('\n* count / balance of dashd is spendable\n(over [6 - received, 100 - mnpayment] confirmations)\n')

    if MOVE_1K_COLLATERAL == True:
        return False
    
    else:
        return need_wallet_rescan


def get_unspent_txs(mnconfig, access, tunnel=None):
    collateral_address   = mnconfig.get('collateral_address')
    collateral_txidtxidn = mnconfig.get('collateral_txidtxidn')

    listunspent = get_listunspent(6, 999999999, collateral_address, access, tunnel)

    unspent_mine = []
    balance_mine = []
  
    for m in listunspent:
        unspent_txidtxidn     = get_txidtxidn(m['txid'], m['vout'])
        unspent_amount        = m['amount']
        #unspent_confirmations = m['confirmations'] # dashd listunspent will not show unmatured coinbase transaction

        balance_mine.append(unspent_amount)

        #print(collateral_address, collateral_txidtxidn, unspent_txidtxidn, unspent_amount)

        #print('MOVE_1K_COLLATERAL --> ', MOVE_1K_COLLATERAL)

        if MOVE_1K_COLLATERAL == True:
            #print('1111')
            unspent_mine.append(m)

        elif MOVE_1K_COLLATERAL == False:
            #print('2222')
            #print(unspent_txidtxidn, collateral_txidtxidn, unspent_amount, max_amounts)
            if (unspent_txidtxidn != collateral_txidtxidn) and (unspent_amount < max_amounts): # and unspent_confirmations > min_conf: # dashd listunspent will not show unmatured coinbase transaction
                #print('333333')
                unspent_mine.append(m)    

    #print('unspent_mine ', unspent_mine)

    txs = []
    for x in unspent_mine:
        if x.get('address') == collateral_address:
            tx = {
                "amount": x.get('amount'),
                "txid": x.get('txid'),
                "vout": x.get('vout')
            }
            txs.append(tx)

    sublist = [txs[i:i+max_unspent] for i  in range(0, len(txs), max_unspent)]

    return unspent_mine, sublist, balance_mine

def make_inputs_for_hw_wallet(tx, receiving_address, collateral_spath, client, mpath, tunnel=None):
    # trezor and keepkey
    import binascii
    from decimal import Decimal

    if TYPE_HW_WALLET.lower().startswith("keepkey"):
        import keepkeylib.messages_pb2 as proto
        import keepkeylib.types_pb2 as proto_types    
        from keepkeylib import tx_api
        from keepkeylib.tx_api import TXAPIDashrpc   

    elif TYPE_HW_WALLET.lower().startswith("trezor"):
        import trezorlib.messages_pb2 as proto
        import trezorlib.types_pb2 as proto_types    
        from trezorlib import tx_api
        from trezorlib.tx_api import TXAPIDashrpc         


    tx_api.rpcuser = rpcuser
    tx_api.rpcpassword = rpcpassword
    tx_api.rpcbindip = rpcbindip
    tx_api.rpcport = (rpcport if tunnel == None else SSH_LOCAL_PORT) 
    
    client.set_tx_api(TXAPIDashrpc())

    inputs = []
    outputs = []
    amount_total = 0
    purpose, coin_type, account, change = chain_path(mpath, tunnel)

    if collateral_spath == None or receiving_address == None:
        err_msg = 'make_inputs_for_hw_wallet receiving_address / collateral_spath : Should not None'
        print_err_exit(get_caller_name(), get_function_name(), err_msg, None, tunnel)

    # make input
    for x in tx:
        amount = x.get('amount', None)
        txid   = x.get('txid', None)
        vout   = x.get('vout', None)

        if amount == None or txid == None or vout == None:
            err_msg = 'make_inputs_for_hw_wallet amount / txid / vout : Should not None'
            print_err_exit(get_caller_name(), get_function_name(), err_msg, None, tunnel)

        amount_total += amount
        inputs.append( proto_types.TxInputType(address_n=[purpose | 0x80000000, coin_type | 0x80000000, account | 0x80000000, change, int(collateral_spath)],
                                                    prev_hash=binascii.unhexlify(txid),
                                                    prev_index=vout) )

    txsizefee = round((len(inputs) * 148 + 33 - 10) / 1000) * min_fee

    # minimal fee if input length is < 4, or fee == 0
    # if len(inputs) < 4:
    if txsizefee == 0:
        txsizefee = min_fee    

    # make output based on inputs
    outputs.append( proto_types.TxOutputType(address=receiving_address,
                      amount=int(amount_total * 100000000) - txsizefee,
                      script_type=proto_types.PAYTOADDRESS,
                      ) )


    feetohuman = round(Decimal(txsizefee / 1e8), 4)
    print('\tsend %s, %s txs to %s with fee of %s : total amount : %s\n' % (amount_total - feetohuman, len(tx), receiving_address, feetohuman, amount_total))

    print_hw_wallet_check()


    try:
        (signatures, serialized_tx) = client.sign_tx(coin_name, inputs, outputs)
        return serialized_tx.hex()

    except Exception as e:
        err_msg = str(e.args)
        print_err_exit(get_caller_name(), get_function_name(), err_msg, None, tunnel)

    except KeyboardInterrupt:
        print_err_exit(get_caller_name(), get_function_name(), 'KeyboardInterrupt', None, tunnel)


def make_txs_for_hwwallet(mnconfig, client, mpath, tunnel=None):  
    
    txs = mnconfig.get('txs', None)
    collateral_spath = mnconfig.get('collateral_spath', None)
    receiving_address = mnconfig.get('receiving_address', None)

    if collateral_spath == None or receiving_address == None:
        err_msg = 'make_inputs_for_hw_wallet receiving_address / collateral_spath : Should not None'
        print_err_exit(get_caller_name(), get_function_name(), err_msg, None, tunnel)

    serialized_txs = []
    if txs != None:
        for tx in txs:
            if (len(tx)) >= min_unspent or MOVE_1K_COLLATERAL == True:
                serialized_tx = make_inputs_for_hw_wallet(tx, receiving_address, collateral_spath, client, mpath, tunnel)
                serialized_txs.append(serialized_tx)

            else:
                print('---> count of txs less than min_unspent : %s' % min_unspent)
                return None
    else:
        return None

    return serialized_txs


# end