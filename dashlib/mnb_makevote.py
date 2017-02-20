import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

import time

from dash_utils import *
from mnb_misc import *
from mnb_signing import *

def make_vote(
        alias,
        proposal_hash,
        vote,
        mnconfig):

    print('%s : %s : %s ' % (alias, vote, proposal_hash))

    sig_time = int(time.time())
    collateral_txidtxidn = mnconfig['collateral_txidtxidn']

    if vote == 'yes':
        voteno = '1'
    elif vote == 'no':
        voteno = '2'

    serialize_for_sig = collateral_txidtxidn + '|' \
                    + proposal_hash + '|' \
                    + '1' + '|' \
                    + voteno + '|' \
                    + str(sig_time)

    sig = signmessage_ecdsa_no_encoding(
        serialize_for_sig,
        mnconfig['masternode_privkey'])

    work = {
        "alias": mnconfig['alias'],
        "collateral_txid": mnconfig['collateral_txid'],
        "collateral_txidn": mnconfig['collateral_txidn'],
        "proposal_hash": proposal_hash,
        "vote": vote,
        "sig_time": sig_time,
        "sig": sig

    }

    return work


