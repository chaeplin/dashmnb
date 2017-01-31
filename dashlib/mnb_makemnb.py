import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

import time

from dash_utils import *
from dash_tx import *
from mnb_misc import *
from mnb_signing import *
from mnb_rpc import *
from mnb_maketx import *

def make_mnb(
        alias,
        protocolversion,
        mnconfig,
        access,
        client,
        mpath):
    print('---> making mnb for %s' % alias)

    # ------ some default config
    scriptSig = ''
    sequence = 0xffffffff
    #protocol_version = 70204
    protocol_version = protocolversion
    sig_time = int(time.time())

    #cur_block_height = access.getblockcount()
    #block_hash = access.getblockhash(cur_block_height - 12)

    block_hash = get_block_hash_for_mnb(access)

    vintx = bytes.fromhex(mnconfig['collateral_txid'])[::-1].hex()
    vinno = mnconfig['collateral_txidn'].to_bytes(4, byteorder='big')[::-1].hex()
    vinsig = num_to_varint(len(scriptSig) / 2).hex() + \
        bytes.fromhex(scriptSig)[::-1].hex()
    vinseq = sequence.to_bytes(4, byteorder='big')[::-1].hex()

    ip, port = mnconfig['ipport'].split(':')

    ipv6map = '00000000000000000000ffff'
    ipdigit = map(int, ip.split('.'))
    for i in ipdigit:
        ipv6map += i.to_bytes(1, byteorder='big')[::-1].hex()

    ipv6map += int(port).to_bytes(2, byteorder='big').hex()

    collateral_in = num_to_varint(
        len(mnconfig['collateral_pubkey']) / 2).hex() + mnconfig['collateral_pubkey']
    delegate_in = num_to_varint(
        len(mnconfig['masternode_pubkey']) / 2).hex() + mnconfig['masternode_pubkey']

    serialize_for_sig = str(mnconfig['ipport']) \
        + str(sig_time) \
        + format_hash(Hash160(bytes.fromhex(mnconfig['collateral_pubkey']))) \
        + format_hash(Hash160(bytes.fromhex(mnconfig['masternode_pubkey']))) \
        + str(protocol_version)

    try:
        sig1 = hwwallet_signmessage(
            serialize_for_sig,
            mnconfig['collateral_spath'],
            mnconfig['collateral_address'],
            client,
            mpath)

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

    work_sig_time = sig_time.to_bytes(8, byteorder='big')[::-1].hex()
    work_protoversion = protocol_version.to_bytes(4, byteorder='big')[
        ::-1].hex()

    last_ping_block_hash = bytes.fromhex(block_hash)[::-1].hex()

    last_ping_serialize_for_sig = serialize_input_str(
        mnconfig['collateral_txid'],
        mnconfig['collateral_txidn'],
        sequence,
        scriptSig) + block_hash + str(sig_time)

#    sig2 = signmessage(
#            last_ping_serialize_for_sig, 
#            mnconfig['masternode_address'],
#            access)

    sig2 = signmessage_ecdsa(
            last_ping_serialize_for_sig, 
            mnconfig['masternode_privkey'])

    work = vintx + vinno + vinsig + vinseq \
        + ipv6map + collateral_in + delegate_in \
        + num_to_varint(len(sig1) / 2).hex() + sig1 \
        + work_sig_time + work_protoversion \
        + vintx + vinno + vinsig + vinseq \
        + last_ping_block_hash + work_sig_time \
        + num_to_varint(len(sig2) / 2).hex() + sig2

    print('---> mnb hex for %s : %s\n' % (mnconfig.get('alias'), work))
    return work

# end
