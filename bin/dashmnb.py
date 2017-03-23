#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# mnb.py

# code from https://github.com/dashpay/electrum-dash
# most bitcoin code from https://github.com/vbuterin/pybitcointools
# ref :
# https://github.com/dashpay/dash/blob/v0.12.1.x/dash-docs/protocol-documentation.md

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'dashlib'))

import argparse
import time
import signal
import atexit

from dashlib import *

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException


def main(args):
    logo_show()

    if TYPE_HW_WALLET.lower().startswith("ledgernanos"):
        args.maketx = False
        args.xfer = False

    # access
    if 'rpcusessl' in globals() and rpcusessl:
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context

        serverURL = 'https://' + rpcuser + ':' + rpcpassword + '@' + rpcbindip + \
            ':' + str(rpcport if USE_SSH_TUNNEL is False else SSH_LOCAL_PORT)

    else:
        serverURL = 'http://' + rpcuser + ':' + rpcpassword + '@' + rpcbindip + \
            ':' + str(rpcport if USE_SSH_TUNNEL is False else SSH_LOCAL_PORT)

    access = AuthServiceProxy(serverURL)

    if len(str(account_no)) == 0:
        err_msg = 'please configure bip32 path : account_no'
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg)

    try:
        print('--> get dash explorer block count')
        #explorer_blockcount = get_explorer_blockcount()

        if rpcbindip == "test.stats.dash.org":
            print('--> get remotesvc status')
        else:
            print('--> get dashd status')

        protocolversion = check_dashd_syncing(access)
        blockcount = get_getblockcount(access)
        blockhash = get_block_hash(blockcount, access)

        print('-> protocolv : %s' % str(protocolversion))
        print('-> blockcnt  : %s' % blockcount)
        print('-> blockhash : %s\n' % blockhash)

        # check explorer block count
        if MAINNET:
            explorer_blockcount = get_insight_blockcount()
        else:
            explorer_blockcount = get_explorer_blockcount()

        assert int(explorer_blockcount) == int(blockcount), "blockcount mismatch, try again : exp : %s <--> dashd : %s" % (explorer_blockcount, blockcount)

        print()

    except AssertionError as e:
        err_msg = str(e.args)
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg)

    except Exception as e:
        err_msg = str(e.args)
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg)

    if TYPE_HW_WALLET.lower().startswith("ledgernanos"):
        client, signing, mpath = check_hw_wallet()

    else:
        client, signing, _, mpath, _ = check_hw_wallet()
    
    chain_pubkey = get_chain_pubkey(client)

    mn_config, signing, mns, mna = checking_mn_config(
        access, signing, chain_pubkey, args.showall)

    print_mnstatus(mn_config, mns, mna)


    # make a signed message for Masternode Owner/Operator badge for forum
    if args.badge:
        if not signing:
            err_msg = 'need HW wallet to Sign'
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

        mnalias_for_signing = args.masternode_to_start
        if len(mnalias_for_signing) == 0:
            err_msg = 'select one alias of masternode'
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

        elif len(mnalias_for_signing) > 1:
            err_msg = 'slect only one alias'
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

        for m in mn_config:
            if m.get('alias') in mnalias_for_signing:
                make_badge(m, mpath, client)


    # vote
    if args.voteyes or args.voteno or args.voteabstain or args.votequery:
        if args.voteyes and args.voteno:
            err_msg = "can't use yes and no together to vote, select one"
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

        proposal_hash = args.masternode_to_start
        if len(proposal_hash) == 0:
            err_msg = 'hash of a proposal needed'
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

        elif len(proposal_hash) > 1:
            err_msg = 'can vote only one proposal at a time'
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

        proposallist = rpc_getproposals(access).keys()
        if proposal_hash[0] in proposallist:
            if args.voteyes or args.voteno or args.voteabstain:
        
                if args.voteyes:
                    vote = 'yes'
                if args.voteno:
                    vote = 'no'
                if args.voteabstain:
                    vote = 'abstain'
    
                print('[making vote(s)]')
                start_votes(mn_config, proposal_hash[0], vote, access)


            elif args.votequery:
                print('[vote(s) result]')
                display_votes(mn_config, proposal_hash[0], access)

    
        else:
            err_msg = 'no matching proposal to vote, check proposal hash'
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

    # signing chck
    if args.anounce and MOVE_1K_COLLATERAL == False:
        if not signing:
            err_msg = 'check masternode config'
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

        mns_to_start = []

        list_of_mn_status_ok = ["ENABLED", "PRE_ENABLED", "WATCHDOG_EXPIRED"]
        list_of_mn_status_to_ignore = ["OUTPOINT_SPENT"]

        for m in mn_config:
            txidtxidn = m.get('collateral_txidtxidn')
            if len(args.masternode_to_start) > 0:
                if m.get('alias') in args.masternode_to_start:
                    mns_to_start.append(m)
            else:
                if ((mns.get(txidtxidn, None) not in list_of_mn_status_ok) and (
                        mns.get(txidtxidn, None) not in list_of_mn_status_to_ignore)):
                    # if ((mns.get(txidtxidn, None) != 'ENABLED'
                    #     and mns.get(txidtxidn, None) != 'PRE_ENABLED')):
                    mns_to_start.append(m)

        if len(mns_to_start) > 0 and signing:
            start_masternode(
                mns_to_start,
                protocolversion,
                blockcount,
                access,
                client,
                args.anounce,
                mpath,
                args.whalemode
                )


    # wallet rescan
    #have_unconfirmed_tx = False
    if args.balance or args.maketx or args.xfer:
        have_unconfirmed_tx = check_mempool(mn_config, access)
        if have_unconfirmed_tx:
            txs_cache_refresh_interval_hour = 0

    if args.balance or args.maketx or args.xfer:
        for m in mn_config:
            #m["unspent"], m["txs"], m["collateral_dashd_balance"] = get_unspent_txs(m, access)
            m["txs"], m["collateral_dashd_balance"] = get_unspent_txs(
                m, blockcount, access)

        need_wallet_rescan = print_balance(mn_config, have_unconfirmed_tx)

        if need_wallet_rescan:
            err_msg = '\n\trestarting Dash-QT or dashd with -rescan needed'
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

    if not signing:
        err_msg = 'need HW wallet to spend'
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg)

    if args.balance or args.maketx or args.xfer:
        if have_unconfirmed_tx:
            err_msg = 'have unconfirmed tx, wait at least 1 confirmation'
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

    if args.maketx or args.xfer:

        if need_wallet_rescan:
            err_msg = '\n\t1) to spend mn payout in HW Wallet, restart Dash-QT or dashd with -rescan\n\t2) if did -rescan and still see this messge, check if 1K was spent'
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

        if signing:
            print('[making txs]')
            for m in mn_config:
                if len(
                    m.get('collateral_dashd_balance')) > 0 and len(
                    m.get(
                        'txs',
                        None)) > 0 and m.get(
                    'receiving_address',
                        None) is not None:
                    if len(args.masternode_to_start) > 0:
                        if m.get('alias') in args.masternode_to_start:
                            print(
                                '---> signing txs for mn %s: ' %
                                m.get('alias'))
                            m["signedrawtx"] = make_txs_for_hwwallet(
                                m, client, mpath)

                    else:
                        print('---> signing txs for mn %s: ' % m.get('alias'))
                        m["signedrawtx"] = make_txs_for_hwwallet(
                            m, client, mpath)

    if args.xfer and signing:
        xfertxid = broadcast_signedrawtx(mn_config, access, args.whalemode)

        print()
        if xfertxid is not None:
            for x in xfertxid:
                print('\t' + x)

    print_err_exit(
        get_caller_name(),
        get_function_name(),
        'end of pg')


