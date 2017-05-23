import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from decimal import Decimal

from config import *
from mnb_misc import *
from mnb_rpc import *
from mnb_mnconf import *
from mnb_hwwallet import *


def print_balance(mn_config, have_unconfirmed_tx):

    need_wallet_rescan = False

    print('[masternodes balance]')
    print('alias\tcnt\tspn\tbalance\t\taddress to send MN earnings')

    for m in mn_config:
        alias = m.get('alias')
        unspent = m.get('collateral_dashd_balance')
        sumofunspent = sum(unspent)
        cnt = len(unspent)

        spn = 0
        for sp in m.get('txs'):
            spn = spn + len(sp)

        if cnt == 0:
            need_wallet_rescan = True

        if 'rpcusessl' in globals() and rpcusessl and rpcbindip == "test.stats.dash.org":
            need_wallet_rescan = False

        if MOVE_1K_COLLATERAL:
            need_wallet_rescan = False

        print(
            alias +
            '\t' +
            '{:2d}\t{:2d}\t{:13.8f}'.format(
                cnt,
                spn,
                sumofunspent) +
            '\t' +
            str(m.get('receiving_address', '----')))

    print('\n* cnt - count    : number of payouts(un + mature) + 1(collateral)')
    print('* spn - spenable : number of spendable payouts(mature)')
    if have_unconfirmed_tx:
        print('* can be inaccurate after a transaction(transfer/xfer), need 1 confirmation')

    return need_wallet_rescan


def check_mtime_of_tx(unspent_cache_abs_path):
    if os.path.exists(unspent_cache_abs_path):
        mtime_of_unspent_cache = int(os.path.getmtime(unspent_cache_abs_path))
        cache_unspent_statinfo = os.stat(unspent_cache_abs_path)

    else:
        return True

    if cache_unspent_statinfo.st_size == 0:
        return True

    if time.time() > (mtime_of_unspent_cache + (txs_cache_refresh_interval_hour * 60 * 60)):
        return True

    return False


def get_unspent_txs(mnconfig, blockcount, access, SEND_TO_BIP32, bip32_unused):

    collateral_address = mnconfig.get('collateral_address')
    collateral_txidtxidn = mnconfig.get('collateral_txidtxidn')

    unspent_cache_abs_path = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)),
        '../cache/' +
        (
            'MAINNET' if MAINNET else 'TESTNET') +
        '-' +
        collateral_txidtxidn +
        '-unspent.dat')

    bgetListUnspentAgain = check_mtime_of_tx(unspent_cache_abs_path)
    if bgetListUnspentAgain:
        #listunspent = get_listunspent(6, 999999999, collateral_address, access)
        listunspent = getaddressutxos(collateral_address, access)
        with open(unspent_cache_abs_path, 'w') as outfile:
            json.dump(listunspent, outfile)
    else:
        with open(unspent_cache_abs_path) as data_file:
            listunspent = json.load(data_file, parse_float=Decimal)

    unspent_mine = []
    balance_mine = []

    for m in listunspent:
        unspent_txidtxidn = get_txidtxidn(m['txid'], m['outputIndex'])
        #unspent_amount = m['amount']
        unspent_amount = round(Decimal(float(m['satoshis'] / 1e8)), 8)

        balance_mine.append(unspent_amount)

        if MOVE_1K_COLLATERAL:
            unspent_mine.append(m)

        elif MOVE_1K_COLLATERAL == False:
            if (unspent_txidtxidn != collateral_txidtxidn) and (
                    unspent_amount < max_amounts):
                unspent_mine.append(m)

    txs = []

    #mature_confirmation = 120
    # for testing
    mature_confirmation = 10

    for x in unspent_mine:
        if (x.get('address') == collateral_address) and ((blockcount - mature_confirmation) > x.get('height')):
            if SEND_TO_BIP32 and bip32_unused != None:
                tx = {
                    "amount": round(Decimal(float(x.get('satoshis') / 1e8)), 8),
                    "txid": x.get('txid'),
                    "vout": x.get('outputIndex'),
                    "bip32sendto": bip32_unused.__next__()
                }

            else:

                tx = {
                    "amount": round(Decimal(float(x.get('satoshis') / 1e8)), 8),
                    "txid": x.get('txid'),
                    "vout": x.get('outputIndex')
                }

            txs.append(tx)

    if SEND_TO_BIP32 and bip32_unused != None:
        return txs, balance_mine

    else:
        sublist = [txs[i:i + max_unspent] for i in range(0, len(txs), max_unspent)]
        return sublist, balance_mine


