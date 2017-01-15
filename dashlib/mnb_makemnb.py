import sys, os
sys.path.append( os.path.join( os.path.dirname(__file__), '..' ) )
sys.path.append( os.path.join( os.path.dirname(__file__), '..', 'dashlib' ) )

import time
from utils import *
from tx import *
from mnb_misc import *
from mnb_signing import *
from mnb_rpc import *
from mnb_maketx import *

def make_mnb(alias, mn_conf, access, client):
    print('---> making mnb for %s' % alias)

    # ------ some default config
    scriptSig = ''
    sequence = 0xffffffff
    protocol_version = 70204
    sig_time = int(time.time())

    cur_block_height = access.getblockcount()
    block_hash = access.getblockhash(cur_block_height - 12)

    vintx  = bytes.fromhex(mn_conf['collateral_txid'])[::-1].hex()
    vinno  = mn_conf['collateral_txidn'].to_bytes(4, byteorder='big')[::-1].hex()
    vinsig = num_to_varint(len(scriptSig)/2).hex() + bytes.fromhex(scriptSig)[::-1].hex()
    vinseq = sequence.to_bytes(4, byteorder='big')[::-1].hex()

    ip, port = mn_conf['ipport'].split(':')

    ipv6map = '00000000000000000000ffff'
    ipdigit = map(int, ip.split('.'))
    for i in ipdigit:  
        ipv6map  += i.to_bytes(1, byteorder='big')[::-1].hex()

    ipv6map += int(port).to_bytes(2, byteorder='big').hex()

    collateral_in = num_to_varint(len(mn_conf['collateral_pubkey'])/2).hex() + mn_conf['collateral_pubkey']
    delegate_in   = num_to_varint(len(mn_conf['masternode_pubkey'])/2).hex() + mn_conf['masternode_pubkey']

    serialize_for_sig = str(mn_conf['ipport']) + str(sig_time) \
                      + format_hash(Hash160(bytes.fromhex(mn_conf['collateral_pubkey']))) \
                      + format_hash(Hash160(bytes.fromhex(mn_conf['masternode_pubkey']))) + str(protocol_version)

    try:
        sig1 = keepkeysign(serialize_for_sig, mn_conf['collateral_spath'], mn_conf['collateral_address'], client)

    except Exception as e:
        print("\n")
        print('%s - %s' % (get_function_name(), e.args))
        sys.exit()

    except KeyboardInterrupt:
        sys.exit()

    work_sig_time     = sig_time.to_bytes(8, byteorder='big')[::-1].hex() 
    work_protoversion = protocol_version.to_bytes(4, byteorder='big')[::-1].hex()

    last_ping_block_hash = bytes.fromhex(block_hash)[::-1].hex() 

    last_ping_serialize_for_sig  = serialize_input_str(mn_conf['collateral_txid'], mn_conf['collateral_txidn'], sequence, scriptSig) + block_hash + str(sig_time)

    if validateaddress(mn_conf['masternode_address'], access) == None:
        keyalias = alias + '-' + ip
        importprivkey(mn_conf['masternode_privkey'], keyalias, access)

    sig2 = signmessage(last_ping_serialize_for_sig, mn_conf['masternode_address'], access)

    work = vintx + vinno + vinsig + vinseq \
        + ipv6map + collateral_in + delegate_in \
        + num_to_varint(len(sig1)/2).hex() + sig1 \
        + work_sig_time + work_protoversion \
        + vintx + vinno + vinsig + vinseq \
        + last_ping_block_hash + work_sig_time \
        + num_to_varint(len(sig2)/2).hex() + sig2

    print('---> mnb hex for %s : %s\n' % (mn_conf.get('alias'), work))
    return work 

# end     