def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument(dest='masternode_to_start',
                        metavar='mnalias[s] or a proposal_hash',
                        nargs='*')

    parser.add_argument('-c', '--check',
                        dest='check',
                        action='store_true',
                        help='check masternode config')

    parser.add_argument('-s', '--status',
                        dest='status',
                        action='store_true',
                        help='show masternode status')

    parser.add_argument('-a', '--anounce',
                        dest='anounce',
                        action='store_true',
                        help='anounce missing masternodes')

    parser.add_argument('-b', '--balance',
                        dest='balance',
                        action='store_true',
                        help='show masternodes balance')

    parser.add_argument('-y', '--voteyes',
                        dest='voteyes',
                        action='store_true',
                        help='vote Yes to a proposal using all mns')

    parser.add_argument('-n', '--voteno',
                        dest='voteno',
                        action='store_true',
                        help='vote No to a proposal using all mns')

    parser.add_argument('-f', '--voteabstain',
                        dest='voteabstain',
                        action='store_true',
                        help='vote Abstain to a proposal using all mns')

    parser.add_argument('-q', '--votequery',
                        dest='votequery',
                        action='store_true',
                        help='get vote status on a proposal by all mns')  

    parser.add_argument('-l', '--showall',
                        dest='showall',
                        action='store_true',
                        help='show all configured masternodes')

    if TYPE_HW_WALLET.lower().startswith("ledgernanos"):
        pass

    else:
        parser.add_argument('-m', '--maketx',
                            dest='maketx',
                            action='store_true',
                            help='make signed raw tx')
    
        parser.add_argument('-x', '--xfer',
                            dest='xfer',
                            action='store_true',
                            help='broadcast signed raw tx')

    parser.add_argument('-w', '--whale',
                        dest='whalemode',
                        action='store_true',
                        help='do not ask yes or no, all yes')    

    parser.add_argument('-o', '--badge',
                        dest='badge',
                        action='store_true',
                        help='Sign message for Masternode Owner/Operator badge')    

    if len(sys.argv) < 2:
        parser.print_help()
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            'print help')

    return parser.parse_args()


if __name__ == "__main__":
    def killsubprocess():
        if tunnel_pid:
            os.kill(tunnel_pid, signal.SIGTERM)

    printdbg('main starting')
    if (sys.version_info < (3, 5, 1)):
        sys.exit('need python 3.5.1')

    try:

        tunnel_pid = None
        # ssh tunnel
        if USE_SSH_TUNNEL:
            tunnel = start_ssh_tunnel()
            tunnel_pid = tunnel._getpid()

        atexit.register(killsubprocess)
        args = parse_args()
        main(args)

    except KeyboardInterrupt:
        if tunnel_pid:
            os.kill(tunnel_pid, signal.SIGTERM)
        sys.exit()

# end