def make_inputs_for_hw_wallet(
        tx,
        receiving_address,
        collateral_spath,
        client,
        mpath):
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
    tx_api.rpcport = (rpcport if USE_SSH_TUNNEL is False else SSH_LOCAL_PORT)
    if 'rpcusessl' in globals() and rpcusessl:
        tx_api.rpcusessl = rpcusessl

    client.set_tx_api(TXAPIDashrpc())

    inputs = []
    outputs = []
    amount_total = 0
    purpose, coin_type, account, change = chain_path(mpath)

    if collateral_spath is None or receiving_address is None:
        err_msg = 'make_inputs_for_hw_wallet receiving_address / collateral_spath : Should not None'
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg)

    # make input
    for x in tx:
        amount = x.get('amount', None)
        txid = x.get('txid', None)
        vout = x.get('vout', None)

        if amount is None or txid is None or vout is None:
            err_msg = 'make_inputs_for_hw_wallet amount / txid / vout : Should not None'
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

        amount_total += amount
        inputs.append(
            proto_types.TxInputType(
                address_n=[
                    purpose | 0x80000000,
                    coin_type | 0x80000000,
                    account | 0x80000000,
                    change,
                    int(collateral_spath)],
                prev_hash=binascii.unhexlify(txid),
                prev_index=vout))

    txsizefee = round((len(inputs) * 148 + 33 - 10) / 1000) * min_fee

    # minimal fee if input length is < 4, or fee == 0
    # if len(inputs) < 4:
    if txsizefee == 0:
        txsizefee = min_fee

    # make output based on inputs
    outputs.append(
        proto_types.TxOutputType(
            address=receiving_address,
            amount=int(
                amount_total *
                100000000) -
            txsizefee,
            script_type=proto_types.PAYTOADDRESS,
        ))

    feetohuman = round(Decimal(txsizefee / 1e8), 4)
    print('\n\tsend %s\n\t%s txs to %s\n\twith fee of %s\n\ttotal amount : %s\n' % (
        amount_total - feetohuman, len(tx), receiving_address, feetohuman, amount_total))

    print_hw_wallet_check()

    try:
        (signatures, serialized_tx) = client.sign_tx(coin_name, inputs, outputs)
        # check tx size
        if len(serialized_tx.hex()) > 90000:
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

        return serialized_tx.hex()

    except Exception as e:
        err_msg = str(e.args)
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg)

    except KeyboardInterrupt:
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            'KeyboardInterrupt')


def make_txs_for_hwwallet(mnconfig, client, mpath, SEND_TO_BIP32):

    txs = mnconfig.get('txs', None)
    collateral_spath = mnconfig.get('collateral_spath', None)
    receiving_address = mnconfig.get('receiving_address', None)

    if collateral_spath is None or receiving_address is None:
        err_msg = 'make_inputs_for_hw_wallet receiving_address / collateral_spath : Should not be None'
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg)

    serialized_txs = []
    if txs is not None:
        for tx in txs:
            if (len(tx)) >= min_unspent or MOVE_1K_COLLATERAL:
                serialized_tx = make_inputs_for_hw_wallet(tx, receiving_address, collateral_spath, client, mpath)
                serialized_txs.append(serialized_tx)

            else:
                print('---> count of txs less than min_unspent : %s' % min_unspent)
                return None
    else:
        return None

    return serialized_txs


# end
